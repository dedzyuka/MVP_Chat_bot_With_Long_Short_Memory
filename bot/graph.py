import uuid
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langmem import create_memory_store_manager
from.config import llm, MAX_MESSAGES, MAX_TOKENS, DB_URI
from.memory import summarize_memory, count_tokens
from.database import AsyncPostgresStore

class State(TypedDict):
    memory: List[dict]
    message: str
    user_id: str

async def process_message(state: State):
    if "memory" not in state:
        state["memory"] = []
    
    user_msg = state["message"]
    user_id = state["user_id"] 
    
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
            memory_context = "Контекст из предыдущих разговоров:\n" + \
                           "\n".join([f"- {mem.content}" for mem in relevant_memories])
        else:
            memory_context = "Ранее вы не обсуждали эту тему."
        
        state["memory"].append({"role": "user", "content": user_msg})
        
        if len(state["memory"]) > MAX_MESSAGES:
            state["memory"] = state["memory"]
        
        while count_tokens(state["memory"]) > MAX_TOKENS:
            state["memory"] = await summarize_memory(state["memory"], keep=3)
        

        conversation_history = "\n".join(
            f"{m['role']}: {m['content']}" for m in state["memory"][:-1]  
        )
        
        full_context = f"""
{memory_context}

История текущего разговора:
{conversation_history}

Текущее сообщение: {user_msg}
"""
        
        if any(keyword in user_msg.lower() for keyword in ["запомни", "запиши", "не забывай", "remember"]):
            
            # --- ИСПРАВЛЕННЫЙ БЛОК ---
            # MemoryStoreManager является Runnable. Вызов ainvoke обрабатывает переданные сообщения,
            # извлекает структурированные воспоминания и автоматически сохраняет их в AsyncPostgresStore.
            
            messages_to_process = [{"role": "user", "content": user_msg}]
            
            extracted_memories = await memory_manager.ainvoke({"messages": messages_to_process}) # [1]
            
            # extracted_memories — это список извлеченных объектов Memory, который
            # используется для печати подтверждения. Сохранение уже произошло как побочный эффект ainvoke.
            # print(f"✅ Сохранено в долговременную память (через ainvoke): {[mem.content for mem in extracted_memories]}")
            # --- КОНЕЦ ИСПРАВЛЕННОГО БЛОКА ---
        

        resp = await llm.ainvoke(full_context)
        state["memory"].append({"role": "assistant", "content": resp.content})
    
    return {"memory": state["memory"], "message": resp.content}

def create_graph():
    graph = StateGraph(State)
    graph.add_node("chat", process_message)
    graph.add_edge("chat", END)
    graph.set_entry_point("chat")
    return graph