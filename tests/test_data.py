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
class EndMarkerTokenizer(FakeTokenizer):
    def apply_chat_template(self, messages, tokenize=False,
                            add_generation_prompt=False, enable_thinking=False):
        text = super().apply_chat_template(
            messages, tokenize, add_generation_prompt, enable_thinking)
        return text if add_generation_prompt else text + "<|im_end|>\n"


def test_completion_ends_with_the_stop_marker_and_no_newline():
    row = {"context": "CREATE TABLE t (a INTEGER)", "question": "How many?",
           "answer": "SELECT COUNT(*) FROM t"}
    ex = to_example(row, EndMarkerTokenizer())
    assert ex["completion"] == "SELECT COUNT(*) FROM t<|im_end|>"
        