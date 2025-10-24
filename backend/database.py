from motor.motor_asyncio import AsyncIOMotorClient

# ✅ Replace <password> with your real password
MONGO_URL = "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@competitor-tracker-clus.nd8lyp9.mongodb.net/competitor_tracker?retryWrites=true&w=majority&appName=competitor-tracker-cluster"

client = AsyncIOMotorClient(MONGO_URL)
db = client["competitor_tracker"]

def get_db():
    return db
