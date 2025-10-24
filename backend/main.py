from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_db
from models import MyProduct, CompetitorData
from datetime import datetime

app = FastAPI(title="Real-Time Competitor Strategy Tracker API")

# --- Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve static files ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Root Route ---
@app.get("/")
def root():
    return {"message": "API is running!"}

# --- Get All Products ---
@app.get("/products")
async def get_products(db=Depends(get_db)):
    products = await db["my_products"].find().to_list(None)
    for p in products:
        p["_id"] = str(p["_id"])
        if p.get("image"):
            p["image"] = f"/static/{p['image'].lstrip('/')}"
    return products

# --- Crawl Competitor Data ---
@app.get("/crawl")
async def crawl_competitors(db=Depends(get_db)):
    competitors = await db["competitor_data"].find().to_list(None)
    for c in competitors:
        c["_id"] = str(c["_id"])
    return {"competitors": competitors}

# --- Dummy Predict Route ---
@app.get("/predict")
def predict():
    return {"prediction": "ML model not yet integrated"}

# --- Dummy Sentiment Route ---
@app.get("/sentiment")
def sentiment():
    return {"sentiment": "Sentiment model not yet integrated"}

# --- Update My Prices Based on Competitors ---
@app.get("/my-prices/update")
async def update_prices(db=Depends(get_db)):
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

    return {"updated_prices": updated}
