from database import get_db
import asyncio

async def drop_and_create_collections():
    db = get_db()

    # Drop existing collections if they exist
    collections = await db.list_collection_names()
    for col in collections:
        await db[col].drop()
        print(f"Dropped collection: {col}")

    # Create empty collections
    await db.create_collection("my_products")
    await db.create_collection("competitor_data")
    print("Recreated collections successfully!")

if __name__ == "__main__":
    asyncio.run(drop_and_create_collections())
