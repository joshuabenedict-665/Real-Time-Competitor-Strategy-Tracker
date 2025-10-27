from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_db
from auth import router as auth_router
from auth_utils import verify_token  # ✅ NEW

app = FastAPI(title="Real-Time Competitor Strategy Tracker API")

# --- ✅ CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ✅ Static Files ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- ✅ Include Authentication Routes ---
app.include_router(auth_router)

# --- ✅ Root Check Route ---
@app.get("/")
def root():
    return {"message": "MongoDB API is running successfully!"}

# --- ✅ Protected: Get Products ---
@app.get("/products")
async def get_products(db=Depends(get_db), user=Depends(verify_token)):
    products = await db["my_products"].find().to_list(None)
    for p in products:
        p["_id"] = str(p["_id"])
        if p.get("image"):
            p["image"] = f"/static/{p['image'].lstrip('/')}"
    return {"user": user, "products": products}

# --- ✅ Protected: Crawl Competitor Data ---
@app.get("/crawl")
async def crawl_competitors(db=Depends(get_db), user=Depends(verify_token)):
    competitors = await db["competitor_data"].find().to_list(None)
    for c in competitors:
        c["_id"] = str(c["_id"])
    return {"user": user, "competitors": competitors}

# --- ✅ Public: Dummy Predict Route ---
@app.get("/predict")
def predict():
    return {"prediction": "ML model not yet integrated"}

# --- ✅ Public: Dummy Sentiment Route ---
@app.get("/sentiment")
def sentiment():
    return {"sentiment": "Sentiment model not yet integrated"}

# --- ✅ Protected: Update My Prices ---
@app.get("/my-prices/update")
async def update_prices(db=Depends(get_db), user=Depends(verify_token)):
    products = await db["my_products"].find().to_list(None)
    competitors = await db["competitor_data"].find().to_list(None)

    updated = []
    for product in products:
        comp_prices = [c["price"] for c in competitors if c["product_name"] == product["name"]]
        if comp_prices:
            min_price = min(comp_prices)
            new_price = max(min_price - 5, 50)
            await db["my_products"].update_one(
                {"_id": product["_id"]},
                {"$set": {"current_price": new_price}}
            )
            updated.append({"product": product["name"], "new_price": new_price})

    return {"user": user, "updated_prices": updated}
