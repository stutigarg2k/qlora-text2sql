import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from prompt import build_messages
from schema_text import build_schema
from transformers import AutoTokenizer

DB = ROOT / "data" / "raw" / "supply_chain.db"
if not DB.exists():
    raise SystemExit(f"Database not found at {DB}. Run src/build_eval_db.py first.")

con = sqlite3.connect(DB)
schema = build_schema(con)
questions = yaml.safe_load((ROOT / "data" / "exam" / "questions.yaml").read_text(encoding="utf-8"))
question = questions[0]["question"]

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM3-3B")
messages = build_messages(schema, question)
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False,
)

print(text)
print("-" * 70)
print("tokens:", len(tokenizer(text, add_special_tokens=False).input_ids))
