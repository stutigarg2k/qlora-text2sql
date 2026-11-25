from datasets import load_dataset

ds = load_dataset("b-mc2/sql-create-context", split="train")
print(ds)
print()
for i in range(3):
    print(ds[i])
    print()