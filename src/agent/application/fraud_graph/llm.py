from langchain_core.runnables import RunnableLambda
from langchain.chat_models import AzureOpenAI
from cache_client import write_exact_cache, write_semantic_cache
import os

# Optional cache writers (can be no-ops if not used)

# Azure OpenAI config
llm = AzureOpenAI(
    deployment_name="gpt-4o-mini",  # Your Azure deployment name
    model="gpt-4",                  # Optional: used for metadata
    api_key= os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2023-07-01-preview"
)

def call_llm(state: dict) -> dict:
    query = state["query"]

    # Call Azure OpenAI LLM
    response = llm.invoke(query)

    # Optional: write to cache
    # Cache keys can include model_id, persona, locale if needed
    cache_key = str(hash(query))
    write_exact_cache.invoke(cache_key, response)
    write_semantic_cache.invoke(query, response)

    return {
        **state,
        "answer": response,
        "source": "llm"
    }

call_llm_node = RunnableLambda(call_llm, name="call_llm")