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

