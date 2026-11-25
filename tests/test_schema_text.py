import sqlite3

from schema_text import build_schema


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute('CREATE TABLE "b_table" ("x" TEXT, "y" INTEGER)')
    con.execute('CREATE TABLE "a_table" ("z" REAL)')
    return con


def test_matches_training_style():
    con = make_db()
    expected = "CREATE TABLE a_table (z REAL); CREATE TABLE b_table (x TEXT, y INTEGER)"
    assert build_schema(con, exclude=()) == expected


def test_excluded_table_is_left_out():
    con = make_db()
    assert build_schema(con, exclude=("b_table",)) == "CREATE TABLE a_table (z REAL)"
    