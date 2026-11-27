from data import to_example


class FakeTokenizer:
    def apply_chat_template(self, messages, tokenize=False,
                            add_generation_prompt=False, enable_thinking=False):
        text = "".join(f"[{m['role']}]{m['content']}" for m in messages)
        if add_generation_prompt:
            text += "[assistant]"
        return text


def test_training_example_splits_into_prompt_and_answer():
    row = {"context": "CREATE TABLE t (a INTEGER)", "question": "How many?",
           "answer": "SELECT COUNT(*) FROM t"}
    ex = to_example(row, FakeTokenizer())
    assert "CREATE TABLE t (a INTEGER)" in ex["prompt"]
    assert ex["prompt"].endswith("Question: How many?[assistant]")
    assert ex["completion"] == "SELECT COUNT(*) FROM t"
    