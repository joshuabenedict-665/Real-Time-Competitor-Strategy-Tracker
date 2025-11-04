from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from routes.auth import get_current_user, get_current_admin_user

from crawl4ai import AsyncWebCrawler
from bson import ObjectId

router = APIRouter(prefix="/admin/scrape", tags=["Scraping"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ✅ Admin validation wrapper
async def get_current_admin(user: dict = Depends(get_current_user)):
    return await get_current_admin_user(user)


# ✅ Simplified crawler — pure HTTP mode (No Playwright)
async def crawl_product(url, platform, query):
    products = []

    try:
        async with AsyncWebCrawler(
            browser_type=None,   # ✅ Disable Playwright
            use_browser=False,   # ✅ Use simple HTTP requests
            debug=False
        ) as crawler:

            result = await crawler.arun(url=url)
            html = result.html if result else ""

            if not html:
                print(f"⚠ No HTML returned from {platform}")
                return []

            # ✅ simple title extraction fallback
            start = html.find("<title>")
            end = html.find("</title>")
            title = html[start+7:end].strip()[:100] if (start != -1 and end != -1) else query

            products.append({
                "_id": ObjectId(),
                "query": query,
                "platform": platform,
                "product": title,
                "price": None
            })

    except Exception as e:
        print(f"❌ Crawl error ({platform}): {e}")

    return products


@router.post("/{query}")
async def scrape_product(
    query: str,
    admin: dict = Depends(get_current_admin),
    database=Depends(get_db)
):
    try:
        amazon_url = f"https://www.amazon.in/s?k={query}"
        flipkart_url = f"https://www.flipkart.com/search?q={query}"

        amazon_results = await crawl_product(amazon_url, "Amazon", query)
        flipkart_results = await crawl_product(flipkart_url, "Flipkart", query)

        results = amazon_results + flipkart_results

        if not results:
            return {"count": 0, "message": f"No results found for '{query}'"}

        await database["scraped_data"].insert_many(results)

        return {
            "count": len(results),
            "message": f"✅ Scraped {len(results)} items successfully!",
            "products": results,
        }

    except Exception as e:
        print("❌ Fatal Crawling Error:", e)
        raise HTTPException(status_code=500, detail="Scraping failed")


@router.get("/results")
async def get_scraped_results(
    admin: dict = Depends(get_current_admin),
    database=Depends(get_db)
):
    data = await database["scraped_data"].find().to_list(200)
    return {"competitors": data}
