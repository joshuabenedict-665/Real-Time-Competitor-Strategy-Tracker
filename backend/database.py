from motor.motor_asyncio import AsyncIOMotorClient
import certifi

# --- MongoDB Atlas Connection URL ---
MONGO_URL = (
    "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@"
    "competitor-tracker-clus.nd8lyp9.mongodb.net/"
    "competitor_tracker?retryWrites=true&w=majority"
)

# --- Create Async MongoDB Client ---
client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())

# --- Access Database ---
db = client["competitor_tracker"]

# --- Get Database Instance (for Dependency Injection) ---
async def get_db():
    return db

# --- Optional: Check Connection Function ---
async def check_connection():
    try:
        await client.admin.command("ping")
        return {"status": "connected", "database": "competitor_tracker"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
