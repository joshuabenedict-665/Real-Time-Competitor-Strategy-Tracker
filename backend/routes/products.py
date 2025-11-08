# backend/routes/products.py - FINAL CORRECTED VERSION

from fastapi import APIRouter, Depends
from routes.auth import get_current_user 
from database import get_db # <-- Corrected import of get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products(user: dict = Depends(get_current_user), db=Depends(get_db)): # Added db=Depends(get_db)
    
    # CRITICAL FIX: Add the filter to fetch *ONLY* non-competitor items (your catalog)
    products = await db["products"].find({"is_competitor": False}).to_list(1000)

    for p in products:
        # Ensure _id is correctly cast for JSON response
        if '_id' in p:
            p["_id"] = str(p["_id"])

    return {"products": products}