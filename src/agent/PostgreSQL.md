
* Step 1. Pull a PostgreSQL image with pgvector preinstalled
# The pgvector extension is not included in the standard PostgreSQL Docker image, but there are official builds that support it — e.g., from ankane/pgvector or you can build your own.

Run this to pull and start the container:

```bash
docker run -d --name pgvector-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fraud_monitoring_db -v pgdata:/var/lib/postgresql/data -p 5432:5432 ankane/pgvector
```

- Verify it's running
```bash
docker ps
```

* Jump inside the running container and connect from the command line

```bash
docker exec -it pgvector-db psql -U postgres -d fraud_monitoring_db
```

- Or if you have psql installed locally
```bash
psql postgres://postgres:postgres@localhost:5432/fraud_monitoring_db
```
- Check pgvector is enabled and create sematic cache table. pgcrypto is optional for random GUID:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS semantic_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    answer TEXT,
    embedding vector(1536) NOT NULL,
    created_ts TIMESTAMPTZ NOT NULL DEFAULT now()
);
\dx
```

- Create ivfflat index for fast nearest-neighbor search using cosine similarity.
- Tune "lists" for performance based on dataset size (e.g., 100..1000).

```bash
CREATE INDEX IF NOT EXISTS semantic_cache_embedding_idx
    ON semantic_cache USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```