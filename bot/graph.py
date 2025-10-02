import uuid
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langmem import create_memory_store_manager

from bot.embedd.embeddsearch import VectorStore
from bot.embedd.reqtoembedd import EmbeddingGenerator
from .config import llm, MAX_MESSAGES, MAX_TOKENS, DB_URI
from .memory import summarize_memory, count_tokens
from .database import AsyncPostgresStore

class State(TypedDict):
    memory: List[dict]
    message: str
    user_id: str
    sys_chanck_msg: str

async def process_message(state: State):
    if "memory" not in state:
        state["memory"] = []
    
    user_msg = state["message"]
    user_id = state["user_id"] 

    vector_store = VectorStore(DB_URI)
    embedding_generator = EmbeddingGenerator()

    query_embedding = await embedding_generator.generate_embedding(user_msg)
    similar_chunks = await vector_store.search_similar_chunks(query_embedding)
    print(f"Найдено чанков: {len(similar_chunks)}", flush=True)
    sys_chanck_msg = ""
    if similar_chunks:
        for chunk in similar_chunks:
            sys_chanck_msg += f"\n\n{chunk['content']}"
    else:
        sys_chanck_msg = ""
    
    async with AsyncPostgresStore.from_conn_string(DB_URI) as store:
        memory_manager = create_memory_store_manager(
            llm,  
            store=store,
            namespace=("telegram_bot", user_id),
            query_limit=3,
            enable_inserts=True,
            enable_deletes=False
        )
        
        relevant_memories = await memory_manager.asearch(
            query=user_msg,
        )
        
        memory_context = ""
        if relevant_memories:
            # ИСПРАВЛЕНИЕ: Используем правильный атрибут для SearchItem
            memory_context = "Контекст из предыдущих разговоров:\n" + \
                           "\n".join([f"- {getattr(mem, 'page_content', getattr(mem, 'text', str(mem)))}" for mem in relevant_memories])
        else:
            memory_context = "Ранее вы не обсуждали эту тему."
        
        # Обновляем память - добавляем новое сообщение
        updated_memory = state["memory"] + [{"role": "user", "content": user_msg}]
        
        # Проверяем и ограничиваем количество сообщений
        if len(updated_memory) > MAX_MESSAGES:
            updated_memory = updated_memory[-MAX_MESSAGES:]
        
        # Проверяем токены
        while count_tokens(updated_memory) > MAX_TOKENS:
            updated_memory = await summarize_memory(updated_memory, keep=3)

        conversation_history = "\n".join(
            f"{m['role']}: {m['content']}" for m in updated_memory[:-1]  
        )
        
        full_context = f"""
факты о пользователе 
по вопросам про эти факты отвечаем всегда
{memory_context}

История текущего разговора:
{conversation_history}

Текущее сообщение: {user_msg}
Всегда отвечай только в контексте Системного контекста. Если ты не знаешь ответ, ответь в начале диалога [найдено из открытых источников].
если вопрос касается личных данных пользователя то ты на них отвечаешь
Системный контекст: {sys_chanck_msg}
"""
        print(f"Полный контекст для LLM: {full_context}", flush=True)
        
        if any(keyword in user_msg.lower() for keyword in ["запомни", "запиши", "не забывай", "remember"]):
            messages_to_process = [{"role": "user", "content": user_msg}]
            await memory_manager.ainvoke({"messages": messages_to_process}) 

        resp = await llm.ainvoke(full_context)
        # Добавляем ответ ассистента в память
        updated_memory.append({"role": "assistant", "content": resp.content})
    
    print(f"Обновленная память содержит {len(updated_memory)} сообщений", flush=True)
    return {"memory": updated_memory, "message": resp.content, "user_id": user_id, "sys_chanck_msg": sys_chanck_msg}

def create_graph():
    graph = StateGraph(State)
    graph.add_node("chat", process_message)
    graph.add_edge("chat", END)
    graph.set_entry_point("chat")
    return graph