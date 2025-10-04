from google import genai
import os
from google.genai import types
import asyncio
from bot.config import GEMINI_EMBEDD


class EmbeddingGenerator:
    def __init__(self, api_key: str = None):

        self.client = genai.Client(api_key=GEMINI_EMBEDD)
    
    async def generate_embedding(self, text: str) -> list[float]:
        try:
            
            result = await asyncio.to_thread(
                self.client.models.embed_content,
                model="gemini-embedding-001",
                contents=[text],
                config=types.EmbedContentConfig(output_dimensionality=1536)
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"Ошибка при генерации эмбеддинга: {e}")
            raise
    

