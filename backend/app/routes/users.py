from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.database.mongodb import users_collection
from app.services.security import hash_password
from datetime import datetime, timezone


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

    hashed_password = hash_password(user.password)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }

    print(user_data.get("created_at"))

    users_collection.insert_one(user_data)

    return {
        "message": "User created successfully",
    }