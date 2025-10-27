from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import get_db
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Replace in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ----- Schemas -----
class UserSignup(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str


# ----- JWT Token Helpers -----
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----- Signup -----
@router.post("/signup")
async def signup(user: UserSignup, db=Depends(get_db)):
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # ✅ Prevent bcrypt length error (truncate >72 bytes)
    password_to_hash = user.password[:72]
    hashed_pw = pwd_context.hash(password_to_hash.encode('utf-8')[:72])


    new_user = {
        "username": user.username,
        "password": hashed_pw,
        "role": user.role
    }
    await db["users"].insert_one(new_user)
    return {"message": "Signup successful!"}


# ----- Login -----
@router.post("/login")
async def login(user: UserLogin, db=Depends(get_db)):
    db_user = await db["users"].find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # ✅ Verify password safely
    if not pwd_context.verify(user.password[:72], db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # ✅ Create JWT access token
    access_token = create_access_token(
        data={"sub": db_user["username"], "role": db_user["role"]}
    )

    return {
        "message": "Login successful!",
        "access_token": access_token,
        "user": {"username": db_user["username"], "role": db_user["role"]}
    }
