import uuid
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from .config import llm, MAX_MESSAGES, MAX_TOKENS, DB_URI
from .memory import summarize_memory, count_tokens
from .database import AsyncPostgresStore

class State(TypedDict):
    memory: List[dict]
    message: str
    user_id: str

async def process_message(state: State):
    if "memory" not in state:
        state["memory"] = []
    
    user_msg = state["message"]
    user_id = state.get("user_id", "bogdan_001")
    
    async with AsyncPostgresStore.from_conn_string(DB_URI) as store:
        namespace = ("memories", user_id)
        
        memories = await store.asearch(namespace, query=user_msg, limit=3)
        memory_info = "\n".join([d.value["data"] for d in memories]) if memories else "Нет информации в долговременной памяти"
        
        state["memory"].append({"role": "user", "content": user_msg})
        
        if len(state["memory"]) > MAX_MESSAGES:
            state["memory"] = state["memory"][-MAX_MESSAGES:]
        
        while count_tokens(state["memory"]) > MAX_TOKENS:
            state["memory"] = await summarize_memory(state["memory"], keep=3)
        
        context = f"""Информация из долговременной памяти пользователя:
{memory_info}

Текущий разговор:
""" + "\n".join(f"{m['role']}: {m['content']}" for m in state["memory"])
        
        if any(keyword in user_msg.lower() for keyword in ["запомни", "запиши", "не забывай", "remember"]):
            memory_prompt = f"Извлеки ключевую информацию для запоминания из сообщения: {user_msg}. Ответь кратко."
            memory_resp = await llm.ainvoke(memory_prompt)
            await store.aput(namespace, str(uuid.uuid4()), {"data": memory_resp.content})
            print(f"Сохранено в долговременную память: {memory_resp.content}")
        
        resp = await llm.ainvoke(context)
        state["memory"].append({"role": "assistant", "content": resp.content})
    
    return {"memory": state["memory"], "message": resp.content}

def create_graph():
    graph = StateGraph(State)
    graph.add_node("chat", process_message)
    graph.add_edge("chat", END)
    graph.set_entry_point("chat")
    return graph