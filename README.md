- Initialize project

uv init .

- Add dependencies and create virtual environment

This installs:

* FastAPI → the web framework
* Uvicorn → the ASGI server
* redis[async] → async Redis client support
* langgraph, pandas, numpy, scikit-learn etc

uv add fastapi uvicorn redis[async]

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



