import re
from typing import List

URL_RE = re.compile(r'https?://\S+|www\.\S+')
USER_RE = re.compile(r'@\w+')
HASHTAG_RE = re.compile(r'#\w+')
WHITESPACE_RE = re.compile(r'\s+')

def basic_clean(text: str) -> str:
    text = URL_RE.sub(' ', text)
    text = USER_RE.sub(' ', text)
    text = HASHTAG_RE.sub(' ', text)
    text = text.replace('\n', ' ')
    text = WHITESPACE_RE.sub(' ', text)
    return text.strip()

def batch_clean(texts: List[str]) -> List[str]:
    return [basic_clean(t) for t in texts]
