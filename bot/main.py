import asyncio
from .graph import create_graph
from .database import AsyncPostgresSaver
from .config import DB_URI

async def main():
    async with AsyncPostgresSaver.from_conn_string(DB_URI) as saver:
        graph = create_graph()
        app = graph.compile(checkpointer=saver)
        
        user_id = "bogdan_001"
        thread_id = f"thread_{user_id}"
        
        saved_state = await app.aget_state(
            config={"configurable": {"thread_id": thread_id}}
        )
        
        if saved_state is None:
            state = {"memory": [], "message": "Привет! Меня зовут Богдан!", "user_id": user_id}
            print("Создана новая сессия")
        else:
            state = saved_state.values
            if "memory" not in state:
                state["memory"] = []
            if "user_id" not in state:
                state["user_id"] = user_id
            state["message"] = "Я вернулся! Что нового?"
            print("Продолжена существующая сессия")
        
        result = await app.ainvoke(
            state, 
            config={"configurable": {"thread_id": thread_id}}
        )
        print("🤖 Бот:", result["message"])
        
        while True:
            user_msg = input("Ты: ")
            if user_msg.lower() in ["выход", "exit", "quit"]:
                print("Выход.")
                break
            
            saved_state = await app.aget_state(
                config={"configurable": {"thread_id": thread_id}}
            )
            
            if saved_state is None:
                state = {"memory": [], "message": user_msg, "user_id": user_id}
            else:
                state = saved_state.values
                if "memory" not in state:
                    state["memory"] = []
                if "user_id" not in state:
                    state["user_id"] = user_id
                state["message"] = user_msg
            
            result = await app.ainvoke(
                state, 
                config={"configurable": {"thread_id": thread_id}}
            )
            print("Бот:", result["message"])
