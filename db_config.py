import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://Anjum:12345@cluster0.kgghy2i.mongodb.net/?appName=Cluster0",
)
DB_NAME = os.getenv("MONGODB_DB_NAME", "plant_disease_db")
DISEASE_COLLECTION = "disease_info"


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)


def get_db() -> Database:
    return get_client()[DB_NAME]


def get_disease_collection() -> Collection:
    return get_db()[DISEASE_COLLECTION]
