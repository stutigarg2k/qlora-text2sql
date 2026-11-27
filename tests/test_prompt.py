from prompt import build_few_shot_messages


def test_few_shot_structure():
    examples = [
        {"question": "Q1", "sql": "SELECT 1"},
        {"question": "Q2", "sql": "SELECT 2"},
    ]
    messages = build_few_shot_messages("SCHEMA", "Real question", examples)

    assert len(messages) == 6  # system + 2 examples x 2 messages + final question
    assert messages[0]["role"] == "system"
    assert messages[2]["content"] == "SELECT 1"
    assert messages[-1]["role"] == "user"
    assert messages[-1]["content"].endswith("Question: Real question")
    