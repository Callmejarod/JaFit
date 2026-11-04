from fastapi import FastAPI
from app.routes import users
from app.routes import workouts
from app.routes import meals
from app.routes import profiles
from app.routes import dashboard

app = FastAPI(
    title="JaFit API",
    description="Health and fitness tracking API",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(meals.router)
app.include_router(profiles.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {
        "message": "jaFit API is running!"
    }