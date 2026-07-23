from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.models.login import LoginRequest
from app.database.mongodb import users_collection
from app.services.security import hash_password, verify_password
from app.services.auth import create_access_token
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

@router.post("/login")
def login(login_data: LoginRequest):

    # Find user by email
    user = users_collection.find_one(
        {"email": login_data.email}
    )

    # User not found
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        login_data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT
    access_token = create_access_token(
        {
            "sub": user["email"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }