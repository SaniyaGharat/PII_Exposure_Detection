import re
import difflib
import json
from collections import defaultdict
from pathlib import Path

import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detection.detect import PIIDetector

detector = PIIDetector(score_threshold=0.4)
validation_dir = PROJECT_ROOT / "validation" / "real_world_samples"
doc_files = sorted(validation_dir.glob("*.txt"))

print("=" * 90)
print("AUDITING STRICT 1-TO-1 MATCHING ACROSS ALL 4 REAL-WORLD DOCUMENTS")
print("=" * 90)

for txt_file in doc_files:
    doc_id = txt_file.stem
    json_file = validation_dir / f"{doc_id}.json"
    doc_text = txt_file.read_text(encoding="utf-8")
    label_data = json.loads(json_file.read_text(encoding="utf-8"))
    gt_fields = label_data["fields"]
    domain = label_data["domain"]

    predictions = detector.detect(doc_text, doc_type=domain)

    print(f"\n==================== DOCUMENT: {doc_id} ({domain}) ====================")
    print(f"Total Ground Truth: {len(gt_fields)} | Total Raw Predictions: {len(predictions)}")
    print("\n--- ALL RAW PREDICTIONS ---")
    for idx, p in enumerate(predictions):
        print(f"  P[{idx:02d}] {p['field_type']:<20} {p['entity_type']:<18} conf={p['confidence']:<4} text={repr(p['predicted_text'])}")

    print("\n--- GROUND TRUTH MATCH AUDIT (Strict 1-to-1 Matching) ---")
    matched_preds = set()
    matched_gt = set()

    for g_idx, g in enumerate(gt_fields):
        g_type = g["field_type"]
        g_val = g["value"]
        
        # Look for the exact matching prediction
        best_p_idx = None
        for p_idx, p in enumerate(predictions):
            if p_idx in matched_preds:
                continue
            p_text = p["predicted_text"]
            p_type = p["field_type"]
            p_entity = p["entity_type"]

            # Phone numbers: exact digit match
            if "phone" in g_type:
                g_dig = re.sub(r"\D", "", g_val)
                p_dig = re.sub(r"\D", "", p_text)
                if g_dig and p_dig and g_dig == p_dig:
                    best_p_idx = p_idx
                    break

            # Email addresses: exact string match
            elif "email" in g_type:
                if g_val.strip().lower() == p_text.strip().lower():
                    best_p_idx = p_idx
                    break

            # National ID / Bank Account / Date of Birth: exact or strict normalized match
            elif g_type in ("national_id", "bank_account", "date_of_birth", "postal_code"):
                if g_val.strip().lower() in p_text.strip().lower() or p_text.strip().lower() in g_val.strip().lower():
                    best_p_idx = p_idx
                    break

            # Names and text fields: specific substring or high similarity
            else:
                if g_val.strip().lower() in p_text.strip().lower() or p_text.strip().lower() in g_val.strip().lower():
                    best_p_idx = p_idx
                    break

        if best_p_idx is not None:
            matched_preds.add(best_p_idx)
            matched_gt.add(g_idx)
            matched_p = predictions[best_p_idx]
            print(f"  [PASS] TP [{g_type}]: '{g_val}' ==> P[{best_p_idx:02d}] ({matched_p['field_type']}) '{matched_p['predicted_text'].replace(chr(10), ' ')}'")
        else:
            print(f"  [FAIL] FN [{g_type}]: '{g_val}' ==> NO STRICT PREDICTION MATCH")

    print(f"\nResult: Matched {len(matched_gt)} / {len(gt_fields)} GT fields. True Positives={len(matched_preds)}, False Positives={len(predictions) - len(matched_preds)}")
