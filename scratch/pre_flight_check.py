"""
Step 0 Pre-flight Check: Compute class distribution of necessity labels
(necessary, contextual, unnecessary) across full dataset and per domain.
"""

import json
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"

def pre_flight_check():
    doc_types = ["job_application", "medical_intake", "loan_application", "rental_agreement"]
    
    total_counts = defaultdict(int)
    domain_counts = {dt: defaultdict(int) for dt in doc_types}
    total_instances = 0
    
    for dt in doc_types:
        labels_dir = DATASET_DIR / dt / "labels"
        for label_file in labels_dir.glob("*.json"):
            with open(label_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for field in data.get("fields", []):
                nec = field["necessity_label"].lower()
                total_counts[nec] += 1
                domain_counts[dt][nec] += 1
                total_instances += 1

    print("=" * 75)
    print("STEP 0: PRE-FLIGHT CLASS DISTRIBUTION ANALYSIS")
    print("=" * 75)
    print(f"Total Evaluated PII Instances: {total_instances} across 400 documents\n")
    
    print("--- FULL DATASET CLASS DISTRIBUTION ---")
    for nec in ["necessary", "contextual", "unnecessary"]:
        count = total_counts[nec]
        pct = (count / total_instances) * 100
        is_low = "<-- BELOW 15% THRESHOLD" if pct < 15.0 else ""
        print(f"  {nec.upper():<12}: {count:>5} instances ({pct:>5.2f}%) {is_low}")
        
    print("\n--- PER-DOMAIN CLASS DISTRIBUTION ---")
    for dt in doc_types:
        d_total = sum(domain_counts[dt].values())
        print(f"\nDomain: {dt} (Total instances = {d_total})")
        for nec in ["necessary", "contextual", "unnecessary"]:
            c = domain_counts[dt][nec]
            pct = (c / d_total) * 100
            is_low = "<-- BELOW 15% THRESHOLD" if pct < 15.0 else ""
            print(f"  {nec.upper():<12}: {c:>5} instances ({pct:>5.2f}%) {is_low}")

    print("\n" + "=" * 75)
    
    # Check splits distribution
    splits_dir = DATASET_DIR / "splits"
    for split_name in ["train", "validation", "test"]:
        with open(splits_dir / f"{split_name}.json", "r", encoding="utf-8") as sf:
            split_data = json.load(sf)
        split_counts = defaultdict(int)
        split_total = 0
        for doc_item in split_data["documents"]:
            doc_id = doc_item["document_id"]
            doc_type = doc_item["document_type"]
            with open(DATASET_DIR / doc_type / "labels" / f"{doc_id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for field in data.get("fields", []):
                nec = field["necessity_label"].lower()
                split_counts[nec] += 1
                split_total += 1
        print(f"Split: {split_name.upper():<10} (Total={split_total}) | " + 
              " | ".join([f"{nec}={split_counts[nec]} ({split_counts[nec]/split_total*100:.1f}%)" for nec in ["necessary", "contextual", "unnecessary"]]))
    print("=" * 75)

if __name__ == "__main__":
    pre_flight_check()
