import os
import argparse
import json
from typing import Dict, Any
import numpy as np
from datasets import load_dataset, Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          Trainer, TrainingArguments)
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from src.config import HF_MODEL_NAME, MAX_SEQ_LEN, NUM_EPOCHS, LR, BATCH_SIZE, CHECKPOINT_DIR
from src.utils.logging_utils import setup_logging

LABEL2ID = {"negative": 0, "neutral": 1, "positive": 2}
ID2LABEL = {v: k for k, v in LABEL2ID.items()}

def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def build_dataset(path: str) -> Dataset:
    data = list(load_jsonl(path))
    return Dataset.from_list(data)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {"accuracy": acc, "precision": p, "recall": r, "f1": f1}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_path", required=True)
    parser.add_argument("--val_path", required=True)
    parser.add_argument("--output_dir", default=CHECKPOINT_DIR)
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("Loading tokenizer and model\n")
    tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        HF_MODEL_NAME, num_labels=3, id2label=ID2LABEL, label2id=LABEL2ID
    )

    def tokenize(example):
        return tokenizer(
            example["text"],
            truncation=True,
            max_length=MAX_SEQ_LEN,
            padding="max_length",
        )

    logger.info("Building datasets\n")
    ds_train = build_dataset(args.train_path)
    ds_val = build_dataset(args.val_path)

    # Map string labels to IDs
    def map_labels(example: Dict[str, Any]):
        label = example.get("label")
        if isinstance(label, str):
            example["label"] = LABEL2ID[label.lower()]
        return example

    ds_train = ds_train.map(map_labels)
    ds_val = ds_val.map(map_labels)

    ds_train = ds_train.map(tokenize, batched=True)
    ds_val = ds_val.map(tokenize, batched=True)

    cols = ["input_ids", "attention_mask", "label"]
    ds_train.set_format(type="torch", columns=cols)
    ds_val.set_format(type="torch", columns=cols)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=LR,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=NUM_EPOCHS,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_steps=50,
        push_to_hub=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds_train,
        eval_dataset=ds_val,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    logger.info("Starting training\n")
    trainer.train()
    logger.info("Evaluating\n")
    metrics = trainer.evaluate()
    logger.info(f"Validation metrics: {metrics}\n")

    best_dir = os.path.join(args.output_dir, "best")
    os.makedirs(best_dir, exist_ok=True)
    trainer.save_model(best_dir)
    tokenizer.save_pretrained(best_dir)
    logger.info(f"Saved best model to {best_dir}\n")

if __name__ == "__main__":
    main()
