from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.get_database("sanquin-matching")


def get_db():
    return db
