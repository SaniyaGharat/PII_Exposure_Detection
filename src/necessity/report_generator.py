"""
PII Exposure Detection - Sample Necessity Report Generator
Generates structured JSON and Markdown audit reports displaying per-field
necessity scores N(f,p), flagged statuses, and human-readable reasoning strings.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.necessity.hybrid import HybridNecessityEvaluator
from src.necessity.ml_classifier import extract_context_window


def generate_necessity_report(
    doc_id: str,
    dataset_dir: Union[str, Path],
    hybrid_evaluator: HybridNecessityEvaluator,
    unnecessary_threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Generates a comprehensive necessity audit report for a single document.

    Args:
        doc_id: Document ID (e.g., 'job_001', 'med_002').
        dataset_dir: Dataset root directory.
        hybrid_evaluator: HybridNecessityEvaluator instance.
        unnecessary_threshold: Threshold below which a field is flagged as unnecessary.

    Returns:
        Structured audit dictionary.
    """
    dataset_path = Path(dataset_dir)

    # Locate document across domain folders
    target_label_file = None
    target_text_file = None
    doc_type = None

    for dt_dir in dataset_path.iterdir():
        if dt_dir.is_dir() and dt_dir.name != "splits":
            lf = dt_dir / "labels" / f"{doc_id}.json"
            tf = dt_dir / "text" / f"{doc_id}.txt"
            if lf.exists() and tf.exists():
                target_label_file = lf
                target_text_file = tf
                doc_type = dt_dir.name
                break

    if not target_label_file:
        raise FileNotFoundError(f"Document '{doc_id}' not found in {dataset_dir}")

    text_content = target_text_file.read_text(encoding="utf-8")
    with open(target_label_file, "r", encoding="utf-8") as f:
        gt_data = json.load(f)

    field_audits: List[Dict[str, Any]] = []
    total_unnecessary_flagged = 0

    for f_entry in gt_data.get("fields", []):
        ft = f_entry["field_type"]
        fn = f_entry.get("field_name", ft.replace("_", " ").title())
        fv = f_entry.get("field_value", "")
        gt_label = f_entry.get("necessity_label", "contextual")

        span = f_entry.get("span", {})
        start, end = span.get("start", 0), span.get("end", 0)
        context_str = extract_context_window(text_content, start, end)

        n_score, r_score, m_score, pred_label, reason_str = hybrid_evaluator.score_field(
            field_type=ft,
            document_type=doc_type,
            context_text=context_str,
            field_value=str(fv),
        )

        flagged = bool(n_score < unnecessary_threshold)
        if flagged:
            total_unnecessary_flagged += 1

        field_audits.append({
            "field_type": ft,
            "field_name": fn,
            "field_value": str(fv),
            "ground_truth_label": gt_label,
            "hybrid_score_N": n_score,
            "rule_score_R": r_score,
            "ml_score_M": m_score,
            "predicted_label": pred_label,
            "flagged_unnecessary": flagged,
            "reasoning": reason_str,
        })

    report = {
        "document_id": doc_id,
        "document_type": doc_type,
        "document_purpose": gt_data.get("document_purpose", ""),
        "hybrid_alpha": hybrid_evaluator.alpha,
        "unnecessary_threshold": unnecessary_threshold,
        "total_fields": len(field_audits),
        "total_unnecessary_flagged": total_unnecessary_flagged,
        "fields": field_audits,
    }
    return report


def render_report_markdown(report: Dict[str, Any]) -> str:
    """Renders structured report dictionary as formatted Markdown."""
    doc_id = report["document_id"]
    doc_type = report["document_type"]
    alpha = report["hybrid_alpha"]
    th = report["unnecessary_threshold"]

    md = []
    md.append(f"# PII Necessity Audit Report: `{doc_id}`")
    md.append(f"**Domain:** `{doc_type}` | **Alpha:** `{alpha}` | **Flagging Threshold:** `< {th}`\n")
    md.append(f"> **Document Purpose:** {report['document_purpose']}\n")
    md.append(f"**Summary:** Flagged **{report['total_unnecessary_flagged']} / {report['total_fields']}** fields as **Unnecessary PII Exposure**.\n")

    md.append("| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |")
    md.append("| :--- | :--- | :---: | :---: | :---: | :--- | :--- |")

    for f in report["fields"]:
        fn = f["field_name"]
        val = f["field_value"].replace("\n", " ")[:35]
        r = f["rule_score_R"]
        m = f["ml_score_M"]
        n = f["hybrid_score_N"]
        flagged_tag = "🔴 **FLAGGED**" if f["flagged_unnecessary"] else ("🟡 CONTEXTUAL" if n < 0.67 else "🟢 NECESSARY")
        reason = f["reasoning"]

        md.append(f"| **{fn}** | `{val}` | {r:.2f} | {m:.2f} | **{n:.2f}** | {flagged_tag} | {reason} |")

    return "\n".join(md)


def generate_and_save_sample_reports(
    dataset_dir: Union[str, Path],
    results_dir: Union[str, Path],
    hybrid_evaluator: HybridNecessityEvaluator,
    sample_doc_ids: Optional[List[str]] = None,
) -> Tuple[List[Path], Path]:
    """Generates 2 sample reports per domain (8 total) and saves JSON and Markdown artifacts."""
    if sample_doc_ids is None:
        sample_doc_ids = [
            "job_001", "job_002",
            "med_001", "med_002",
            "loan_001", "loan_002",
            "rent_001", "rent_002",
        ]

    out_dir = Path(results_dir) / "necessity_reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    combined_md = ["# Sample Necessity Classification Audit Reports (8 Representative Documents)\n"]

    for doc_id in sample_doc_ids:
        report = generate_necessity_report(doc_id, dataset_dir, hybrid_evaluator)

        # 1. Save individual JSON
        json_path = out_dir / f"{doc_id}_necessity_report.json"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(report, jf, indent=2)

        # 2. Save individual Markdown
        md_text = render_report_markdown(report)
        md_path = out_dir / f"{doc_id}_necessity_report.md"
        md_path.write_text(md_text, encoding="utf-8")

        saved_files.append(md_path)
        combined_md.append(md_text + "\n---\n")

    combined_md_path = out_dir / "all_sample_necessity_reports.md"
    combined_md_path.write_text("\n".join(combined_md), encoding="utf-8")

    return saved_files, combined_md_path
