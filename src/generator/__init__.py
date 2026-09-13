"""
PII Exposure Detection - Generator Package
Provides synthetic document generation, ground truth labeling, and dataset splitting.
"""

from .generate_documents import (
    DocumentGenerator,
    generate_full_dataset,
    split_dataset,
)

__all__ = [
    "DocumentGenerator",
    "generate_full_dataset",
    "split_dataset",
]
