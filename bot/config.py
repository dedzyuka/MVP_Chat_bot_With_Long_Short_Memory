import os
import tiktoken
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=MAX_TOKENS)

enc = tiktoken.encoding_for_model("gpt-4o-mini")
DB_URI =  os.getenv("DB_URI", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")