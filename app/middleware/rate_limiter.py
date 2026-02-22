from fastapi import Request, HTTPException
from app.redis_client import redis_client

RATE_LIMIT=10
WINDOW_SECONDS=60

async def rate_limiter(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    current_count= await redis_client.incr(key)

    if current_count == 1:
        await redis_client.expire(key, WINDOW_SECONDS)

    if current_count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="TOO many request. Please Try Again"
        )