from datetime import date
from pydantic import BaseModel

class Food(BaseModel):
    name: str
    calories: int
    protein: int
    carbohydrate: int | None = None
    fat: int | None = None

class Meal(BaseModel):
    name: str
    date: date
    items: list[Food]
    description: str | None = None
