from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from database import get_db
from models import MyProduct, CompetitorData

app = FastAPI(title="Real-Time Competitor Strategy Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "API is running!"}


@app.get("/products")
async def get_products():
    db = get_db()
    products = await db["my_products"].find().to_list(100)
    return [
        {
            "id": str(p["_id"]),
            "name": p["name"],
            "current_price": p["current_price"],
            "stock": p["stock"],
            "category": p["category"],
            "image": f"/static/{p.get('image')}" if p.get("image") else None
        }
        for p in products
    ]


@app.get("/crawl")
async def crawl_competitors():
    db = get_db()
    competitors = await db["competitor_data"].find().to_list(100)
    return {"competitors": competitors}


@app.get("/my-prices/update")
async def update_prices():
    db = get_db()
    products = await db["my_products"].find().to_list(100)
    competitors = await db["competitor_data"].find().to_list(100)

    updated = []
    for product in products:
        comp_prices = [c["price"] for c in competitors if c["product_name"] == product["name"]]
        if comp_prices:
            min_price = min(comp_prices)
            new_price = max(min_price - 5, 50)
            await db["my_products"].update_one(
                {"_id": ObjectId(product["_id"])},
                {"$set": {"current_price": new_price}},
            )
            updated.append({"product": product["name"], "new_price": new_price})

    return {"updated_prices": updated}
