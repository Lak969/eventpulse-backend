from fastapi import FastAPI,APIRouter
from app.database import orders_collection
from contextlib import asynccontextmanager
from app.schemas.order_schema import Order
from app.routers import order_router
from app.routers.analytics_router import router as analytics_router 




@asynccontextmanager
async def lifespan(app:FastAPI):
    await orders_collection.create_index("order_id", unique=True)
    await orders_collection.create_index([("user_id", 1),("created_at",-1)])
    await orders_collection.create_index("status")
    await orders_collection.create_index([("status", 1),("created_at",-1)])
    print("Indexes created successfully")
    yield

app=FastAPI(title = "EventPulse API", lifespan = lifespan)
app.include_router(order_router.router)
app.include_router(analytics_router)

@app.get("/health")
async def health():
    return {"status": "ok"}



@app.get("/test-order")
async def test_order():
    order = Order(
        user_id="user123",
        status="completed",
        total_amount=150.0,
        items=[
            {"product_id": 1, "quantity": 2, "price": 50.0}
        ]
    )
    return order

