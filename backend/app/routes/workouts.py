from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.models.workout import Workout
from app.database.mongodb import workouts_collection
from app.services.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/")
def create_workout(workout: Workout, current_user: str = Depends(get_current_user)):

    workout_data = {
        "user_email": current_user,
        "name": workout.name,
        "date": workout.date,
        "exercises": [exercise.model_dump() for exercise in workout.exercises],
    }

    workouts_collection.insert_one(workout_data)

    return {"message": "Workout created successfully"}


@router.get("/")
def get_workouts(current_user: str = Depends(get_current_user)):

    query = {"user_email": current_user}

    workouts = workouts_collection.find(query)

    cleaned_workouts = []
    for workout in workouts:
        workout["_id"] = str(workout["_id"])
        cleaned_workouts.append(workout)

    return cleaned_workouts


@router.get("/{workout_id}")
def get_workout(workout_id: str, current_user: str = Depends(get_current_user)):

    # Check if it's a valid Object ID
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID")

    # Find the workout by its ID
    workout = workouts_collection.find_one(
        {"_id": ObjectId(workout_id), "user_email": current_user}
    )

    # Check if that workout exist
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    workout["_id"] = str(workout["_id"])

    return workout


@router.put("/{workout_id}")
def update_workout(
    workout_id: str, workout: Workout, current_user: str = Depends(get_current_user)
):

    # Check if it's a valid Object ID
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID")

    # Prepare teh updated workout data
    updated_data = {
        "name": workout.name,
        "date": workout.date,
        "exercises": [exercise.model_dump() for exercise in workout.exercises],
    }

    # Update the workout
    result = workouts_collection.update_one(
        {"_id": ObjectId(workout_id), "user_email": current_user},
        {"$set": updated_data},
    )

    # Check if the workout was found
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")

    return {"message": "Workout updated successfully!"}

@router.delete("/{workout_id}")
def delete_workout(
    workout_id: str, current_user: str = Depends(get_current_user)
):
    
    # Check if it's a valid Object ID
    if not ObjectId.is_valid(workout_id):
        raise HTTPException(status_code=400, detail="Invalid workout ID")

    # Delete the workout that belongs to the current user
    result = workouts_collection.delete_one({
        "_id": ObjectId(workout_id),
        "user_email": current_user
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")

    return {"message": "Workout deleted successfully!"}
