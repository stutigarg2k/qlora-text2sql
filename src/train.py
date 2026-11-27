import json
import sys

import torch
import yaml
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

from data import load_training_data

# optional: python src/train.py 20   -> stop after 20 steps (a quick speed test)
max_steps = int(sys.argv[1]) if len(sys.argv) > 1 else -1

cfg = yaml.safe_load(open("configs/qlora.yaml"))
t = cfg["training"]

tokenizer = AutoTokenizer.from_pretrained(cfg["model"])
train, val = load_training_data(tokenizer, cfg["data"]["n_train"], cfg["data"]["n_val"], cfg["data"]["seed"])

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)
model = AutoModelForCausalLM.from_pretrained(
    cfg["model"], quantization_config=bnb_config, device_map="auto", dtype=torch.float16
)

lora = LoraConfig(
    r=cfg["lora"]["r"],
    lora_alpha=cfg["lora"]["alpha"],
    lora_dropout=cfg["lora"]["dropout"],
    target_modules=cfg["lora"]["target_modules"],
    task_type="CAUSAL_LM",
)

args = SFTConfig(
    output_dir="outputs",
    num_train_epochs=t["epochs"],
    max_steps=max_steps,
    learning_rate=t["learning_rate"],
    per_device_train_batch_size=t["batch_size"],
    per_device_eval_batch_size=t["batch_size"],
    gradient_accumulation_steps=t["grad_accumulation"],
    max_length=t["max_length"],
    fp16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="no",
    report_to="none",
)

trainer = SFTTrainer(model=model, args=args, train_dataset=train,
                     eval_dataset=val, processing_class=tokenizer, peft_config=lora)

trainer.model.print_trainable_parameters()
trainer.train()

trainer.save_model("outputs/adapter")
with open("results/train_log.json", "w") as f:
    json.dump(trainer.state.log_history, f, indent=2)
print("saved: outputs/adapter and results/train_log.json")
