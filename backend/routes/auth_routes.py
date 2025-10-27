from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from passlib.context import CryptContext
from pymongo import MongoClient
import jwt
import datetime

# MongoDB Connection
client = MongoClient("mongodb+srv://joshuabenedict665_db_user:YOUR_PASSWORD@competitor-tracker-clus.nd8lyp9.mongodb.net/")
db = client["competitor_tracker"]
users_collection = db["users"]

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecretkey"

# User schema
class User(BaseModel):
    username: str
    password: str
    role: str = "user"  # user or admin

# Signup
@router.post("/signup")
def signup(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(user.password)
    users_collection.insert_one({
        "username": user.username,
        "password": hashed_pw,
        "role": user.role
    })
    return {"message": "Signup successful!"}

# Login
@router.post("/login")
def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"username": user.username, "role": db_user["role"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"token": token, "role": db_user["role"]}
