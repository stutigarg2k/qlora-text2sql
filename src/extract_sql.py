import re


def extract_sql(text):
    fence = re.search(r"```(?:[a-zA-Z]*\n)?(.*?)```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip()

    text = text.strip()
    if text.lower().startswith(("select", "with")):
        return text.split("\n\n")[0].strip()

    start = re.search(r"\bselect\b", text, re.IGNORECASE)
    if start:
        return text[start.start():].split("\n\n")[0].strip()

    return text
