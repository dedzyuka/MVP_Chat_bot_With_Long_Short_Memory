import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from .graph import create_graph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from .config import DB_URI, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_or_create_state(app, thread_id, user_id, initial_message, sys_chanck_msg: str = ""):
    saved_state = await app.aget_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    if saved_state is None:
        print(f"Создано новое состояние для пользователя {user_id}", flush=True)
        return {"memory": [], "message": initial_message, "user_id": user_id, "sys_chanck_msg": sys_chanck_msg}
    else:
        state = saved_state.values
        current_memory = state.get("memory", [])
        print(f"Восстановлено состояние с {len(current_memory)} сообщениями для пользователя {user_id}", flush=True)
        return {
            "memory": current_memory,
            "message": initial_message, 
            "user_id": user_id,
            "sys_chanck_msg": sys_chanck_msg or state.get("sys_chanck_msg", "")
        }

@dp.message(CommandStart())
async def handle_start(message: Message):
    user_id = str(message.from_user.id)
    thread_id = f"thread_{user_id}"

    async with AsyncPostgresSaver.from_conn_string(DB_URI) as saver:
        graph = create_graph()
        app = graph.compile(checkpointer=saver)

        state = await get_or_create_state(
            app, thread_id, user_id, "Привет! Я готов помочь."
        )

        result = await app.ainvoke(
            state,
            config={"configurable": {"thread_id": thread_id}}
        )

    await message.answer(result["message"])

@dp.message()
async def handle_message(message: Message):
    user_id = str(message.from_user.id)
    thread_id = f"thread_{user_id}"
    user_msg = message.text or ""

    async with AsyncPostgresSaver.from_conn_string(DB_URI) as saver:
        graph = create_graph()
        app = graph.compile(checkpointer=saver)
        
        state = await get_or_create_state(app, thread_id, user_id, user_msg)
        result = await app.ainvoke(
            state,
            config={"configurable": {"thread_id": thread_id}}
        )

    await message.answer(result["message"])

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Please set it in your .env file.")
    await dp.start_polling(bot, skip_updates=True)