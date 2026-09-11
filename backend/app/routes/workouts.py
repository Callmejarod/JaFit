from fastapi import APIRouter, HTTPException, Depends
from app.models.workout import Workout
from app.database.mongodb import workouts_collection
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"]
)

@router.post("/")
def create_workout(
    workout: Workout,
    current_user: str = Depends(get_current_user)
):

    workout_data = {
        "user_email": current_user,
        "name": workout.name,
        "date": workout.date,
        "exercises": [
            exercise.model_dump()
            for exercise in workout.exercises
        ]
    }

    workouts_collection.insert_one(workout_data)

    return {
        "message": "Workout created successfully"
    }

@router.get("/")
def get_workouts(
    current_user: str = Depends(get_current_user)
):

    query = {"user_email": current_user}

    workouts = workouts_collection.find(query)

    cleaned_workouts = []
    for workout in workouts:
        workout["_id"] = str(workout["_id"])
        cleaned_workouts.append(workout)
        
    return cleaned_workouts