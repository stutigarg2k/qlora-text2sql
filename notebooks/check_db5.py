import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)

print("min / avg / max order total:",
      con.execute("SELECT MIN(total_amount), ROUND(AVG(total_amount), 2), MAX(total_amount) "
                  "FROM purchase_orders").fetchone())
for threshold in (3000, 4000, 5000, 6000):
    n = con.execute("SELECT COUNT(*) FROM purchase_orders WHERE total_amount > ?",
                    (threshold,)).fetchone()[0]
    print(f"orders with total above {threshold}: {n}")
    