from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

'''REQUESTS'''
class CreateCartItemRequest(BaseModel):
    user_id: UUID
    product_id: UUID
    quantity : int = Field(gt=0)



'''RESPONSE'''
class CartItemResponse(BaseModel):
    cart_id: UUID
    cart_item_id: UUID
    product_id: UUID
    quantity: int


model_config=ConfigDict(from_attributes=True)