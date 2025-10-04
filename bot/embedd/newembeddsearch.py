import asyncio
from langchain_postgres.v2.vectorstores import AsyncPGVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings  
from langchain_postgres.v2.engine import PGEngine


from bot.config import LIMIT_SEARCH_EMBEDDINGS, EMBEDDING_MODEL,GEMINI_EMBEDD,DB_URI,TABLE_EMBEDDNAME #????




async def embeddsearch(req: str):
    engine = PGEngine.from_connection_string(url="postgresql+asyncpg://botuser:botpassword@localhost:5432/botdb")
    embedding = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_EMBEDD,
    )
    store = await AsyncPGVectorStore.create(
        embedding_service=embedding,
        engine=engine,
        table_name=TABLE_EMBEDDNAME
    )

    docs = await store.asimilarity_search(
        query=req,
        k=LIMIT_SEARCH_EMBEDDINGS
    )
    allSearch = " "
    if docs:
        print("Найдены данные в базе:")
        doc_texts = [
            doc.page_content if hasattr(doc, "page_content") else doc.content
            for doc in docs
        ]
        for i, text in enumerate(doc_texts, 1):
            allSearch += f"{i}: {text}\n{'='*50}"
            print(f"{i}: {text}\n{'='*50}")
        return allSearch
    else:
        print("Не найдены данные в базе")
        return []

