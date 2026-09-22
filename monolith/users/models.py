from sqlalchemy import Column, Integer, String, Boolean
from core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__="users"
    user_id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=Column(String(50), nullable=False)
    password=Column(String(100), nullable=False)
    is_deleted=Column(Boolean, default=False, nullable=False)