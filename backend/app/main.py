from fastapi import FastAPI
from app.routes import users

app = FastAPI(
    title="JaFit API",
    description="Health and fitness tracking API",
    version="1.0.0"
)

app.include_router(users.router)

@app.get("/")
def root():
    return {
        "message": "jaFit API is running!"
    }