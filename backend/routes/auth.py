from fastapi import APIRouter, Depends, HTTPException, status, Header
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from database import get_db
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignupModel(BaseModel):
    username: str
    password: str
    role: str = "user"


class LoginModel(BaseModel):
    username: str
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Extract Token + Validate User Exists
async def get_current_user(
    Authorization: str = Header(None), 
    db=Depends(get_db)
):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        scheme, token = Authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Token missing required data")

        user = await db["users"].find_one({"username": username})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user["role"] = role  # ✅ Ensure role stays attached to user

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ✅ Admin-Only Guard
async def get_current_admin_user(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ✅ Signup Route
@router.post("/signup")
async def signup(user: SignupModel, db=Depends(get_db)):
    existing = await db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(user.password)

    await db["users"].insert_one({
        "username": user.username,
        "password": hashed_pw,
        "role": user.role
    })

    return {"message": "User registered successfully ✅"}


# ✅ Login Route
@router.post("/login")
async def login(user: LoginModel, db=Depends(get_db)):
    existing = await db["users"].find_one({"username": user.username})
    if not existing or not pwd_context.verify(user.password, existing["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": existing["username"],
        "role": existing["role"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": existing["role"]
    }
