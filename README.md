# Text-to-SQL with QLoRA

Fine-tuning a small open-source language model with QLoRA to translate
English questions into SQL, evaluated on a supply-chain database.

**Status:** work in progress. No results yet.

## Plan
1. Measure the untrained model (zero-shot and few-shot) on a held-out exam
2. Fine-tune with QLoRA
3. Re-measure and compare, with error analysis

## Data sources
- Training: `b-mc2/sql-create-context` (CC-BY-4.0)
- Evaluation database: built from `mindweave/purchasing-procurement-us`,
  CC-BY-NC-4.0 (credit: Mindweave Technologies). Used for non-commercial,
  educational purposes only. The data is not included in this repo;
  `src/build_eval_db.py` downloads it and builds the database locally.
- Code: MIT License. The MIT license does not extend to the datasets above.