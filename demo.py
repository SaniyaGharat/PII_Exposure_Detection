"""
demo.py — End-to-end live demonstration of the PII Necessity + Blockchain
Audit framework.

Run a single real document through the full pipeline and narrate each
step for a live audience (viva / presentation):

    detect PII  ->  classify necessity  ->  generate report
        ->  anchor on-chain  ->  verify on-chain

USAGE:
    python demo.py --doc dataset/job_application/text/job_001.txt --type job_application
    python demo.py --doc validation/real_world_samples/real_rent_001.txt --type rental_agreement

NOTES BEFORE YOU RUN THIS:
  1. Ganache must already be running (e.g. `npx ganache --port 8545 --wallet.deterministic --chain.chainId 1337`)
     and the contract must already be deployed (`npx hardhat run scripts/deploy.js
     --network localhost`), same as your normal Phase 4 workflow.
  2. The Necessity model needs to be fitted once at startup (train + validation
     split), same as in run_phase3.py — this takes a few seconds.
  3. Import paths and method signatures below match the validated modules
     in src/detection, src/necessity, and src/blockchain.
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Ensure immediate unbuffered streaming output
sys.stdout.reconfigure(line_buffering=True)

# --- imports matching actual module paths and interfaces ---
from src.detection.detect import PIIDetector
from src.necessity.hybrid import HybridNecessityEvaluator
from src.necessity.ml_classifier import extract_context_window
from src.blockchain.audit_client import BlockchainAuditClient


DIVIDER = "=" * 78

# Field types excluded from console DISPLAY ONLY (per Section 5.1.1 / 5.5 noise limitation).
# They remain fully included in detection, scoring, metrics, and saved reports.
DISPLAY_NOISE_TYPES = {"organization", "url"}


def banner(title: str):
    print("\n" + DIVIDER)
    print(f"  {title}")
    print(DIVIDER)


def pause(seconds: float = 0.6):
    """Small pause so a live audience can read each step. Set to 0 to skip."""
    time.sleep(seconds)


def step(n: int, total: int, text: str):
    print(f"\n[Step {n}/{total}] {text}")
    pause()


def main():
    parser = argparse.ArgumentParser(description="Live end-to-end pipeline demo.")
    parser.add_argument("--doc", required=True, help="Path to a document (.txt)")
    parser.add_argument("--type", required=True,
                         help="Document domain, e.g. job_application, medical_intake, "
                              "loan_application, rental_agreement")
    parser.add_argument("--recipient", default=None,
                         help="Recipient wallet address (defaults to a Ganache test account)")
    parser.add_argument("--purpose", default=None,
                         help="Free-text sharing purpose (defaults to a generic label per domain)")
    parser.add_argument("--no-pause", action="store_true", help="Skip pacing pauses")
    args = parser.parse_args()

    if args.no_pause:
        global pause
        pause = lambda *a, **k: None  # noqa: E731

    doc_path = Path(args.doc)
    if not doc_path.exists():
        print(f"ERROR: document not found at {doc_path}")
        sys.exit(1)

    doc_type = args.type
    doc_text = doc_path.read_text(encoding="utf-8")
    purpose = args.purpose or f"{doc_type}_review_and_processing"

    TOTAL_STEPS = 6

    banner("PII NECESSITY + BLOCKCHAIN AUDIT — LIVE DEMONSTRATION")
    print(f"  Document : {doc_path}")
    print(f"  Domain   : {doc_type}")
    print(f"  Purpose  : {purpose}")

    # ------------------------------------------------------------------
    step(1, TOTAL_STEPS, "Detecting PII fields in the document (Presidio + custom recognizers)...")
    detector = PIIDetector(score_threshold=0.4)
    predictions = detector.detect(doc_text, doc_type=doc_type)
    print(f"  -> Detected {len(predictions)} candidate PII fields.")
    display_predictions = [p for p in predictions if p["field_type"] not in DISPLAY_NOISE_TYPES]
    hidden_step1 = len(predictions) - len(display_predictions)
    for p in display_predictions[:8]:
        print(f"     - {p['field_type']:<22} '{p['predicted_text'][:40]}'  (confidence {p['confidence']:.2f})")
    if len(display_predictions) > 8:
        print(f"     ... and {len(display_predictions) - 8} more.")
    if hidden_step1 > 0:
        print(f"     (Note: {hidden_step1} noisy/formatting detections excluded from display; full set in saved report)")

    # ------------------------------------------------------------------
    step(2, TOTAL_STEPS, "Loading the hybrid necessity model (rule engine + trained classifier)...")
    evaluator = HybridNecessityEvaluator(model_type="random_forest")
    evaluator.fit_ml("dataset", "train")
    best_alpha, _ = evaluator.tune_alpha_on_validation("dataset", "validation")
    print(f"  -> Model ready. Validation-selected alpha = {best_alpha:.2f}")

    # ------------------------------------------------------------------
    step(3, TOTAL_STEPS, "Scoring each detected field for necessity relative to the declared purpose...")
    field_reports = []
    flagged_count = 0
    for p in predictions:
        ctx = extract_context_window(doc_text, p["predicted_span"][0], p["predicted_span"][1])
        n_score, r_score, m_score, label, justification = evaluator.score_field(
            field_type=p["field_type"],
            document_type=doc_type,
            context_text=ctx,
            field_value=p["predicted_text"],
        )
        status = "FLAGGED (unnecessary)" if n_score < 0.35 else (
            "REVIEW (contextual)" if n_score <= 0.65 else "CLEARED (necessary)"
        )
        if n_score < 0.35:
            flagged_count += 1
        field_reports.append({
            "field_type": p["field_type"],
            "value": p["predicted_text"],
            "N": round(float(n_score), 3),
            "R": round(float(r_score), 3),
            "M": round(float(m_score), 3),
            "status": status,
            "justification": justification,
        })

    display_reports = [f for f in field_reports if f["field_type"] not in DISPLAY_NOISE_TYPES]
    hidden_step3 = len(field_reports) - len(display_reports)

    print(f"\n  {'Field':<22} {'Value':<30} {'N':>6} {'Status'}")
    print("  " + "-" * 74)
    for f in display_reports:
        print(f"  {f['field_type']:<22} {f['value'][:28]:<30} {f['N']:>6.3f}  {f['status']}")
    if hidden_step3 > 0:
        print(f"  (Note: {hidden_step3} noisy detections omitted from table display; see saved report for full details)")
    print(f"\n  -> {flagged_count} / {len(field_reports)} fields flagged as unnecessary for '{purpose}'.")

    # Save a human-readable report alongside the run
    report = {
        "document_id": doc_path.stem,
        "document_type": doc_type,
        "purpose": purpose,
        "total_fields": len(field_reports),
        "total_fields_evaluated": len(field_reports),
        "total_unnecessary_flagged": flagged_count,
        "flagged_for_minimization": flagged_count,
        "flagged_ratio": (flagged_count / len(field_reports)) if field_reports else 0.0,
        "fields": field_reports,
    }
    out_path = Path("results/necessity_reports") / f"{doc_path.stem}_demo_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"  -> Necessity report saved to {out_path}")

    # ------------------------------------------------------------------
    step(4, TOTAL_STEPS, "Connecting to the blockchain audit layer (Ganache)...")
    try:
        client = BlockchainAuditClient()
        connected = client.w3.is_connected()
        print(f"  -> Connected: {connected}")
        print(f"  -> Contract address: {client.contract_address}")
        print(f"  -> Signing account:  {client.default_account}")
    except Exception as e:
        print(f"  ERROR: could not connect to blockchain layer: {e}")
        print("  Make sure Ganache is running and the contract is deployed (see docstring).")
        sys.exit(1)

    recipient = args.recipient or client.default_account  # self-share fallback for demo purposes

    # ------------------------------------------------------------------
    step(5, TOTAL_STEPS, "Anchoring the document share and necessity report on-chain...")
    if client.is_document_registered(str(doc_path)):
        print("  -> Document is already registered on-chain (immutable record exists).")
        existing_record = client.verify_share(str(doc_path))
        print(f"  -> Existing document hash : {existing_record.get('doc_hash')}")
        print(f"  -> Existing report hash   : {existing_record.get('report_hash')}")
    else:
        try:
            tx_result = client.register_share(
                document_path=str(doc_path),
                recipient_address=recipient,
                purpose=purpose,
                necessity_report=report,
            )
            print(f"  -> Transaction hash : {tx_result.get('transaction_hash', tx_result.get('tx_hash'))}")
            print(f"  -> Gas used         : {tx_result.get('gas_used', 'n/a')}")
            print(f"  -> Document hash    : {tx_result.get('doc_hash', 'n/a')}")
            print(f"  -> Report hash      : {tx_result.get('report_hash', 'n/a')}")
        except Exception as e:
            print(f"  ERROR during on-chain registration: {e}")
            sys.exit(1)

    # ------------------------------------------------------------------
    step(6, TOTAL_STEPS, "Verifying the on-chain record matches the off-chain report...")
    try:
        on_chain_record = client.verify_share(str(doc_path))
        print(f"  -> On-chain sender    : {on_chain_record.get('sender')}")
        print(f"  -> On-chain recipient : {on_chain_record.get('recipient')}")
        print(f"  -> On-chain purpose   : {on_chain_record.get('purpose')}")
        print(f"  -> On-chain flagged   : {on_chain_record.get('flagged_count')}"
              f" / {on_chain_record.get('total_field_count')}")
        match = str(on_chain_record.get("purpose")) == purpose
        print(f"  -> Off-chain / on-chain purpose match: {match}")
    except Exception as e:
        print(f"  ERROR during on-chain verification: {e}")
        sys.exit(1)

    banner("DEMO COMPLETE")
    print(f"  {flagged_count} of {len(field_reports)} PII fields in this document were flagged as")
    print(f"  unnecessary for the stated purpose, and the assessment is now anchored")
    print(f"  on-chain — auditable and tamper-evident — without the document's raw")
    print(f"  PII ever touching the blockchain.\n")


if __name__ == "__main__":
    main()
