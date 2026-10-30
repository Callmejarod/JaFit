from fastapi import APIRouter, HTTPException, Depends, Query
from bson import ObjectId
from datetime import date
from app.models.meal import Meal
from app.database.mongodb import meals_collection
from app.services.auth import get_current_user

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/")
def create_meal(meal: Meal, current_user: str = Depends(get_current_user)):

    meal_data = {
        "user_email": current_user,
        "name": meal.name,
        "date": meal.date.isoformat(),
        "items": [food.model_dump() for food in meal.items],
        "description": meal.description,
    }

    meals_collection.insert_one(meal_data)

    return {"message": "Meal was added successfully"}


@router.get("/")
def get_meals(current_user: str = Depends(get_current_user)):

    query = {"user_email": current_user}

    meals = meals_collection.find(query)

    cleaned_meals = []
    for meal in meals:
        meal["_id"] = str(meal["_id"])
        cleaned_meals.append(meal)

    return cleaned_meals


@router.get("/summary")
def get_daily_summary(
    date: date = Query(), current_user: str = Depends(get_current_user)
):

    # Find meals that belong to the user on the selected date
    meals = meals_collection.find(
        {"user_email": current_user, "date": date.isoformat()}
    )

    # Initialize daily totals
    total_calories = 0
    total_protein = 0
    total_carbohydrate = 0
    total_fat = 0

    # Loop through each meal
    for meal in meals:

        # Loop through each food item in side a meal
        for food in meal["items"]:
            total_calories += food["calories"]
            total_protein += food["protein"]
            total_carbohydrate += food.get("carbohydrate") or 0
            total_fat += food.get("fat") or 0

    return {
        "date": date.isoformat(),
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbohydrate": total_carbohydrate,
        "total_fat": total_fat,
    }


@router.get("/{meal_id}")
def get_meal(meal_id: str, current_user: str = Depends(get_current_user)):

    # Check if it's a valid Object ID
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=400, detail="Invalid meal ID")

    # Find the meal by its ID
    meal = meals_collection.find_one(
        {"_id": ObjectId(meal_id), "user_email": current_user}
    )

    # Check if that meal exist
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")

    meal["_id"] = str(meal["_id"])

    return meal


@router.put("/{meal_id}")
def update_meal(
    meal_id: str, meal: Meal, current_user: str = Depends(get_current_user)
):

    # Check if it's a valid Object ID
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=400, detail="Invalid meal ID")

    # Prepare the updated meal data
    updated_data = {
        "name": meal.name,
        "date": meal.date.isoformat(),
        "items": [food.model_dump() for food in meal.items],
        "description": meal.description,
    }

    # Update the meal
    result = meals_collection.update_one(
        {"_id": ObjectId(meal_id), "user_email": current_user}, {"$set": updated_data}
    )

    # Check if the meal was found
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Meal not found")

    return {"message": "Meal updated successfully!"}


@router.delete("/{meal_id}")
def delete_meal(meal_id: str, current_user: str = Depends(get_current_user)):

    # Check if it's a valid Object ID
    if not ObjectId.is_valid(meal_id):
        raise HTTPException(status_code=400, detail="Invalid meal ID")

    # Delete the meal that belongs to the current user
    result = meals_collection.delete_one(
        {"_id": ObjectId(meal_id), "user_email": current_user}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Meal not found")

    return {"message": "Meal deleted successfully!"}
