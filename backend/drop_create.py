from database import get_db
import asyncio

async def drop_and_create_collections():
    db = get_db()
    collections = await db.list_collection_names()

    for col in collections:
        await db[col].drop()
        print(f"Dropped collection: {col}")

    await db.create_collection("my_products")
    await db.create_collection("competitor_data")
    await db.create_collection("users")
    print("Recreated collections successfully!")

if __name__ == "__main__":
    asyncio.run(drop_and_create_collections())
