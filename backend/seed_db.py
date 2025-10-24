import asyncio
from database import get_db

async def seed():
    db = get_db()

    sample_products = [
        {"name": "Sneakers", "current_price": 2500, "stock": 10, "category": "Footwear", "image": "/Sneakers.png"},
        {"name": "Headphones", "current_price": 4999, "stock": 15, "category": "Electronics", "image": "/Headphones.png"},
        {"name": "Smartwatch", "current_price": 6999, "stock": 5, "category": "Electronics", "image": "/Smartwatch.png"},
    ]

    await db["my_products"].delete_many({})  # clear existing
    await db["my_products"].insert_many(sample_products)
    print("✅ Sample products added to MongoDB!")

if __name__ == "__main__":
    asyncio.run(seed())
