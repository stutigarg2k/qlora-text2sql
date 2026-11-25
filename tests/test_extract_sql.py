from extract_sql import extract_sql


def test_plain_sql_unchanged():
    assert extract_sql("SELECT 1") == "SELECT 1"


def test_sql_fence():
    assert extract_sql("```sql\nSELECT 1\n```") == "SELECT 1"


def test_fence_without_language():
    assert extract_sql("```\nSELECT 1\n```") == "SELECT 1"


def test_one_line_fence():
    assert extract_sql("```SELECT 1```") == "SELECT 1"


def test_prose_around_fence():
    text = "Here is the query:\n```sql\nSELECT 1\n```\nIt returns one."
    assert extract_sql(text) == "SELECT 1"


def test_prose_before_unfenced_sql():
    assert extract_sql("Here is the query:\n\nSELECT 1") == "SELECT 1"


def test_prose_on_same_line():
    assert extract_sql("Here is the query: SELECT 1") == "SELECT 1"


def test_trailing_explanation_is_cut():
    assert extract_sql("SELECT 1\n\nThis returns one.") == "SELECT 1"


def test_multiline_sql_is_kept():
    sql = "SELECT a\nFROM t\nWHERE b = 1"
    assert extract_sql(sql) == sql


def test_cte_query_is_kept():
    sql = "WITH x AS (SELECT 1) SELECT * FROM x"
    assert extract_sql(sql) == sql


def test_no_sql_returns_text():
    assert extract_sql("I cannot do that.") == "I cannot do that."
    
