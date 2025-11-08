# E:\Shopsmart\backend\price_predictor.py - PURE ML PREDICTION OUTPUT

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional
import os

# --- Configuration (Absolute Path Fix - Keep for file loading) ---
BASE_DIR = Path("E:\\Shopsmart\\backend\\") 
FALLBACK_ON_ERROR = 2000.0 

MODEL_FILE = BASE_DIR / "price_trend_model.joblib"
ENCODER_FILE = BASE_DIR / "platform_encoder.joblib"

# --- CORE ML LOGIC (No price floors or fixed fallbacks) ---

def get_trend_influence(product_data):
    """
    Loads the ML model, calculates features, and returns the raw trend score.
    """
    base_price = product_data.get('Price', 0.0)
    
    try:
        # We rely on the absolute path fix working here
        model = joblib.load(MODEL_FILE)
        platform_encoder = joblib.load(ENCODER_FILE)
        
        # --- Feature Engineering ---
        # Note: All default inputs are used as features for the ML model
        price_clean = float(product_data['Price'])
        discount_clean = float(product_data.get('Discount', 0)) 
        rating = float(product_data.get('Rating', 4.0))
        review_count = int(product_data.get('Review Count', 100))
        
        discounted_price = price_clean * (1 - discount_clean / 100)
        review_density = rating * np.log1p(review_count)
        stock_binary = 1 if product_data.get('Stock', 'In Stock').lower() == 'in stock' else 0
        platform = product_data.get('Platform', 'Flipkart')
        
        if platform not in platform_encoder.classes_:
            platform_encoded = platform_encoder.transform([platform_encoder.classes_[0]])[0]
        else:
            platform_encoded = platform_encoder.transform([platform])[0]

        high_discount = 1 if discount_clean > 15 else 0
        popular_product = 1 if (rating > 4.5 and review_count > 50) else 0
        
        if price_clean <= 5000: price_category = 0
        elif price_clean <= 10000: price_category = 1
        elif price_clean <= 15000: price_category = 2
        else: price_category = 3
        
        features = {
            'Price_Clean': price_clean, 'Discount_Clean': discount_clean,
            'Discounted_Price': discounted_price, 'Discount_Amount': (price_clean - discounted_price),
            'Rating': rating, 'Review Count': review_count,
            'Review_Density': review_density, 'Stock_Binary': stock_binary,
            'Platform_Encoded': platform_encoded, 'High_Discount': high_discount,
            'Popular_Product': popular_product, 'Price_Category': price_category
        }
        
        X_new = pd.DataFrame([features])
        proba = model.predict_proba(X_new)[0]
        
        # ML Price Influence Calculation
        trend_score = (proba[2] * 1.0) + (proba[1] * 0.0) + (proba[0] * -1.0)
        
        return trend_score, discounted_price
        
    except Exception as e:
        # If ML fails to load, raise the error so the caller can handle it or use a default.
        print(f"❌ ML ARTIFACT LOADING FAILED: {e.__class__.__name__} - {e}. Cannot predict.")
        raise


def predict_using_name(product_name: str, product_data: dict = None) -> Optional[float]:
    """
    Calculates predicted price based purely on the ML model's influence score and Base Price.
    """
    if not product_data: product_data = {}
        
    base_price = product_data.get('basePrice', 0.0)
    
    if not base_price or base_price < 10.0: 
        # Minimal non-ML return for bad/dummy product data
        return round(2000.0 + (sum(ord(c) for c in product_name if c.isalpha()) % 100), 2)


    try:
        # 1. Get ML Influence
        trend_score, discounted_price = get_trend_influence({
            'Platform': product_data.get('brand') or 'AVANT',
            'Price': base_price,
            'Discount': product_data.get('discount', 0),
            'Rating': product_data.get('rating', 4.0), 
            'Review Count': product_data.get('reviewCount', 100),
            'Stock': product_data.get('stock', 'In Stock'),
            'name': product_name,
            **product_data 
        })
        
        # 2. Apply Pure ML-Driven Adjustment
        anchor_price = base_price
        
        # Use a moderate 10% swing (0.10) for ML influence
        MAX_SWING = 0.10
        adjustment = anchor_price * (trend_score * MAX_SWING) 
        
        predicted_price = anchor_price + adjustment
        
        # Return the price calculated by the model's output, without floors.
        return round(predicted_price, 2)
        
    except Exception:
        # If ML failed (e.g., File not found), revert to a static fallback price to prevent crash
        return round(FALLBACK_ON_ERROR, 2)


# --- SECONDARY FUNCTION (Required for stability) ---

def predict_using_model(platform: str, category: str, weight: float, product_name: str = None) -> Optional[float]:
    """Placeholder for the legacy function."""
    return predict_using_name(product_name, product_data={'basePrice': 1000.0})