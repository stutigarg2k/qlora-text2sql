import sqlite3

con = sqlite3.connect("data/raw/supply_chain.db")


def q(label, sql):
    print("\n" + label)
    for row in con.execute(sql).fetchall():
        print("  ", row)


q("companies rows", "SELECT COUNT(*) FROM companies")
q("lines per PO (min, max)",
  "SELECT MIN(n), MAX(n) FROM (SELECT COUNT(*) n FROM purchase_order_lines GROUP BY order_id)")
q("PO statuses", "SELECT status, COUNT(*) FROM purchase_orders GROUP BY status")
q("invoice statuses", "SELECT status, COUNT(*) FROM supplier_invoices GROUP BY status")
q("POs with no invoice",
  "SELECT COUNT(*) FROM purchase_orders p WHERE NOT EXISTS (SELECT 1 FROM supplier_invoices i WHERE i.po_id = p.id)")
q("invoice total differs from PO total",
  "SELECT COUNT(*) FROM supplier_invoices i JOIN purchase_orders p ON i.po_id = p.id WHERE ROUND(i.total_amount,2) != ROUND(p.total_amount,2)")
q("receipts later than expected date",
  "SELECT COUNT(*) FROM goods_receipts g JOIN purchase_orders p ON g.po_id = p.id WHERE g.receipt_date > p.expected_date")
q("invoices not fully paid",
  "SELECT COUNT(*) FROM supplier_invoices WHERE amount_paid < total_amount")
q("receipts with notes", "SELECT COUNT(*) FROM goods_receipts WHERE notes IS NOT NULL")
q("POs with more than one receipt",
  "SELECT COUNT(*) FROM (SELECT po_id FROM goods_receipts GROUP BY po_id HAVING COUNT(*) > 1)")
