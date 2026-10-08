from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

'''REQUESTS'''
class CreateOrderRequest(BaseModel):
    user_id: UUID


'''RESPONSE'''

class OrderItemResponse(BaseModel):
    product_id: UUID
    product_name: str
    price: int
    quantity: int

    model_config=ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    order_id: UUID
    total_amount: int
    items: list[OrderItemResponse]

    model_config=ConfigDict(from_attributes=True)
    