import json
import sys
from pathlib import Path
from difflib import SequenceMatcher
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
evaluator.tune_alpha_on_validation(Path('dataset'), 'validation')

with open('dataset/splits/test.json') as f:
    test_docs = json.load(f)['documents']

dataset_path = Path('dataset')
pred_path = Path('results/predictions')

print("=" * 80)
print("INVESTIGATING SPAN PAIRING AND CLASSIFICATION MISSES")
print("=" * 80)

for modality in ['clean', 'ocr']:
    print(f"\n--- MODALITY: {modality.upper()} ---")
    
    # Trackers for OLD naive pairing
    old_caught = 0
    old_det_miss = 0
    old_class_miss = 0
    old_class_miss_list = []
    
    # Trackers for NEW span-overlap / closest-distance pairing
    new_caught = 0
    new_det_miss = 0
    new_class_miss = 0
    new_class_miss_list = []
    
    # Field type breakdown
    ft_stats = defaultdict(lambda: {
        'gt_unnec': 0,
        'old_caught': 0, 'old_det_miss': 0, 'old_class_miss': 0,
        'new_caught': 0, 'new_det_miss': 0, 'new_class_miss': 0,
    })

    for doc_item in test_docs:
        doc_id = doc_item['document_id']
        doc_type = doc_item['document_type']
        
        pred_file = pred_path / modality / f'{doc_id}.json'
        gt_file = dataset_path / doc_type / 'labels' / f'{doc_id}.json'
        text_file = dataset_path / doc_type / 'text' / f'{doc_id}.txt'
        
        if not (pred_file.exists() and gt_file.exists() and text_file.exists()):
            continue
            
        with open(pred_file, encoding='utf-8') as pf:
            preds = json.load(pf).get('predictions', [])
        with open(gt_file, encoding='utf-8') as gf:
            gt_doc = json.load(gf)
        text_content = text_file.read_text(encoding='utf-8')
        
        det_map = {}
        for p in preds:
            ft = p['field_type']
            det_map.setdefault(ft, []).append(p)
            
        gt_fields = gt_doc.get('fields', [])
        gt_ft_counts = Counter(g['field_type'] for g in gt_fields)
        
        for g in gt_fields:
            ft = g['field_type']
            fv = str(g['field_value'])
            is_unnec = (g['necessity_label'].lower() == 'unnecessary')
            if not is_unnec:
                continue
                
            ft_stats[ft]['gt_unnec'] += 1
            span = g.get('span', {})
            s, e = span.get('start', 0), span.get('end', 0)
            
            # --- 1. OLD NAIVE PAIRING ---
            if ft in det_map and len(det_map[ft]) > 0:
                best_old = det_map[ft][0]
                p_span = best_old.get('predicted_span', [0, 0])
                p_text = best_old.get('predicted_text', '')
                det_ctx = extract_context_window(text_content, p_span[0], p_span[1]) if p_span[1] > 0 else extract_context_window(text_content, s, e)
                n_score, _, _, _, _ = evaluator.score_field(ft, doc_type, det_ctx, p_text)
                if n_score < 0.5:
                    old_caught += 1
                    ft_stats[ft]['old_caught'] += 1
                else:
                    old_class_miss += 1
                    ft_stats[ft]['old_class_miss'] += 1
                    is_multi = (len(det_map[ft]) > 1 or gt_ft_counts[ft] > 1)
                    old_class_miss_list.append({
                        'doc_id': doc_id, 'doc_type': doc_type, 'field_type': ft,
                        'gt_value': fv, 'pred_text': p_text,
                        'gt_span': [s, e], 'pred_span': p_span,
                        'num_preds': len(det_map[ft]), 'num_gt': gt_ft_counts[ft],
                        'is_multi': is_multi, 'n_score': n_score,
                    })
            else:
                old_det_miss += 1
                ft_stats[ft]['old_det_miss'] += 1
                
            # --- 2. NEW SPAN-OVERLAP / CLOSEST-DISTANCE PAIRING ---
            if ft in det_map and len(det_map[ft]) > 0:
                candidates = det_map[ft]
                best_cand = None
                best_overlap = -1
                best_dist = float('inf')
                
                # Check overlap first
                for cand in candidates:
                    p_span = cand.get('predicted_span', [0, 0])
                    ps, pe = p_span[0], p_span[1]
                    inter = max(0, min(e, pe) - max(s, ps))
                    dist = abs((s + e)/2.0 - (ps + pe)/2.0)
                    if inter > best_overlap:
                        best_overlap = inter
                        best_dist = dist
                        best_cand = cand
                    elif inter == best_overlap and inter > 0:
                        if dist < best_dist:
                            best_dist = dist
                            best_cand = cand
                            
                # If no overlap, pick candidate with closest midpoint distance
                if best_overlap == 0:
                    for cand in candidates:
                        p_span = cand.get('predicted_span', [0, 0])
                        ps, pe = p_span[0], p_span[1]
                        dist = abs((s + e)/2.0 - (ps + pe)/2.0)
                        if dist < best_dist:
                            best_dist = dist
                            best_cand = cand
                            
                p_span = best_cand.get('predicted_span', [0, 0])
                p_text = best_cand.get('predicted_text', '')
                det_ctx = extract_context_window(text_content, p_span[0], p_span[1]) if p_span[1] > 0 else extract_context_window(text_content, s, e)
                n_score, _, _, _, _ = evaluator.score_field(ft, doc_type, det_ctx, p_text)
                if n_score < 0.5:
                    new_caught += 1
                    ft_stats[ft]['new_caught'] += 1
                else:
                    new_class_miss += 1
                    ft_stats[ft]['new_class_miss'] += 1
                    new_class_miss_list.append({
                        'doc_id': doc_id, 'doc_type': doc_type, 'field_type': ft,
                        'gt_value': fv, 'pred_text': p_text,
                        'gt_span': [s, e], 'pred_span': p_span,
                        'overlap': best_overlap, 'dist': best_dist,
                        'n_score': n_score,
                    })
            else:
                new_det_miss += 1
                ft_stats[ft]['new_det_miss'] += 1
                
    multi_in_old = sum(1 for x in old_class_miss_list if x['is_multi'])
    print(f"Total GT Unnecessary Instances: {old_caught + old_det_miss + old_class_miss}")
    print(f"OLD NAIVE PAIRING ([0]):")
    print(f"  - Caught:              {old_caught:>3} ({(old_caught/211)*100:.1f}%)")
    print(f"  - Detection Miss:      {old_det_miss:>3} ({(old_det_miss/211)*100:.1f}%)")
    print(f"  - Classification Miss: {old_class_miss:>3} ({(old_class_miss/211)*100:.1f}%)")
    print(f"  - Multi-instance / Multi-pred in Old Class Misses: {multi_in_old} / {old_class_miss} ({multi_in_old/old_class_miss*100:.1f}%)")
    
    print(f"\nNEW SPAN-OVERLAP PAIRING:")
    print(f"  - Caught:              {new_caught:>3} ({(new_caught/211)*100:.1f}%)")
    print(f"  - Detection Miss:      {new_det_miss:>3} ({(new_det_miss/211)*100:.1f}%)")
    print(f"  - Classification Miss: {new_class_miss:>3} ({(new_class_miss/211)*100:.1f}%)")
    
    print(f"\nPer-Field Breakdown ({modality.upper()}):")
    print(f"{'Field Type':<25} | {'GT Unnec':<8} | {'Old Caught':<10} | {'Old ClassMiss':<13} | {'New Caught':<10} | {'New ClassMiss':<13}")
    print("-" * 90)
    for ft, st in sorted(ft_stats.items()):
        print(f"{ft:<25} | {st['gt_unnec']:<8} | {st['old_caught']:<10} | {st['old_class_miss']:<13} | {st['new_caught']:<10} | {st['new_class_miss']:<13}")
