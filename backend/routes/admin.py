from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from routes.auth import get_current_admin_user
from database import get_db
from price_predictor import predict_using_model # Kept but may be unused if logic is in admin_predictions
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
        "is_competitor": False,
        "created_at": datetime.utcnow(),
    }

    result = await db["products"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    return {"message": "Product created ✅", "product": doc}


@router.get("/scrape/results")
async def get_scraped(db=Depends(get_db), admin=Depends(get_current_admin_user)):
    if db is None:
        raise HTTPException(status_code=500, detail="DB not connected")

    results = []
    async for p in db["products"].find({"is_competitor": True}).sort("name", 1):
        p = fix_mongo_id(p)
        results.append({
            "_id": p["_id"],
            "name": p.get("name"),
            "price": p.get("price") or p.get("current_price") or None,
            "source": p.get("source") or p.get("competitor") or "Unknown"
        })

    return results  # ✅ frontend directly receives array


# REMOVED CONFLICTING @router.get("/predictions") ROUTE.
# This ensures that routes/admin_predictions.py can handle the /admin/predictions call
# to show catalog product predictions without collision.