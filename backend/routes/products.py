from fastapi import APIRouter, Depends
from routes.auth import get_current_user  # ✅ import correct auth dependency
from database import get_products_collection

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products(user: dict = Depends(get_current_user)):  # ✅ check valid token
    collection = get_products_collection()
    products = await collection.find().to_list(1000)

    for p in products:
        p["_id"] = str(p["_id"])

    return {"products": products}
