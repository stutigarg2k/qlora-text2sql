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
- Evaluation database: derived from `mindweave/purchasing-procurement-us` (license: TBD)