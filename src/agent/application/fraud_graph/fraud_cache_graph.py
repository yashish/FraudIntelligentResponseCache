from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
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
    graph.add_node("input_transaction", RunnableLambda(lambda x: x))
    #graph.add_node("fraud_detection", llm | prompt)
    graph.add_node("output_result", RunnableLambda(lambda x: x))

    # Define edges
    graph.add_edge("input_transaction", "output_result")
    #graph.add_edge("output_result", "fraud_detection")

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

def score_transaction(transaction_details: str) -> dict:
    """Scores a transaction for fraud."""
    # Placeholder logic for scoring
    score = random.randint(0, 100)
    is_fraud = score > 70  # Example threshold
    return {"transaction_details": transaction_details, "score": score, "is_fraud": is_fraud}

def score_risk(state):
    """Scores risk based on the state."""
    # Placeholder logic for risk scoring
    risk_score = random.randint(0, 100)
  

    features = state.get("aml_features", {})
    # simulated model prediction. Replace with actual model inference

    return {"state": state, "risk_score": risk_score}


