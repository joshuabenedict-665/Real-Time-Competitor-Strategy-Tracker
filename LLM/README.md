# Competitor Sentiment Tracker (Module 3)

Real-time NLP sentiment analysis and trend detection for competitor products (Amazon, Flipkart).

## Features
- DistilBERT/BERT fine-tuning for sentiment classification.
- Pluggable LLM summarization (OpenAI GPT / local HF model).
- FastAPI endpoint `/sentiment` for scoring and optional trend summaries.
- Clean, modular code with training, inference, and evaluation utilities.
- Docker-ready.

## Quick Start (Local)
1. **Python env** (>=3.10):
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment variables** (create `.env` from example):
   ```bash
   cp .env.example .env
   # Add OPENAI_API_KEY if you want GPT summarization
   ```

3. **Train** (optional, if you have data):
   ```bash
   bash scripts/train.sh
   ```

4. **Run API**:
   ```bash
   bash scripts/run_api.sh
   # Then POST to http://localhost:8000/sentiment
   ```

### Example Request
```bash
curl -X POST http://localhost:8000/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Battery life is amazing but camera is mediocre", "Worst delivery experience ever"],
    "do_summary": true,
    "summary_focus": "product and price"
  }'
```

---

## Project Structure
```
competitor-sentiment-tracker/
├─ README.md
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env.example
├─ .gitignore
├─ scripts/
│  ├─ run_api.sh
│  └─ train.sh
├─ src/
│  ├─ config.py
│  ├─ utils/logging_utils.py
│  ├─ ingestion/amazon_flipkart_scraper.py
│  ├─ ingestion/social_ingestion.py
│  ├─ preprocessing/clean.py
│  ├─ models/train_sentiment.py
│  ├─ models/infer_sentiment.py
│  ├─ models/summarizer.py
│  ├─ evaluation/metrics.py
│  └─ api/main.py
└─ tests/
   └─ test_api.py
```

## Data Notes
- Put raw datasets under `data/raw/`.
- Put processed/training files under `data/processed/`.
- Model checkpoints under `models/checkpoints/`.

## Summarization Providers
- **OpenAI** (preferred): set `OPENAI_API_KEY` and `SUMMARIZER_PROVIDER=openai`.
- **HF Local** (fallback): set `SUMMARIZER_PROVIDER=hf` and `HF_SUMMARY_MODEL` (e.g. `sshleifer/distilbart-cnn-12-6`).

## Amazon/Flipkart
- This repo provides **ingestion placeholders**. Scraping must follow each platform's ToS/robots and local laws. Prefer official APIs/datasets where available.


## Google Gemini Integration
- Set `SUMMARIZER_PROVIDER=google` (default) and provide `GOOGLE_API_KEY` in `.env`.
- Optionally change `GOOGLE_GEMINI_MODEL` (e.g., `gemini-1.5-pro`, `gemini-1.5-flash`).
