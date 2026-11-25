import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)

ties = con.execute(
    "SELECT total, COUNT(*) FROM ("
    "  SELECT SUM(quantity) AS total FROM purchase_order_lines GROUP BY description"
    ") GROUP BY total HAVING COUNT(*) > 1"
).fetchall()

print("tied totals (total, how many products):", ties if ties else "none")
