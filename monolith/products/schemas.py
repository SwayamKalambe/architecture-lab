from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

'''REQUESTS'''

class CreateProductRequest(BaseModel):
    product_name: str
    price: int
    description: str

'''RESPONSE'''

class ProductResponse(BaseModel):
    product_id: UUID
    product_name: str
    price: int
    description: str


model_config = ConfigDict(from_attributes=True)