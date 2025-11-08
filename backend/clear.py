# clear_db.py - Final Working MongoDB Cleanup Script

import pymongo
from pymongo.errors import ConnectionFailure
from typing import Optional, Dict
import os

# --- Configuration: Use the provided Cloud URI and Database Name ---
# NOTE: The URI contains the database name 'competitor_tracker'
MONGODB_URI = "mongodb+srv://joshuabenedict665_db_user:wy1rVbZ9auyhGEyw@competitor-tracker-clus.nd8lyp9.mongodb.net/competitor_tracker?retryWrites=true&w=majority"
DATABASE_NAME = "competitor_tracker"
COLLECTION_NAME = "products"

def clear_competitive_data():
    """Connects directly to the cloud MongoDB cluster and deletes all competitor products."""
    client = None
    try:
        # Connect to the MongoDB client with a short timeout
        print(f"Attempting to connect to: {DATABASE_NAME}...")
        client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
        
        # Force a check on the connection status
        client.admin.command('ping') 
        
        # Access the database and collection
        db = client[DATABASE_NAME]
        products_collection = db[COLLECTION_NAME]
        
        # --- The Deletion Query ---
        filter_query = {"is_competitor": True}
        
        result = products_collection.delete_many(filter_query)
        
        print("="*60)
        print("MONGO DB CLEANUP SCRIPT EXECUTED")
        print(f"Database: {DATABASE_NAME}, Collection: {COLLECTION_NAME}")
        print(f"✅ SUCCESSFULLY DELETED: {result.deleted_count} unwanted competitor record(s)")
        print("="*60)
        
    except ConnectionFailure as e:
        print("\n❌ DATABASE CONNECTION FAILURE:")
        print("Please check your network and ensure your MongoDB cluster allows connections from your IP.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during DB operation: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    clear_competitive_data()