from data import to_example


def test_training_example_uses_the_exam_prompt_format():
    row = {"context": "CREATE TABLE t (a INTEGER)", "question": "How many?",
           "answer": "SELECT COUNT(*) FROM t"}
    ex = to_example(row)
    assert ex["prompt"][0]["role"] == "system"
    assert "CREATE TABLE t (a INTEGER)" in ex["prompt"][-1]["content"]
    assert ex["prompt"][-1]["content"].endswith("Question: How many?")
    assert ex["completion"] == [{"role": "assistant", "content": "SELECT COUNT(*) FROM t"}]
    