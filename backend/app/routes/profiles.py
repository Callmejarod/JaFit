from fastapi import APIRouter, HTTPException, Depends, Query
from bson import ObjectId
from app.models.fitnessProfile import FitnessProfile
from app.services.calorie_calculator import calculate_bmr, calculate_tdee, calculate_calorie_target, calculate_macros
from app.database.mongodb import profiles_collection
from app.services.auth import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/")
def create_profile(profile: FitnessProfile, current_user: str = Depends(get_current_user)):

    # Check if this user already has a profile
    existing_profile = profiles_collection.find_one({
        "user_email": current_user
    })

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Fitness profile already exists"
        )

    profile_data = {
        "user_email": current_user,
        "age": profile.age,
        "height_cm": profile.height_cm,
        "weight_lbs": profile.weight_lbs,
        "gender": profile.gender,
        "activity_level": profile.activity_level,
        "goal": profile.goal 
    }

    profiles_collection.insert_one(profile_data)

    return {"message": "Fitness profile was created successfully"}

@router.get("/me")
def get_profile(current_user: str = Depends(get_current_user)):

    profile = profiles_collection.find_one({
        "user_email": current_user
    })

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Fitness profile not found"
        )

    # Convert ObjectId to string for JSON serialization
    profile["_id"] = str(profile["_id"])

    return profile

@router.put("/me")
def update_profile(profile: FitnessProfile, current_user: str = Depends(get_current_user)):

    existing_profile = profiles_collection.find_one({
        "user_email": current_user
    })

    if not existing_profile:
        raise HTTPException(
            status_code=404,
            detail="Fitness profile not found"
        )

    updated_data = {
        "age": profile.age,
        "height_cm": profile.height_cm,
        "weight_lbs": profile.weight_lbs,
        "gender": profile.gender,
        "activity_level": profile.activity_level,
        "goal": profile.goal 
    }

    result = profiles_collection.update_one(
        {"user_email": current_user},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Fitness profile not found"
        )

    return {"message": "Fitness profile was updated successfully"}

@router.get("/me/calories")
def get_calorie_estimate(current_user: str = Depends(get_current_user)):

    profile = profiles_collection.find_one({
        "user_email": current_user
    })

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    bmr = calculate_bmr(
        profile["weight_lbs"],
        profile["height_cm"],
        profile["age"],
        profile["gender"]
    )

    tdee = calculate_tdee(bmr, profile["activity_level"])

    calorie_target = calculate_calorie_target(tdee, profile["goal"])

    macros_target = calculate_macros(calorie_target)

    return {
        "bmr": bmr,
        "tdee": tdee,
        "calorie_target": calorie_target,
        "goal": profile["goal"],
        "macro_targets": macros_target,
        "unit": "kcal/day"
    }