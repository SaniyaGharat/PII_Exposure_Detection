"""
PII Exposure Detection - End-to-End Pipeline & Compounding Error Test
Rigorously evaluates end-to-end necessity classification over all ground-truth PII instances
in the held-out test split, explicitly scoring undetected PII as distinct 'undetected -> unassessed'
pipeline failures to expose the deployment-readiness gap introduced by upstream detection errors.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from src.necessity.hybrid import HybridNecessityEvaluator
from src.necessity.ml_classifier import extract_context_window


def run_end_to_end_evaluation(
    dataset_dir: Union[str, Path],
    predictions_dir: Union[str, Path],
    hybrid_evaluator: HybridNecessityEvaluator,
    unnecessary_threshold: float = 0.5,
    split_name: str = "test",
) -> Dict[str, Any]:
    """
    Evaluates end-to-end necessity pipeline performance against ALL ground-truth PII instances
    on the held-out test split documents.

    Args:
        dataset_dir: Dataset root path.
        predictions_dir: Path to results/predictions (containing 'clean' and 'ocr' subdirs).
        hybrid_evaluator: Trained and tuned HybridNecessityEvaluator instance.
        unnecessary_threshold: Cutoff below which a field is flagged as unnecessary.
        split_name: Split to evaluate on ('test' by default, matching Step 4).

    Returns:
        Dictionary containing honest Clean vs. OCR end-to-end performance,
        undetected -> unassessed failure rates by field type, and Oracle vs. E2E catch rate gaps.
    """
    dataset_path = Path(dataset_dir)
    pred_path = Path(predictions_dir)

    split_file = dataset_path / "splits" / f"{split_name}.json"
    with open(split_file, "r", encoding="utf-8") as sf:
        split_info = json.load(sf)
    test_docs = split_info["documents"]

    results = {}

    for modality in ["clean", "ocr"]:
        mod_dir = pred_path / modality
        if not mod_dir.exists():
            continue

        total_docs = 0
        total_gt_instances = 0
        total_detected_instances = 0
        total_undetected_unassessed = 0

        total_gt_unnecessary = 0
        caught_unnecessary_e2e = 0
        missed_unnecessary_due_to_detection = 0
        missed_unnecessary_due_to_classification = 0

        total_gt_necessary = 0
        correctly_cleared_necessary = 0
        unassessed_necessary_leakage = 0
        over_redacted_necessary = 0

        # Oracle counters (what Phase 3 necessity classifier scores on GT text)
        oracle_caught_unnecessary = 0

        # Field-type specific tracking
        field_stats = defaultdict(lambda: {
            "total_gt": 0,
            "detected": 0,
            "undetected_unassessed": 0,
            "gt_unnecessary": 0,
            "caught_unnecessary": 0,
            "missed_detection_unnecessary": 0,
        })

        for doc_item in test_docs:
            doc_id = doc_item["document_id"]
            doc_type = doc_item["document_type"]

            pred_file = mod_dir / f"{doc_id}.json"
            if not pred_file.exists():
                continue

            total_docs += 1

            with open(pred_file, "r", encoding="utf-8") as f:
                pred_doc = json.load(f)

            preds = pred_doc.get("predictions", [])

            # Load GT
            gt_file = dataset_path / doc_type / "labels" / f"{doc_id}.json"
            text_file = dataset_path / doc_type / "text" / f"{doc_id}.txt"
            if not (gt_file.exists() and text_file.exists()):
                continue

            with open(gt_file, "r", encoding="utf-8") as gf:
                gt_doc = json.load(gf)
            text_content = text_file.read_text(encoding="utf-8")

            gt_fields = gt_doc.get("fields", [])

            # Map predicted fields by field_type (taking highest confidence if multiple)
            detected_field_map = {}
            for p in preds:
                ft = p["field_type"]
                if ft not in detected_field_map:
                    detected_field_map[ft] = []
                detected_field_map[ft].append(p)

            # Process every ground-truth instance
            for gt_field in gt_fields:
                ft = gt_field["field_type"]
                fv = gt_field["field_value"]
                gt_label = gt_field["necessity_label"].lower()
                is_gt_unnec = (gt_label == "unnecessary")
                span = gt_field.get("span", {})
                s, e = span.get("start", 0), span.get("end", 0)

                total_gt_instances += 1
                field_stats[ft]["total_gt"] += 1

                if is_gt_unnec:
                    total_gt_unnecessary += 1
                    field_stats[ft]["gt_unnecessary"] += 1
                else:
                    total_gt_necessary += 1

                # Evaluate Oracle score on GT instance with exact context window
                oracle_ctx = extract_context_window(text_content, s, e)
                oracle_n, _, _, _, _ = hybrid_evaluator.score_field(
                    field_type=ft,
                    document_type=doc_type,
                    context_text=oracle_ctx,
                    field_value=str(fv),
                )
                if is_gt_unnec and (oracle_n < unnecessary_threshold):
                    oracle_caught_unnecessary += 1

                # Select candidate prediction matching this ground truth instance
                candidates = detected_field_map.get(ft, [])
                best_match = None
                best_overlap = -1
                best_dist = float("inf")

                for cand in candidates:
                    p_span = cand.get("predicted_span", [0, 0])
                    ps, pe = p_span[0], p_span[1]
                    inter = max(0, min(e, pe) - max(s, ps))
                    dist = abs((s + e) / 2.0 - (ps + pe) / 2.0)
                    if inter > best_overlap:
                        best_overlap = inter
                        best_dist = dist
                        best_match = cand
                    elif inter == best_overlap and inter > 0:
                        if dist < best_dist:
                            best_dist = dist
                            best_match = cand

                # If no candidate overlapped, select candidate with closest midpoint distance
                if best_overlap == 0:
                    for cand in candidates:
                        p_span = cand.get("predicted_span", [0, 0])
                        ps, pe = p_span[0], p_span[1]
                        dist = abs((s + e) / 2.0 - (ps + pe) / 2.0)
                        if dist < best_dist:
                            best_dist = dist
                            best_match = cand

                is_detected = (best_match is not None)

                if is_detected:
                    total_detected_instances += 1
                    field_stats[ft]["detected"] += 1

                    # Evaluate necessity on detected prediction
                    p_span = best_match.get("predicted_span", [0, 0])
                    p_text = best_match.get("predicted_text", "")

                    det_ctx = (
                        extract_context_window(text_content, p_span[0], p_span[1])
                        if p_span[1] > 0
                        else oracle_ctx
                    )

                    n_score, _, _, _, _ = hybrid_evaluator.score_field(
                        field_type=ft,
                        document_type=doc_type,
                        context_text=det_ctx,
                        field_value=p_text,
                    )
                    is_pred_unnec = (n_score < unnecessary_threshold)

                    if is_gt_unnec:
                        if is_pred_unnec:
                            caught_unnecessary_e2e += 1
                            field_stats[ft]["caught_unnecessary"] += 1
                        else:
                            missed_unnecessary_due_to_classification += 1
                    else:
                        if is_pred_unnec:
                            over_redacted_necessary += 1
                        else:
                            correctly_cleared_necessary += 1

                else:
                    # Detection failure -> Undetected and Unassessed
                    total_undetected_unassessed += 1
                    field_stats[ft]["undetected_unassessed"] += 1

                    if is_gt_unnec:
                        missed_unnecessary_due_to_detection += 1
                        field_stats[ft]["missed_detection_unnecessary"] += 1
                    else:
                        unassessed_necessary_leakage += 1

        # Calculate rates
        overall_undetected_rate = total_undetected_unassessed / total_gt_instances if total_gt_instances > 0 else 0.0
        e2e_unnecessary_catch_rate = caught_unnecessary_e2e / total_gt_unnecessary if total_gt_unnecessary > 0 else 0.0
        oracle_unnecessary_catch_rate = oracle_caught_unnecessary / total_gt_unnecessary if total_gt_unnecessary > 0 else 0.0
        detection_gap = oracle_unnecessary_catch_rate - e2e_unnecessary_catch_rate
        e2e_necessary_clearance_rate = correctly_cleared_necessary / total_gt_necessary if total_gt_necessary > 0 else 0.0

        # Compile per-field summary
        per_field_summary = {}
        for ft, stats in sorted(field_stats.items()):
            n_gt = stats["total_gt"]
            n_undetected = stats["undetected_unassessed"]
            undetected_rate = n_undetected / n_gt if n_gt > 0 else 0.0

            n_unnec_gt = stats["gt_unnecessary"]
            n_caught = stats["caught_unnecessary"]
            field_catch_rate = n_caught / n_unnec_gt if n_unnec_gt > 0 else (1.0 if n_unnec_gt == 0 else 0.0)

            per_field_summary[ft] = {
                "total_gt_instances": n_gt,
                "detected_instances": stats["detected"],
                "undetected_unassessed_count": n_undetected,
                "undetected_unassessed_rate": round(undetected_rate, 4),
                "gt_unnecessary_instances": n_unnec_gt,
                "caught_unnecessary_e2e": n_caught,
                "missed_due_to_detection": stats["missed_detection_unnecessary"],
                "field_unnecessary_catch_rate": round(field_catch_rate, 4) if n_unnec_gt > 0 else "N/A",
            }

        results[modality] = {
            "total_documents": total_docs,
            "total_gt_instances": total_gt_instances,
            "total_detected_instances": total_detected_instances,
            "total_undetected_unassessed": total_undetected_unassessed,
            "overall_undetected_rate": round(overall_undetected_rate, 4),
            "unnecessary_pii_evaluation": {
                "total_gt_unnecessary": total_gt_unnecessary,
                "caught_unnecessary_e2e": caught_unnecessary_e2e,
                "missed_due_to_detection": missed_unnecessary_due_to_detection,
                "missed_due_to_classification": missed_unnecessary_due_to_classification,
                "e2e_unnecessary_catch_rate": round(e2e_unnecessary_catch_rate, 4),
                "oracle_unnecessary_catch_rate": round(oracle_unnecessary_catch_rate, 4),
                "detection_gap": round(detection_gap, 4),
            },
            "necessary_pii_evaluation": {
                "total_gt_necessary": total_gt_necessary,
                "correctly_cleared_necessary": correctly_cleared_necessary,
                "unassessed_necessary_leakage": unassessed_necessary_leakage,
                "over_redacted_necessary": over_redacted_necessary,
                "e2e_necessary_clearance_rate": round(e2e_necessary_clearance_rate, 4),
            },
            "per_field_undetected_breakdown": per_field_summary,
        }

    return results
