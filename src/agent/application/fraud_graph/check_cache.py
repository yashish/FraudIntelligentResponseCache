# Check cache node implementation
import json
import redis
import time
from langchain_core.runnables import RunnableLambda
from pgvector_search import get_embedding

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


def check_cache(state: dict) -> dict:
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
    
    # 1. Exact cache match
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
    
    # 2. Semantic cache match (not implemented here, placeholder)
    # This would involve embedding the query and searching for similar cached entries.  
    # TODO: Implement semantic search in cache.
    embedding = get_embedding(norm_query)  # Placeholder function
    sem_keys = redis_client.smembers("semantic_keys")

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
