from motor.motor_asyncio import AsyncIOMotorClient
import certifi

MONGO_URL = "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@competitor-tracker-clus.nd8lyp9.mongodb.net/competitor_tracker?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
db = client["competitor_tracker"]

def get_db():
    return db
