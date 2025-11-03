# price_scraper.py
import requests
from bs4 import BeautifulSoup
import random
import time

HEADERS = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
]

def _get(url, timeout=8):
    try:
        hdr = random.choice(HEADERS)
        r = requests.get(url, headers=hdr, timeout=timeout)
        if r.status_code == 200:
            return r.text
    except Exception:
        return None

def scrape_amazon(product):
    q = "+".join(product.split())
    url = f"https://www.amazon.in/s?k={q}"
    html = _get(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    price_tag = soup.select_one("span.a-price-whole")
    if price_tag:
        text = price_tag.get_text(strip=True).replace(",", "")
        try:
            return int("".join(ch for ch in text if ch.isdigit()))
        except:
            return None
    return None

def scrape_flipkart(product):
    q = "+".join(product.split())
    url = f"https://www.flipkart.com/search?q={q}"
    html = _get(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    price_tag = soup.select_one("div._30jeq3._1_WHN1")
    if price_tag:
        txt = price_tag.get_text(strip=True).replace("₹", "").replace(",", "")
        try:
            return int("".join(ch for ch in txt if ch.isdigit()))
        except:
            return None
    return None

def scrape_prices(product_names):
    results = []
    for name in product_names:
        # add small delay to be gentle
        time.sleep(0.8)
        prices = []
        a = scrape_amazon(name)
        if a: prices.append(a)
        f = scrape_flipkart(name)
        if f: prices.append(f)
        if prices:
            results.append({"name": name, "price": min(prices), "sources": {"amazon": a, "flipkart": f}})
        else:
            results.append({"name": name, "price": None, "sources": {"amazon": a, "flipkart": f}})
    return results
