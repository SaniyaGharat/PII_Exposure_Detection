"""
PII Exposure Detection - End-to-End Pipeline & Compounding Error Test
Evaluates necessity classification over Phase 2's detected PII fields (Clean & OCR)
to quantify the compounding accuracy loss introduced by upstream detection errors.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.necessity.hybrid import HybridNecessityEvaluator


def run_end_to_end_evaluation(
    dataset_dir: Union[str, Path],
    predictions_dir: Union[str, Path],
    hybrid_evaluator: HybridNecessityEvaluator,
    unnecessary_threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Evaluates end-to-end necessity classification performance on Phase 2 predictions.

    Args:
        dataset_dir: Dataset root path.
        predictions_dir: Path to results/predictions (containing 'clean' and 'ocr' subdirs).
        hybrid_evaluator: Trained and tuned HybridNecessityEvaluator instance.
        unnecessary_threshold: Cutoff below which a field is flagged as unnecessary.

    Returns:
        Dictionary containing Clean vs. OCR end-to-end performance and degradation metrics.
    """
    dataset_path = Path(dataset_dir)
    pred_path = Path(predictions_dir)

    results = {}

    for modality in ["clean", "ocr"]:
        mod_dir = pred_path / modality
        if not mod_dir.exists():
            continue

        pred_files = list(mod_dir.glob("*.json"))
        total_docs = len(pred_files)

        # Ground truth mapping: doc_id -> list of gt fields with their necessity
        # Evaluation at the field instance level
        gt_binary_list = []
        pred_binary_list = []

        total_gt_unnecessary = 0
        correctly_flagged_unnecessary = 0
        missed_unnecessary = 0
        spurious_flagged_unnecessary = 0

        for pf in pred_files:
            with open(pf, "r", encoding="utf-8") as f:
                pred_doc = json.load(f)

            doc_id = pred_doc["doc_id"]
            doc_type = pred_doc["document_type"]
            preds = pred_doc.get("predictions", [])

            # Load GT
            gt_file = dataset_path / doc_type / "labels" / f"{doc_id}.json"
            if not gt_file.exists():
                continue

            with open(gt_file, "r", encoding="utf-8") as gf:
                gt_doc = json.load(gf)

            gt_fields = {
                f["field_type"]: (f["necessity_label"].lower() == "unnecessary")
                for f in gt_doc.get("fields", [])
            }

            # Predictions for this document
            detected_field_types = {}
            for p in preds:
                ft = p["field_type"]
                text_snippet = p.get("predicted_text", "")
                span = p.get("predicted_span", [0, 0])

                n_score, r_score, m_score, label, reason = hybrid_evaluator.score_field(
                    field_type=ft,
                    document_type=doc_type,
                    context_text=text_snippet,
                    field_value=text_snippet,
                )
                is_unnecessary_pred = (n_score < unnecessary_threshold)

                # Keep highest priority prediction per field_type
                if ft not in detected_field_types or is_unnecessary_pred:
                    detected_field_types[ft] = is_unnecessary_pred

            # Compare on all ground truth fields in the document
            for ft, is_gt_unnec in gt_fields.items():
                if is_gt_unnec:
                    total_gt_unnecessary += 1

                is_pred_unnec = detected_field_types.get(ft, False)
                gt_binary_list.append(1 if is_gt_unnec else 0)
                pred_binary_list.append(1 if is_pred_unnec else 0)

                if is_gt_unnec and is_pred_unnec:
                    correctly_flagged_unnecessary += 1
                elif is_gt_unnec and not is_pred_unnec:
                    missed_unnecessary += 1

            # Check spurious false positives from detection that were flagged unnecessary
            for ft, is_pred_unnec in detected_field_types.items():
                if ft not in gt_fields and is_pred_unnec:
                    spurious_flagged_unnecessary += 1

        y_true = np.array(gt_binary_list)
        y_pred = np.array(pred_binary_list)

        prec = float(precision_score(y_true, y_pred, zero_division=0))
        rec = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))
        acc = float(accuracy_score(y_true, y_pred))

        results[modality] = {
            "total_documents": total_docs,
            "total_evaluated_instances": len(y_true),
            "total_gt_unnecessary": total_gt_unnecessary,
            "correctly_flagged_unnecessary": correctly_flagged_unnecessary,
            "missed_unnecessary": missed_unnecessary,
            "spurious_flagged_unnecessary": spurious_flagged_unnecessary,
            "end_to_end_precision": round(prec, 4),
            "end_to_end_recall": round(rec, 4),
            "end_to_end_f1": round(f1, 4),
            "end_to_end_accuracy": round(acc, 4),
        }

    return results
