# backend/rotes/admin_predictions.py - Final Complete Code (FIXED FILTER)

from fastapi import APIRouter, Depends
from database import get_db
from routes.auth import get_current_user, get_current_admin_user
from price_predictor import predict_using_name 
from bson import ObjectId # Added missing import

router = APIRouter(prefix="/admin", tags=["Admin"])

async def get_current_admin(user: dict = Depends(get_current_user)):
    return await get_current_admin_user(user)

@router.get("/predictions") 
async def get_product_predictions(
    admin: dict = Depends(get_current_admin),
    db=Depends(get_db)
):
    # CRITICAL FIX: Fetch only *non-competitor* products (your catalog)
    products = await db["products"].find({"is_competitor": False}).to_list(None)
    results = []
    
    for p in products:
        product_name = p.get("name", "")
        # Call the corrected prediction function
        # Note: Your function predicts the price number here, which will be near the Base Price
        predicted_price = predict_using_name(product_name=product_name, product_data=p)
        
        base_price = p.get("basePrice")
        if base_price is not None:
            try:
                # Ensure base price is a float for display consistency
                base_price = float(base_price)
            except (TypeError, ValueError):
                base_price = None
        
        results.append({
            "product_id": str(p.get("_id") or ""),
            "product_name": product_name,
            "base_price": base_price,
            "predicted_price": predicted_price
        })
        
    return {"predictions": results}