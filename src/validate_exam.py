import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "raw" / "supply_chain.db"
EXAM_DIR = ROOT / "data" / "exam"

if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")

con = sqlite3.connect(DB)
con.execute("PRAGMA query_only = ON")  # the exam can never modify the data

seen_ids = {}  # id -> file it first appeared in
for name in ["dev.yaml", "test.yaml"]:
    path = EXAM_DIR / name
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    items = yaml.safe_load(text) or []
    print("#" * 70)
    print(f"{name}: {len(items)} questions")

    for it in items:
        if it["id"] in seen_ids:
            raise SystemExit(
                f"Duplicate id '{it['id']}' in {name} (first seen in {seen_ids[it['id']]})"
            )
        seen_ids[it["id"]] = name

        print("=" * 70)
        print(it["id"], "|", it["category"])
        print("Q:", it["question"])
        try:
            rows = con.execute(it["sql"]).fetchall()
        except Exception as e:
            print("  ERROR:", e)
            continue
        note = "   <-- EMPTY: unusable" if not rows else ""
        print(f"  rows: {len(rows)}{note}")
        for r in rows[:3]:
            print("   ", r)
            