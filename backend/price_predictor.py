# price_predictor.py
import os
import joblib
import numpy as np

BASE = os.path.dirname(__file__)
ENCODER_PATH = os.path.join(BASE, "ml", "platform_encoder.joblib")
MODEL_PATH = os.path.join(BASE, "ml", "price_trend_model.joblib")

encoder = None
model = None

try:
    if os.path.exists(ENCODER_PATH):
        encoder = joblib.load(ENCODER_PATH)
        print("✅ Loaded platform_encoder.joblib")
    else:
        print("⚠️ platform_encoder.joblib not found:", ENCODER_PATH)
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Loaded price_trend_model.joblib")
    else:
        print("⚠️ price_trend_model.joblib not found:", MODEL_PATH)
except Exception as e:
    print("⚠️ Error loading ML models:", e)
    encoder = None
    model = None

def predict_using_model(platform: str, category: str, weight: float, product_name: str = None):
    """
    Expected final model input (example):
      [weight, encoded_platform_features..., encoded_category_features...]
    This function attempts to construct that vector. If encoder/model missing we fallback.
    """
    # Fallback heuristic when model missing
    if model is None:
        # best-effort fallback: predicted price = weight * 100 (simple)
        try:
            return round(float(weight) * 100.0, 2)
        except Exception:
            return None

    try:
        # Build numeric features: weight first
        x = [float(weight)]
        # If encoder exists and can transform both platform and category, try to append.
        if encoder is not None:
            # Try to transform platform and category as a combined array; many encoders expect single field so try platform first
            try:
                enc_p = encoder.transform([platform])
                enc_p = np.array(enc_p).reshape(1, -1)
                enc_p = enc_p.flatten().tolist()
                x.extend(enc_p)
            except Exception:
                # try encoding category instead
                try:
                    enc_c = encoder.transform([category])
                    enc_c = np.array(enc_c).reshape(1, -1)
                    enc_c = enc_c.flatten().tolist()
                    x.extend(enc_c)
                except Exception:
                    pass

        features = np.array(x, dtype=float).reshape(1, -1)
        pred = float(model.predict(features)[0])
        return round(pred, 2)
    except Exception:
        # last-resort heuristic
        try:
            return round(float(weight) * 100.0, 2)
        except:
            return None
