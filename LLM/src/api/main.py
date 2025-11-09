from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from src.models.infer_sentiment import predict
from src.models.summarizer import summarize
from src.utils.logging_utils import setup_logging
from src.config import LOG_LEVEL

logger = setup_logging(LOG_LEVEL)

app = FastAPI(title="Competitor Sentiment API", version="0.1.0")

class SentimentRequest(BaseModel):
    texts: List[str] = Field(..., description="List of review or social texts")
    do_summary: bool = False
    summary_focus: Optional[str] = None

class SentimentResponse(BaseModel):
    results: List[dict]
    summary: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment(req: SentimentRequest):
    logger.info("Scoring sentiment for %d texts\n" % len(req.texts))
    results = predict(req.texts)
    summary = summarize([r["text"] for r in results], req.summary_focus) if req.do_summary else None
    return {"results": results, "summary": summary}
