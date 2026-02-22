from app.celery_worker import celery_app
from app.database import orders_collection
import asyncio
from datetime import datetime
from app.database import analytics_collection
import nest_asyncio

nest_asyncio.apply()

@celery_app.task
def process_order():
    try:
        #asyncio.run(run_analytics())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(run_analytics())

        loop.close()
    except Exception as e:
         print("Analytics task failed:", e)

async def run_analytics():
        revenue_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_revenue":{"$sum":"$total_amount"}
                }
            }
        ]
        revenue_result = await orders_collection.aggregate(revenue_pipeline).to_list(1)
        total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0

        status_pipeline = [
            {
                "$group":{
                    "_id":"$status",
                    "count":{"$sum":1}
                }
            }
        ]
        status_result= await orders_collection.aggregate(status_pipeline).to_list(None)
        orders_by_status = { item["_id"]:item["count"] for item in status_result}

        customer_pipeline=[
            {
                "$group":{
                    "_id":"$user_id",
                    "total_spent":{ "$sum":"$total_amount"}
                }
            },
            {"$sort":{"total_spent":-1}},
            {"$limit":5}
        ]
        customer_result=await orders_collection.aggregate(customer_pipeline).to_list(None)

        top_customers=[
              {
            "user_id": item["_id"],
            "total_spent":item["total_spent"]
            }
            for item in customer_result
        ]
        analytics_data={
              "type": "summary",
              "Total_Revenue": total_revenue,
              "Orders by_Status": orders_by_status,
              "top_customers":top_customers,
              "updated_at": datetime.utcnow().isoformat()
        }

        await analytics_collection.update_one(
              {"type":"summary"},
              {"$set":analytics_data},
              upsert=True
        )
        
        