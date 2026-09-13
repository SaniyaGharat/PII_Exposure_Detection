import sys
import json
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, classification_report, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.necessity.hybrid import HybridNecessityEvaluator

evaluator = HybridNecessityEvaluator()
feats_train, y_train, weights = evaluator.ml_classifier.prepare_dataset(Path('dataset'), 'train')
evaluator.ml_classifier.train(feats_train, y_train, weights)
best_alpha, _ = evaluator.tune_alpha_on_validation(Path('dataset'), 'validation')

feats_test, y_test, _ = evaluator.ml_classifier.prepare_dataset(Path('dataset'), 'test')
m_scores = evaluator.ml_classifier.predict(feats_test)
r_scores = np.array([evaluator.rule_engine.evaluate(f['field_type'], f['document_type'])[0] for f in feats_test], dtype=np.float32)
n_scores = best_alpha * r_scores + (1.0 - best_alpha) * m_scores

AFFECTED_PAIRS = {
    ('job_application', 'home_address'),
    ('medical_intake', 'home_address'),
    ('loan_application', 'marital_status'),
    ('rental_agreement', 'emergency_contact'),
}

is_affected = np.array([(f['document_type'], f['field_type']) in AFFECTED_PAIRS for f in feats_test])

def to_3tier(scores):
    res = np.zeros(len(scores), dtype=int)
    for i, s in enumerate(scores):
        if s < 0.35:
            res[i] = 0  # Unnecessary
        elif s <= 0.65:
            res[i] = 1  # Contextual / Needs Review
        else:
            res[i] = 2  # Necessary
    return res

subsets = {
    'Context-Affected Subset (Varies with Document Context)': is_affected,
    'Unaffected Subset (Static Default Rule Holds)': ~is_affected,
    'Overall Test Set (All Fields Combined)': np.ones_like(is_affected, dtype=bool),
}

approaches = {
    'Rule-Only (R)': r_scores,
    'ML-Only (M)': m_scores,
    f'Hybrid (N, a={best_alpha:.2f})': n_scores,
}

for sname, mask in subsets.items():
    print('=' * 105)
    print(f'{sname.upper()} [N = {np.sum(mask)} instances]')
    print('=' * 105)
    y_sub = y_test[mask]
    y_sub_3t = to_3tier(y_sub)
    
    counts = Counter(y_sub)
    print(f"Ground Truth Class Counts: Unnecessary(0.0)={counts.get(0.0,0)}, Contextual(0.5)={counts.get(0.5,0)}, Necessary(1.0)={counts.get(1.0,0)}")
    print('-' * 105)
    header = f"{'Approach':<20} | {'Accuracy':<8} | {'Macro Prec':<11} | {'Macro Rec':<11} | {'Macro F1':<10} | {'Unnec F1':<10} | {'Context F1':<11} | {'Nec F1':<10}"
    print(header)
    print('-' * 105)
    
    for aname, scores in approaches.items():
        s_sub = scores[mask]
        pred_3t = to_3tier(s_sub)
        
        acc = accuracy_score(y_sub_3t, pred_3t)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_sub_3t, pred_3t, average='macro', zero_division=0)
        p_per, r_per, f1_per, _ = precision_recall_fscore_support(y_sub_3t, pred_3t, labels=[0, 1, 2], zero_division=0)
        
        print(f"{aname:<20} | {acc:<8.4f} | {p_macro:<11.4f} | {r_macro:<11.4f} | {f1_macro:<10.4f} | {f1_per[0]:<10.4f} | {f1_per[1]:<11.4f} | {f1_per[2]:<10.4f}")
        
    print("\nDetailed Per-Class Breakdown (Precision / Recall / F1):")
    for aname, scores in approaches.items():
        s_sub = scores[mask]
        pred_3t = to_3tier(s_sub)
        p_per, r_per, f1_per, sup = precision_recall_fscore_support(y_sub_3t, pred_3t, labels=[0, 1, 2], zero_division=0)
        print(f"  [{aname}]")
        print(f"    - Unnecessary (N < 0.35)   : P={p_per[0]:.4f}, R={r_per[0]:.4f}, F1={f1_per[0]:.4f} (Support={sup[0]})")
        print(f"    - Contextual (0.35-0.65)   : P={p_per[1]:.4f}, R={r_per[1]:.4f}, F1={f1_per[1]:.4f} (Support={sup[1]})")
        print(f"    - Necessary (N > 0.65)     : P={p_per[2]:.4f}, R={r_per[2]:.4f}, F1={f1_per[2]:.4f} (Support={sup[2]})")
    print()
