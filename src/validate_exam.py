import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "raw" / "supply_chain.db"
QUESTIONS = ROOT / "data" / "exam" / "questions.yaml"

if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")

con = sqlite3.connect(DB)
con.execute("PRAGMA query_only = ON")  # the exam can never modify the data
items = yaml.safe_load(QUESTIONS.read_text(encoding="utf-8"))

ids = [it["id"] for it in items]
assert len(ids) == len(set(ids)), "duplicate question ids"

for it in items:
    print("=" * 70)
    print(it["id"], "|", it["category"])
    print("Q:", it["question"])
    try:
        rows = con.execute(it["sql"]).fetchall()
    except Exception as e:
        print("  ERROR:", e)
        continue
    note = "   <-- EMPTY: unusable, a wrong query could also return nothing" if not rows else ""
    print(f"  rows: {len(rows)}{note}")
    for r in rows[:3]:
        print("   ", r)