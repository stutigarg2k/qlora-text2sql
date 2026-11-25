import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)

rows = con.execute(
    "SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name"
).fetchall()
for name, sql in rows:
    print(sql)
    print()
    