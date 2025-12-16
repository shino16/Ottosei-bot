import json
from pathlib import Path
import os

BASE_DIR = Path(os.getenv("DATA_DIR", "/data"))
FILE = BASE_DIR / "responses.json"

def load_responses():
    if not FILE.exists():
        return load_default_responses()
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_default_responses():
    with open("data/default_responses.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
