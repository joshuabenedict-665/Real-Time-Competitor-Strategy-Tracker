from fastapi import HTTPException, Header
import jwt

SECRET_KEY = "ADMIN_SECRET_KEY"

def verify_admin_token(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Admin token missing")

    try:
        token = Authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")
