import os, json, pandas as pd, numpy as np, re, argparse
from typing import List, Dict

TEXT_CANDIDATES = [
    "review", "review_text", "text", "comment", "content", "body",
    "message", "feedback", "description", "title", "summary"
]

LABEL_CANDIDATES = [
    "label", "sentiment", "polarity"
]

RATING_CANDIDATES = [
    "rating", "ratings", "stars", "star", "score"
]

def pick_text_columns(df: pd.DataFrame) -> List[str]:
    cols = []
    for c in df.columns:
        cl = c.lower().strip()
        if any(k in cl for k in TEXT_CANDIDATES) and df[c].dtype == object:
            cols.append(c)
    if not cols:
        # fallback: choose first few object columns
        cols = [c for c in df.columns if df[c].dtype == object][:2]
    return cols

def try_map_label(val):
    if isinstance(val, str):
        v = val.lower().strip()
        if "pos" in v or v in {"positive","pos"}: return "positive"
        if "neg" in v or v in {"negative","neg"}: return "negative"
        if "neu" in v or v in {"neutral","neu"}: return "neutral"
    return None

def label_from_rating(x):
    try:
        r = float(x)
    except Exception:
        return None
    # map 1-5 or 0-5
    if r >= 4: return "positive"
    if r <= 2: return "negative"
    return "neutral"

def build_rows(df: pd.DataFrame) -> List[Dict]:
    text_cols = pick_text_columns(df)
    label_col = None
    for c in df.columns:
        if c.lower().strip() in LABEL_CANDIDATES:
            label_col = c
            break
    rating_col = None
    for c in df.columns:
        if c.lower().strip() in RATING_CANDIDATES:
            rating_col = c
            break

    rows = []
    for _, row in df.iterrows():
        # Join candidate text columns
        parts = []
        for c in text_cols:
            v = row.get(c, None)
            if isinstance(v, str) and v.strip():
                parts.append(v.strip())
        text = " ".join(parts).strip()
        if not text:
            continue
        lab = None
        if label_col is not None:
            lab = try_map_label(row[label_col])
        if lab is None and rating_col is not None:
            lab = label_from_rating(row[rating_col])
        if lab is None:
            # keep unlabeled as neutral for now (weak label)
            lab = "neutral"
        rows.append({"text": text, "label": lab})
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True, help="Paths to CSV/XLSX files")
    parser.add_argument("--out_dir", required=True, help="Output dir with train/val jsonl")
    parser.add_argument("--val_ratio", type=float, default=0.2)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    all_rows = []
    for path in args.inputs:
        if path.lower().endswith(".csv"):
            df = pd.read_csv(path)
        elif path.lower().endswith(".xlsx") or path.lower().endswith(".xls"):
            df = pd.read_excel(path)
        else:
            print(f"Skipping unsupported file: {path}")
            continue
        rows = build_rows(df)
        all_rows.extend(rows)

    # Shuffle and split
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(all_rows))
    split = int(len(idx) * (1 - args.val_ratio))
    train = [all_rows[i] for i in idx[:split]]
    val = [all_rows[i] for i in idx[split:]]

    with open(os.path.join(args.out_dir, "train.jsonl"), "w", encoding="utf-8") as f:
        for r in train: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(args.out_dir, "val.jsonl"), "w", encoding="utf-8") as f:
        for r in val: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(train)} train and {len(val)} val examples to {args.out_dir}")

if __name__ == "__main__":
    main()
