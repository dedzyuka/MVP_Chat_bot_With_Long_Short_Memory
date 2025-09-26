from typing import List, Dict
from .config import llm, MAX_MESSAGES, MAX_TOKENS, enc

async def summarize_memory(memory: List[dict], keep: int = 1) -> List[dict]:
    if len(memory) <= keep:
        return memory
    old_messages = memory[:-keep]
    summary_prompt = "Сделай краткое резюме этих сообщений:\n" + \
                     "\n".join(m["content"] for m in old_messages)
    resp = await llm.ainvoke(summary_prompt)
    summarized = [{"role": "assistant", "content": resp.content}]
    return summarized + memory[-keep:]

def count_tokens(memory: List[dict]) -> int:
    return sum(len(enc.encode(m["content"])) for m in memory)