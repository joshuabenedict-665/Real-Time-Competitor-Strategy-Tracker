# price_scraper.py - FINAL WORKING SELECTORS (Flipkart Fix)

from bs4 import BeautifulSoup
import re
import asyncio
from typing import Optional, List, Dict, Any

# =========================================================================
# 1. FLIPKART SCRAPER (FINAL WORKING SELECTORS)
# =========================================================================
async def scrape_flipkart(query: str, html_content: str = None) -> List[Dict[str, Any]]:
    """
    Parses Flipkart search results using the validated selectors (data-id, WKTcLC, Nx9bqj).
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # 1. FIX: Find all containers using the reliable 'data-id' attribute
    containers = soup.find_all('div', attrs={'data-id': True}) 
    
    if not containers:
        print(f"DEBUG: Flipkart containers not found for query '{query}'. Scraper logic failed.")
        return []

    for container in containers:
        try:
            # 2. FIX: Extract Name/Title using validated classes
            # WKTcLC is the most stable class for the anchor tag with the product title
            name_tag = container.find('a', class_='WKTcLC')
            
            # 3. FIX: Extract Price using validated class 'Nx9bqj'
            price_tag = container.find('div', class_='Nx9bqj')

            # Data Extraction
            # We use the 'title' attribute which is cleaner than .text
            name = name_tag.get('title', 'N/A').strip() if name_tag else "N/A"
            price_text = price_tag.text.strip().replace('₹', '').replace(',', '') if price_tag else "0"
            price = int(float(price_text))
            
            # Data Validation (Skip if data is clearly bad)
            if price == 0 or "N/A" in name:
                continue

            # 4. Extract URL (using the main product link wrapper)
            url_tag = container.find('a', class_='rPDeLR', href=True)
            relative_url = url_tag['href'] if url_tag else ""
            full_url = "https://www.flipkart.com" + relative_url.split('&lid')[0]

            # 5. Extract Image URL 
            # Note: _53J4C- is a randomized class, but using re.compile ensures some resilience
            img_tag = container.find('img', class_=re.compile('_53J4C-'))
            image_url = img_tag.get('src', 'N/A')
            
            results.append({
                "name": name,
                "price": price,
                "url": full_url,
                "image": image_url,
                "competitor": "Flipkart"
            })
            
        except Exception:
            # Silently skip any individual product card that fails to parse
            continue 

    print(f"✅ Flipkart: Parsed {len(results)} products successfully!")
    return results

# =========================================================================
# 2. AMAZON SCRAPER (UNCORRECTED - For Structural Completeness)
# =========================================================================
async def scrape_amazon(query: str, html_content: str = None) -> List[Dict[str, Any]]:
    """
    Parses Amazon search results. This logic is likely outdated and will return zero results.
    """
    if not html_content:
        return []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # Amazon containers (This selector is likely the one that needs replacement next)
    containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for container in containers:
        try:
            # Data extraction logic is known to be faulty
            name_tag = container.find('span', class_='a-text-normal')
            price_box = container.find('span', class_='a-price')
            
            price = 0
            if price_box:
                price_whole = price_box.find('span', class_='a-price-whole')
                if price_whole:
                    price_text = price_whole.text.replace(',', '') 
                    price = int(float(price_text))
            
            if price == 0:
                continue

            url_tag = container.find('a', class_='a-link-normal', href=True)
            relative_url = url_tag['href']
            
            results.append({
                "name": name_tag.text.strip(),
                "price": price,
                "url": "https://www.amazon.in" + relative_url.split('/ref=')[0],
                "image": container.find('img', class_='s-image').get('src', 'N/A'),
                "competitor": "Amazon"
            })
        except Exception:
            continue

    print(f"✅ Amazon: Parsed {len(results)} potential products.")
    return results