from datasets import load_dataset

NAME = "mindweave/purchasing-procurement-us"
TABLES = [
    "companies",
    "goods_receipts",
    "purchase_order_lines",
    "purchase_orders",
    "supplier_invoices",
    "supplier_payments",
    "suppliers",
]

for t in TABLES:
    print("=" * 60)
    print(t)
    try:
        d = load_dataset(NAME, t, split="train")
    except Exception as e:
        print("FAILED:", type(e).__name__, e)
        continue
    print("rows:", d.num_rows)
    print("columns:", d.column_names)
    print("sample:", d[0])