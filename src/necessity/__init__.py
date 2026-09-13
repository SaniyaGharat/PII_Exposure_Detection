"""
PII Exposure Detection - Necessity Classification Package (Phase 3)
Implements Hybrid Rule + ML framework N(f, p) = alpha * R(f, p) + (1 - alpha) * M(f, p)
for ordinal necessity scoring and automated privacy audit reporting.
"""

from .rule_engine import RuleEngine, LABEL_TO_SCORE, SCORE_TO_LABEL
from .ml_classifier import MLNecessityClassifier, extract_context_window
from .hybrid import HybridNecessityEvaluator
from .pipeline_test import run_end_to_end_evaluation
from .report_generator import (
    generate_necessity_report,
    render_report_markdown,
    generate_and_save_sample_reports,
)

__all__ = [
    "RuleEngine",
    "LABEL_TO_SCORE",
    "SCORE_TO_LABEL",
    "MLNecessityClassifier",
    "extract_context_window",
    "HybridNecessityEvaluator",
    "run_end_to_end_evaluation",
    "generate_necessity_report",
    "render_report_markdown",
    "generate_and_save_sample_reports",
]
