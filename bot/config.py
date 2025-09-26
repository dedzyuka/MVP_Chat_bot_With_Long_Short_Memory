import os
import tiktoken
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=800)
MAX_MESSAGES = 5
MAX_TOKENS = 800
enc = tiktoken.encoding_for_model("gpt-4o-mini")
