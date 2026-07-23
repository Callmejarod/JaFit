from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.database.mongodb import users_collection
from app.services.security import hash_password
from datetime import datetime


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register_user(user: User):

    # Check if email already exsist
    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code = 400,
            detail="Email already registered"
        )

    print(user.password)
    print(len(user.password))

    hashed_password = hash_password(user.password)



    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "created_at": datetime.now()
    }

    users_collection.insert_one(user_data)

    return {
        "message": "User created successfully",
    }