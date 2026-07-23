from fastapi import APIRouter
from models.user import User
from database.mongodb import users_collection


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register_user(user: User):

    user_data = user.dict()

    users_collection.insert_one(user_data)

    return {
        "message": "User created successfully",
        "user": user_data
    }