from extract_sql import extract_sql
from grader import grade
from prompt import build_few_shot_messages, build_messages


def evaluate(con, questions, generate, schema, examples=None):
    """Run every question through the model and grade the answers."""
    results = []
    for q in questions:
            if examples:
              messages = build_few_shot_messages(schema, q["question"], examples)
            else:
             messages = build_messages(schema, q["question"])
            raw = generate(messages)
            sql = extract_sql(raw)
            verdict = grade(con, q["sql"], sql)
            results.append({
            "id": q["id"],
            "category": q["category"],
            "question": q["question"],
            "raw_reply": raw,
            "extracted_sql": sql,
            "passed": verdict["passed"],
            "reason": verdict["reason"],
        })
    return results


def summarize(results):
    """Counts of passed/total, overall and per category."""
    def count(items):
        return {"passed": sum(r["passed"] for r in items), "total": len(items)}

    by_category = {}
    for r in results:
        by_category.setdefault(r["category"], []).append(r)

    return {
        "overall": count(results),
        "by_category": {c: count(items) for c, items in by_category.items()},
    }
