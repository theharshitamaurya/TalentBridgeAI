import re

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def safe_text(text: str) -> str:
    return re.sub(r"[\"\'<>]", " ", text).strip()
