from typing import List, Dict, Optional
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from src.config import CHECKPOINT_DIR, HF_MODEL_NAME, MAX_SEQ_LEN
from src.preprocessing.clean import batch_clean

LABELS = ["negative", "neutral", "positive"]

def load_model():
    best_path = os.path.join(CHECKPOINT_DIR, "best")
    if os.path.isdir(best_path):
        tok = AutoTokenizer.from_pretrained(best_path)
        mdl = AutoModelForSequenceClassification.from_pretrained(best_path)
    else:
        # Fallback to zero-shot sentiment pipeline
        tok = None
        mdl = None
    return tok, mdl

_tok, _mdl = load_model()
_fallback_pipe = pipeline("sentiment-analysis")

def predict(texts: List[str]) -> List[Dict]:
    cleaned = batch_clean(texts)
    if _mdl is not None and _tok is not None:
        enc = _tok(cleaned, truncation=True, padding=True, max_length=MAX_SEQ_LEN, return_tensors="pt")
        with torch.no_grad():
            logits = _mdl(**enc).logits
        probs = torch.softmax(logits, dim=-1).cpu().numpy()
        preds = probs.argmax(axis=-1)
        out = []
        for t, p, pr in zip(cleaned, preds, probs):
            out.append({
                "text": t,
                "label": LABELS[int(p)],
                "scores": {LABELS[i]: float(pr[i]) for i in range(len(LABELS))}
            })
        return out
    else:
        results = _fallback_pipe(cleaned)
        out = []
        for t, r in zip(cleaned, results):
            # Map to 3-class if needed
            label = r["label"].lower()
            mapped = "positive" if "pos" in label else "negative"
            out.append({
                "text": t,
                "label": mapped,
                "scores": {mapped: float(r["score"])}
            })
        return out
