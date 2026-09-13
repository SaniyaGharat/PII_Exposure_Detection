"""
PII Exposure Detection - Hybrid Necessity Engine
Implements N(f, p) = alpha * R(f, p) + (1 - alpha) * M(f, p).
Performs validation-only alpha grid search and final evaluation on the held-out test set.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    precision_score,
    recall_score,
    root_mean_squared_error,
)

from src.necessity.ml_classifier import MLNecessityClassifier, extract_context_window
from src.necessity.rule_engine import RuleEngine, LABEL_TO_SCORE


class HybridNecessityEvaluator:
    """Combines deterministic rule lookup R(f,p) and learned ML regression M(f,p)."""

    def __init__(self, alpha: float = 0.5, model_type: str = "random_forest"):
        self.alpha = alpha
        self.rule_engine = RuleEngine()
        self.ml_classifier = MLNecessityClassifier(model_type=model_type)

    def fit_ml(
        self,
        dataset_dir: Union[str, Path],
        train_split: str = "train",
    ) -> None:
        """Trains the internal ML component on the training split."""
        feats, y_train, weights = self.ml_classifier.prepare_dataset(dataset_dir, train_split)
        self.ml_classifier.train(feats, y_train, weights)

    def tune_alpha_on_validation(
        self,
        dataset_dir: Union[str, Path],
        val_split: str = "validation",
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Performs grid search over alpha in [0.0, 0.1, ..., 1.0] on validation set only.
        Returns optimal alpha and the full grid search table.
        """
        feats, y_val, _ = self.ml_classifier.prepare_dataset(dataset_dir, val_split)
        ml_scores = self.ml_classifier.predict(feats)

        rule_scores = np.array(
            [self.rule_engine.evaluate(f["field_type"], f["document_type"])[0] for f in feats],
            dtype=np.float32,
        )

        alphas = [round(a, 2) for a in np.linspace(0.0, 1.0, 11)]
        grid_results: List[Dict[str, Any]] = []
        best_alpha = 0.5
        best_mae = float("inf")

        for a in alphas:
            hybrid_scores = a * rule_scores + (1.0 - a) * ml_scores
            mae = float(mean_absolute_error(y_val, hybrid_scores))
            rmse = float(root_mean_squared_error(y_val, hybrid_scores))

            grid_results.append({
                "alpha": a,
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
            })

            if mae < best_mae:
                best_mae = mae
                best_alpha = a

        self.alpha = best_alpha
        return best_alpha, grid_results

    def evaluate_test_set(
        self,
        dataset_dir: Union[str, Path],
        test_split: str = "test",
        unnecessary_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Comprehensive final evaluation on the held-out test split.
        Compares Rule-Only (alpha=1.0), ML-Only (alpha=0.0), and Hybrid (alpha=best_alpha).
        """
        feats, y_test, _ = self.ml_classifier.prepare_dataset(dataset_dir, test_split)
        m_scores = self.ml_classifier.predict(feats)
        r_scores = np.array(
            [self.rule_engine.evaluate(f["field_type"], f["document_type"])[0] for f in feats],
            dtype=np.float32,
        )
        n_scores = self.alpha * r_scores + (1.0 - self.alpha) * m_scores

        # Ground truth binary: True if strictly unnecessary (target < 0.5)
        # Or threshold-based (target < unnecessary_threshold)
        y_test_binary = (y_test < unnecessary_threshold).astype(int)

        approaches = {
            "rule_only": r_scores,
            "ml_only": m_scores,
            "hybrid": n_scores,
        }

        eval_summary: Dict[str, Any] = {
            "alpha": self.alpha,
            "unnecessary_threshold": unnecessary_threshold,
            "total_test_instances": len(y_test),
            "approaches": {},
            "per_domain": {},
            "threshold_sensitivity": {},
            "disagreement_analysis": {},
        }

        # 1. Evaluate Overall Approaches
        for name, scores in approaches.items():
            mae = float(mean_absolute_error(y_test, scores))
            rmse = float(root_mean_squared_error(y_test, scores))

            pred_binary = (scores < unnecessary_threshold).astype(int)
            p = float(precision_score(y_test_binary, pred_binary, zero_division=0))
            r = float(recall_score(y_test_binary, pred_binary, zero_division=0))
            f1 = float(f1_score(y_test_binary, pred_binary, zero_division=0))
            acc = float(accuracy_score(y_test_binary, pred_binary))

            eval_summary["approaches"][name] = {
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
                "binary_unnecessary_precision": round(p, 4),
                "binary_unnecessary_recall": round(r, 4),
                "binary_unnecessary_f1": round(f1, 4),
                "binary_unnecessary_accuracy": round(acc, 4),
            }

        # 2. Per-Domain Breakdown
        doc_types = sorted(list(set(f["document_type"] for f in feats)))
        for dt in doc_types:
            indices = [i for i, f in enumerate(feats) if f["document_type"] == dt]
            dt_y = y_test[indices]
            dt_y_bin = y_test_binary[indices]

            eval_summary["per_domain"][dt] = {}
            for name, scores in approaches.items():
                dt_scores = scores[indices]
                dt_pred_bin = (dt_scores < unnecessary_threshold).astype(int)

                eval_summary["per_domain"][dt][name] = {
                    "count": len(indices),
                    "mae": round(float(mean_absolute_error(dt_y, dt_scores)), 4),
                    "rmse": round(float(root_mean_squared_error(dt_y, dt_scores)), 4),
                    "binary_f1": round(float(f1_score(dt_y_bin, dt_pred_bin, zero_division=0)), 4),
                }

        # 3. Threshold Sensitivity Analysis
        for th in [0.25, 0.50, 0.75]:
            th_gt_bin = (y_test < th).astype(int)
            th_hybrid_bin = (n_scores < th).astype(int)
            eval_summary["threshold_sensitivity"][f"threshold_{th}"] = {
                "precision": round(float(precision_score(th_gt_bin, th_hybrid_bin, zero_division=0)), 4),
                "recall": round(float(recall_score(th_gt_bin, th_hybrid_bin, zero_division=0)), 4),
                "f1": round(float(f1_score(th_gt_bin, th_hybrid_bin, zero_division=0)), 4),
            }

        # 4. Disagreement Analysis between Rule-Only and ML-Only
        r_bin = (r_scores < unnecessary_threshold).astype(int)
        m_bin = (m_scores < unnecessary_threshold).astype(int)
        disagreements_mask = (r_bin != m_bin)

        disagree_count = int(np.sum(disagreements_mask))
        eval_summary["disagreement_analysis"] = {
            "total_disagreements": disagree_count,
            "disagreement_rate": round(disagree_count / len(y_test), 4),
            "confusion_matrix_r_vs_m": confusion_matrix(r_bin, m_bin).tolist(),
            "rule_accuracy_on_disagreements": round(float(accuracy_score(y_test_binary[disagreements_mask], r_bin[disagreements_mask])), 4) if disagree_count > 0 else 0.0,
            "ml_accuracy_on_disagreements": round(float(accuracy_score(y_test_binary[disagreements_mask], m_bin[disagreements_mask])), 4) if disagree_count > 0 else 0.0,
            "hybrid_accuracy_on_disagreements": round(float(accuracy_score(y_test_binary[disagreements_mask], (n_scores[disagreements_mask] < unnecessary_threshold).astype(int))), 4) if disagree_count > 0 else 0.0,
        }

        return eval_summary

    def score_field(
        self,
        field_type: str,
        document_type: str,
        context_text: str = "",
        field_value: str = "",
    ) -> Tuple[float, float, float, str, str]:
        """
        Scores a single field instance.

        Returns:
            Tuple of (hybrid_score N, rule_score R, ml_score M, label, explanation_string).
        """
        r_score, r_label, r_reason = self.rule_engine.evaluate(field_type, document_type)

        if self.ml_classifier.is_trained:
            m_score = float(self.ml_classifier.predict([{
                "field_type": field_type,
                "document_type": document_type,
                "context_text": context_text,
                "field_value": field_value,
            }])[0])
        else:
            m_score = r_score

        n_score = self.alpha * r_score + (1.0 - self.alpha) * m_score

        # Determine driver for explanation
        if self.alpha >= 0.5:
            reason_str = r_reason
        else:
            confidence = round(abs(m_score - 0.5) * 200, 1)
            reason_str = f"Flagged by learned contextual pattern (Model Confidence: {confidence}%)."

        label = "unnecessary" if n_score < 0.33 else ("contextual" if n_score < 0.67 else "necessary")
        return round(n_score, 4), round(r_score, 4), round(m_score, 4), label, reason_str
