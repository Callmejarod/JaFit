import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

database = client["jafit"]

users_collection = database["users"]