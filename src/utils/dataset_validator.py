"""
PII Exposure Detection - Dataset Validator
Performs rigorous structural, semantic, and span-level integrity checks on the dataset.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Union

from src.policies.necessity_policy import DOCUMENT_POLICIES, validate_necessity_label


@dataclass
class ValidationReport:
    """Stores the aggregated results and error logs of the dataset validation."""
    total_documents: int = 0
    type_counts: Dict[str, int] = field(default_factory=dict)
    text_count: int = 0
    pdf_count: int = 0
    scanned_count: int = 0
    label_count: int = 0
    train_count: int = 0
    validation_count: int = 0
    test_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    passed: bool = False

    def print_summary(self) -> None:
        """Prints a clean, formatted validation summary."""
        print("\n" + "=" * 45)
        print("         DATASET VALIDATION REPORT")
        print("=" * 45)

        for doc_type, count in self.type_counts.items():
            display_name = DOCUMENT_POLICIES.get(doc_type).display_name if doc_type in DOCUMENT_POLICIES else doc_type
            print(f"{display_name}: {count}")

        print(f"\nTotal Documents: {self.total_documents}")
        print("-" * 45)
        print(f"Text Files:    {self.text_count}")
        print(f"PDF Files:     {self.pdf_count}")
        print(f"Scanned Files: {self.scanned_count}")
        print(f"Label Files:   {self.label_count}")
        print("-" * 45)
        print(f"Train:         {self.train_count}")
        print(f"Validation:    {self.validation_count}")
        print(f"Test:          {self.test_count}")
        print("=" * 45)

        if self.errors:
            print("\n[VALIDATION ERRORS ENCOUNTERED]")
            for err in self.errors[:20]:  # Cap display to top 20
                print(f"  ❌ {err}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors.")

        if self.warnings:
            print("\n[VALIDATION WARNINGS]")
            for warn in self.warnings[:10]:
                print(f"  ⚠️  {warn}")

        status_str = "PASSED" if self.passed else "FAILED"
        print(f"\nValidation Status: {status_str}")
        print("=" * 45 + "\n")


def validate_dataset(dataset_root: Optional[Union[str, Path]] = None) -> ValidationReport:
    """
    Executes all 10 integrity checks on the generated dataset:
    1. Every text document has a label file.
    2. Every PDF has a corresponding text document.
    3. Every label file references an existing text document.
    4. Field values exist inside the text document.
    5. Span locations are exact (text[start:end] == field_value).
    6. Necessity labels are valid ('necessary', 'contextual', 'unnecessary').
    7. No document IDs are duplicated.
    8. Train/validation/test splits do not overlap.
    9. Every document type is represented in every split.
    10. File counts match and are reported clearly.

    Args:
        dataset_root: Path to dataset directory (defaults to ./dataset relative to workspace).

    Returns:
        ValidationReport object.
    """
    if dataset_root is None:
        dataset_root = Path(__file__).resolve().parent.parent.parent / "dataset"
    else:
        dataset_root = Path(dataset_root)

    report = ValidationReport()

    if not dataset_root.exists():
        report.errors.append(f"Dataset root directory not found: {dataset_root}")
        report.passed = False
        return report

    doc_types = list(DOCUMENT_POLICIES.keys())
    all_doc_ids: Set[str] = set()
    total_docs_count = 0

    for dt in doc_types:
        dt_dir = dataset_root / dt
        if not dt_dir.exists():
            report.warnings.append(f"Directory missing for document type: {dt}")
            report.type_counts[dt] = 0
            continue

        text_dir = dt_dir / "text"
        pdf_dir = dt_dir / "pdf"
        scanned_dir = dt_dir / "scanned"
        labels_dir = dt_dir / "labels"

        text_files = {p.stem: p for p in text_dir.glob("*.txt")} if text_dir.exists() else {}
        pdf_files = {p.stem: p for p in pdf_dir.glob("*.pdf")} if pdf_dir.exists() else {}
        scanned_files = {p.stem: p for p in scanned_dir.glob("*.png")} if scanned_dir.exists() else {}
        label_files = {p.stem: p for p in labels_dir.glob("*.json")} if labels_dir.exists() else {}

        report.type_counts[dt] = len(text_files)
        total_docs_count += len(text_files)
        report.text_count += len(text_files)
        report.pdf_count += len(pdf_files)
        report.scanned_count += len(scanned_files)
        report.label_count += len(label_files)

        # Check 1: Every text document has a label file
        for doc_id in text_files:
            if doc_id not in label_files:
                report.errors.append(f"Missing label file for text document: {dt}/text/{doc_id}.txt")
            if doc_id not in pdf_files:
                report.errors.append(f"Missing PDF file for text document: {dt}/text/{doc_id}.txt")

        # Check 2: Every PDF has a corresponding text document
        for doc_id in pdf_files:
            if doc_id not in text_files:
                report.errors.append(f"Orphan PDF without corresponding text document: {dt}/pdf/{doc_id}.pdf")

        # Check 3, 4, 5, 6, 7: Label contents, spans, and duplicate IDs
        for doc_id, label_path in label_files.items():
            if doc_id in all_doc_ids:
                report.errors.append(f"Duplicate document ID detected across dataset: {doc_id}")
            all_doc_ids.add(doc_id)

            if doc_id not in text_files:
                report.errors.append(f"Label file {label_path.name} references non-existent text document")
                continue

            # Read text and label
            text_content = text_files[doc_id].read_text(encoding="utf-8")
            try:
                with open(label_path, "r", encoding="utf-8") as f:
                    label_data = json.load(f)
            except Exception as e:
                report.errors.append(f"Invalid JSON in {label_path}: {e}")
                continue

            # Validate label metadata
            if label_data.get("document_id") != doc_id:
                report.errors.append(f"Document ID mismatch in {label_path.name}: expected {doc_id}, found {label_data.get('document_id')}")

            if label_data.get("document_type") != dt:
                report.errors.append(f"Document type mismatch in {label_path.name}: expected {dt}, found {label_data.get('document_type')}")

            # Validate each field
            fields = label_data.get("fields", [])
            for field_entry in fields:
                field_type = field_entry.get("field_type")
                field_val = field_entry.get("field_value")
                nec_label = field_entry.get("necessity_label")
                span = field_entry.get("span")

                # Check 6: Valid necessity label
                if not validate_necessity_label(nec_label):
                    report.errors.append(f"Invalid necessity label '{nec_label}' for field '{field_type}' in {label_path.name}")

                # Check 4 & 5: Field value exists and span is exact
                if field_val not in text_content:
                    report.errors.append(f"Field value '{field_val}' for '{field_type}' not found in text: {doc_id}")

                if span:
                    start, end = span.get("start"), span.get("end")
                    if start is None or end is None or start < 0 or end > len(text_content):
                        report.errors.append(f"Invalid span bounds [{start}, {end}] in {label_path.name} for {field_type}")
                    else:
                        extracted = text_content[start:end]
                        if extracted != field_val:
                            report.errors.append(
                                f"Span mismatch in {label_path.name} for '{field_type}': "
                                f"expected '{field_val}', extracted '{extracted}' at [{start}:{end}]"
                            )

    report.total_documents = total_docs_count

    # Check 8 & 9: Dataset Splits
    splits_dir = dataset_root / "splits"
    if not splits_dir.exists():
        report.errors.append(f"Splits directory missing: {splits_dir}")
    else:
        split_sets = {}
        for split_name in ["train", "validation", "test"]:
            split_file = splits_dir / f"{split_name}.json"
            if not split_file.exists():
                report.errors.append(f"Split file missing: {split_file.name}")
                continue

            try:
                with open(split_file, "r", encoding="utf-8") as sf:
                    split_data = json.load(sf)
                    split_ids = {item["document_id"] for item in split_data.get("documents", [])}
                    split_types = {item["document_type"] for item in split_data.get("documents", [])}
                    split_sets[split_name] = split_ids

                    if split_name == "train":
                        report.train_count = len(split_ids)
                    elif split_name == "validation":
                        report.validation_count = len(split_ids)
                    elif split_name == "test":
                        report.test_count = len(split_ids)

                    # Check 9: Every doc type represented in split
                    for dt in doc_types:
                        if dt not in split_types and report.type_counts.get(dt, 0) > 0:
                            report.errors.append(f"Document type '{dt}' missing from {split_name} split")
            except Exception as e:
                report.errors.append(f"Error reading split file {split_file.name}: {e}")

        # Check 8: No overlap between train, val, test
        if "train" in split_sets and "validation" in split_sets and "test" in split_sets:
            train_val_overlap = split_sets["train"].intersection(split_sets["validation"])
            train_test_overlap = split_sets["train"].intersection(split_sets["test"])
            val_test_overlap = split_sets["validation"].intersection(split_sets["test"])

            if train_val_overlap:
                report.errors.append(f"Overlap between Train and Validation splits: {train_val_overlap}")
            if train_test_overlap:
                report.errors.append(f"Overlap between Train and Test splits: {train_test_overlap}")
            if val_test_overlap:
                report.errors.append(f"Overlap between Validation and Test splits: {val_test_overlap}")

            total_split_docs = len(split_sets["train"]) + len(split_sets["validation"]) + len(split_sets["test"])
            if total_split_docs != report.total_documents:
                report.warnings.append(
                    f"Total split documents ({total_split_docs}) does not match total generated documents ({report.total_documents})"
                )

    report.passed = (len(report.errors) == 0)
    return report
