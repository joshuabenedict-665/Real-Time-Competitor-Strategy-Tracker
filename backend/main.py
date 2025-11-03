# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_db
from auth import router as auth_router
from auth_utils import verify_token, verify_admin_token
from price_scraper import scrape_prices
from price_predictor import run_model
import asyncio

app = FastAPI(title="ShopSmart Competitor Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/products")
async def get_products(db=Depends(get_db), user=Depends(verify_token)):
    products = await db["my_products"].find().to_list(None)
    for p in products:
        p["_id"] = str(p["_id"])
    return {"user": user, "products": products}

@app.get("/crawl")
async def crawl_competitors(db=Depends(get_db), user=Depends(verify_token)):
    competitors = await db["competitor_data"].find().to_list(None)
    for c in competitors:
        c["_id"] = str(c["_id"])
    return {"user": user, "competitors": competitors}

@app.get("/admin/dashboard")
async def admin_dashboard(db=Depends(get_db), admin=Depends(verify_admin_token)):
    try:
        # fetch product list from db (names)
        products = await db["my_products"].find().to_list(None)
        product_names = [p["name"] for p in products] if products else ["iPhone 15", "Samsung S24"]

        scraped = scrape_prices(product_names)
        preds = run_model(scraped)

        # combine into final list (merge by name)
        merged = []
        for s in scraped:
            name = s["name"]
            scraped_price = s.get("price")
            pred_item = next((x for x in preds if x["name"] == name), {})
            predicted_price = pred_item.get("predicted_price")
            merged.append({
                "name": name,
                "scraped_price": scraped_price,
                "predicted_price": predicted_price,
                "sources": s.get("sources", {})
            })

        # store snapshot to DB (async)
        await db["price_snapshots"].insert_one({"timestamp": __import__("datetime").datetime.utcnow(), "data": merged})

        return {"scraper_status": "success", "predicted_prices": merged, "scraped_prices": scraped}
    except Exception as e:
        print("ADMIN DASHBOARD ERROR:", e)
        return {"scraper_status": "failed", "error": str(e)}
