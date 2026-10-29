from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.models.meal import Meal
from app.database.mongodb import meals_collection
from app.services.auth import get_current_user

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("/")
def create_meal(meal: Meal, current_user: str = Depends(get_current_user)):

    meal_data = {
        "user_email": current_user,
        "name": meal.name,
        "items": [food.model_dump() for food in meal.items],
        "description": meal.description
    }

    meals_collection.insert_one(meal_data)

    return {"message": "Meal was added successfully"}

