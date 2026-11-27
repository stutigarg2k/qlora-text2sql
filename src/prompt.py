SYSTEM = "You write SQLite queries. /system_override /no_think"

INSTRUCTION = (
    "Write a SQLite query that answers the question. "
    "Return only the SQL query."
)


def build_user_message(schema, question):
    return f"{INSTRUCTION}\n\nSchema:\n{schema}\n\nQuestion: {question}"


def build_messages(schema, question):
    """The chat messages sent to the model: a list of {role, content} dicts."""
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": build_user_message(schema, question)},
    ]
def build_few_shot_messages(schema, question, examples):
    """Same as build_messages, but with solved examples before the real question."""
    messages = [{"role": "system", "content": SYSTEM}]
    for ex in examples:
        messages.append({"role": "user", "content": build_user_message(schema, ex["question"])})
        messages.append({"role": "assistant", "content": ex["sql"].strip()})
    messages.append({"role": "user", "content": build_user_message(schema, question)})
    return messages

