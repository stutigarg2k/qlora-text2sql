import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")
con = sqlite3.connect(DB)


def q(label, sql):
    print("\n" + label)
    for row in con.execute(sql).fetchall():
        print("  ", row)


q("payment methods",
  "SELECT payment_method, COUNT(*) FROM supplier_payments GROUP BY payment_method")

q("supplier terms (payment_terms_days, lead_time_days)",
  "SELECT name, payment_terms_days, lead_time_days FROM suppliers ORDER BY name")

q("orders per year",
  "SELECT substr(order_date, 1, 4), COUNT(*) FROM purchase_orders GROUP BY 1")

q("distinct product descriptions, and the 5 most ordered",
  "SELECT COUNT(DISTINCT description) FROM purchase_order_lines")
q("top 5 products by number of order lines",
  "SELECT description, COUNT(*) FROM purchase_order_lines "
  "GROUP BY description ORDER BY 2 DESC LIMIT 5")

q("quantity per order line: min, max, distinct values",
  "SELECT MIN(quantity), MAX(quantity), COUNT(DISTINCT quantity) FROM purchase_order_lines")

q("days between invoice due date and payment (negative = paid early)",
  "SELECT CAST(julianday(s.payment_date) - julianday(i.due_date) AS INTEGER) AS d, COUNT(*) "
  "FROM supplier_payments s JOIN supplier_invoices i ON s.supplier_invoice_id = i.id "
  "GROUP BY d ORDER BY d")
  