"""Locate retained artifacts after moving a checkout; preserve frozen metadata."""
from pathlib import Path


def artifact_path(record, study):
    # Frozen records retain original absolute paths as provenance. Collection
    # and reporting operate on the corresponding retained run in this checkout.
    return Path(study) / 'runs' / record['task'] / record['condition'] / f"run-{record['repeat']}"
