"""
Test sequence matcher alignment on OCR ground truth spans.
"""

import difflib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OCR_PREDS_DIR = PROJECT_ROOT / "results" / "predictions" / "ocr"


def align_spans(clean_text: str, ocr_text: str, gt_fields: list):
    matcher = difflib.SequenceMatcher(None, clean_text, ocr_text, autojunk=False)
    matching_blocks = matcher.get_matching_blocks()
    
    clean_to_ocr = [-1] * len(clean_text)
    for a, b, size in matching_blocks:
        for k in range(size):
            clean_to_ocr[a + k] = b + k
            
    aligned_fields = []
    unalignable_count = 0
    
    for gf in gt_fields:
        ft = gf["field_type"]
        gt_s, gt_e = gf["span"]["start"], gf["span"]["end"]
        gt_val = gf["field_value"]
        
        valid_mapped = [clean_to_ocr[k] for k in range(gt_s, gt_e) if clean_to_ocr[k] != -1]
        
        # Check alignment quality
        span_len = gt_e - gt_s
        if len(valid_mapped) >= max(1, int(span_len * 0.4)):
            mapped_start = min(valid_mapped)
            mapped_end = max(valid_mapped) + 1
            ocr_substring = ocr_text[mapped_start:mapped_end]
            aligned_fields.append({
                "field_type": ft,
                "clean_span": [gt_s, gt_e],
                "ocr_span": [mapped_start, mapped_end],
                "clean_value": gt_val,
                "ocr_value": ocr_substring,
                "is_aligned": True,
            })
        else:
            unalignable_count += 1
            aligned_fields.append({
                "field_type": ft,
                "clean_span": [gt_s, gt_e],
                "ocr_span": None,
                "clean_value": gt_val,
                "ocr_value": None,
                "is_aligned": False,
            })
            
    return aligned_fields, unalignable_count


def test_alignment():
    ocr_files = sorted(list(OCR_PREDS_DIR.glob("*.json")))[:5]
    for i, ocr_file in enumerate(ocr_files, 1):
        with open(ocr_file, "r", encoding="utf-8") as f:
            ocr_pred_doc = json.load(f)
            
        doc_id = ocr_pred_doc["doc_id"]
        doc_type = ocr_pred_doc["document_type"]
        ocr_text = ocr_pred_doc.get("ocr_text", "")
        
        clean_text = (DATASET_DIR / doc_type / "text" / f"{doc_id}.txt").read_text(encoding="utf-8")
        gt_doc = json.loads((DATASET_DIR / doc_type / "labels" / f"{doc_id}.json").read_text(encoding="utf-8"))
        
        aligned, unalignable = align_spans(clean_text, ocr_text, gt_doc["fields"])
        print(f"\nDocument {doc_id}: Total GT fields={len(aligned)}, Unalignable={unalignable}")
        for af in aligned[:4]:
            print(f"  Field: {af['field_type']:<18} | Clean Span: {af['clean_span']} -> OCR Span: {af['ocr_span']}")
            print(f"    Clean Val: {repr(af['clean_value'])}")
            print(f"    OCR Val:   {repr(af['ocr_value'])}")

if __name__ == "__main__":
    test_alignment()
