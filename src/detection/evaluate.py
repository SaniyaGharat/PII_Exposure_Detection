"""
PII Exposure Detection - Evaluation Suite
Computes multi-strategy PII detection metrics (Exact Span, Partial Overlap, Field Presence),
generates per-field Precision, Recall, and F1, and quantifies OCR degradation effects.
"""

import csv
import difflib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union


@dataclass
class MetricScore:
    """Stores Precision, Recall, F1, and raw contingency counts."""
    tp: int = 0
    fp: int = 0
    fn: int = 0
    support: int = 0
    unalignable_count: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1, 4),
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
            "support": self.support,
            "unalignable_count": self.unalignable_count,
        }


def find_ocr_span_for_field(
    clean_val: str,
    ocr_text: str,
    similarity_threshold: float = 0.5,
) -> Tuple[Optional[Tuple[int, int]], float]:
    """
    Locates the corresponding span [start, end] of a ground truth field value inside
    the OCR-extracted text using difflib.SequenceMatcher.

    Args:
        clean_val: The ground truth text value from the clean document.
        ocr_text: The full text extracted by OCR.
        similarity_threshold: Minimum SequenceMatcher ratio to accept alignment.

    Returns:
        ((start, end), similarity_score) if aligned, else (None, 0.0).
    """
    clean_val = clean_val.strip()
    if not clean_val or not ocr_text:
        return None, 0.0

    # 1. Direct exact substring match in OCR text
    idx = ocr_text.find(clean_val)
    if idx != -1:
        return (idx, idx + len(clean_val)), 1.0

    # 2. SequenceMatcher longest matching block
    matcher = difflib.SequenceMatcher(None, clean_val, ocr_text, autojunk=False)
    match = matcher.find_longest_match(0, len(clean_val), 0, len(ocr_text))

    if match.size >= max(3, int(len(clean_val) * similarity_threshold)):
        ocr_start = match.b - match.a
        ocr_end = ocr_start + len(clean_val)

        ocr_start = max(0, min(ocr_start, len(ocr_text)))
        ocr_end = max(ocr_start, min(ocr_end, len(ocr_text)))

        candidate = ocr_text[ocr_start:ocr_end]
        ratio = difflib.SequenceMatcher(None, clean_val, candidate).ratio()

        block_start = match.b
        block_end = match.b + match.size

        if ratio >= similarity_threshold:
            return (ocr_start, ocr_end), ratio
        else:
            return (block_start, block_end), match.size / len(clean_val)

    return None, 0.0


class EvaluationSuite:
    """Evaluates predicted PII against ground truth annotations across 3 matching protocols."""

    def __init__(self, dataset_dir: Union[str, Path]):
        self.dataset_dir = Path(dataset_dir)
        self.ground_truth_cache: Dict[str, Dict[str, Any]] = {}
        self._load_ground_truth()

    def _load_ground_truth(self) -> None:
        """Caches all ground truth JSON labels across document categories."""
        for dt_dir in self.dataset_dir.iterdir():
            if dt_dir.is_dir() and dt_dir.name != "splits":
                labels_dir = dt_dir / "labels"
                if labels_dir.exists():
                    for label_file in labels_dir.glob("*.json"):
                        try:
                            with open(label_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                doc_id = data.get("document_id", label_file.stem)
                                self.ground_truth_cache[doc_id] = data
                        except Exception:
                            pass

    def evaluate_predictions(
        self,
        predictions_dir: Union[str, Path],
        is_ocr: bool = False,
    ) -> Dict[str, Any]:
        """
        Evaluates a directory of prediction JSON files against ground truth.

        For OCR documents, ground truth spans are realigned into the OCR coordinate system
        using SequenceMatcher before computing span-based metrics.
        """
        pred_path = Path(predictions_dir)
        pred_files = list(pred_path.glob("*.json"))

        if not pred_files:
            return {"error": f"No prediction files found in {predictions_dir}"}

        # Counters for the 3 matching strategies
        exact_metrics: Dict[str, MetricScore] = {}
        partial_metrics: Dict[str, MetricScore] = {}
        presence_metrics: Dict[str, MetricScore] = {}

        total_docs_evaluated = 0
        total_gt_fields = 0
        total_unalignable_fields = 0
        total_aligned_fields = 0

        for pf in pred_files:
            with open(pf, "r", encoding="utf-8") as f:
                pred_doc = json.load(f)

            doc_id = pred_doc["doc_id"]
            if doc_id not in self.ground_truth_cache:
                continue

            total_docs_evaluated += 1
            gt_doc = self.ground_truth_cache[doc_id]
            gt_fields = gt_doc.get("fields", [])
            preds = pred_doc.get("predictions", [])
            ocr_text = pred_doc.get("ocr_text", "") if is_ocr else ""

            # Extract ground truth items: [(field_type, start, end, field_val, is_aligned)]
            gt_items: List[Dict[str, Any]] = []
            for gf in gt_fields:
                ft = gf["field_type"]
                clean_val = gf.get("field_value", "")
                span = gf.get("span", {})
                clean_start = span.get("start", 0)
                clean_end = span.get("end", 0)

                total_gt_fields += 1

                if is_ocr:
                    ocr_span, score = find_ocr_span_for_field(clean_val, ocr_text)
                    if ocr_span:
                        s, e = ocr_span
                        gt_items.append({
                            "field_type": ft,
                            "start": s,
                            "end": e,
                            "value": clean_val,
                            "is_aligned": True,
                        })
                        total_aligned_fields += 1
                    else:
                        gt_items.append({
                            "field_type": ft,
                            "start": None,
                            "end": None,
                            "value": clean_val,
                            "is_aligned": False,
                        })
                        total_unalignable_fields += 1
                else:
                    gt_items.append({
                        "field_type": ft,
                        "start": clean_start,
                        "end": clean_end,
                        "value": clean_val,
                        "is_aligned": True,
                    })
                    total_aligned_fields += 1

            # Update support and unalignable counts
            for item in gt_items:
                ft = item["field_type"]
                for metric_dict in [exact_metrics, partial_metrics, presence_metrics]:
                    if ft not in metric_dict:
                        metric_dict[ft] = MetricScore()
                    metric_dict[ft].support += 1
                    if not item["is_aligned"]:
                        metric_dict[ft].unalignable_count += 1

            # ----------------------------------------------------
            # 1. Exact Span Matching
            # ----------------------------------------------------
            matched_gt_exact = set()
            matched_pred_exact = set()

            for p_idx, p in enumerate(preds):
                p_ft = p["field_type"]
                p_start, p_end = p["predicted_span"]
                if p_ft not in exact_metrics:
                    exact_metrics[p_ft] = MetricScore()

                found_match = False
                for g_idx, g in enumerate(gt_items):
                    if g_idx in matched_gt_exact or not g["is_aligned"] or g["start"] is None:
                        continue
                    if g["field_type"] == p_ft and g["start"] == p_start and g["end"] == p_end:
                        matched_gt_exact.add(g_idx)
                        matched_pred_exact.add(p_idx)
                        exact_metrics[p_ft].tp += 1
                        found_match = True
                        break

                if not found_match:
                    exact_metrics[p_ft].fp += 1

            for g_idx, g in enumerate(gt_items):
                if g_idx not in matched_gt_exact:
                    exact_metrics[g["field_type"]].fn += 1

            # ----------------------------------------------------
            # 2. Partial Span Overlap Matching
            # ----------------------------------------------------
            matched_gt_partial = set()
            matched_pred_partial = set()

            for p_idx, p in enumerate(preds):
                p_ft = p["field_type"]
                p_start, p_end = p["predicted_span"]
                if p_ft not in partial_metrics:
                    partial_metrics[p_ft] = MetricScore()

                found_match = False
                for g_idx, g in enumerate(gt_items):
                    if g_idx in matched_gt_partial or not g["is_aligned"] or g["start"] is None:
                        continue
                    if g["field_type"] == p_ft:
                        overlap = max(0, min(p_end, g["end"]) - max(p_start, g["start"]))
                        if overlap > 0:
                            matched_gt_partial.add(g_idx)
                            matched_pred_partial.add(p_idx)
                            partial_metrics[p_ft].tp += 1
                            found_match = True
                            break

                if not found_match:
                    partial_metrics[p_ft].fp += 1

            for g_idx, g in enumerate(gt_items):
                if g_idx not in matched_gt_partial:
                    partial_metrics[g["field_type"]].fn += 1

            # ----------------------------------------------------
            # 3. Field Presence Matching (Document-Level Existence)
            # ----------------------------------------------------
            gt_field_types = {g["field_type"] for g in gt_items}
            pred_field_types = {p["field_type"] for p in preds}

            all_field_types = gt_field_types.union(pred_field_types)
            for ft in all_field_types:
                if ft not in presence_metrics:
                    presence_metrics[ft] = MetricScore()

                in_gt = ft in gt_field_types
                in_pred = ft in pred_field_types

                if in_gt and in_pred:
                    presence_metrics[ft].tp += 1
                elif in_pred and not in_gt:
                    presence_metrics[ft].fp += 1
                elif in_gt and not in_pred:
                    presence_metrics[ft].fn += 1

        # Calculate macro and micro aggregates
        results = {
            "is_ocr": is_ocr,
            "total_documents_evaluated": total_docs_evaluated,
            "alignment_stats": {
                "total_gt_fields": total_gt_fields,
                "aligned_fields": total_aligned_fields,
                "unalignable_fields": total_unalignable_fields,
                "alignment_rate": round(total_aligned_fields / total_gt_fields, 4) if total_gt_fields > 0 else 1.0,
            } if is_ocr else None,
            "strategies": {
                "exact_span": self._compile_strategy_summary(exact_metrics),
                "partial_overlap": self._compile_strategy_summary(partial_metrics),
                "field_presence": self._compile_strategy_summary(presence_metrics),
            }
        }
        return results

    def _compile_strategy_summary(self, metrics_by_field: Dict[str, MetricScore]) -> Dict[str, Any]:
        """Aggregates per-field metrics into micro/macro summaries."""
        per_field = {}
        total_tp, total_fp, total_fn, total_support = 0, 0, 0, 0
        precisions, recalls, f1s = [], [], []

        for ft, score in sorted(metrics_by_field.items()):
            per_field[ft] = score.to_dict()
            total_tp += score.tp
            total_fp += score.fp
            total_fn += score.fn
            total_support += score.support

            if score.support > 0 or (score.tp + score.fp) > 0:
                precisions.append(score.precision)
                recalls.append(score.recall)
                f1s.append(score.f1)

        micro_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        micro_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        micro_f1 = (2 * micro_p * micro_r) / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0.0

        macro_p = sum(precisions) / len(precisions) if precisions else 0.0
        macro_r = sum(recalls) / len(recalls) if recalls else 0.0
        macro_f1 = sum(f1s) / len(f1s) if f1s else 0.0

        return {
            "macro_precision": round(macro_p, 4),
            "macro_recall": round(macro_r, 4),
            "macro_f1": round(macro_f1, 4),
            "micro_precision": round(micro_p, 4),
            "micro_recall": round(micro_r, 4),
            "micro_f1": round(micro_f1, 4),
            "total_tp": total_tp,
            "total_fp": total_fp,
            "total_fn": total_fn,
            "total_support": total_support,
            "per_field": per_field,
        }


def save_evaluation_reports(
    clean_results: Dict[str, Any],
    ocr_results: Optional[Dict[str, Any]],
    output_dir: Union[str, Path],
) -> Tuple[Path, Path, Path]:
    """Saves structured JSON and CSV reports comparing Clean vs. OCR performance."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    clean_json_path = out_dir / "detection_metrics_clean.json"
    ocr_json_path = out_dir / "detection_metrics_ocr.json"
    summary_csv_path = out_dir / "detection_comparison_clean_vs_ocr.csv"

    # 1. Save Clean Metrics JSON
    with open(clean_json_path, "w", encoding="utf-8") as f:
        json.dump(clean_results, f, indent=2)

    # 2. Save OCR Metrics JSON
    if ocr_results:
        with open(ocr_json_path, "w", encoding="utf-8") as f:
            json.dump(ocr_results, f, indent=2)

    # 3. Save Comparative CSV Report
    clean_partial = clean_results["strategies"]["partial_overlap"]["per_field"]
    ocr_partial = ocr_results["strategies"]["partial_overlap"]["per_field"] if ocr_results else {}

    all_fields = sorted(set(list(clean_partial.keys()) + list(ocr_partial.keys())))

    with open(summary_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Field_Type",
            "Clean_Precision", "Clean_Recall", "Clean_F1", "Clean_Support",
            "OCR_Precision", "OCR_Recall", "OCR_F1", "OCR_Support",
            "F1_Delta_(Clean-OCR)"
        ])

        for ft in all_fields:
            c_data = clean_partial.get(ft, {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "support": 0})
            o_data = ocr_partial.get(ft, {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "support": 0})
            f1_delta = round(c_data["f1_score"] - o_data["f1_score"], 4) if ocr_results else 0.0

            writer.writerow([
                ft,
                c_data["precision"], c_data["recall"], c_data["f1_score"], c_data["support"],
                o_data["precision"], o_data["recall"], o_data["f1_score"], o_data["support"],
                f1_delta
            ])

    return clean_json_path, ocr_json_path, summary_csv_path


def print_evaluation_summary(
    clean_results: Dict[str, Any],
    ocr_results: Optional[Dict[str, Any]] = None,
) -> None:
    """Prints a clear, structured research summary to console highlighting top and bottom performers."""
    print("\n" + "=" * 70)
    print("           PII DETECTION EVALUATION REPORT (PHASE 2)")
    print("=" * 70)

    clean_strat = clean_results.get("strategies", {})
    clean_partial = clean_strat.get("partial_overlap", {})
    clean_exact = clean_strat.get("exact_span", {})
    clean_presence = clean_strat.get("field_presence", {})

    print(f"\n[CLEAN DIGITAL DOCUMENTS] Evaluated: {clean_results.get('total_documents_evaluated', 0)} docs")
    print("-" * 70)
    print(f"  Exact Span Match:     Precision={clean_exact.get('macro_precision', 0):.4f} | Recall={clean_exact.get('macro_recall', 0):.4f} | Macro F1={clean_exact.get('macro_f1', 0):.4f}")
    print(f"  Partial Overlap:      Precision={clean_partial.get('macro_precision', 0):.4f} | Recall={clean_partial.get('macro_recall', 0):.4f} | Macro F1={clean_partial.get('macro_f1', 0):.4f}")
    print(f"  Field Presence:       Precision={clean_presence.get('macro_precision', 0):.4f} | Recall={clean_presence.get('macro_recall', 0):.4f} | Macro F1={clean_presence.get('macro_f1', 0):.4f}")

    if ocr_results and "strategies" in ocr_results:
        ocr_strat = ocr_results.get("strategies", {})
        ocr_exact = ocr_strat.get("exact_span", {})
        ocr_partial = ocr_strat.get("partial_overlap", {})
        ocr_presence = ocr_strat.get("field_presence", {})
        align_stats = ocr_results.get("alignment_stats", {})

        print(f"\n[SCANNED OCR DOCUMENTS (REALIGNED)] Evaluated: {ocr_results.get('total_documents_evaluated', 0)} docs")
        if align_stats:
            print(f"  GT Span Alignment:    Aligned={align_stats.get('aligned_fields', 0)} / {align_stats.get('total_gt_fields', 0)} fields ({align_stats.get('alignment_rate', 0)*100:.1f}%) | Unalignable (OCR corrupted)={align_stats.get('unalignable_fields', 0)}")
        print("-" * 70)
        print(f"  Exact Span Match:     Precision={ocr_exact.get('macro_precision', 0):.4f} | Recall={ocr_exact.get('macro_recall', 0):.4f} | Macro F1={ocr_exact.get('macro_f1', 0):.4f}")
        print(f"  Partial Overlap:      Precision={ocr_partial.get('macro_precision', 0):.4f} | Recall={ocr_partial.get('macro_recall', 0):.4f} | Macro F1={ocr_partial.get('macro_f1', 0):.4f}")
        print(f"  Field Presence:       Precision={ocr_presence.get('macro_precision', 0):.4f} | Recall={ocr_presence.get('macro_recall', 0):.4f} | Macro F1={ocr_presence.get('macro_f1', 0):.4f}")
        macro_drop = clean_partial.get('macro_f1', 0) - ocr_partial.get('macro_f1', 0)
        print(f"  OCR Degradation Delta: Delta Macro F1 = -{macro_drop:.4f} (Clean vs. OCR Partial Overlap)")

    print("\n" + "-" * 70)
    print(f"{'Field Type':<24} | {'Clean F1 (Part)':<15} | {'OCR F1 (Part)':<15} | {'Delta F1':<8}")
    print("-" * 70)

    clean_per_field = clean_partial.get("per_field", {})
    ocr_per_field = ocr_results.get("strategies", {}).get("partial_overlap", {}).get("per_field", {}) if ocr_results else {}

    sorted_fields = sorted(
        clean_per_field.items(),
        key=lambda item: item[1]["f1_score"],
        reverse=True
    )

    for ft, scores in sorted_fields:
        c_f1 = scores["f1_score"]
        o_f1 = ocr_per_field.get(ft, {}).get("f1_score", 0.0) if ocr_results else 0.0
        delta = c_f1 - o_f1 if ocr_results else 0.0
        print(f"{ft:<24} | {c_f1:<15.4f} | {o_f1:<15.4f} | {delta:<8.4f}")

    # Identify top and lowest performing fields for research discussion
    print("\n" + "=" * 70)
    print("               RESEARCH LIMITATIONS & INSIGHTS")
    print("=" * 70)
    top_performers = [ft for ft, s in sorted_fields if s["f1_score"] >= 0.85]
    low_performers = [ft for ft, s in sorted_fields if s["f1_score"] < 0.60]

    print(f"  [HIGH] High-Performing Fields (F1 >= 0.85): {', '.join(top_performers[:6]) if top_performers else 'None'}")
    print(f"  [LOW]  Lowest-Performing Fields (F1 < 0.60): {', '.join(low_performers) if low_performers else 'None'}")
    print("=" * 70 + "\n")


def run_evaluation_pipeline(
    dataset_dir: Union[str, Path],
    predictions_dir: Union[str, Path],
    results_dir: Union[str, Path],
) -> Dict[str, Any]:
    """Runs complete evaluation across clean and OCR predictions and saves reports."""
    suite = EvaluationSuite(dataset_dir=dataset_dir)
    pred_path = Path(predictions_dir)

    clean_preds = pred_path / "clean"
    ocr_preds = pred_path / "ocr"

    clean_results = suite.evaluate_predictions(clean_preds, is_ocr=False)
    ocr_results = suite.evaluate_predictions(ocr_preds, is_ocr=True) if ocr_preds.exists() else None

    save_evaluation_reports(clean_results, ocr_results, results_dir)
    print_evaluation_summary(clean_results, ocr_results)

    return {
        "clean": clean_results,
        "ocr": ocr_results,
    }
