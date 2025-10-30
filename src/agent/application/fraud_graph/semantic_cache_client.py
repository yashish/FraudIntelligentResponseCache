import asyncpg
from typing import List, Optional
import numpy

class SemanticCacheClient:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def insert_vector(self, vector: List[float], metadata: str):
        if not self.pool:
            raise RuntimeError("Database connection is not established. Call connect() first.")
        
        async with self.pool.acquire() as connection:
            await connection.execute(
                "INSERT INTO semantic_cache (embedding, metadata) VALUES ($1, $2)",
                vector,
                metadata
            )

    async def search_similar_cache(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        if not self.pool:
            raise RuntimeError("Database connection is not established. Call connect() first.")
        
        async with self.pool.acquire() as connection:
            query = """
                SELECT query, answer, 1 - (embedding <=> $1::vector) AS similarity
                FROM semantic_cache
                WHERE 1 - (embedding <=> $1::vector) >= $2
                ORDER BY embedding <=> $1::vector
                LIMIT 1;
            """

            rows = await connection.fetch(
                """
                SELECT metadata, embedding <=> $1 AS distance
                FROM semantic_cache
                ORDER BY embedding <=> $1
                LIMIT $2
                """,
                query_vector,
                top_k
            )
            return [{"metadata": row["metadata"], "distance": row["distance"]} for row in rows] if rows else []
        
# Example usage:
# async def main():
#     client = SemanticCacheClient(dsn="postgresql://user:password@localhost/dbname")
#     await client.connect()
#     await client.insert_vector([0.1, 0.2, 0.3], "Sample metadata")
#     results = await client.search_similar([0.1, 0.2, 0.25], top_k=3)
#     print(results)
#     await client.close()
