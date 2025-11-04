import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict
import asyncio

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}

PRICE_RE = re.compile(r"[\d,]+(?:\.\d+)?")


def _parse_price(text: str):
    if not text:
        return None
    text = text.replace("₹", "").strip()
    match = PRICE_RE.search(text)
    if match:
        return float(match.group(0).replace(",", ""))
    return None


async def fetch(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url, headers=HEADERS) as resp:
            return await resp.text()
    except:
        return ""


# ✅ Updated Flipkart selectors
async def scrape_flipkart(query: str, limit: int = 8) -> List[Dict]:
    q = query.replace(" ", "+")
    url = f"https://www.flipkart.com/search?q={q}"
    results = []

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("a._1fQZEK") or soup.select("a.s1Q9rs")

    for card in cards[:limit]:
        name = card.select_one("div._4rR01T, a.s1Q9rs")
        price = card.select_one("div._30jeq3")
        image = card.select_one("img")
        link = card.get("href")

        if not name or not price:
            continue

        results.append({
            "name": name.get_text(strip=True),
            "price": _parse_price(price.get_text()),
            "competitor": "Flipkart",
            "url": "https://www.flipkart.com" + link if link else None,
            "image": image.get("src") or image.get("data-src") if image else None,
            "last_updated": datetime.utcnow().isoformat()
        })

    return results


# ✅ Updated Amazon selectors
async def scrape_amazon(query: str, limit: int = 8) -> List[Dict]:
    q = query.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={q}"
    results = []

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div.s-result-item")

    for card in cards[:limit]:
        title = card.select_one("span.a-size-medium, span.a-text-normal")
        price_whole = card.select_one("span.a-price-whole")
        image = card.select_one("img.s-image")
        link = card.select_one("a.a-link-normal")

        if not title or not price_whole:
            continue

        results.append({
            "name": title.get_text(strip=True),
            "price": _parse_price(price_whole.get_text()),
            "competitor": "Amazon",
            "url": "https://www.amazon.in" + link.get("href") if link else None,
            "image": image.get("src") if image else None,
            "last_updated": datetime.utcnow().isoformat()
        })

    return results


async def scrape_all(query: str):
    fk_task = scrape_flipkart(query)
    amz_task = scrape_amazon(query)
    fk, amz = await asyncio.gather(fk_task, amz_task)
    return fk + amz
