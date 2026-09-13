import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
from collections import defaultdict
from src.necessity.hybrid import HybridNecessityEvaluator
from src.policies.necessity_policy import AFFECTED_FIELDS

evaluator = HybridNecessityEvaluator(model_type="random_forest")
evaluator.fit_ml("dataset", "train")
evaluator.tune_alpha_on_validation("dataset", "validation")

feats, y_test, _ = evaluator.ml_classifier.prepare_dataset("dataset", "test")
m_scores = evaluator.ml_classifier.predict(feats)
r_scores = [evaluator.rule_engine.evaluate(f["field_type"], f["document_type"])[0] for f in feats]

# Isolate unaffected fields
unaffected_indices = [
    i for i, f in enumerate(feats)
    if f["field_type"] not in AFFECTED_FIELDS.get(f["document_type"], [])
]

print(f"Total unaffected instances in test set: {len(unaffected_indices)}")

# Check false positives under threshold < 0.5
fp_list = []
tp_list = []
tn_list = []
fn_list = []

for idx in unaffected_indices:
    f = feats[idx]
    yt = y_test[idx]
    m_s = m_scores[idx]
    
    is_gt_unnec = (yt < 0.5)
    is_pred_unnec = (m_s < 0.5)
    
    if is_pred_unnec and not is_gt_unnec:
        fp_list.append({
            "doc_type": f["document_type"],
            "field_type": f["field_type"],
            "y_true": yt,
            "m_score": m_s,
            "field_value": f["field_value"],
        })
    elif is_pred_unnec and is_gt_unnec:
        tp_list.append(idx)
    elif not is_pred_unnec and not is_gt_unnec:
        tn_list.append(idx)
    elif not is_pred_unnec and is_gt_unnec:
        fn_list.append(idx)

print(f"TP: {len(tp_list)}, FP: {len(fp_list)}, TN: {len(tn_list)}, FN: {len(fn_list)}")

fp_from_contextual = [fp for fp in fp_list if fp["y_true"] == 0.5]
fp_from_necessary = [fp for fp in fp_list if fp["y_true"] == 1.0]

print(f"Total FP: {len(fp_list)}")
print(f"  - From true-label == 0.5 (Contextual): {len(fp_from_contextual)} ({len(fp_from_contextual)/len(fp_list)*100:.1f}%)")
print(f"  - From true-label == 1.0 (Necessary):  {len(fp_from_necessary)} ({len(fp_from_necessary)/len(fp_list)*100:.1f}%)")

print("\nBreakdown of FP instances from Contextual (true=0.5):")
ctx_field_counts = defaultdict(list)
for fp in fp_from_contextual:
    key = f"{fp['doc_type']}.{fp['field_type']}"
    ctx_field_counts[key].append(fp["m_score"])

for k, scores in sorted(ctx_field_counts.items()):
    min_s, max_s, avg_s = min(scores), max(scores), sum(scores)/len(scores)
    print(f"  - {k:<35}: count={len(scores):>2} | score range: [{min_s:.4f}, {max_s:.4f}] | avg: {avg_s:.4f}")

if fp_from_necessary:
    print("\nBreakdown of FP instances from Necessary (true=1.0):")
    for fp in fp_from_necessary:
        print(f"  - {fp['doc_type']}.{fp['field_type']}: score={fp['m_score']:.4f}")
else:
    print("\nBreakdown of FP instances from Necessary (true=1.0): ZERO (0) instances (0.0%)!")

# Check 3-way evaluation
print("\n=== 3-WAY THRESHOLD SCHEME ANALYSIS (N < 0.35, 0.35 <= N <= 0.65, N > 0.65) ===")
correct_3way = 0
for idx in unaffected_indices:
    yt = y_test[idx]
    m_s = m_scores[idx]
    
    true_3way = "unnecessary" if yt == 0.0 else ("contextual" if yt == 0.5 else "necessary")
    pred_3way = "unnecessary" if m_s < 0.35 else ("contextual" if m_s <= 0.65 else "necessary")
    
    if true_3way == pred_3way:
        correct_3way += 1

print(f"3-way classification accuracy on unaffected fields: {correct_3way} / {len(unaffected_indices)} ({correct_3way/len(unaffected_indices)*100:.2f}%)")

# Check binary precision when threshold < 0.35 (strict unnecessary cutoff)
tp_35 = sum(1 for idx in unaffected_indices if y_test[idx] == 0.0 and m_scores[idx] < 0.35)
fp_35 = sum(1 for idx in unaffected_indices if y_test[idx] > 0.0 and m_scores[idx] < 0.35)
fn_35 = sum(1 for idx in unaffected_indices if y_test[idx] == 0.0 and m_scores[idx] >= 0.35)

p_35 = tp_35 / (tp_35 + fp_35) if (tp_35 + fp_35) > 0 else 1.0
r_35 = tp_35 / (tp_35 + fn_35) if (tp_35 + fn_35) > 0 else 1.0
f1_35 = 2 * p_35 * r_35 / (p_35 + r_35) if (p_35 + r_35) > 0 else 0.0

print(f"Under threshold < 0.35: Precision = {p_35:.4f}, Recall = {r_35:.4f}, F1 = {f1_35:.4f} (FP count dropped from {len(fp_list)} to {fp_35})")
