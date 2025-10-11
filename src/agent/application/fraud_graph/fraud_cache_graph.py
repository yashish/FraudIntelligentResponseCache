from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from .score_risk import score_risk_node
from .check_cache import check_cache_node
#from langchain_core import LLM
#from langchain_core.prompts import PromptTemplate
#from langchain_community.cache import RedisCache
#from redis import asyncio as aioredis
#import os
import random

def create_fraud_cache_graph(redis_url: str) -> StateGraph:
    """Creates a fraud detection graph with Redis caching."""
    #redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    #cache = RedisCache(redis)

    # Example LLM and prompt (placeholders, replace with actual implementations)
    #llm = LLM(model_name="gpt-4", cache=cache)
    #prompt = PromptTemplate("Detect fraud in the following transaction: {transaction_details}")

    # Define the graph
    graph = StateGraph()

    # Add nodes to the graph (placeholders, replace with actual implementations)
    #graph.add_node("score_transaction", score_transaction_node)
    graph.add_node("score_risk", score_risk_node)
    graph.add_node("check_cache", check_cache_node)  # Placeholder for check cache node
    graph.add_node("call_llm", RunnableLambda(lambda x: x))  # Placeholder for call LLM node  llm | prompt
    graph.add_node("compliance_check", RunnableLambda(lambda x: x))  # Optional compliance check node

    # Define edges
    graph.add_conditional_edges("score_risk", {
        "is_high_risk": "compliance_check",
        "default": "check_cache"
    })

    #graph.add_edge("score_transaction", "compliance_check")
    graph.add_edge("check_cache", "call_llm", condition=lambda state: state.get("miss")) # Only call LLM if cache miss
    #graph.add_edge("compliance_check", "score_risk")

    graph.set_start_node("score_risk")
    graph.set_end_node("call_llm")

    return graph
    # Note: The above code is a skeleton. Replace placeholders with actual implementations as needed.
    # Ensure to handle Redis connection lifecycle appropriately in a real application.
    # Also, consider adding error handling and logging as necessary.
    # Example usage:
    # redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    # fraud_graph = create_fraud_cache_graph(redis_url)
    # result = fraud_graph.run({"transaction_details": "Sample transaction data"})
    # print(result)
    # return graph

    def example_usage():
        redis_url = "redis://localhost:6379/0"  # Replace with actual Redis URL
        fraud_graph = create_fraud_cache_graph(redis_url)
        result = fraud_graph.run({"transaction_details": "Sample transaction data"})
        print(result)
        return graph
    
    example_usage()
    return graph

# TODO: Club this in score risk file to score risk with transaction and account details
def score_transaction(transaction_details: str) -> dict:
    """Scores a transaction for fraud."""
    # Placeholder logic for scoring
    score = random.randint(0, 100)
    is_fraud = score > 80  # Example threshold
    return {"transaction_details": transaction_details, "score": score, "is_fraud": is_fraud}

score_transaction_node = RunnableLambda(score_transaction, name="score_transaction")    

    


