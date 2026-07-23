import os 
from pymango import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

databases = client["jafit"]

users_collection = database["users"]
