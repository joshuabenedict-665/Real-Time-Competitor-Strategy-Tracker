# backend/routes/scrape.py - STABLE CODE (FLIPKART ONLY)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from routes.auth import get_current_user, get_current_admin_user
from price_scraper import scrape_amazon, scrape_flipkart 
from bson import ObjectId
from datetime import datetime
import asyncio
import aiohttp 
import os 

router = APIRouter(prefix="/admin/scrape", tags=["Scraping"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_admin(user: dict = Depends(get_current_user)):
    return await get_current_admin_user(user)

# --- AIOHTTP FETCH FUNCTION ---
async def fetch_simple_http(url: str):
    """
    Simple HTTP fetch using aiohttp. 
    Saves raw HTML to file for debugging selectors.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=20, ssl=False) as resp: 
                resp.raise_for_status() 
                html_content = await resp.text()

                # --- DEBUGGING ADDITION ---
                source = 'flipkart' if 'flipkart' in url else 'amazon'
                filename = f"debug_{source}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"DEBUG: Saved raw HTML to {filename}")
                # --- END DEBUGGING ADDITION ---

                return html_content
    except Exception as e:
        print(f"❌ Simple HTTP Fetch Error for {url}: {e.__class__.__name__} - {e}")
        return ""

# --- WRAPPER FUNCTION FOR FLIPKART ONLY ---
async def scrape_flipkart_stable(query: str):
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    html = await fetch_simple_http(url)
    if html:
        return await scrape_flipkart(query, html_content=html)
    return []

# --- AMAZON WRAPPER COMMENTED OUT FOR ISOLATION ---
# async def scrape_amazon_stable(query: str):
#     # url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
#     # html = await fetch_simple_http(url)
#     # if html:
#     #     return await scrape_amazon(query, html_content=html)
#     return [] # Returns an empty list immediately


@router.post("/{query}")
async def scrape_product(
    query: str,
    admin: dict = Depends(get_current_admin),
    database=Depends(get_db)
):
    """Uses the stable HTTP method for scraping (currently Flipkart only)."""
    try:
        # 🟢 Execute ONLY Flipkart scraper
        fk_task = scrape_flipkart_stable(query)
        # amz_task = scrape_amazon_stable(query) # Amazon task commented out
        
        # Collect results. amazon_results is now an empty list.
        flipkart_results = await fk_task
        # flipkart_results, amazon_results = await asyncio.gather(fk_task, amz_task)
        results = flipkart_results # + amazon_results

        if not results:
            return {"count": 0, "message": f"⚠️ Static scraping failed for Flipkart. Check selectors in price_scraper.py against the saved HTML."}

        # --- Data insertion logic (unchanged) ---
        products_to_insert = []
        for r in results:
            doc = {
                "name": r.get("name"),
                "basePrice": r.get("price"),
                "is_competitor": True,
                "source": r.get("competitor") or "Unknown",
                "imageUrl": r.get("image"),
                "url": r.get("url"),
                "created_at": datetime.utcnow(),
            }
            products_to_insert.append(doc)

        await database["products"].insert_many(products_to_insert)

        for doc in products_to_insert:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        return {
            "count": len(products_to_insert),
            "message": f"✅ Scraped {len(products_to_insert)} competitor items from Flipkart successfully!",
            "products": products_to_insert,
        }

    except Exception as e:
        print(f"❌ Fatal Scraping Route Error: {e.__class__.__name__} - {e}")
        raise HTTPException(status_code=500, detail=f"Scraping failed during processing: {e.__class__.__name__}")

# (get_scraped_results function remains the same)
@router.get("/results")
async def get_scraped_results(
    admin: dict = Depends(get_current_admin),
    database=Depends(get_db)
):
    """Fetches the list of all products marked as is_competitor=True."""
    data = await database["products"].find({"is_competitor": True}).to_list(200)
    
    for d in data:
        if '_id' in d:
            d['_id'] = str(d['_id'])
            
    return data