"""
PII Exposure Detection - Necessity Policy Package
Defines document purpose policies and field necessity rules for dataset generation and classification.
"""

from .necessity_policy import (
    NecessityLabel,
    FieldPolicy,
    DocumentPurposePolicy,
    DOCUMENT_POLICIES,
    DOCUMENT_PURPOSES,
    get_field_policy,
    get_all_policies,
    validate_necessity_label,
)

__all__ = [
    "NecessityLabel",
    "FieldPolicy",
    "DocumentPurposePolicy",
    "DOCUMENT_POLICIES",
    "DOCUMENT_PURPOSES",
    "get_field_policy",
    "get_all_policies",
    "validate_necessity_label",
]
