from fastapi import APIRouter 
from app.database import analytics_collection

from app.redis_client import redis_client 
import json

router = APIRouter(prefix= "/analytics", tags=["Analytics"])

@router.get("/summary")
async def get_summary():
    try:
        cache_key = "analytics_summary"
        cached = await redis_client.get(cache_key)

        if cached:
            return json.loads(cached)
        
        data = await analytics_collection.find_one({},{"_id":0})

        if not data:
            return {"message": "no analytics found"}
        
        await redis_client.set(cache_key,json.dumps(data),ex=60)
        print(data)
        return data
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/top-customers")
async def get_top_customers(limit: int=5):
    cache_key = f"top_customers_{limit}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    data = await analytics_collection.find_one({},{"_id":0})
    if not data or "top_customers" not in data:
        return {"message":"No data available"}

    customers=data["top_customers"] 
    customers_sorted=sorted(
        customers,
        key = lambda x:x["total_spent"],
        reverse=True
        )
    
    result = customers_sorted[:limit]
    await redis_client.set(cache_key, json.dumps(result), ex=60)

    return result