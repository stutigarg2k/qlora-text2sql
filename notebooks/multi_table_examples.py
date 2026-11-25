from datasets import load_dataset

ds = load_dataset("b-mc2/sql-create-context", split="train")

multi = [r for r in ds if r["context"].count("CREATE TABLE") >= 2]
print("examples with 2+ tables:", len(multi), "of", len(ds))
print()
for r in multi[:3]:
    print(repr(r["context"]))
    print("Q:", r["question"])
    print("A:", r["answer"])
    print()