from datasets import load_dataset
from prompt import build_messages


def to_example(row, tokenizer):
    messages = build_messages(row["context"], row["question"])
    answer = {"role": "assistant", "content": row["answer"]}
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    full = tokenizer.apply_chat_template(
        messages + [answer], tokenize=False, enable_thinking=False)
    return {"prompt": prompt, "completion": full[len(prompt):].rstrip("\n")}


def load_training_data(tokenizer, n_train, n_val, seed=42):
    ds = load_dataset("b-mc2/sql-create-context", split="train").shuffle(seed=seed)
    ds = ds.select(range(n_train + n_val))
    ds = ds.map(to_example, fn_kwargs={"tokenizer": tokenizer}, remove_columns=ds.column_names)
    return ds.select(range(n_train)), ds.select(range(n_train, n_train + n_val))




