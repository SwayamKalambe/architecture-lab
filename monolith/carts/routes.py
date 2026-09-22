from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from monolith.carts import CreateCartItemRequest, CartItemResponse
from monolith.carts import Cart, CartItem
from monolith.users import User
from core import getdb
from uuid import UUID
from typing import List

carts_router=APIRouter(tags=["CARTS"])

@carts_router.post("/cart/items")
def create_cart(payload: CreateCartItemRequest, db: Session=Depends(getdb)):


    # check if user exists
    user=db.query(User).filter(
        User.user_id==payload.user_id
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # get users cart
    cart=db.query(Cart).filter(
        Cart.user_id==payload.user_id
    ).first()

    # create cart if doesn't exist
    if not cart:
        cart=Cart(
            user_id=payload.user_id
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # check if product already exist in cart
    cart_item= db.query(CartItem).filter(
        CartItem.cart_id==cart.cart_id,
        CartItem.product_id==payload.product_id
    ).first()


    if cart_item:
        cart_item.quantity += payload.quantity

    # create new cart item if doesn't exist
    else:
        cart_item=CartItem(
                cart_id=cart.cart_id,
                product_id=payload.product_id,
                quantity=payload.quantity
            )


    

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {
        "cart_id": cart_item.cart_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity
    }