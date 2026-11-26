import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)

print("orders above average total:", con.execute(
    "SELECT COUNT(*) FROM purchase_orders "
    "WHERE total_amount > (SELECT AVG(total_amount) FROM purchase_orders)").fetchone()[0])

print("orders sharing the highest total:", con.execute(
    "SELECT COUNT(*) FROM purchase_orders "
    "WHERE total_amount = (SELECT MAX(total_amount) FROM purchase_orders)").fetchone()[0])

print("distinct product_id vs distinct description:", con.execute(
    "SELECT COUNT(DISTINCT product_id), COUNT(DISTINCT description) "
    "FROM purchase_order_lines").fetchone())
