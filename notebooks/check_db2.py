import sqlite3

con = sqlite3.connect("data/raw/supply_chain.db")


def q(label, sql):
    print("\n" + label)
    for row in con.execute(sql).fetchall():
        print("  ", row)


q("order date range", "SELECT MIN(order_date), MAX(order_date) FROM purchase_orders")
q("days late distribution (receipt_date - expected_date)",
  "SELECT CAST(julianday(g.receipt_date) - julianday(p.expected_date) AS INTEGER) AS d, COUNT(*) "
  "FROM goods_receipts g JOIN purchase_orders p ON g.po_id = p.id GROUP BY d ORDER BY d")
q("sent POs with no receipt",
  "SELECT COUNT(*) FROM purchase_orders p WHERE p.status = 'sent' "
  "AND NOT EXISTS (SELECT 1 FROM goods_receipts g WHERE g.po_id = p.id)")
q("payments after invoice due date",
  "SELECT COUNT(*) FROM supplier_payments s JOIN supplier_invoices i ON s.supplier_invoice_id = i.id "
  "WHERE s.payment_date > i.due_date")
q("payment amount differs from invoice total",
  "SELECT COUNT(*) FROM supplier_payments s JOIN supplier_invoices i ON s.supplier_invoice_id = i.id "
  "WHERE ROUND(s.amount,2) != ROUND(i.total_amount,2)")
q("spend per supplier",
  "SELECT s.name, s.category, COUNT(*), ROUND(SUM(p.total_amount),2) "
  "FROM purchase_orders p JOIN suppliers s ON p.supplier_id = s.id GROUP BY s.id ORDER BY 4 DESC")
q("distinct supplier categories", "SELECT category, COUNT(*) FROM suppliers GROUP BY category")
