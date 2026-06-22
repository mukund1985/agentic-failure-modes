"""
Push agentic-failure-modes dataset to HuggingFace Hub.

Usage:
    pip install huggingface_hub datasets
    huggingface-cli login
    python push_to_hub.py
"""

from datasets import load_dataset, DatasetDict
from huggingface_hub import HfApi
import os

HF_REPO_ID = "mukund1985/agentic-failure-modes"

DATA_FILES = {
    "failure_modes": "data/failure_modes.jsonl",
    "metric_coverage": "data/metric_coverage.jsonl",
    "distribution_collapse_traces": "data/distribution_collapse_traces.jsonl",
    "tool_degradation_traces": "data/tool_degradation_traces.jsonl",
}


def push():
    api = HfApi()

    # Create the repo if it doesn't exist
    api.create_repo(
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        exist_ok=True,
        private=False,
    )

    # Load each split and push as a DatasetDict
    splits = {}
    for name, path in DATA_FILES.items():
        ds = load_dataset("json", data_files=path, split="train")
        splits[name] = ds
        print(f"Loaded {name}: {len(ds)} rows")

    dataset = DatasetDict(splits)
    dataset.push_to_hub(HF_REPO_ID)

    # Push the README (dataset card) separately
    api.upload_file(
        path_or_fileobj="README.md",
        path_in_repo="README.md",
        repo_id=HF_REPO_ID,
        repo_type="dataset",
    )

    print(f"\nDone. Dataset live at: https://huggingface.co/datasets/{HF_REPO_ID}")


if __name__ == "__main__":
    push()
