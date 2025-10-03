# seed_db.py
from database import SessionLocal
from models import MyProduct

db = SessionLocal()

# Sample products to seed the database
sample_products = [
    {"name": "Sneakers", "current_price": 2500, "stock": 10, "category": "Footwear", "image": "/Sneakers.png"},
    {"name": "Headphones", "current_price": 4999, "stock": 15, "category": "Electronics", "image": "/Headphones.png"},
    {"name": "Smartwatch", "current_price": 6999, "stock": 5, "category": "Electronics", "image": "/Smartwatch.png"},
]

for p in sample_products:
    db.add(MyProduct(**p))

db.commit()
db.close()
print("Sample products added!")
