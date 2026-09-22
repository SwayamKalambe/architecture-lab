from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Cart(Base):
    __tablename__="carts"
    cart_id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id= Column(UUID, ForeignKey("users.user_id"), unique=True, nullable=False)

class CartItem(Base):
    __tablename__="cart_items"
    cart_item_id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id=Column(UUID(as_uuid=True), ForeignKey("carts.cart_id"), nullable=False)
    product_id=Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    quantity=Column(Integer, nullable=False, default=0)

    __table_args__=(
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="unq_cart_product"
        ),
    )


    