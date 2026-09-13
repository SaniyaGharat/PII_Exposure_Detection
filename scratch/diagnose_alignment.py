"""
Diagnostic script to confirm the coordinate system mismatch between clean ground-truth spans and OCR text spans.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OCR_PREDS_DIR = PROJECT_ROOT / "results" / "predictions" / "ocr"

def diagnose():
    ocr_files = sorted(list(OCR_PREDS_DIR.glob("*.json")))[:5]
    
    for i, ocr_file in enumerate(ocr_files, 1):
        with open(ocr_file, "r", encoding="utf-8") as f:
            ocr_pred_doc = json.load(f)
            
        doc_id = ocr_pred_doc["doc_id"]
        doc_type = ocr_pred_doc["document_type"]
        ocr_text = ocr_pred_doc.get("ocr_text", "")
        preds = ocr_pred_doc.get("predictions", [])
        
        # Load clean text
        clean_text_path = DATASET_DIR / doc_type / "text" / f"{doc_id}.txt"
        clean_text = clean_text_path.read_text(encoding="utf-8")
        
        # Load ground truth label
        gt_path = DATASET_DIR / doc_type / "labels" / f"{doc_id}.json"
        with open(gt_path, "r", encoding="utf-8") as f:
            gt_doc = json.load(f)
        gt_fields = gt_doc.get("fields", [])
        
        print(f"\n{'='*75}")
        print(f"EXAMPLE {i}: Document ID = {doc_id} ({doc_type})")
        print(f"{'='*75}")
        print(f"Clean Text Length: {len(clean_text)} chars | OCR Text Length: {len(ocr_text)} chars")
        
        # Show first 3 matching field types between GT and Preds to demonstrate the offset shift
        shown_count = 0
        for gf in gt_fields:
            ft = gf["field_type"]
            gt_s, gt_e = gf["span"]["start"], gf["span"]["end"]
            gt_sub = clean_text[gt_s:gt_e]
            
            # Find any prediction of this field_type
            matching_preds = [p for p in preds if p["field_type"] == ft]
            if matching_preds and shown_count < 2:
                pred = matching_preds[0]
                p_s, p_e = pred["predicted_span"]
                pred_sub_in_ocr = ocr_text[p_s:p_e] if p_e <= len(ocr_text) else "[OUT OF BOUNDS]"
                
                # What does GT span point to in OCR text?
                gt_span_in_ocr = ocr_text[gt_s:gt_e] if gt_e <= len(ocr_text) else "[OUT OF BOUNDS]"
                
                print(f"\n--- Field: '{ft}' ---")
                print(f"(a) Ground-truth span in CLEAN text [{gt_s}:{gt_e}]:")
                print(f"    Value: {repr(gt_sub)}")
                print(f"(b) Predicted span in OCR text [{p_s}:{p_e}]:")
                print(f"    Value: {repr(pred_sub_in_ocr)}")
                print(f"(c) What the clean GT span [{gt_s}:{gt_e}] actually points to inside OCR text:")
                print(f"    Value: {repr(gt_span_in_ocr)}")
                
                shown_count += 1

if __name__ == "__main__":
    diagnose()
