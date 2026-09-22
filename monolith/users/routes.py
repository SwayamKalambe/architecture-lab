from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from monolith.users import CreateUserRequest, UserResponse
from monolith.users import User
from core import getdb
from uuid import UUID
from typing import List

user_router=APIRouter(tags=["USERS"])

@user_router.post("/create-user")
def create_user(payload: CreateUserRequest, db: Session=Depends(getdb)):

    new_user=User(
        name=payload.name,
        password=payload.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"Welcome {new_user.name}",
        "user_id": new_user.user_id
    }


@user_router.get("/retrieve-all-users", response_model=List[UserResponse])
def retrieve_all_users(db: Session=Depends(getdb)):
    users = db.query(User).all()

    return users

@user_router.get("/retrieve-user/{user_id}", response_model=UserResponse)
def retrieve_user(user_id : UUID, db: Session=Depends(getdb)):
    users = db.query(User).filter(
        User.user_id == user_id
    ).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    return users