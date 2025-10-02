import os
import tiktoken
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=800)
MAX_MESSAGES = 5
MAX_TOKENS = 800
enc = tiktoken.encoding_for_model("gpt-4o-mini")
DB_URI = "postgresql://botuser:botpassword@localhost:5432/botdb"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")