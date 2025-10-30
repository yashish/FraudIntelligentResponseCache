- Initialize project

uv init .

- Add dependencies and create virtual environment

This installs:

* FastAPI - the web framework
* Uvicorn - the ASGI server
* redis[async] - async Redis client support
* asyncpg - pgvector client
* langgraph, pandas, numpy, scikit-learn etc

uv add fastapi uvicorn redis[async] asyncpg

uv add scikit-learn pandas numpy joblib

uv add langchain_core --pre langgraph

- Verify installed dependencies

uv pip list

- Set in your environment

export REDIS_URL="redis://:password@redis-host:6379/0"

Run the code

- uv run uvicorn main:app --reload

* INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
* INFO:     Started reloader process [20968] using StatReload
* INFO:     Started server process [9060]
* INFO:     Waiting for application startup.
* INFO:     Application startup complete.

Then visit:
- http://127.0.0.1:8000/user/42

# Optional: Use environment variables

If connecting to a cloud Redis (e.g., AWS ElastiCache, Azure Cache, etc.):

- export REDIS_URL="redis://:password@redis-host:6379/0"

# Confirm that Redis is installed

Run one of these commands in your terminal or command prompt:

Windows (PowerShell / CMD):

redis-server --version

Windows: You can only run on Docker

 https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/

## Use Case: Agentic Cache + AML/KYC Model
# Goal
- Use a trained fraud detection model (e.g., for suspicious transaction patterns, identity risk scoring) to:
- Pre-screen inputs before LLM invocation
- Gate cache admission based on risk
- Trigger cache bypass or regeneration for high-risk cases

## Azure OpenAI configuration

The project supports Azure OpenAI embeddings via the `openai` Python package. Set the following environment variables before running code that calls OpenAI:

- `AZURE_OPENAI_ENDPOINT` — your Azure OpenAI resource base URL, e.g. `https://<your-resource>.openai.azure.com`
- `AZURE_OPENAI_API_KEY` — the API key for your Azure OpenAI resource
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` — the deployment name you created for an embedding model (e.g. `text-embedding-3-small`)
- `AZURE_OPENAI_API_VERSION` (optional) — API version (default `2023-05-15`)

You can set these as OS environment variables or use a `.env` file for local development (do NOT commit real secrets).

Example `.env` (create a file named `.env` in the repo root):

```
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2023-05-15
```

If you use `.env` locally, add it to `.gitignore` to avoid committing secrets. See the repo's `.env.example` for placeholders.

Note: The project uses `python-dotenv` (if installed) to automatically load a `.env` file during local development. Install dependencies (`pip install -r requirements.txt` or the project's chosen tool) to enable this behavior.

# Semantic Cache
## Install pgvector extension and create the index

CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX ON semantic_cache USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

- Create a PostgreSQL table named semantic_cache with columns
* id: UUID
* query: original query text
* answer: cached LLM response
* embedding: vector(1536) or similar
* created_ts: timestamp

* Best Practices
- Use ivfflat index for fast similarity search
- Normalize embeddings before insert/search
- Store model_id, persona, locale as additional filters if needed for cache multi-dimensional cache
- Add TTL logic to exclude stale entries

# After installing PostgreSQL create table and index:

-- Ensure pgvector is available
CREATE EXTENSION IF NOT EXISTS vector;

-- (Optional) for gen_random_uuid() default — requires pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create semantic_cache table
CREATE TABLE IF NOT EXISTS semantic_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    answer TEXT,
    embedding vector(1536) NOT NULL,
    created_ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create ivfflat index for fast nearest-neighbor search using cosine similarity.
-- Tune "lists" for performance based on dataset size (e.g., 100..1000).
CREATE INDEX IF NOT EXISTS semantic_cache_embedding_idx
    ON semantic_cache USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

* Note that using a Docker image with pre-installed pgvector and pgcrypto is the preferred developer workflow




