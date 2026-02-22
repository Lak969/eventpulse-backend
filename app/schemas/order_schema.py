from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
from datetime import datetime

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda : str(uuid4()))
    user_id: str
    status: str
    total_amount: float
    currency: str = "USD"
    items: List[OrderItem]
    created_at: datetime = Field(default_factory = datetime.utcnow)
    updated_at: datetime = Field(default_factory= datetime.utcnow)
    source: str = "shopify"