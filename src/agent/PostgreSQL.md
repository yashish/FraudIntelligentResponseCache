
* Step 1. Pull a PostgreSQL image with pgvector preinstalled
# The pgvector extension is not included in the standard PostgreSQL Docker image, but there are official builds that support it — e.g., from ankane/pgvector or you can build your own.

Run this to pull and start the container:
```bash
docker run -d \
  --name pgvector-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=vector_db \
  -p 5432:5432 \
  ankane/pgvector
```

- Verify it's running
```bash
docker ps
```

* Jump inside the running container and connect from the command line

```bash
docker exec -it pgvector-db psql -U postgres -d vector_db
```

- Or if you have psql installed locally
```bash
psql postgres://postgres:postgres@localhost:5432/vector_db
```
- Check pgvector is enabled:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
\dx
```
