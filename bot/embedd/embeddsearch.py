import asyncpg

class VectorStore:
    def __init__(self, database_url: str):
        self.db_url = database_url
    
    
    
    
    
    async def search_similar_chunks(self, query_embedding: list, limit: int = 5):
        conn = await asyncpg.connect(self.db_url)
        try:
            # Также форматируем embedding запроса
            embedding_str = '[' + ','.join(str(x) for x in query_embedding) + ']'
            
            records = await conn.fetch('''
                SELECT 
                    content,
                    document_name,
                    chunk_index,
                    1 - (embedding <=> $1::vector) as similarity
                FROM document_chunks 
                ORDER BY embedding <=> $1::vector
                LIMIT $2
            ''', embedding_str, limit)
            
            return [
                {
                    "content": record["content"],
                    "document_name": record["document_name"],
                    "chunk_index": record["chunk_index"],
                    "similarity": float(record["similarity"])
                }
                for record in records
            ]
        finally:
            await conn.close()