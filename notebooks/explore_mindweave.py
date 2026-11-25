from datasets import get_dataset_config_names

configs = get_dataset_config_names("mindweave/purchasing-procurement-us")
print(len(configs))
for c in configs:
    print(c)