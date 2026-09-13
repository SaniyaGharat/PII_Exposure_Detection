"""
PII Exposure Detection - Utilities Package
Provides PDF generation, scanner degradation simulation, and dataset validation.
"""

from .pdf_generator import generate_pdf_from_text
from .scanner_simulator import simulate_scanned_document
from .dataset_validator import validate_dataset, ValidationReport

__all__ = [
    "generate_pdf_from_text",
    "simulate_scanned_document",
    "validate_dataset",
    "ValidationReport",
]
