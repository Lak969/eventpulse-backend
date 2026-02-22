from fastapi import HTTPException, APIRouter, Depends
from app.schemas.order_schema import Order
from app.database import orders_collection
from app.tasks.order_tasks import process_order
from typing import List
import time
from app.redis_client import redis_client
from app.middleware.rate_limiter import rate_limiter

router = APIRouter(prefix="/orders", tags= ["Orders"])

@router.post("/ingest", status_code=201, dependencies =[Depends(rate_limiter)])
async def ingest_order(orders: List[Order]):
    try:
        start_time = time.time()
        order_dicts = [order.model_dump() for order in orders]
        CHUNK_SIZE= 1000
        total_inserted=0
        
        for i in range(0,len(order_dicts),CHUNK_SIZE):
            chunk=order_dicts[i:i+CHUNK_SIZE]
            result = await orders_collection.insert_many(chunk)
            total_inserted += len(result.inserted_ids)

        duration = time.time() - start_time
        process_order.delay()

    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=409, detail = "Order already exist")
        raise HTTPException(status_code=500, detail=str(e))
    return{"total_received":len(order_dicts), "total_inserted": total_inserted, "time_taken_seconds": round(duration,2)}

@router.get("/redis-test")
async def redis_test():
    await redis_client.set("test-value", "eventpulse")
    value = await redis_client.get("test-value")
    return {"redis_value":value}