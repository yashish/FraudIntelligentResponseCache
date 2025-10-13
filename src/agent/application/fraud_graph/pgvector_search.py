# pgvector search utilities and functions
# e.g., functions to interact with a pgvector database for semantic search
# This file can include connection setup, query functions, and embedding utilities.
# For example:
# import psycopg2
# from pgvector.psycopg2 import register_vector
# def connect_to_pgvector_db():
#     # connection logic here
#     pass
# def insert_vector(vector, metadata):
#     # insertion logic here
#     pass

import os
from typing import List

# Try to load .env automatically for local development (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # If python-dotenv isn't installed, environment variables must be set externally.
    pass

try:
    import openai
except Exception:  # pragma: no cover - environment dependent
    openai = None


# Configure the openai package to talk to Azure OpenAI. Set these environment
# variables in your environment before calling `get_embedding`:
# - AZURE_OPENAI_ENDPOINT (e.g. https://<resource>.openai.azure.com)
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_EMBEDDING_DEPLOYMENT (the deployment name for your embedding model)
# Optionally set AZURE_OPENAI_API_VERSION (defaults to 2023-05-15)

#$Env:AZURE_OPENAI_ENDPOINT = 'https://<your-resource>.openai.azure.com'
#$Env:AZURE_OPENAI_API_KEY = '<your-key-here>'
#$Env:AZURE_OPENAI_EMBEDDING_DEPLOYMENT = '<your-embedding-deployment>'  
#e.g. text-embedding-3-small\n$Env:AZURE_OPENAI_API_VERSION = '2023-05-15'

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

if openai is not None:
    openai.api_type = "azure"
    openai.api_key = AZURE_OPENAI_API_KEY
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_version = AZURE_OPENAI_API_VERSION


def get_embedding(text: str) -> List[float]:
    """Return embedding vector for text using Azure OpenAI via the openai package.

    Requires the environment variables described above. This avoids depending on
    the azure.ai.openai SDK and uses the widely-available `openai` package.
    """
    if openai is None:
        raise RuntimeError("openai package is not installed. Install with `pip install openai`.")

    if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY and AZURE_OPENAI_EMBEDDING_DEPLOYMENT):
        raise RuntimeError("Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and AZURE_OPENAI_EMBEDDING_DEPLOYMENT env vars before calling get_embedding()")

    # `engine` param is used when talking to Azure OpenAI via the openai package
    resp = openai.Embedding.create(engine=AZURE_OPENAI_EMBEDDING_DEPLOYMENT, input=text)
    return resp["data"][0]["embedding"]
# Example usage:
# vector = get_embedding("Sample text to embed")


def search_similar_cache(embedding: List[float], model_id, threshold=0.8): # "gpt-5o-mini", top_k=5
   # Query pgvector table for similar embeddings
   # Return {"answer": "...", "similarity": 0.92} or None
   


