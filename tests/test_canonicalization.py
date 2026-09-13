"""
PII Exposure Detection - Canonicalization & Report Hashing Verification Test
Verifies that:
1. Re-serializing existing Phase 3 reports produces hashes identical to those anchored on-chain.
2. Semantically identical reports with shuffled key orders, indentation changes, and alternate formatting
   produce strictly identical Keccak-256 hashes when passed through canonicalize_json.
"""

import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web3 import Web3
from src.blockchain.audit_client import BlockchainAuditClient, canonicalize_json


def recursively_shuffle_dict(obj: Any, seed: int = 42) -> Any:
    """
    Recursively shuffles dictionary key insertion orders without modifying values.
    In Python 3.7+, dict preserves insertion order. Shuffling keys creates
    different raw string serializations unless canonical sorting is applied.
    """
    if isinstance(obj, dict):
        keys = list(obj.keys())
        rng = random.Random(seed)
        rng.shuffle(keys)
        return {k: recursively_shuffle_dict(obj[k], seed + 1) for k in keys}
    elif isinstance(obj, list):
        return [recursively_shuffle_dict(elem, seed + 1) for elem in obj]
    else:
        return obj


def recursively_reverse_dict(obj: Any) -> Any:
    """Recursively reverses dictionary key insertion orders."""
    if isinstance(obj, dict):
        keys = sorted(list(obj.keys()), reverse=True)
        return {k: recursively_reverse_dict(obj[k]) for k in keys}
    elif isinstance(obj, list):
        return [recursively_reverse_dict(elem) for elem in obj]
    else:
        return obj


def run_canonicalization_tests():
    print("=" * 80)
    print("  CANONICALIZATION & CRYPTOGRAPHIC HASH INVARIANCE VERIFICATION TEST")
    print("=" * 80)

    project_root = Path(__file__).resolve().parent.parent
    reports_dir = project_root / "results" / "necessity_reports"
    summary_file = project_root / "results" / "blockchain_audit_summary.json"

    with open(summary_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    anchored_records = {
        r["document_id"]: r["registration"]["report_hash"]
        for r in summary["audit_records"]
    }

    test_docs = ["job_001", "rent_001", "med_001"]

    print("\n--- TEST PART 1: Parity Against On-Chain Anchored Hashes ---")
    for doc_id in test_docs:
        report_path = reports_dir / f"{doc_id}_necessity_report.json"
        assert report_path.exists(), f"Report file not found: {report_path}"

        # 1. Load raw JSON file
        with open(report_path, "r", encoding="utf-8") as f:
            raw_dict = json.load(f)

        # 2. Compute canonical hash using audit_client method
        computed_hash_bytes = BlockchainAuditClient.compute_report_hash(report_path)
        computed_hash_hex = "0x" + computed_hash_bytes.hex()
        anchored_hash_hex = anchored_records[doc_id]

        print(f"\nDocument [{doc_id}]:")
        print(f"  - On-Chain Anchored reportHash: {anchored_hash_hex}")
        print(f"  - Re-computed Canonical Hash:  {computed_hash_hex}")

        match = (computed_hash_hex.lower() == anchored_hash_hex.lower())
        print(f"  - Exact Match Status:          {'PASS (MATCHED)' if match else 'FAIL (MISMATCH)'}")
        assert match, f"Hash mismatch for {doc_id}! On-chain: {anchored_hash_hex}, Computed: {computed_hash_hex}"

    print("\n[+] Part 1 Complete: All 3 existing reports re-serialize to the exact on-chain hashes.")

    print("\n--- TEST PART 2: Semantic Invariance Under Key Order & Format Perturbations ---")

    # Pick job_001 for comprehensive perturbation tests
    sample_report_path = reports_dir / "job_001_necessity_report.json"
    with open(sample_report_path, "r", encoding="utf-8") as f:
        original_dict = json.load(f)

    # Compute baseline canonical hash
    baseline_bytes = canonicalize_json(original_dict)
    baseline_hash = Web3.keccak(baseline_bytes).hex()
    if not baseline_hash.startswith("0x"):
        baseline_hash = "0x" + baseline_hash

    print(f"\nTarget Document: job_001_necessity_report.json")
    print(f"Baseline Canonical Hash: {baseline_hash}")
    print(f"Baseline Canonical Bytes Length: {len(baseline_bytes)} bytes")

    # Case A: Raw non-canonical formatting differences (spaces, indentation, newlines)
    # Without canonicalization, non-canonical json strings produce totally different hashes:
    raw_compact = json.dumps(original_dict, separators=(",", ":")).encode("utf-8")
    raw_pretty_2sp = json.dumps(original_dict, indent=2).encode("utf-8")
    raw_pretty_4sp = json.dumps(original_dict, indent=4).encode("utf-8")

    hash_raw_compact = "0x" + Web3.keccak(raw_compact).hex()
    hash_raw_pretty_2sp = "0x" + Web3.keccak(raw_pretty_2sp).hex()
    hash_raw_pretty_4sp = "0x" + Web3.keccak(raw_pretty_4sp).hex()

    print("\n  [Observation: Raw (Non-Canonical) JSON Hashing is Fragile]")
    print(f"    - Raw compact string hash:      {hash_raw_compact}")
    print(f"    - Raw 2-space indented hash:    {hash_raw_pretty_2sp} (Different!)")
    print(f"    - Raw 4-space indented hash:    {hash_raw_pretty_4sp} (Different!)")

    # Case B: Applying canonicalize_json to differently formatted / parsed versions
    print("\n  [Verification: Canonicalization Produces Identical Hashes Across Variations]")

    # Create valid JSON text where specific numeric literals have trailing zeros or scientific notation
    # (e.g., '0.5000', '1.000', '0.000', '1.0e0')
    import re
    # Match standalone floating point numbers in JSON and format them with extra trailing zeros
    def reformat_floats(match):
        num_str = match.group(0)
        try:
            val = float(num_str)
            return f"{val:.6f}"
        except ValueError:
            return num_str

    json_str_with_float_literals = re.sub(r'(?<=:\s)\d+\.\d+(?=[,\n\s\}])', reformat_floats, json.dumps(original_dict, indent=2))
    dict_from_alt_floats = json.loads(json_str_with_float_literals)

    variations: List[Tuple[str, Dict[str, Any]]] = [
        ("1. Original in-memory dictionary", original_dict),
        ("2. Parsed from 2-space pretty-printed JSON", json.loads(raw_pretty_2sp)),
        ("3. Parsed from 4-space pretty-printed JSON", json.loads(raw_pretty_4sp)),
        ("4. Parsed from compact JSON string", json.loads(raw_compact)),
        ("5. Reverse-alphabetical key order (all nested levels)", recursively_reverse_dict(original_dict)),
        ("6. Randomly shuffled key order (Seed 101)", recursively_shuffle_dict(original_dict, seed=101)),
        ("7. Randomly shuffled key order (Seed 202)", recursively_shuffle_dict(original_dict, seed=202)),
        ("8. Randomly shuffled key order (Seed 999)", recursively_shuffle_dict(original_dict, seed=999)),
        ("9. Parsed from alternate float literals (e.g. '0.500000', '1.000000')", dict_from_alt_floats),
        ("10. Shuffled + Parsed from 4-space indent combined", recursively_shuffle_dict(json.loads(raw_pretty_4sp), seed=777)),
    ]

    all_passed = True
    for label, var_dict in variations:
        c_bytes = canonicalize_json(var_dict)
        c_hash = "0x" + Web3.keccak(c_bytes).hex()
        is_identical = (c_hash == baseline_hash)
        byte_len_match = (len(c_bytes) == len(baseline_bytes))

        print(f"    * {label}:")
        print(f"        Computed Hash: {c_hash}")
        print(f"        Match Baseline: {'PASS (EXACT MATCH)' if is_identical else 'FAIL'}")

        if not is_identical:
            all_passed = False

        assert is_identical, f"Canonicalization failed for: {label}"
        assert byte_len_match, f"Byte length mismatch for: {label}"

    print("\n" + "=" * 80)
    print("  FINAL VERIFICATION RESULT: ALL TESTS PASSED")
    print("  - Part 1: All re-computed report hashes strictly match on-chain anchors.")
    print("  - Part 2: Key re-ordering, indentation, and formatting changes preserve 100% hash parity.")
    print("=" * 80)


if __name__ == "__main__":
    run_canonicalization_tests()
