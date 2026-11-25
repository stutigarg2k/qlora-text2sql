import sqlite3
from pathlib import Path
from datasets import load_dataset

NAME = "mindweave/purchasing-procurement-us"
TABLES = [
    "companies", "goods_receipts", "purchase_order_lines",
    "purchase_orders", "supplier_invoices", "supplier_payments", "suppliers",
]
OUT = Path("data/raw/supply_chain.db")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    con = sqlite3.connect(OUT)
    for t in TABLES:
        df = load_dataset(NAME, t, split="train").to_pandas()
        df.to_sql(t, con, index=False)
        print(f"{t}: {len(df)} rows")
    con.close()
    print("Built", OUT)


if __name__ == "__main__":
    main()