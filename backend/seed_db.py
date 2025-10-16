# seed_db.py
from database import get_db
import asyncio

async def seed():
    db = get_db()
    sample_products = [
        {"name": "Sneakers", "current_price": 2500, "stock": 10, "category": "Footwear", "image": "Sneakers.png"},
        {"name": "Headphones", "current_price": 4999, "stock": 15, "category": "Electronics", "image": "Headphones.png"},
        {"name": "Smartwatch", "current_price": 6999, "stock": 5, "category": "Electronics", "image": "Smartwatch.png"},
    ]
    await db["my_products"].insert_many(sample_products)
    print("✅ Sample products added!")

asyncio.run(seed())
