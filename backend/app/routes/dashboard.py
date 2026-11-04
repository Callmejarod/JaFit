from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Query
from app.services.auth import get_current_user
from app.database.mongodb import meals_collection, profiles_collection
from app.services.calorie_calculator import calculate_bmr, calculate_tdee, calculate_calorie_target, calculate_macros

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/daily")
def get_daily_dashboard(date: date = Query(), current_user: str = Depends(get_current_user)):

    profile = profiles_collection.find_one({
        "user_email": current_user
    })

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Fitness profile not found"
        )

    bmr = calculate_bmr(
        profile["weight_lbs"],
        profile["height_cm"],
        profile["age"],
        profile["gender"]
    )

    tdee = calculate_tdee(bmr, profile["activity_level"])

    calorie_target = calculate_calorie_target(tdee, profile["goal"])

    target_macros = calculate_macros(calorie_target)

    meals = meals_collection.find({
        "user_email": current_user, "date": date.isoformat()
    })

    # Initialize daily totals
    total_calories = 0
    total_macros = {
        "total_protein": 0,
        "total_carbohydrate": 0,
        "total_fat": 0
    }

    # Loop through each meal
    for meal in meals:

        # Loop through each food item in side a meal
        for food in meal["items"]:
            total_calories += food["calories"]
            total_macros["total_protein"] += food["protein"]
            total_macros["total_carbohydrate"] += food.get("carbohydrate") or 0
            total_macros["total_fat"] += food.get("fat") or 0

    calories_remaining = calorie_target - total_calories

    macros_remaining = {
        "protein_remains": target_macros["protein_grams"] - total_macros["total_protein"],
        "carbohydrate_remains": target_macros["carbohydrate_grams"] - total_macros["total_carbohydrate"],
        "fat_remains": target_macros["fat_grams"] - total_macros["total_fat"]
    }

    return{
        "date": date.isoformat(),
        "calorie_target": calorie_target,
        "calories_remaining": calories_remaining,
        "total_calories": total_calories,
        "target_macros": target_macros,
        "total_macros": total_macros,
        "macros_remaining": macros_remaining
    }


