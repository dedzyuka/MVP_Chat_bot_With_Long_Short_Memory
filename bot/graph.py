import uuid
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langmem import create_memory_store_manager
from langgraph.store.postgres import AsyncPostgresStore

from .config import llm, MAX_MESSAGES, MAX_TOKENS, DB_URI
from .memory import summarize_memory, count_tokens

from bot.embedd.newembeddsearch import embeddsearch

class State(TypedDict):
    memory: List[dict]
    message: str
    user_id: str
    sys_chanck_msg: str
    memory_context: str
    full_context: str

async def retrieve_chunks(state: State):
    print("=== НОДА: Поиск чанков ===", flush=True)
    user_msg = state["message"]
    user_id = state["user_id"]

    similar_chunks = await embeddsearch(state["message"])
    print(f"Чанки найдены", flush=True)
    
    sys_chanck_msg = ""
    if similar_chunks:
        sys_chanck_msg = similar_chunks
        print(similar_chunks, flush=True)
    else:
        sys_chanck_msg = ""
    
    return {
        **state,
        "sys_chanck_msg": sys_chanck_msg
    }

# Нода 2: Поиск в долговременной памяти
async def retrieve_memory(state: State):
    print("=== НОДА: Поиск в памяти ===", flush=True)
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
        
        relevant_memories = await memory_manager.asearch(query=user_msg)
        
        memory_context = ""
        if relevant_memories:
            memory_context = "Контекст из предыдущих разговоров:\n" + \
                           "\n".join([f"- {getattr(mem, 'page_content', getattr(mem, 'text', str(mem)))}" for mem in relevant_memories])
        else:
            memory_context = "Ранее вы не обсуждали эту тему."
    
   
    return {
        **state,
        "memory_context": memory_context
    }


async def prepare_context(state: State):
    print("=== НОДА: Подготовка контекста ===", flush=True)
    user_msg = state["message"]
    

    updated_memory = state.get("memory", []) + [{"role": "user", "content": user_msg}]
    

    if len(updated_memory) > MAX_MESSAGES:
        updated_memory = updated_memory[-MAX_MESSAGES:]
    

    while count_tokens(updated_memory) > MAX_TOKENS:
        updated_memory = await summarize_memory(updated_memory, keep=3)


    conversation_history = "\n".join(
        f"{m['role']}: {m['content']}" for m in updated_memory[:-1]  
    )
    
    # Собираем полный контекст
    full_context = f"""
факты о пользователе 
по вопросам про эти факты отвечаем всегда
{state.get('memory_context', '')}

История текущего разговора:
{conversation_history}

Текущее сообщение: {user_msg}
Всегда отвечай только в контексте Системного контекста. Если ты не знаешь ответ, ответь в начале диалога [найдено из открытых источников].
если вопрос касается личных данных пользователя то ты на них отвечаешь
Системный контекст: {state.get('sys_chanck_msg', '')}
"""
    print(f"Полный контекст для LLM: {full_context}", flush=True)
    
    return {
        **state,
        "memory": updated_memory,
        "full_context": full_context
    }


async def generate_response(state: State):
    print("=== НОДА: Генерация ответа ===", flush=True)
    user_msg = state["message"]
    user_id = state["user_id"]
    

    resp = await llm.ainvoke(state["full_context"])
    
    updated_memory = state["memory"] + [{"role": "assistant", "content": resp.content}]
    
    if any(keyword in user_msg.lower() for keyword in ["запомни", "запиши", "не забывай", "remember"]):
        async with AsyncPostgresStore.from_conn_string(DB_URI) as store:
            memory_manager = create_memory_store_manager(
                llm,  
                store=store,
                namespace=("telegram_bot", user_id),
                query_limit=3,
                enable_inserts=True,
                enable_deletes=False
            )
            messages_to_process = [{"role": "user", "content": user_msg}]
            await memory_manager.ainvoke({"messages": messages_to_process})
    
    print(f"Обновленная память содержит {len(updated_memory)} сообщений", flush=True)
    
 
    return {
        **state,
        "memory": updated_memory,
        "message": resp.content
    }

def create_graph():
    graph = StateGraph(State)
    
    # Добавляем ноды
    graph.add_node("retrieve_chunks", retrieve_chunks)
    graph.add_node("retrieve_memory", retrieve_memory)
    graph.add_node("prepare_context", prepare_context)
    graph.add_node("generate_response", generate_response)
    

    graph.set_entry_point("retrieve_chunks")
    
    graph.add_edge("retrieve_chunks", "retrieve_memory")
    graph.add_edge("retrieve_memory", "prepare_context")
    graph.add_edge("prepare_context", "generate_response")
    graph.add_edge("generate_response", END)
    
    return graph