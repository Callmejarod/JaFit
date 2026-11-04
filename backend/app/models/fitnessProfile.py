from pydantic import BaseModel
from typing import Literal

class FitnessProfile(BaseModel):
    age: int
    height_cm: float #height in centimeters
    weight_lbs: float #weight in pounds
    gender: Literal ["male", "female"]
    activity_level: Literal[
        "sedentary",
        "lightly_active",
        "moderately_active",
        "very_active",
        "extra_active"
    ]
    goal : Literal["lose_weight", "maintain_weight", "gain_weight"]