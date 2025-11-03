from langchain.tools import tool
import redis, json
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import Document

rdb = redis.Redis(host="localhost", port=6379, decode_responses=True)

@tool
def check_exact_cache(key: str) -> str | None:
    """Check Redis for exact cache hit."""
    val = rdb.get(key)
    return val if val else None

@tool
def write_exact_cache(key: str, value: str, ttl: int = 3600) -> str:
    """Write to Redis exact cache."""
    rdb.set(key, value, ex=ttl)
    return "written"

vectorstore = PGVector(
    connection_string="postgresql+psycopg2://user:pass@localhost/db",
    embedding_function=embedder,
    collection_name="semantic_cache"
)

@tool
def semantic_search(query: str, k: int = 3) -> str | None:
    """Search semantic cache for similar responses."""
    docs = vectorstore.similarity_search(query, k=k)
    return docs[0].page_content if docs else None

@tool
def write_semantic_cache(query: str, answer: str) -> str:
    """Write to semantic cache."""
    doc = Document(page_content=answer, metadata={"query": query})
    vectorstore.add_documents([doc])
    return "written"