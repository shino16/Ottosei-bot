import json
from pathlib import Path

FILE = Path("responses.json")

def load_responses():
    if not FILE.exists():
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
