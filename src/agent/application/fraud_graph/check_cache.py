# Check cache node implementation
import json
import redis
import time
from langchain_core.runnables import RunnableLambda
from pgvector_search import get_embedding, search_similar_cache
from semantic_cache_client import SemanticCacheClient
from typing import List, Optional

# Redis connection setup (ensure Redis server is running and accessible)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def is_fresh(cached_timestamp, freshness_threshold=300):
    """Check if the cached data is fresh based on a threshold (in seconds)."""  
    current_time = time.time()
    return (current_time - float(cached_timestamp)) < freshness_threshold

def is_fresh(meta: dict) -> bool:
    """Check if cached data is fresh based on a threshold (in seconds) in metadata.
    A more advanced freshness check could use soft_ttl/hard_ttl from metadata.
    Defaults to 1 hour if not specified.
    Args:
        meta (dict): Metadata containing 'created_ts' and optional 'soft_ttl', 'hard_ttl'.
    
    Example Redis set operation:
    await redis.set(key, json.dumps({
    "answer": answer,
    "meta": {
        "created_ts": time.time(),
        "soft_ttl": 3600,
        "hard_ttl": 86400
        }
    }), ex=86400)
    """
    created = meta.get("created_ts", 0)
    soft_ttl = meta.get("soft_ttl", 3600)  # default 1 hour
    return time.time() - created <= soft_ttl


async def check_cache(state: dict) -> dict:
    """Checks the cache for a response based on the state."""
    query = state.get("query")
    model_id = state.get("model_id", "gpt-5o-mini")
    # consider using persona and locale if available
    
    # normalize and hash query to create a cache key
    norm_query = " ".join(query.strip().lower().split())
    key_blob = json.dumps({
        "query": norm_query,
        "model_id": model_id
        #"persona": persona,
        #"locale": locale
    }, sort_keys=True)
    
    cache_key = f"exact:{hash(key_blob)}"
    
    # 1. Exact cache match TODO: turn into async
    cached = redis_client.get(cache_key)
    if cached:
        cached_data = json.loads(cached)
        if is_fresh(cached_data.get("meta", {})):
            state.update({
                "answer": cached_data.get("answer"),
                "miss": False,
                "cache_key": cache_key,
                "source": "exact_cache",
                "cache_meta": cached_data.get("meta", {})
            })
            return state
    
    # 2. Semantic cache match
    # Embed the query and searching for similar cached entries.  
    #query = state["query"]


    #TODO: Make SemanticCacheClient a singleton or manage its lifecycle appropriately
    # Consider using a context manager or dependency injection for better lifecycle management
    # get connection details from config or environment
    client = SemanticCacheClient({
        "user": "postgres",
        "password": "postgres",
        "database": "fraud_monitoring_db",
        "host": "postgres-db",
        "port": 5432
    })

    embedding = client.get_embedding(norm_query) # get embedding for the normalized query

    # Ensure to connect to the database before searching
    await client.connect() 
    # Perform the semantic search
    # semantic_hit = search_similar_cache(embedding, model_id, threshold=0.8) # Implement this function
    semantic_hit = await client.search_similar_cache(embedding, top_k=5)
    await client.close()  

    if semantic_hit:
        state.update({
            **state,
            "answer": semantic_hit["answer"],
            "miss": False,
            "similarity": semantic_hit["similarity"],
            "source": "semantic_cache"
            #"cache_key": semantic_hit.get("cache_key"),
            #"cache_meta": semantic_hit.get("meta", {})
        })
        return state

    # Step 6: Cache admission control
    # if risk_score < 0.8:
    #     await set_exact_cache(key, response, ttl=3600)
    #     await upsert_semantic_cache(req.query, response, embedding)


    # 3. Cache miss
    return {
        **state,
        "miss": True
    }

check_cache_node = RunnableLambda(check_cache, name="check_cache")

# Example usage:
# result = check_cache_node.invoke({"transaction_id": "12345"})
# print(result)
# Output: {'transaction_id': '12345', 'miss': True}
