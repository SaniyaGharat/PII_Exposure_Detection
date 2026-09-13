import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.necessity.hybrid import HybridNecessityEvaluator
from src.necessity.ml_classifier import extract_context_window

evaluator = HybridNecessityEvaluator()
feats_train, y_train, weights = evaluator.ml_classifier.prepare_dataset(Path('dataset'), 'train')
evaluator.ml_classifier.train(feats_train, y_train, weights)
best_alpha, _ = evaluator.tune_alpha_on_validation(Path('dataset'), 'validation')

with open('dataset/splits/test.json', 'r', encoding='utf-8') as f:
    test_docs = json.load(f)['documents']

dataset_path = Path('dataset')
pred_path = Path('results/predictions')

print("=" * 90)
print("3-TIER END-TO-END PIPELINE EVALUATION (CLEAN & OCR STREAMS)")
print("=" * 90)

for modality in ['clean', 'ocr']:
    mod_dir = pred_path / modality
    if not mod_dir.exists():
        continue
        
    total_gt_unnecessary = 0
    det_miss = 0
    
    # Bins for detected unnecessary fields
    bin_under_035 = 0          # Tier 1: Confidently Unnecessary (Automated Minimization)
    bin_035_to_050 = 0         # Tier 2a: Unnecessary in Review Band
    bin_050_to_065 = 0         # Tier 2b: Missed in binary, but routed to Human Review
    bin_over_065 = 0           # Tier 3: Confidently Necessary (Hard Miss / Silent Failure)
    
    # Field type breakdowns
    ft_breakdown = defaultdict(lambda: {
        'total': 0, 'det_miss': 0,
        'n_under_035': 0, 'n_035_050': 0, 'n_050_065': 0, 'n_over_065': 0,
        'scores': []
    })
    
    for doc_item in test_docs:
        doc_id = doc_item['document_id']
        doc_type = doc_item['document_type']
        
        pred_file = mod_dir / f'{doc_id}.json'
        gt_file = dataset_path / doc_type / 'labels' / f'{doc_id}.json'
        text_file = dataset_path / doc_type / 'text' / f'{doc_id}.txt'
        
        if not (pred_file.exists() and gt_file.exists() and text_file.exists()):
            continue
            
        with open(pred_file, 'r', encoding='utf-8') as pf:
            preds = json.load(pf).get('predictions', [])
        with open(gt_file, 'r', encoding='utf-8') as gf:
            gt_doc = json.load(gf)
        text_content = text_file.read_text(encoding='utf-8')
        
        det_map = {}
        for p in preds:
            ft = p['field_type']
            det_map.setdefault(ft, []).append(p)
            
        for g in gt_doc.get('fields', []):
            ft = g['field_type']
            fv = str(g['field_value'])
            is_unnec = (g['necessity_label'].lower() == 'unnecessary')
            if not is_unnec:
                continue
                
            total_gt_unnecessary += 1
            ft_breakdown[ft]['total'] += 1
            span = g.get('span', {})
            s, e = span.get('start', 0), span.get('end', 0)
            
            # Match candidate with overlap-based logic
            candidates = det_map.get(ft, [])
            best_match = None
            best_overlap = -1
            best_dist = float('inf')
            
            for cand in candidates:
                p_span = cand.get('predicted_span', [0, 0])
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
                        
            if best_overlap == 0:
                for cand in candidates:
                    p_span = cand.get('predicted_span', [0, 0])
                    ps, pe = p_span[0], p_span[1]
                    dist = abs((s + e) / 2.0 - (ps + pe) / 2.0)
                    if dist < best_dist:
                        best_dist = dist
                        best_match = cand
                        
            if best_match is not None:
                p_span = best_match.get('predicted_span', [0, 0])
                p_text = best_match.get('predicted_text', '')
                det_ctx = (
                    extract_context_window(text_content, p_span[0], p_span[1])
                    if p_span[1] > 0
                    else extract_context_window(text_content, s, e)
                )
                
                n_score, r_score, m_score, _, _ = evaluator.score_field(
                    field_type=ft,
                    document_type=doc_type,
                    context_text=det_ctx,
                    field_value=p_text,
                )
                
                ft_breakdown[ft]['scores'].append(n_score)
                
                if n_score < 0.35:
                    bin_under_035 += 1
                    ft_breakdown[ft]['n_under_035'] += 1
                elif n_score < 0.50:
                    bin_035_to_050 += 1
                    ft_breakdown[ft]['n_035_050'] += 1
                elif n_score <= 0.65:
                    bin_050_to_065 += 1
                    ft_breakdown[ft]['n_050_065'] += 1
                else:
                    bin_over_065 += 1
                    ft_breakdown[ft]['n_over_065'] += 1
            else:
                det_miss += 1
                ft_breakdown[ft]['det_miss'] += 1

    binary_caught = bin_under_035 + bin_035_to_050
    binary_class_miss = bin_050_to_065 + bin_over_065
    
    print(f"\n--- MODALITY: {modality.upper()} STREAM ---")
    print(f"Total Ground-Truth Unnecessary Instances: {total_gt_unnecessary}")
    print(f"\n1. STANDARD BINARY EVALUATION (Threshold = 0.50):")
    print(f"   - Binary Caught (N < 0.50):         {binary_caught:>3} / {total_gt_unnecessary} ({binary_caught/total_gt_unnecessary*100:.2f}%)")
    print(f"   - Binary Class Miss (N >= 0.50):    {binary_class_miss:>3} / {total_gt_unnecessary} ({binary_class_miss/total_gt_unnecessary*100:.2f}%)")
    print(f"   - Detection Miss (Undetected):      {det_miss:>3} / {total_gt_unnecessary} ({det_miss/total_gt_unnecessary*100:.2f}%)")
    
    print(f"\n2. DISSECTION OF BINARY 'CLASSIFICATION MISSES' ({binary_class_miss} instances):")
    print(f"   - [REVIEW BAND]  0.50 <= N <= 0.65 (Routed to Human Review):  {bin_050_to_065:>3} / {binary_class_miss} ({bin_050_to_065/binary_class_miss*100:.2f}% of misses | {bin_050_to_065/total_gt_unnecessary*100:.2f}% of total GT)")
    print(f"   - [HARD ERROR]   N > 0.65 (Confidently Wrong as Necessary):   {bin_over_065:>3} / {binary_class_miss} ({bin_over_065/binary_class_miss*100:.2f}% of misses | {bin_over_065/total_gt_unnecessary*100:.2f}% of total GT)")
    
    print(f"\n3. COMPLETE 3-TIER OPERATIONAL OUTCOMES:")
    print(f"   [Tier 1] Confident Automated Catch (N < 0.35):       {bin_under_035:>3} ({bin_under_035/total_gt_unnecessary*100:.2f}%)")
    print(f"   [Tier 2] Routed to Human Review (0.35 <= N <= 0.65): {bin_035_to_050 + bin_050_to_065:>3} ({(bin_035_to_050 + bin_050_to_065)/total_gt_unnecessary*100:.2f}%)")
    print(f"            * of which N < 0.50 (review-lean unnecessary):   {bin_035_to_050:>3} ({bin_035_to_050/total_gt_unnecessary*100:.2f}%)")
    print(f"            * of which N >= 0.50 (review-lean contextual):   {bin_050_to_065:>3} ({bin_050_to_065/total_gt_unnecessary*100:.2f}%)")
    print(f"   [Tier 3] Confidently Missed (N > 0.65):               {bin_over_065:>3} ({bin_over_065/total_gt_unnecessary*100:.2f}%)")
    print(f"   [DetMiss] Undetected Upstream:                        {det_miss:>3} ({det_miss/total_gt_unnecessary*100:.2f}%)")
    
    total_safe = bin_under_035 + bin_035_to_050 + bin_050_to_065
    silent_failures = bin_over_065 + det_miss
    print(f"\n   -> EFFECTIVE SAFETY COVERAGE (Auto Catch + Human Review): {total_safe:>3} / {total_gt_unnecessary} ({total_safe/total_gt_unnecessary*100:.2f}%)")
    print(f"   -> TRUE SILENT FAILURES (Hard Misclass + Undetected):      {silent_failures:>3} / {total_gt_unnecessary} ({silent_failures/total_gt_unnecessary*100:.2f}%)")
    
    print(f"\n4. PER-FIELD 3-TIER BREAKDOWN ({modality.upper()}):")
    print(f"{'Field Type':<24} | {'Total':<6} | {'N<0.35':<8} | {'0.35-0.50':<10} | {'0.50-0.65':<10} | {'N>0.65':<8} | {'DetMiss':<8}")
    print("-" * 88)
    for ft, st in sorted(ft_breakdown.items()):
        print(f"{ft:<24} | {st['total']:<6} | {st['n_under_035']:<8} | {st['n_035_050']:<10} | {st['n_050_065']:<10} | {st['n_over_065']:<8} | {st['det_miss']:<8}")
