from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
import os

# client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi("1"))
# db = client.get_database("sanquin")

client = AsyncIOMotorClient(os.environ["MONGO_URI"])
db = client.get_database("sanquin-matching")


def get_db():
    return db
