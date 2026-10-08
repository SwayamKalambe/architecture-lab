from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Orders(Base):
    __tablename__="orders"
    order_id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id= Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    total_amount= Column(Integer, nullable=False)

class OrderItem(Base):
    __tablename__="order_items"
    order_item_id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id=Column(UUID(as_uuid=True), ForeignKey("orders.order_id"), nullable=False)
    product_id=Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    quantity=Column(Integer, nullable=False, default=1)
    price= Column(Integer,nullable=False)
   