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


q("late deliveries per supplier (all rows, check for ties)",
  "SELECT s.name, COUNT(*) AS late FROM goods_receipts g "
  "JOIN purchase_orders p ON g.po_id = p.id JOIN suppliers s ON p.supplier_id = s.id "
  "WHERE g.receipt_date > p.expected_date GROUP BY s.id ORDER BY late DESC")

q("unpaid vs status 'received': rows where they disagree (0 = identical)",
  "SELECT COUNT(*) FROM supplier_invoices "
  "WHERE (amount_paid < total_amount) != (status = 'received')")

q("uninvoiced vs status 'sent': rows where they disagree (0 = identical)",
  "SELECT COUNT(*) FROM purchase_orders p "
  "WHERE (NOT EXISTS (SELECT 1 FROM supplier_invoices i WHERE i.po_id = p.id)) != (p.status = 'sent')")

q("all suppliers with status", "SELECT name, status, category FROM suppliers")