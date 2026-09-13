"""
Script to analyze the exact breakdown of alignment failures vs detector failures
for specific OCR fields:
Group 1 (0.0000 F1): rental_history, education, emergency_contact, income, annual_income
Group 2 (OCR F1 > Clean F1): gender, job_title, bank_account_number
"""

import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATASET_DIR = PROJECT_ROOT / "dataset"
OCR_PREDS_DIR = PROJECT_ROOT / "results" / "predictions" / "ocr"

from src.detection.evaluate import find_ocr_span_for_field

TARGET_FIELDS_GROUP1 = [
    "rental_history",
    "education",
    "emergency_contact",
    "income",
    "annual_income",
]

TARGET_FIELDS_GROUP2 = [
    "gender",
    "job_title",
    "bank_account_number",
]

ALL_TARGETS = TARGET_FIELDS_GROUP1 + TARGET_FIELDS_GROUP2


def analyze():
    ocr_files = sorted(list(OCR_PREDS_DIR.glob("*.json")))
    
    # Track stats per field
    stats = {
        ft: {
            "total_gt": 0,
            "unalignable": 0,
            "aligned": 0,
            "detected_tp": 0,
            "missed_fn": 0,
            "fp": 0,
            "samples": []
        }
        for ft in ALL_TARGETS
    }
    
    for ocr_file in ocr_files:
        with open(ocr_file, "r", encoding="utf-8") as f:
            pred_doc = json.load(f)
            
        doc_id = pred_doc["doc_id"]
        doc_type = pred_doc["document_type"]
        ocr_text = pred_doc.get("ocr_text", "")
        preds = pred_doc.get("predictions", [])
        
        # Load GT
        gt_path = DATASET_DIR / doc_type / "labels" / f"{doc_id}.json"
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_doc = json.load(f)
            
        gt_fields = gt_doc.get("fields", [])
        
        for gf in gt_fields:
            ft = gf["field_type"]
            if ft not in ALL_TARGETS:
                continue
                
            clean_val = gf.get("field_value", "")
            stats[ft]["total_gt"] += 1
            
            ocr_span, score = find_ocr_span_for_field(clean_val, ocr_text)
            
            if not ocr_span:
                stats[ft]["unalignable"] += 1
                # If unalignable, it's counted as a missed GT
                if len(stats[ft]["samples"]) < 2:
                    stats[ft]["samples"].append({
                        "doc_id": doc_id,
                        "type": "unalignable",
                        "clean_val": clean_val[:60],
                    })
            else:
                stats[ft]["aligned"] += 1
                s, e = ocr_span
                # Check if any prediction overlaps
                matching_preds = [
                    p for p in preds
                    if p["field_type"] == ft and max(0, min(p["predicted_span"][1], e) - max(p["predicted_span"][0], s)) > 0
                ]
                if matching_preds:
                    stats[ft]["detected_tp"] += 1
                else:
                    stats[ft]["missed_fn"] += 1
                    if len(stats[ft]["samples"]) < 2:
                        stats[ft]["samples"].append({
                            "doc_id": doc_id,
                            "type": "missed_detection",
                            "ocr_val": ocr_text[s:e][:60],
                        })
                        
        # Also check False Positives for these fields
        for p in preds:
            p_ft = p["field_type"]
            if p_ft in ALL_TARGETS:
                # Check if this prediction overlaps with any aligned GT of the same field_type
                p_s, p_e = p["predicted_span"]
                has_gt = False
                for gf in gt_fields:
                    if gf["field_type"] == p_ft:
                        ocr_span, _ = find_ocr_span_for_field(gf.get("field_value", ""), ocr_text)
                        if ocr_span:
                            s, e = ocr_span
                            if max(0, min(p_e, e) - max(p_s, s)) > 0:
                                has_gt = True
                                break
                if not has_gt:
                    stats[p_ft]["fp"] += 1

    return stats


if __name__ == "__main__":
    stats = analyze()
    
    print("\n" + "="*80)
    print("GROUP 1: FIELDS DROPPED TO 0.0000 F1 IN OCR PARTIAL OVERLAP")
    print("="*80)
    for ft in TARGET_FIELDS_GROUP1:
        s = stats[ft]
        print(f"\nField: '{ft}'")
        print(f"  • Total Ground-Truth Instances: {s['total_gt']}")
        print(f"  • Unalignable (OCR garbled/truncated): {s['unalignable']} ({s['unalignable']/s['total_gt']*100:.1f}%)")
        print(f"  • Successfully Aligned: {s['aligned']} ({s['aligned']/s['total_gt']*100:.1f}%)")
        print(f"    - Correctly Detected by Presidio (TP): {s['detected_tp']}")
        print(f"    - Genuinely Missed by Presidio (FN):   {s['missed_fn']}")
        print(f"  • False Positives (FP): {s['fp']}")
        if s["samples"]:
            print(f"  • Sample Failure Diagnostics:")
            for samp in s["samples"]:
                if samp["type"] == "unalignable":
                    print(f"    - [Doc {samp['doc_id']} Unalignable] Clean: {repr(samp['clean_val'])}")
                else:
                    print(f"    - [Doc {samp['doc_id']} Missed Detection] OCR Text: {repr(samp['ocr_val'])}")

    print("\n" + "="*80)
    print("GROUP 2: FIELDS WHERE OCR F1 EXCEEDED CLEAN F1")
    print("="*80)
    for ft in TARGET_FIELDS_GROUP2:
        s = stats[ft]
        print(f"\nField: '{ft}'")
        print(f"  • Total Ground-Truth Instances: {s['total_gt']}")
        print(f"  • Unalignable (OCR garbled/truncated): {s['unalignable']} ({s['unalignable']/s['total_gt']*100:.1f}%)")
        print(f"  • Successfully Aligned: {s['aligned']} ({s['aligned']/s['total_gt']*100:.1f}%)")
        print(f"    - Correctly Detected by Presidio (TP): {s['detected_tp']}")
        print(f"    - Genuinely Missed by Presidio (FN):   {s['missed_fn']}")
        print(f"  • False Positives (FP): {s['fp']}")
