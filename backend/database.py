# database.py
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@competitor-tracker-clus.nd8lyp9.mongodb.net/competitor_tracker?retryWrites=true&w=majority"
)

client = None
db = None

async def connect_to_mongo():
    global client, db
    if client:
        return
    try:
        client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
        db = client.get_database("competitor_tracker")
        await client.admin.command("ping")
        print("✅ MongoDB Connected")
    except Exception as e:
        client = None
        db = None
        print("❌ MongoDB connection failed:", e)
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        client = None
        print("🔌 MongoDB Disconnected")

def get_db():
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
    return db

# ✅ Products collection getter (no imports here!)
def get_products_collection():
    return get_db()["products"]
