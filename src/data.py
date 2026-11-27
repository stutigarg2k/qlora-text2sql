from datasets import load_dataset
from prompt import build_messages


def to_example(row):
    return {
        "prompt": build_messages(row["context"], row["question"]),
        "completion": [{"role": "assistant", "content": row["answer"]}],
    }


def load_training_data(n_train, n_val, seed=42):
    ds = load_dataset("b-mc2/sql-create-context", split="train").shuffle(seed=seed)
    ds = ds.select(range(n_train + n_val))
    ds = ds.map(to_example, remove_columns=ds.column_names)
    return ds.select(range(n_train)), ds.select(range(n_train, n_train + n_val))
    