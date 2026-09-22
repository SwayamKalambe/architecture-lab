from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

'''REQUESTS'''

class CreateUserRequest(BaseModel):
    name: str
    password: str

'''RESPONSE'''

class UserResponse(BaseModel):
    user_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)