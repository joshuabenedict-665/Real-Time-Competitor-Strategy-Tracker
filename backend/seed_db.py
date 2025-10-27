import asyncio
from database import get_db
from datetime import datetime

async def seed():
    db = get_db()

    await db["my_products"].delete_many({})
    await db["competitor_data"].delete_many({})

    my_products = [
        {"name": "Wireless Headphones", "current_price": 1999, "stock": 50, "category": "Electronics", "image": "headphones.jpg"},
        {"name": "Smart Watch", "current_price": 2999, "stock": 40, "category": "Wearables", "image": "smartwatch.jpg"},
        {"name": "Bluetooth Speaker", "current_price": 1499, "stock": 60, "category": "Audio", "image": "speaker.jpg"},
    ]
    await db["my_products"].insert_many(my_products)

    competitor_data = [
        {"product_name": "Wireless Headphones", "competitor_name": "TechStore", "price": 1899, "discount": 10.0, "last_updated": datetime.utcnow()},
        {"product_name": "Smart Watch", "competitor_name": "GadgetWorld", "price": 2899, "discount": 5.0, "last_updated": datetime.utcnow()},
        {"product_name": "Bluetooth Speaker", "competitor_name": "AudioPlus", "price": 1399, "discount": 8.0, "last_updated": datetime.utcnow()},
    ]
    await db["competitor_data"].insert_many(competitor_data)

    print("✅ Database seeded successfully with sample data!")

if __name__ == "__main__":
    asyncio.run(seed())
