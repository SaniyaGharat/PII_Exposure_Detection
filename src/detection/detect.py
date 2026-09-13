"""
PII Exposure Detection - Detection Pipeline Module
Executes Microsoft Presidio analysis with default spaCy and custom domain recognizers
over clean digital text and OCR-extracted scanned documents.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, RecognizerResult
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider

from src.detection.custom_recognizers import get_custom_recognizers, DOMAIN_ENTITY_MAPPING
from src.detection.ocr_engine import OCREngine, extract_text_from_image


class PIIDetector:
    """Configures and runs Microsoft Presidio Analyzer with domain-specific recognizers."""

    def __init__(self, score_threshold: float = 0.4, language: str = "en"):
        self.language = language
        self.score_threshold = score_threshold
        self.analyzer = self._init_analyzer_engine()

    def _init_analyzer_engine(self) -> AnalyzerEngine:
        """Initializes Presidio AnalyzerEngine with spaCy and custom recognizers."""
        try:
            # Configure spaCy English model
            provider = NlpEngineProvider(nlp_configuration={
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
            })
            nlp_engine = provider.create_engine()
            registry = RecognizerRegistry()
            registry.load_predefined_recognizers(nlp_engine=nlp_engine)
        except Exception:
            # Fallback without explicit provider if model loaded globally
            registry = RecognizerRegistry()
            registry.load_predefined_recognizers()
            nlp_engine = None

        # Register custom domain-specific recognizers
        custom_recs = get_custom_recognizers()
        for rec in custom_recs:
            registry.add_recognizer(rec)

        if nlp_engine:
            return AnalyzerEngine(registry=registry, nlp_engine=nlp_engine)
        return AnalyzerEngine(registry=registry)

    def detect(
        self,
        text: str,
        doc_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Runs Presidio analysis on the given text and maps detected entities to project field types.

        Args:
            text: The text to analyze.
            doc_type: Optional document type to assist contextual resolution.

        Returns:
            List of detected PII prediction dictionaries.
        """
        if not text or not text.strip():
            return []

        results: List[RecognizerResult] = self.analyzer.analyze(
            text=text,
            language=self.language,
            score_threshold=self.score_threshold,
        )

        predictions: List[Dict[str, Any]] = []

        # Sort results by position
        results = sorted(results, key=lambda r: (r.start, -r.score))

        for res in results:
            entity_type = res.entity_type
            mapped_field = DOMAIN_ENTITY_MAPPING.get(entity_type, entity_type.lower())

            # Refine context-sensitive mappings based on doc_type if needed
            if entity_type == "CUSTOM_ANNUAL_INCOME" and doc_type == "rental_agreement":
                mapped_field = "income"
            elif entity_type == "CUSTOM_HOME_ADDRESS" and doc_type == "rental_agreement":
                mapped_field = "current_address"

            predicted_text = text[res.start:res.end]

            predictions.append({
                "entity_type": entity_type,
                "field_type": mapped_field,
                "predicted_text": predicted_text,
                "predicted_span": [res.start, res.end],
                "confidence": round(float(res.score), 4),
            })

        # Deduplicate identical or fully subsumed spans for the same field_type
        deduped = self._deduplicate_predictions(predictions)
        return deduped

    def _deduplicate_predictions(self, predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Removes exact duplicate spans and keeps highest confidence predictions."""
        if not predictions:
            return []

        seen_spans = set()
        deduped = []

        for pred in predictions:
            span_key = (pred["field_type"], pred["predicted_span"][0], pred["predicted_span"][1])
            if span_key not in seen_spans:
                seen_spans.add(span_key)
                deduped.append(pred)

        return deduped


def run_detection_pipeline(
    dataset_dir: Union[str, Path],
    output_dir: Union[str, Path],
    splits: Optional[List[str]] = None,
    process_ocr: bool = True,
    score_threshold: float = 0.4,
) -> Dict[str, Any]:
    """
    Runs the full PII detection pipeline across specified dataset splits.

    Processes both clean text and scanned document OCR versions.
    Saves output predictions in output_dir/clean/ and output_dir/ocr/.

    Args:
        dataset_dir: Path to dataset root directory.
        output_dir: Path to store prediction JSONs.
        splits: List of splits to process (default: ['train', 'validation', 'test']).
        process_ocr: Whether to process OCR scanned documents.
        score_threshold: Presidio confidence score threshold.

    Returns:
        Summary dictionary of detection counts.
    """
    dataset_path = Path(dataset_dir)
    out_path = Path(output_dir)
    clean_out_dir = out_path / "clean"
    ocr_out_dir = out_path / "ocr"

    clean_out_dir.mkdir(parents=True, exist_ok=True)
    if process_ocr:
        ocr_out_dir.mkdir(parents=True, exist_ok=True)

    if splits is None:
        splits = ["train", "validation", "test"]

    detector = PIIDetector(score_threshold=score_threshold)
    ocr_engine = OCREngine() if process_ocr else None

    # Gather all target document IDs from split files
    target_docs: List[Tuple[str, str, str]] = [] # (split_name, doc_id, doc_type)
    splits_dir = dataset_path / "splits"

    for sp in splits:
        sp_file = splits_dir / f"{sp}.json"
        if sp_file.exists():
            with open(sp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("documents", []):
                    target_docs.append((sp, item["document_id"], item["document_type"]))

    stats = {
        "total_clean_processed": 0,
        "total_clean_predictions": 0,
        "total_ocr_processed": 0,
        "total_ocr_predictions": 0,
    }

    print(f"\n[Detection Pipeline] Processing {len(target_docs)} documents across splits {splits}...")

    for split_name, doc_id, doc_type in target_docs:
        text_file = dataset_path / doc_type / "text" / f"{doc_id}.txt"
        if not text_file.exists():
            continue

        # 1. Clean Text Detection
        clean_text = text_file.read_text(encoding="utf-8")
        clean_preds = detector.detect(clean_text, doc_type=doc_type)

        clean_doc_record = {
            "doc_id": doc_id,
            "document_type": doc_type,
            "split": split_name,
            "is_ocr": False,
            "text_length": len(clean_text),
            "predictions": clean_preds,
        }

        clean_pred_file = clean_out_dir / f"{doc_id}.json"
        with open(clean_pred_file, "w", encoding="utf-8") as f:
            json.dump(clean_doc_record, f, indent=2)

        stats["total_clean_processed"] += 1
        stats["total_clean_predictions"] += len(clean_preds)

        # 2. OCR Scanned Document Detection
        if process_ocr and ocr_engine:
            scanned_img = dataset_path / doc_type / "scanned" / f"{doc_id}.png"
            if scanned_img.exists():
                ocr_text = ocr_engine.extract_text(scanned_img)
                ocr_preds = detector.detect(ocr_text, doc_type=doc_type)

                ocr_doc_record = {
                    "doc_id": doc_id,
                    "document_type": doc_type,
                    "split": split_name,
                    "is_ocr": True,
                    "ocr_text": ocr_text,
                    "text_length": len(ocr_text),
                    "predictions": ocr_preds,
                }

                ocr_pred_file = ocr_out_dir / f"{doc_id}.json"
                with open(ocr_pred_file, "w", encoding="utf-8") as f:
                    json.dump(ocr_doc_record, f, indent=2)

                stats["total_ocr_processed"] += 1
                stats["total_ocr_predictions"] += len(ocr_preds)

    print(f" -> Completed: {stats['total_clean_processed']} clean docs ({stats['total_clean_predictions']} PII predicted), "
          f"{stats['total_ocr_processed']} OCR docs ({stats['total_ocr_predictions']} PII predicted).")
    return stats
