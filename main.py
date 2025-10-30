from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from redis import asyncio as aioredis
import asyncio
import json
import random
import os

app = FastAPI(title="FastAPI + Redis/Semantic Cache")

class AMLInput(BaseModel):
    transaction_amount: float
    transaction_type: str
    transaction_hour: int
    origin_country: str
    destination_country: str
    customer_age: int
    account_tenure_days: int
    kyc_verified: bool
    prior_fraud_flag: bool
    device_type: str
    ip_risk_score: float
    velocity_score: float

#Placeholder for actual model prediction function
@app.post("/score")
async def score(input: AMLInput):
    raw = input.dict()
    risk_score = predict_risk_score(raw)
    return {
        "risk_score": risk_score,
        "risk_level": (
            "low" if risk_score < 0.3 else
            "medium" if risk_score < 0.6 else
            "elevated" if risk_score < 0.8 else
            "high"
        ),
        "note": "Use this score to gate cache admission or route to compliance agent"
    }


REDIS_HOST = os.getenv("REDIS_HOST", "redis://localhost:6379/0")
#redis = aioredis.from_url(f"redis://{REDIS_HOST}", decode_responses=True)
#lock = asyncio.Lock()

# Dependency async function to get Redis connection
async def get_redis():
    """Dependency function to provide a Redis connection."""
    redis = await aioredis.from_url(
        REDIS_HOST,
        encoding="utf-8",
        decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()


# Simulated slow DB call
async def get_user_from_db(user_id: int):
    print("Fetching from DB...")
    await asyncio.sleep(2)  # simulate latency
    return {"id": user_id, "name": f"User{user_id}", "score": random.randint(0, 100)}

@app.get("/user/{user_id}")
async def get_user(user_id: int, redis: aioredis.Redis = Depends(get_redis)):
    cache_key = f"user:{user_id}"

    # Try to get cached user
    cached = await redis.get(cache_key)
    if cached:
        print("Cache hit!")
        return json.loads(cached)

    # Cache miss: fetch from "DB"
    print("Cache miss!")
    user = await get_user_from_db(user_id)

    # Store in cache for 60 seconds
    await redis.setex(cache_key, 60, json.dumps(user))

    return user