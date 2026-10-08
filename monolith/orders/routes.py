from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from monolith.orders import CreateOrderRequest, OrderResponse
from monolith.orders import Orders, OrderItem
from monolith.users import User
from monolith.carts import Cart, CartItem
from monolith.products import Product
from core import getdb
from uuid import UUID
from typing import List


orders_router=APIRouter(tags=["ORDERS"])

@orders_router.post("/create-order", response_model=OrderResponse)
def create_order(payload: CreateOrderRequest, db: Session= Depends(getdb)):

    user=db.query(User).filter(
            User.user_id==payload.user_id
        ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    cart= db.query(Cart).filter(
        Cart.user_id==payload.user_id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()


    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart Empty"
        )
    product_ids = [item.product_id for item in cart_items]

    products = db.query(Product).filter(
        Product.product_id.in_(product_ids)
    ).all()

    products_by_id = {
        product.product_id: product
        for product in products
    }

    total_amount = 0
    order_items_data = []

    for item in cart_items:
        product = products_by_id[item.product_id]

        total_amount += product.price * item.quantity

        order_items_data.append({
            "product_id": product.product_id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity
        })



    order=Orders(
        user_id=payload.user_id,
        total_amount=total_amount
    )

    db.add(order)
    db.flush()

    for item in order_items_data:
        order_item = OrderItem(
            order_id=order.order_id,
            product_id=item["product_id"],
            price=item["price"],
            quantity=item["quantity"]
    )

        db.add(order_item)
    db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).delete()
    db.commit()

    return OrderResponse(
    order_id=order.order_id,
    total_amount=order.total_amount,
    items=order_items_data
    )


@orders_router.get("/orders/{order_id}",response_model=OrderResponse)
def get_order(order_id: UUID,db: Session = Depends(getdb)):
    # 1. Get order
    order = db.query(Orders).filter(
        Orders.order_id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # 2. Get order items
    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order.order_id
    ).all()

    # 3. Get all products in one query
    product_ids = [item.product_id for item in order_items]

    products = db.query(Product).filter(
        Product.product_id.in_(product_ids)
    ).all()

    products_by_id = {
        product.product_id: product
        for product in products
    }

    # 4. Build response items
    items = []

    for item in order_items:
        product = products_by_id[item.product_id]

        items.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "price": item.price,
            "quantity": item.quantity
        })

    # 5. Return order
    return OrderResponse(
        order_id=order.order_id,
        total_amount=order.total_amount,
        items=items
    )


@orders_router.get("/orders/user/{user_id}",response_model=List[OrderResponse])
def get_user_orders(user_id: UUID,db: Session = Depends(getdb)):
    
    # 1. Check user exists
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 2. Get all orders for the user
    orders = db.query(Orders).filter(
        Orders.user_id == user_id
    ).all()

    if not orders:
        return []

    # 3. Get all order IDs
    order_ids = [order.order_id for order in orders]

    # 4. Get all order items in one query
    order_items = db.query(OrderItem).filter(
        OrderItem.order_id.in_(order_ids)
    ).all()

    # 5. Get all product IDs
    product_ids = [item.product_id for item in order_items]

    # 6. Get all products in one query
    products = db.query(Product).filter(
        Product.product_id.in_(product_ids)
    ).all()

    # 7. Create product lookup
    products_by_id = {
        product.product_id: product
        for product in products
    }

    # 8. Group order items by order_id
    items_by_order = {}

    for item in order_items:
        items_by_order.setdefault(item.order_id, []).append({
            "product_id": item.product_id,
            "product_name": products_by_id[item.product_id].name,
            "price": item.price,
            "quantity": item.quantity
        })

    # 9. Build response
    result = []

    for order in orders:
        result.append(
            OrderResponse(
                order_id=order.order_id,
                total_amount=order.total_amount,
                items=items_by_order.get(order.order_id, [])
            )
        )

    return result

@orders_router.delete("/orders/{order_id}")
def delete_order(order_id: UUID,db: Session = Depends(getdb)):
    # 1. Find order
    order = db.query(Orders).filter(
        Orders.order_id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # 2. Delete order items
    db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).delete(synchronize_session=False)

    # 3. Delete order
    db.delete(order)

    # 4. Commit
    db.commit()

    return {
        "message": "Order deleted successfully"
    }