from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import os

# ✅ Use environment variable OR fallback to your hardcoded URI
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@"
    "competitor-tracker-clus.nd8lyp9.mongodb.net/"
    "competitor_tracker?retryWrites=true&w=majority"
)

# ✅ Create Client
client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())

# ✅ Select DB
db = client["competitor_tracker"]

# ✅ Dependency Injection for FastAPI
async def get_db():
    return db  # ✔ No context manager needed in Motor client

# ✅ Connection Test Function (Optional)
async def check_connection():
    try:
        await client.admin.command("ping")
        return {"status": "connected", "database": "competitor_tracker"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
