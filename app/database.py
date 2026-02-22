from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

print("DB NAME:", settings.DATABASE_NAME)
client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

orders_collection = database["orders"]
analytics_collection = database["analytics"]

