import os
from dotenv import load_dotenv

load_dotenv()

HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "distilbert-base-uncased")
MAX_SEQ_LEN = int(os.getenv("MAX_SEQ_LEN", "256"))
NUM_EPOCHS = int(os.getenv("NUM_EPOCHS", "3"))
LR = float(os.getenv("LR", "2e-5"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "16"))

DATA_DIR = os.getenv("DATA_DIR", "./data")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR", "./models/checkpoints")

# Summarization providers: google | openai | hf | none
SUMMARIZER_PROVIDER = os.getenv("SUMMARIZER_PROVIDER", "google")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_SUMMARY_MODEL = os.getenv("HF_SUMMARY_MODEL", "sshleifer/distilbart-cnn-12-6")

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_GEMINI_MODEL = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-1.5-flash")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
