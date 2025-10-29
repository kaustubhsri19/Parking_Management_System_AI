import os
import torch
from datasets import load_dataset, ClassLabel
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

DATASET_FILE = os.path.join(os.path.dirname(__file__), 'data', 'intents.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'models', 'parking_intent_model')
MODEL_NAME = 'distilbert-base-uncased'
NUM_LABELS = 14  # 13 intents + fallback (labels 0-13)


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')

    print('Loading dataset...')
    ds = load_dataset('csv', data_files=DATASET_FILE, split='train').train_test_split(test_size=0.2, seed=42)

    # Normalize column names to handle headers with extra spaces like "text        , label"
    def _normalize_columns(dset):
        mapping_made = False
        for c in list(dset.column_names):
            cl = c.strip().lower()
            if cl == 'text' and c != 'text':
                dset = dset.rename_column(c, 'text')
                mapping_made = True
            elif cl == 'label' and c != 'label':
                dset = dset.rename_column(c, 'label')
                mapping_made = True
        return dset

    ds['train'] = _normalize_columns(ds['train'])
    ds['test'] = _normalize_columns(ds['test'])

    # Ensure label is integer
    def _cast_label(example):
        example['label'] = int(str(example['label']).strip())
        return example

    ds['train'] = ds['train'].map(_cast_label)
    ds['test'] = ds['test'].map(_cast_label)

    print('Loading tokenizer...')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize_fn(batch):
        return tokenizer(batch['text'], padding='max_length', truncation=True, max_length=64)

    print('Tokenizing dataset...')
    tokenized = ds.map(tokenize_fn, batched=True)
    tokenized = tokenized.remove_columns([c for c in tokenized['train'].column_names if c not in ['input_ids', 'attention_mask', 'label']])

    print('Loading model...')
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
    model.to(device)

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy='epoch',
        num_train_epochs=50,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        fp16=True if device == 'cuda' else False,
        dataloader_pin_memory=True,
        logging_dir=os.path.join(os.path.dirname(__file__), '..', 'logs'),
        save_strategy='epoch',
        load_best_model_at_end=True,
        metric_for_best_model='eval_loss',
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized['train'],
        eval_dataset=tokenized['test'],
    )

    print('--- Starting Training ---')
    trainer.train()
    print('--- Training Complete ---')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f'Model saved to {OUTPUT_DIR}')


if __name__ == '__main__':
    main()


