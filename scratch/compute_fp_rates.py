"""
Calculate exact FP counts and per-document FP rates for gender, job_title, and bank_account_number.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_METRICS = PROJECT_ROOT / "results" / "detection_metrics_clean.json"
OCR_METRICS = PROJECT_ROOT / "results" / "detection_metrics_ocr.json"

with open(CLEAN_METRICS, "r") as f:
    clean_data = json.load(f)

with open(OCR_METRICS, "r") as f:
    ocr_data = json.load(f)

fields = ["gender", "job_title", "bank_account_number"]

clean_docs = clean_data["total_documents_evaluated"] # 400
ocr_docs = ocr_data["total_documents_evaluated"]     # 100

clean_partial = clean_data["strategies"]["partial_overlap"]["per_field"]
ocr_partial = ocr_data["strategies"]["partial_overlap"]["per_field"]

print(f"{'Field':<22} | {'Clean FP':<8} | {'Clean FP/Doc':<12} | {'OCR FP':<8} | {'OCR FP/Doc':<12} | {'FP/Doc Ratio (OCR/Clean)':<24}")
print("-" * 95)

for ft in fields:
    c = clean_partial[ft]
    o = ocr_partial[ft]
    
    c_fp = c["fp"]
    o_fp = o["fp"]
    
    c_fp_per_doc = c_fp / clean_docs
    o_fp_per_doc = o_fp / ocr_docs
    ratio = o_fp_per_doc / c_fp_per_doc if c_fp_per_doc > 0 else 0
    
    print(f"{ft:<22} | {c_fp:<8} | {c_fp_per_doc:<12.4f} | {o_fp:<8} | {o_fp_per_doc:<12.4f} | {ratio:<24.2f}")

print("\n--- Raw Metrics Summary ---")
for ft in fields:
    c = clean_partial[ft]
    o = ocr_partial[ft]
    print(f"\nField: {ft}")
    print(f"  Clean (400 docs): TP={c['tp']}, FP={c['fp']}, FN={c['fn']}, Support={c['support']} | Prec={c['precision']:.4f}, Rec={c['recall']:.4f}, F1={c['f1_score']:.4f}")
    print(f"  OCR   (100 docs): TP={o['tp']}, FP={o['fp']}, FN={o['fn']}, Support={o['support']} | Prec={o['precision']:.4f}, Rec={o['recall']:.4f}, F1={o['f1_score']:.4f}")
