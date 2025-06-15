from pathlib import Path
import json
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "menu_scraper" / "products.json"

def load_data() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        print("⚠️ File not found!")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)