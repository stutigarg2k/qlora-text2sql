INSTRUCTION = (
    "Write a SQLite query that answers the question. "
    "Return only the SQL query."
)


def build_user_message(schema, question):
    return f"{INSTRUCTION}\n\nSchema:\n{schema}\n\nQuestion: {question}"


def build_messages(schema, question):
    """The chat messages sent to the model: a list of {role, content} dicts."""
    return [{"role": "user", "content": build_user_message(schema, question)}]
