import sqlite3

from eval_loop import evaluate, summarize


def make_db():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE t (a INTEGER)")
    con.executemany("INSERT INTO t VALUES (?)", [(1,), (2,), (3,)])
    return con


QUESTIONS = [
    {"id": "q1", "category": "simple", "question": "How many rows?",
     "sql": "SELECT COUNT(*) FROM t"},
    {"id": "q2", "category": "simple", "question": "Sum of a?",
     "sql": "SELECT SUM(a) FROM t"},
    {"id": "q3", "category": "hard", "question": "Max of a?",
     "sql": "SELECT MAX(a) FROM t"},
]

# What the fake "model" says for each question
REPLIES = {
    "How many rows?": "```sql\nSELECT COUNT(*) FROM t\n```",  # correct, in a fence
    "Sum of a?": "SELECT AVG(a) FROM t",                      # wrong aggregate
    "Max of a?": "SELECT MAX(a) FROM missing_table",           # crashes
}


def fake_generate(messages):
    prompt = messages[0]["content"]
    for question, reply in REPLIES.items():
        if prompt.endswith("Question: " + question):
            return reply
    return "no sql here"


def run():
    return evaluate(make_db(), QUESTIONS, fake_generate, "CREATE TABLE t (a INTEGER)")


def test_one_result_per_question_with_raw_and_extracted():
    results = run()
    assert len(results) == 3
    assert results[0]["raw_reply"].startswith("```")
    assert results[0]["extracted_sql"] == "SELECT COUNT(*) FROM t"


def test_verdicts():
    results = run()
    assert [r["passed"] for r in results] == [True, False, False]
    assert results[2]["reason"].startswith("error")


def test_summary_counts():
    summary = summarize(run())
    assert summary["overall"] == {"passed": 1, "total": 3}
    assert summary["by_category"]["simple"] == {"passed": 1, "total": 2}
    assert summary["by_category"]["hard"] == {"passed": 0, "total": 1}

    