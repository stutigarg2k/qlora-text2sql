import sqlite3
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from schema_text import build_schema

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)
text = build_schema(con)
print(text)
print()
print("characters:", len(text))
