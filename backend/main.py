from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import MyProduct, CompetitorData

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time Competitor Strategy Tracker API")

# --- Enable CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve static files ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Routes ---
@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/crawl")
def crawl_competitors(db: Session = Depends(get_db)):
    competitors = db.query(CompetitorData).all()
    return {"competitors": [c.__dict__ for c in competitors]}

@app.get("/predict")
def predict():
    return {"prediction": "ML model not yet integrated"}

@app.get("/sentiment")
def sentiment():
    return {"sentiment": "Sentiment model not yet integrated"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(MyProduct).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "current_price": p.current_price,
            "stock": p.stock,
            "category": p.category,
            "image": f"/static/{p.image}" if p.image else None
        }
        for p in products
    ]

@app.get("/my-prices/update")
def update_prices(db: Session = Depends(get_db)):
    products = db.query(MyProduct).all()
    competitors = db.query(CompetitorData).all()

    updated = []
    for product in products:
        comp_prices = [c.price for c in competitors if c.product_name == product.name]
        if comp_prices:
            min_price = min(comp_prices)
            new_price = max(min_price - 5, 50)  # simple rule
            product.current_price = new_price
            db.commit()
            updated.append({"product": product.name, "new_price": new_price})

    return {"updated_prices": updated}
