#!/usr/bin/env bash
set -euo pipefail
python -m src.models.train_sentiment   --train_path data/processed/train.jsonl   --val_path data/processed/val.jsonl
