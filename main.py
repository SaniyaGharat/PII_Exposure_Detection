"""
PII Exposure Detection - Main CLI Entry Point
An Intelligent Blockchain-Assisted Framework for Detecting Unnecessary PII Exposure in Document Sharing
Supports:
  - Phase 1: Dataset Generation, Splitting & Validation
  - Phase 2: PII Detection (Presidio + OCR) & Multi-Strategy Evaluation
  - Phase 3: Necessity Classification (Rule + ML Hybrid Engine)
"""

import argparse
import shutil
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generator.generate_documents import generate_full_dataset, split_dataset
from src.utils.dataset_validator import validate_dataset
from src.detection.detect import run_detection_pipeline
from src.detection.evaluate import run_evaluation_pipeline
from src.necessity.run_phase3 import run_phase3_workflow
from src.necessity.report_generator import generate_necessity_report, render_report_markdown
from src.necessity.hybrid import HybridNecessityEvaluator


def clean_dataset(dataset_dir: Path, results_dir: Path) -> None:
    """Removes existing generated dataset and prediction results directories."""
    if dataset_dir.exists():
        print(f"Cleaning dataset at: {dataset_dir} ...")
        shutil.rmtree(dataset_dir)
        print("Dataset directory cleaned successfully.")
    if results_dir.exists():
        print(f"Cleaning results at: {results_dir} ...")
        shutil.rmtree(results_dir)
        print("Results directory cleaned successfully.")


def run_phase1_pipeline(
    dataset_dir: Path,
    count_per_type: int = 100,
    scanned_ratio: float = 0.25,
    seed: int = 42,
    clean_first: bool = False,
) -> bool:
    """Executes Phase 1: synthetic dataset generation, splitting, and validation."""
    print("\n" + "=" * 65)
    print("  PHASE 1: SYNTHETIC DATASET PREPARATION & POLICY LABELING")
    print("=" * 65)
    print(f"Target Directory:    {dataset_dir}")
    print(f"Documents Per Type:  {count_per_type} (Total: {count_per_type * 4})")
    print(f"Scanned Ratio:       {scanned_ratio * 100:.0f}% (~{int(count_per_type * 4 * scanned_ratio)} files)")
    print(f"Reproducibility Seed:{seed}")
    print("=" * 65)

    if clean_first and dataset_dir.exists():
        shutil.rmtree(dataset_dir)

    print("\n[Step 1/3] Generating synthetic documents (Text, PDF, Scanned, JSON Labels)...")
    stats = generate_full_dataset(
        dataset_dir=dataset_dir,
        count_per_type=count_per_type,
        scanned_ratio=scanned_ratio,
        seed=seed,
    )
    print(f" -> Generated {stats['text_count']} text files, {stats['pdf_count']} PDFs, "
          f"{stats['scanned_count']} scanned images, {stats['label_count']} JSON labels.")

    print("\n[Step 2/3] Performing stratified train/validation/test split (70% / 15% / 15%)...")
    splits = split_dataset(
        dataset_dir=dataset_dir,
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15,
        seed=seed,
    )
    print(f" -> Split created: Train={splits['train']}, Validation={splits['validation']}, Test={splits['test']}.")

    print("\n[Step 3/3] Validating dataset integrity...")
    report = validate_dataset(dataset_dir)
    report.print_summary()

    return report.passed


def run_phase2_pipeline(
    dataset_dir: Path,
    results_dir: Path,
    process_ocr: bool = True,
    score_threshold: float = 0.4,
) -> bool:
    """Executes Phase 2: Microsoft Presidio detection and multi-strategy evaluation."""
    print("\n" + "=" * 65)
    print("  PHASE 2: PII DETECTION & MULTI-STRATEGY EVALUATION")
    print("=" * 65)

    predictions_dir = results_dir / "predictions"

    # 1. Detection
    print("\n[Step 1/2] Executing PII Detection Pipeline (Clean Text + Scanned OCR)...")
    run_detection_pipeline(
        dataset_dir=dataset_dir,
        output_dir=predictions_dir,
        process_ocr=process_ocr,
        score_threshold=score_threshold,
    )

    # 2. Evaluation
    print("\n[Step 2/2] Running Multi-Strategy Evaluation Suite...")
    eval_results = run_evaluation_pipeline(
        dataset_dir=dataset_dir,
        predictions_dir=predictions_dir,
        results_dir=results_dir,
    )

    return "clean" in eval_results and "error" not in eval_results["clean"]


def run_phase3_pipeline(
    dataset_dir: Path,
    results_dir: Path,
    model_type: str = "random_forest",
) -> bool:
    """Executes Phase 3: Rule + ML Hybrid necessity classification and evaluation."""
    res = run_phase3_workflow(
        dataset_dir=dataset_dir,
        results_dir=results_dir,
        model_type=model_type,
    )
    return "test_evaluation" in res


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PII Exposure Detection Research Framework (Phases 1, 2, and 3)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Dataset Preparation arguments (Phase 1)
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of documents to generate per category for Phase 1",
    )
    parser.add_argument(
        "--scanned-ratio",
        type=float,
        default=0.25,
        help="Proportion of documents with simulated scanned versions",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic generation and splitting",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing dataset/results before running",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run integrity validation on existing dataset",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Run Phase 1 synthetic dataset generation",
    )

    # Detection & Evaluation arguments (Phase 2)
    parser.add_argument(
        "--detect",
        action="store_true",
        help="Run Phase 2 PII detection on dataset documents",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run Phase 2 multi-strategy PII evaluation",
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Skip OCR processing on scanned documents during detection",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.4,
        help="Confidence threshold for Presidio detection",
    )

    # Necessity Classification arguments (Phase 3)
    parser.add_argument(
        "--necessity",
        action="store_true",
        help="Run Phase 3 Necessity Classification (Rule + ML Hybrid)",
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="random_forest",
        choices=["random_forest", "ridge"],
        help="ML model type for necessity component M(f,p)",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Generate a necessity audit report for a single document ID (e.g. 'job_001')",
    )

    # End-to-End full workflow
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run full end-to-end pipeline (Phase 1 + Phase 2 + Phase 3)",
    )

    args = parser.parse_args()
    dataset_dir = PROJECT_ROOT / "dataset"
    results_dir = PROJECT_ROOT / "results"

    if args.clean and not (args.generate or args.detect or args.evaluate or args.necessity or args.run_all):
        clean_dataset(dataset_dir, results_dir)
        sys.exit(0)

    if args.validate:
        print(f"\nValidating dataset at: {dataset_dir} ...")
        report = validate_dataset(dataset_dir)
        report.print_summary()
        sys.exit(0 if report.passed else 1)

    if args.report:
        evaluator = HybridNecessityEvaluator(model_type=args.model_type)
        evaluator.fit_ml(dataset_dir, "train")
        evaluator.tune_alpha_on_validation(dataset_dir, "validation")
        rep = generate_necessity_report(args.report, dataset_dir, evaluator)
        print(render_report_markdown(rep))
        sys.exit(0)

    if args.generate:
        success = run_phase1_pipeline(
            dataset_dir=dataset_dir,
            count_per_type=args.count,
            scanned_ratio=args.scanned_ratio,
            seed=args.seed,
            clean_first=args.clean,
        )
        sys.exit(0 if success else 1)

    if args.detect and not args.evaluate:
        predictions_dir = results_dir / "predictions"
        run_detection_pipeline(
            dataset_dir=dataset_dir,
            output_dir=predictions_dir,
            process_ocr=not args.no_ocr,
            score_threshold=args.threshold,
        )
        sys.exit(0)

    if args.evaluate and not args.detect:
        predictions_dir = results_dir / "predictions"
        eval_results = run_evaluation_pipeline(
            dataset_dir=dataset_dir,
            predictions_dir=predictions_dir,
            results_dir=results_dir,
        )
        sys.exit(0)

    if args.necessity:
        p3_success = run_phase3_pipeline(
            dataset_dir=dataset_dir,
            results_dir=results_dir,
            model_type=args.model_type,
        )
        sys.exit(0 if p3_success else 1)

    if args.run_all:
        p1_success = run_phase1_pipeline(
            dataset_dir=dataset_dir,
            count_per_type=args.count,
            scanned_ratio=args.scanned_ratio,
            seed=args.seed,
            clean_first=args.clean,
        )
        if not p1_success:
            print("Phase 1 failed. Aborting.")
            sys.exit(1)

        p2_success = run_phase2_pipeline(
            dataset_dir=dataset_dir,
            results_dir=results_dir,
            process_ocr=not args.no_ocr,
            score_threshold=args.threshold,
        )
        if not p2_success:
            print("Phase 2 failed. Aborting.")
            sys.exit(1)

        p3_success = run_phase3_pipeline(
            dataset_dir=dataset_dir,
            results_dir=results_dir,
            model_type=args.model_type,
        )
        sys.exit(0 if p3_success else 1)

    # Default action if run without explicit flags: Run Phase 3
    if dataset_dir.exists():
        p3_success = run_phase3_pipeline(
            dataset_dir=dataset_dir,
            results_dir=results_dir,
            model_type=args.model_type,
        )
        sys.exit(0 if p3_success else 1)
    else:
        print("Dataset not found. Running full pipeline from scratch...")
        p1_success = run_phase1_pipeline(dataset_dir=dataset_dir, count_per_type=args.count, seed=args.seed)
        if p1_success:
            run_phase2_pipeline(dataset_dir=dataset_dir, results_dir=results_dir, process_ocr=not args.no_ocr)
            run_phase3_pipeline(dataset_dir=dataset_dir, results_dir=results_dir, model_type=args.model_type)


if __name__ == "__main__":
    main()
