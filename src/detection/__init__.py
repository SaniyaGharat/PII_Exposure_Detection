"""
PII Exposure Detection - Detection & Evaluation Package
Implements Microsoft Presidio baseline, custom domain-specific recognizers,
OCR extraction pipelines, and multi-strategy PII evaluation metrics.
"""

from .custom_recognizers import get_custom_recognizers, DOMAIN_ENTITY_MAPPING
from .ocr_engine import OCREngine, extract_text_from_image
from .detect import PIIDetector, run_detection_pipeline
from .evaluate import EvaluationSuite, run_evaluation_pipeline

__all__ = [
    "get_custom_recognizers",
    "DOMAIN_ENTITY_MAPPING",
    "OCREngine",
    "extract_text_from_image",
    "PIIDetector",
    "run_detection_pipeline",
    "EvaluationSuite",
    "run_evaluation_pipeline",
]
