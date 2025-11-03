# auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db
from auth_utils import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSignup(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup")
async def signup(user: UserSignup, db=Depends(get_db)):
    existing = await db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username exists")
    hashed = pwd_context.hash(user.password[:72])
    await db["users"].insert_one({"username": user.username, "password": hashed, "role": user.role})
    return {"message": "Signup successful"}

@router.post("/login")
async def login(user: UserLogin, db=Depends(get_db)):
    db_user = await db["users"].find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password[:72], db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"message": "Login successful", "access_token": token, "user": {"username": db_user["username"], "role": db_user["role"]}}

@router.post("/admin-login")
async def admin_login(user: UserLogin, db=Depends(get_db)):
    # Option A: require a user in DB with role=admin
    db_user = await db["users"].find_one({"username": user.username})
    if db_user and pwd_context.verify(user.password[:72], db_user["password"]) and db_user.get("role") == "admin":
        token = create_access_token({"sub": db_user["username"], "role": "admin"})
        return {"message": "Admin login successful", "access_token": token}
    # Option B: fallback built-in admin (only for dev)
    if user.username == "admin" and user.password == "admin123":
        token = create_access_token({"sub": "admin", "role": "admin"})
        return {"message": "Admin login successful", "access_token": token}
    raise HTTPException(status_code=401, detail="Invalid admin credentials")
