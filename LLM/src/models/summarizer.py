from typing import List, Optional
import os
from tenacity import retry, wait_exponential, stop_after_attempt
from src.config import SUMMARIZER_PROVIDER, OPENAI_API_KEY, HF_SUMMARY_MODEL, GOOGLE_API_KEY, GOOGLE_GEMINI_MODEL
from transformers import pipeline as hf_pipeline

def _chunk(items: List[str], max_chars_per_chunk: int = 8000):
    current, length = [], 0
    for t in items:
        l = len(t)
        if length + l > max_chars_per_chunk and current:
            yield current
            current, length = [], 0
        current.append(t)
        length += l
    if current:
        yield current

# ---- Google Gemini ----
def _google_summarize(texts: List[str], focus: Optional[str] = None) -> str:
    import google.generativeai as genai
    if not GOOGLE_API_KEY:
        return "Google API key not configured."
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GOOGLE_GEMINI_MODEL)

    system = "You are an e-commerce analyst. Produce concise, actionable trend summaries from customer feedback."
    focus_line = f" Emphasize: {focus}." if focus else ""
    prompt_prefix = system + focus_line + " Use bullet points and separate positives vs negatives if possible."

    parts = []
    for chunk in _chunk(texts):
        joined = "\n- " + "\n- ".join(chunk[:100])
        prompt = f"{prompt_prefix}\n\nReviews:{joined}"
        resp = model.generate_content(prompt)
        parts.append(resp.text.strip() if hasattr(resp, "text") else str(resp))
    return "\n".join(parts)

# ---- OpenAI ----
def _openai_summarize(texts: List[str], focus: Optional[str] = None) -> str:
    from openai import OpenAI
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured."
    client = OpenAI(api_key=OPENAI_API_KEY or None)
    prompt = "You are an e-commerce analyst. Summarize customer feedback into key positive and negative themes"
    if focus:
        prompt += f" with emphasis on {focus}."
    prompt += " Be concise and actionable."
    joined = "\n- " + "\n- ".join(texts[:50])
    msg = f"""{prompt}

Reviews:
{joined}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
        temperature=0.3,
        max_tokens=350
    )
    return resp.choices[0].message.content.strip()

# ---- HF local ----
_hf_summarizer = None
def _hf_summarize(texts: List[str], focus: Optional[str] = None) -> str:
    global _hf_summarizer
    if _hf_summarizer is None:
        _hf_summarizer = hf_pipeline("summarization", model=HF_SUMMARY_MODEL)
    prefix = f"Focus: {focus}. " if focus else ""
    out_parts = []
    for chunk in _chunk(texts, max_chars_per_chunk=16000):
        inp = prefix + "\n".join(chunk)
        s = _hf_summarizer(inp, max_length=180, min_length=60, do_sample=False)[0]["summary_text"]
        out_parts.append(s)
    return "\n".join(out_parts)

def summarize(texts: List[str], focus: Optional[str] = None) -> str:
    if not texts:
        return "No texts provided."
    prov = (SUMMARIZER_PROVIDER or "google").lower()
    if prov == "google":
        return _google_summarize(texts, focus)
    elif prov == "openai":
        return _openai_summarize(texts, focus)
    elif prov == "hf":
        return _hf_summarize(texts, focus)
    else:
        bullets = [t[:180] + ("..." if len(t) > 180 else "") for t in texts[:10]]
        return "Key points:\n- " + "\n- ".join(bullets)
