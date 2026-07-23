from fastapi import APIRouter
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
def register_user(user: User):

    return {
        "message": "User created successfully",
        "user": user
    }