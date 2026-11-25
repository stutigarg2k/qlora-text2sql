import sqlite3

import pytest

from grader import grade

GOLD = "SELECT SUM(amount) FROM purchase_orders WHERE supplier = 'Acme'"


@pytest.fixture
def con():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE purchase_orders (po_id, supplier, quantity, amount)")
    c.executemany(
        "INSERT INTO purchase_orders VALUES (?,?,?,?)",
        [(101, "Acme", 500, 12000), (102, "Birla", 300, 4500), (103, "Acme", 200, 3000)],
    )
    return c


def test_identical_query_passes(con):
    assert grade(con, GOLD, GOLD)["passed"]


def test_different_text_same_result_passes(con):
    model = "SELECT SUM(amount) FROM purchase_orders WHERE supplier LIKE 'Acme'"
    assert grade(con, GOLD, model)["passed"]


def test_wrong_aggregate_fails(con):
    model = "SELECT AVG(amount) FROM purchase_orders WHERE supplier = 'Acme'"
    assert not grade(con, GOLD, model)["passed"]


def test_wrong_table_name_is_an_error(con):
    model = "SELECT SUM(amount) FROM purchase_order WHERE supplier = 'Acme'"
    r = grade(con, GOLD, model)
    assert not r["passed"]
    assert r["reason"].startswith("error")


def test_row_order_ignored_when_gold_has_no_order_by(con):
    gold = "SELECT po_id FROM purchase_orders"
    model = "SELECT po_id FROM purchase_orders ORDER BY po_id DESC"
    assert grade(con, gold, model)["passed"]


def test_row_order_enforced_when_gold_has_order_by(con):
    gold = "SELECT po_id FROM purchase_orders ORDER BY po_id"
    model = "SELECT po_id FROM purchase_orders ORDER BY po_id DESC"
    assert not grade(con, gold, model)["passed"]


def test_duplicate_rows_are_not_ignored(con):
    gold = "SELECT DISTINCT supplier FROM purchase_orders"
    model = "SELECT supplier FROM purchase_orders"
    assert not grade(con, gold, model)["passed"]


def test_float_noise_is_tolerated(con):
    assert grade(con, "SELECT 0.3", "SELECT 0.1 + 0.2")["passed"]


def test_multiple_statements_are_rejected(con):
    r = grade(con, GOLD, "SELECT 1; DROP TABLE purchase_orders")
    assert not r["passed"]
    assert con.execute("SELECT COUNT(*) FROM purchase_orders").fetchone()[0] == 3