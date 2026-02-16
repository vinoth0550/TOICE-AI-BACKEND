
# database.py

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["prd_database"]
collection = db["prds"]


def save_prd(data: dict):
    data["created_at"] = datetime.utcnow()
    result = collection.insert_one(data)
    return str(result.inserted_id)
