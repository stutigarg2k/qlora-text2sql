import re
import sqlite3
import time
from collections import Counter
from pathlib import Path

TIMEOUT_S = 5.0


def open_readonly(db_path):
    """Open the database so that no query can modify it."""
    uri = Path(db_path).resolve().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _run(con, sql):
    start = time.monotonic()
    # abort queries that run longer than TIMEOUT_S
    con.set_progress_handler(
        lambda: 1 if time.monotonic() - start > TIMEOUT_S else 0, 10000
    )
    try:
        return con.execute(sql).fetchall()
    finally:
        con.set_progress_handler(None, 0)


def _normalize(rows):
    return [
        tuple(round(v, 2) if isinstance(v, float) else v for v in row)
        for row in rows
    ]


def _has_order_by(sql):
    return re.search(r"\border\s+by\b", sql, re.IGNORECASE) is not None


def grade(con, gold_sql, model_sql):
    """Return {"passed": bool, "reason": str}."""
    gold = _normalize(_run(con, gold_sql))  # a gold error is our bug: let it raise
    try:
        pred = _normalize(_run(con, model_sql))
    except Exception as e:
        return {"passed": False, "reason": f"error: {e}"}

    if _has_order_by(gold_sql):
        ok = pred == gold
    else:
        ok = Counter(pred) == Counter(gold)
    return {"passed": ok, "reason": "ok" if ok else "result mismatch"}