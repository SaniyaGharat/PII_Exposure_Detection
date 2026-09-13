"""
PII Exposure Detection - Phase 3 Execution Pipeline
Executes Pre-flight checks, ML training, Validation Alpha Tuning,
Held-out Test Evaluation, End-to-End Pipeline Testing, and Sample Report Generation.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

# Ensure root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.necessity.hybrid import HybridNecessityEvaluator
from src.necessity.pipeline_test import run_end_to_end_evaluation
from src.necessity.report_generator import generate_and_save_sample_reports


def run_phase3_workflow(
    dataset_dir: Union[str, Path],
    results_dir: Union[str, Path],
    model_type: str = "random_forest",
) -> Dict[str, Any]:
    """
    Executes the complete Phase 3 workflow.
    """
    dataset_path = Path(dataset_dir)
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 75)
    print("  PHASE 3: NECESSITY CLASSIFICATION (RULE + ML HYBRID FRAMEWORK)")
    print("=" * 75)
    print(f"Dataset Directory: {dataset_path}")
    print(f"Results Directory: {results_path}")
    print(f"ML Model:          {model_type.replace('_', ' ').title()}")
    print("=" * 75)

    # 1. Step 0: Pre-Flight Check
    print("\n[Step 0/5] Executing Pre-Flight Class Distribution Check...")
    evaluator = HybridNecessityEvaluator(model_type=model_type)

    feats_train, y_train, weights = evaluator.ml_classifier.prepare_dataset(dataset_path, "train")
    classes, counts = np.unique(y_train, return_counts=True)
    print(f"  Training instances: {len(y_train)} across 280 documents")
    for c, cnt in zip(classes, counts):
        lbl = "unnecessary" if c == 0.0 else ("contextual" if c == 0.5 else "necessary")
        print(f"    - {lbl.upper():<12}: {cnt:>4} instances ({cnt/len(y_train)*100:.1f}%) | Weight: {weights[y_train==c][0]:.3f}")

    # 2. Step 1 & 2: ML Model Training
    print("\n[Step 1/5] Training ML Ordinal Regressor M(f, p) on Training Split (280 docs)...")
    evaluator.ml_classifier.train(feats_train, y_train, weights)
    train_metrics = evaluator.ml_classifier.evaluate_on_split(feats_train, y_train)
    print(f"  -> Training Fit: MAE = {train_metrics['mae']:.4f} | RMSE = {train_metrics['rmse']:.4f}")

    # 3. Step 3: Alpha Grid Search on Validation Split ONLY
    print("\n[Step 2/5] Tuning Alpha on Validation Split (60 docs, 810 instances)...")
    best_alpha, grid_table = evaluator.tune_alpha_on_validation(dataset_path, "validation")

    print("\n  --- VALIDATION ALPHA GRID SEARCH TABLE ---")
    print(f"  {'Alpha':<8} | {'Validation MAE':<16} | {'Validation RMSE':<16} | {'Status'}")
    print("  " + "-" * 55)
    for row in grid_table:
        is_best = "<-- OPTIMAL ALPHA" if row["alpha"] == best_alpha else ""
        print(f"  {row['alpha']:<8.2f} | {row['mae']:<16.4f} | {row['rmse']:<16.4f} | {is_best}")

    print(f"\n  -> Optimal Alpha Selected: alpha* = {best_alpha:.2f}")

    # Save Grid Search CSV
    grid_csv_path = results_path / "necessity_alpha_grid_search.csv"
    with open(grid_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["alpha", "mae", "rmse"])
        writer.writeheader()
        writer.writerows(grid_table)

    # 4. Step 4: Final Evaluation on Held-Out Test Split (60 docs, 810 instances)
    print("\n[Step 3/5] Evaluating on Held-Out Test Set (60 docs, 810 instances)...")
    test_eval = evaluator.evaluate_test_set(dataset_path, "test", unnecessary_threshold=0.5)

    print("\n" + "=" * 75)
    print("        HELD-OUT TEST SET EVALUATION REPORT (60 Documents)")
    print("=" * 75)
    print(f"{'Approach':<16} | {'MAE':<8} | {'RMSE':<8} | {'Binary Prec':<12} | {'Binary Rec':<12} | {'Binary F1':<10}")
    print("-" * 75)

    for app_name, m in test_eval["approaches"].items():
        disp_name = "Rule-Only (R)" if app_name == "rule_only" else ("ML-Only (M)" if app_name == "ml_only" else f"Hybrid (N, a={best_alpha})")
        print(f"{disp_name:<16} | {m['mae']:<8.4f} | {m['rmse']:<8.4f} | {m['binary_unnecessary_precision']:<12.4f} | {m['binary_unnecessary_recall']:<12.4f} | {m['binary_unnecessary_f1']:<10.4f}")

    print("\n--- PER-DOMAIN BREAKDOWN (Test Set MAE / Binary F1) ---")
    for dt, approaches in test_eval["per_domain"].items():
        print(f"\nDomain: {dt} (N={approaches['rule_only']['count']} instances)")
        for app_name, m in approaches.items():
            disp_name = "Rule-Only" if app_name == "rule_only" else ("ML-Only" if app_name == "ml_only" else "Hybrid")
            print(f"  {disp_name:<12}: MAE = {m['mae']:.4f} | RMSE = {m['rmse']:.4f} | Unnecessary F1 = {m['binary_f1']:.4f}")

    print("\n--- THRESHOLD SENSITIVITY (Hybrid Model) ---")
    for th_key, th_m in test_eval["threshold_sensitivity"].items():
        th_val = th_key.replace("threshold_", "")
        print(f"  Threshold < {th_val}: Precision = {th_m['precision']:.4f} | Recall = {th_m['recall']:.4f} | F1 = {th_m['f1']:.4f}")

    dis = test_eval["disagreement_analysis"]
    print("\n--- RULE vs. ML DISAGREEMENT ANALYSIS ---")
    print(f"  Total Disagreements: {dis['total_disagreements']} / {test_eval['total_test_instances']} ({dis['disagreement_rate']*100:.2f}%)")
    print(f"  Rule vs. ML Binary Confusion Matrix:\n    {dis['confusion_matrix_r_vs_m']}")
    print(f"  Accuracy when Rule & ML Disagree:")
    print(f"    - Rule-Only Accuracy:   {dis['rule_accuracy_on_disagreements']:.4f}")
    print(f"    - ML-Only Accuracy:     {dis['ml_accuracy_on_disagreements']:.4f}")
    print(f"    - Hybrid (N) Accuracy:  {dis['hybrid_accuracy_on_disagreements']:.4f}")

    # 5. Step 5: End-to-End Compounding Error Test
    print("\n[Step 4/5] Running End-to-End Compounding Error Test on Phase 2 Predictions...")
    predictions_dir = results_path / "predictions"
    e2e_results = run_end_to_end_evaluation(
        dataset_dir=dataset_path,
        predictions_dir=predictions_dir,
        hybrid_evaluator=evaluator,
        unnecessary_threshold=0.5,
    )

    print("\n" + "=" * 75)
    print("         END-TO-END SYSTEM RELIABILITY (DETECT -> CLASSIFY)")
    print("=" * 75)
    print(f"{'Document Stream':<20} | {'Docs':<6} | {'E2E Prec':<10} | {'E2E Rec':<10} | {'E2E F1':<10} | {'E2E Acc':<10}")
    print("-" * 75)

    # Compare against Oracle / Perfect Detection from Step 4
    oracle_f1 = test_eval["approaches"]["hybrid"]["binary_unnecessary_f1"]
    oracle_acc = test_eval["approaches"]["hybrid"]["binary_unnecessary_accuracy"]
    print(f"{'Oracle (GT Detection)':<20} | {'60':<6} | {test_eval['approaches']['hybrid']['binary_unnecessary_precision']:<10.4f} | {test_eval['approaches']['hybrid']['binary_unnecessary_recall']:<10.4f} | {oracle_f1:<10.4f} | {oracle_acc:<10.4f}")

    for mod, e_m in e2e_results.items():
        disp_mod = "Clean Digital Text" if mod == "clean" else "Scanned OCR Images"
        delta_f1 = e_m["end_to_end_f1"] - oracle_f1
        print(f"{disp_mod:<20} | {e_m['total_documents']:<6} | {e_m['end_to_end_precision']:<10.4f} | {e_m['end_to_end_recall']:<10.4f} | {e_m['end_to_end_f1']:<10.4f} | {e_m['end_to_end_accuracy']:<10.4f} (Delta F1={delta_f1:+.4f})")

    # 6. Step 6: Sample Necessity Reports Generation
    print("\n[Step 5/5] Generating Sample Necessity Reports (8 representative documents)...")
    saved_reports, combined_md_path = generate_and_save_sample_reports(
        dataset_dir=dataset_path,
        results_dir=results_path,
        hybrid_evaluator=evaluator,
    )
    print(f"  -> Generated {len(saved_reports)} individual audit reports and combined summary at:\n     {combined_md_path}")

    # Save full metrics JSON
    metrics_export = {
        "alpha_grid_search": grid_table,
        "optimal_alpha": best_alpha,
        "test_evaluation": test_eval,
        "end_to_end_compounding_error": e2e_results,
    }
    with open(results_path / "necessity_evaluation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_export, f, indent=2)

    print("\n" + "=" * 75)
    print("            PHASE 3 WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 75 + "\n")
    return metrics_export


import numpy as np
