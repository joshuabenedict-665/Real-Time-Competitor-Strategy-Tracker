from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo, close_mongo_connection, db
from routes.auth import router as auth_router
from routes.scrape import router as scrape_router
from routes.products import router as products_router
from routes.admin import router as admin_router
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="ShopSmart Competitor Tracker API")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(admin_router)

# ✅ Remove extra prefix — already defined in routes.scrape
app.include_router(scrape_router)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

    if db is not None:
        admin = await db["users"].find_one({"username": "admin"})
        if not admin:
            hashed = pwd_context.hash("admin123")
            await db["users"].insert_one(
                {"username": "admin", "password": hashed, "role": "admin"}
            )
            print("✅ Admin user created: admin/admin123")
        else:
            print("✅ Admin exists")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "ShopSmart API Running ✅"}
