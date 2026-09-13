"""
Test robust SequenceMatcher entity span alignment between clean GT and OCR text.
"""

import difflib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OCR_PREDS_DIR = PROJECT_ROOT / "results" / "predictions" / "ocr"


def find_ocr_span_for_field(clean_val: str, ocr_text: str, similarity_threshold: float = 0.5):
    """
    Finds the best matching span in OCR text for a ground truth field value using SequenceMatcher.
    """
    clean_val = clean_val.strip()
    if not clean_val or not ocr_text:
        return None, 0.0

    # 1. Direct exact match in OCR text
    idx = ocr_text.find(clean_val)
    if idx != -1:
        return [idx, idx + len(clean_val)], 1.0

    # 2. SequenceMatcher longest match / window alignment
    matcher = difflib.SequenceMatcher(None, clean_val, ocr_text, autojunk=False)
    match = matcher.find_longest_match(0, len(clean_val), 0, len(ocr_text))

    if match.size >= max(3, int(len(clean_val) * similarity_threshold)):
        # Refine window around match in OCR text
        ocr_start = match.b - match.a
        ocr_end = ocr_start + len(clean_val)
        
        # Clamp to bounds
        ocr_start = max(0, min(ocr_start, len(ocr_text)))
        ocr_end = max(ocr_start, min(ocr_end, len(ocr_text)))
        
        candidate = ocr_text[ocr_start:ocr_end]
        ratio = difflib.SequenceMatcher(None, clean_val, candidate).ratio()
        
        # Also check exact match block boundaries
        block_start = match.b
        block_end = match.b + match.size
        
        # Return the window with highest overlap
        if ratio >= similarity_threshold:
            return [ocr_start, ocr_end], ratio
        else:
            return [block_start, block_end], match.size / len(clean_val)

    return None, 0.0


def test_field_level_alignment():
    ocr_files = sorted(list(OCR_PREDS_DIR.glob("*.json")))[:5]
    
    for i, ocr_file in enumerate(ocr_files, 1):
        with open(ocr_file, "r", encoding="utf-8") as f:
            ocr_pred_doc = json.load(f)
            
        doc_id = ocr_pred_doc["doc_id"]
        doc_type = ocr_pred_doc["document_type"]
        ocr_text = ocr_pred_doc.get("ocr_text", "")
        
        gt_doc = json.loads((DATASET_DIR / doc_type / "labels" / f"{doc_id}.json").read_text(encoding="utf-8"))
        
        print(f"\n=======================================================")
        print(f"Document {doc_id} ({doc_type}) - Total Fields: {len(gt_doc['fields'])}")
        print(f"=======================================================")
        
        aligned_count = 0
        for gf in gt_doc["fields"]:
            ft = gf["field_type"]
            gt_val = gf["field_value"]
            ocr_span, score = find_ocr_span_for_field(gt_val, ocr_text)
            
            if ocr_span:
                aligned_count += 1
                ocr_sub = ocr_text[ocr_span[0]:ocr_span[1]]
                print(f"  [ALIGNED {score:.2f}] {ft:<20} | OCR Span: {ocr_span} | Sub: {repr(ocr_sub)}")
            else:
                print(f"  [UNALIGNABLE]  {ft:<20} | Val: {repr(gt_val[:30])}")
        print(f"Summary: Aligned {aligned_count} / {len(gt_doc['fields'])}")

if __name__ == "__main__":
    test_field_level_alignment()
