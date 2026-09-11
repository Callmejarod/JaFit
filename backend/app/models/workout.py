from pydantic import BaseModel
from datetime import datetime

class WorkoutExercise(BaseModel):
    name: str
    sets: int
    reps: int
    weight: float

class Workout(BaseModel):
    name: str
    date: datetime
    exercises: list[WorkoutExercise]