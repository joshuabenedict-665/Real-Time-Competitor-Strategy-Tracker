from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from routes.auth import get_current_admin_user
from database import get_db
from price_predictor import predict_using_name 
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


def fix_mongo_id(doc):
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


@router.post("/products/create")
async def create_product(payload: dict, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")

    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    doc = {
        "name": name,
        "brand": payload.get("brand"),
        "imageUrl": payload.get("imageUrl"),
        "basePrice": float(payload.get("basePrice", 0.0)),
        # Ensure your catalog products are marked False
        "is_competitor": False, 
        "created_at": datetime.utcnow(),
    }

    result = await db["products"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    return {"message": "Product created ✅", "product": doc}


# In backend/routes/admin.py, modify the get_scraped function:

@router.get("/scrape/results")
async def get_scraped(db=Depends(get_db), admin=Depends(get_current_admin_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")

    results = []
    # Fetch only competitor products
    async for p in db["products"].find({"is_competitor": True}).sort("name", 1):
        p = fix_mongo_id(p)
        results.append({
            "_id": p["_id"],
            "name": p.get("name"),
            # 🟢 CRITICAL FIX: Check p.get("basePrice") first!
            "price": p.get("price") or p.get("current_price") or p.get("basePrice") or None, 
            "source": p.get("source") or p.get("competitor") or "Unknown"
        })

    return results

@router.delete("/scrape/clear")
async def clear_scraped_data(
    db=Depends(get_db), 
    admin: dict = Depends(get_current_admin_user)
):
    """
    Deletes all scraped competitor products (where is_competitor=True) from the database.
    """
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")
    
    try:
        delete_result = await db["products"].delete_many({"is_competitor": True})
        
        return {
            "message": f"✅ Cleared {delete_result.deleted_count} unwanted scraped product(s) from the database.",
            "deleted_count": delete_result.deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database DELETE operation failed: {e}")