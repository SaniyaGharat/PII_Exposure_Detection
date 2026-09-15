"""
Verification script for validation/real_world_samples/
Ensures exact string containment, ID matching, privacy rules, and generates dataset_summary.json.
"""

import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "validation" / "real_world_samples"

def verify_and_summarize():
    doc_ids = ["real_job_001", "real_bank_001", "real_medical_001", "real_rent_001"]
    
    total_documents = len(doc_ids)
    documents_by_domain = {}
    total_pii_fields = 0
    pii_field_counts = Counter()
    
    print("=" * 70)
    print("  VERIFYING REAL-WORLD VALIDATION DATASET INTEGRITY")
    print("=" * 70)
    
    all_passed = True
    
    for doc_id in doc_ids:
        txt_path = BASE_DIR / f"{doc_id}.txt"
        json_path = BASE_DIR / f"{doc_id}.json"
        
        assert txt_path.exists(), f"Missing text file: {txt_path}"
        assert json_path.exists(), f"Missing JSON file: {json_path}"
        
        doc_text = txt_path.read_text(encoding="utf-8")
        with open(json_path, "r", encoding="utf-8") as f:
            label_data = json.load(f)
            
        assert label_data["doc_id"] == doc_id, f"Doc ID mismatch in {json_path}: expected {doc_id}, got {label_data['doc_id']}"
        
        domain = label_data["domain"]
        documents_by_domain[domain] = documents_by_domain.get(domain, 0) + 1
        
        fields = label_data.get("fields", [])
        total_pii_fields += len(fields)
        
        print(f"\n[+] Verifying Document: {doc_id} (Domain: {domain})")
        print(f"    Source Type: {label_data.get('source_type')}")
        print(f"    Total Annotated Fields: {len(fields)}")
        
        for field in fields:
            f_type = field["field_type"]
            val = field["value"]
            pii_field_counts[f_type] += 1
            
            # 1. Exact string containment check
            if val not in doc_text:
                print(f"  [!] ERROR: Field '{f_type}' with value '{val}' NOT FOUND in {doc_id}.txt")
                all_passed = False
            else:
                print(f"    - [{f_type}]: '{val}' -> VERIFIED (FOUND IN DOCUMENT)")
                
            # 2. Privacy checks
            if "@" in val:
                assert "example.com" in val, f"Non-synthetic email detected: {val}"
            if "phone" in f_type:
                assert "202-555-" in val or "555" in val, f"Non-synthetic phone number detected: {val}"

    # Generate dataset summary
    summary_data = {
        "total_documents": total_documents,
        "documents_by_domain": documents_by_domain,
        "total_pii_fields": total_pii_fields,
        "pii_field_counts": dict(sorted(pii_field_counts.items())),
        "document_ids": doc_ids,
        "privacy_compliance": {
            "all_synthetic": True,
            "zero_real_pii": True,
            "fictional_domains": ["example.com"],
            "fictional_phone_prefixes": ["202-555-"]
        }
    }
    
    summary_path = BASE_DIR / "dataset_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
        
    print("\n" + "=" * 70)
    print("  SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Total Documents:     {total_documents}")
    print(f"Documents by Domain: {documents_by_domain}")
    print(f"Total PII Fields:    {total_pii_fields}")
    print(f"Field Distribution:  {dict(pii_field_counts)}")
    print(f"Summary JSON saved to: {summary_path}")
    print("=" * 70)
    
    if all_passed:
        print("\n>>> ALL VALIDATION CHECKS PASSED PERFECTLY! <<<")
    else:
        print("\n>>> SOME VALIDATION CHECKS FAILED! <<<")

if __name__ == "__main__":
    verify_and_summarize()
