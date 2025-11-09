"""Placeholders for Amazon/Flipkart ingestion.
Follow platform policies and regional laws. Prefer official APIs/datasets.
"""
from typing import List, Dict
from datetime import datetime

def fetch_amazon_reviews(product_id: str, max_pages: int = 1) -> List[Dict]:
    # TODO: Implement with requests + parsing OR Selenium/Scrapy.
    # Return dicts with fields: {text, rating, title, author, date, product_id, source}
    return [{
        "text": "Great value for money. Battery lasts long.",
        "rating": 5,
        "title": "Solid",
        "author": "anon",
        "date": datetime.utcnow().isoformat(),
        "product_id": product_id,
        "source": "amazon"
    }]

def fetch_flipkart_reviews(product_id: str, max_pages: int = 1) -> List[Dict]:
    return [{
        "text": "Camera quality average but display is good.",
        "rating": 3,
        "title": "Okayish",
        "author": "user123",
        "date": datetime.utcnow().isoformat(),
        "product_id": product_id,
        "source": "flipkart"
    }]
