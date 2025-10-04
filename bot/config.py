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

GEMINI_EMBEDD = os.getenv("GEMINI_EMBEDD")

LIMIT_SEARCH_EMBEDDINGS = int(os.getenv("LIMIT_SEARCH_EMBEDDINGS", 3))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


TABLE_EMBEDDNAME=os.getenv("TABLE_EMBEDDNAME")