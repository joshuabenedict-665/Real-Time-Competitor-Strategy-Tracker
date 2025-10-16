# database.py
from motor.motor_asyncio import AsyncIOMotorClient

# Replace with your MongoDB Atlas credentials
MONGO_URL = "mongodb+srv://adminUser:YourStrongPass123@cluster0.mongodb.net/competitor_tracker?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL)
db = client["competitor_tracker"]  # database name

def get_db():
    return db
