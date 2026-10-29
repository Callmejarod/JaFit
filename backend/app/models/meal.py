from pydantic import BaseModel

class Food(BaseModel):
    name: str
    calories: int
    protien: int
    carbohydrate: int
    fat: int

class Meal(BaseModel):
    name: str
    items: list[Food]
    description: str | None = None
