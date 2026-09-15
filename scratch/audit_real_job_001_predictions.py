import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detection.detect import PIIDetector

txt_path = PROJECT_ROOT / "validation" / "real_world_samples" / "real_job_001.txt"
text = txt_path.read_text(encoding="utf-8")
detector = PIIDetector(score_threshold=0.4)
predictions = detector.detect(text, doc_type="job_application")

print(f"Total Raw Predictions for real_job_001: {len(predictions)}")
print("=" * 90)
for idx, p in enumerate(predictions):
    txt_val = repr(p["predicted_text"])
    print(f"[{idx:02d}] Field: {p['field_type']:<22} Entity: {p['entity_type']:<22} Conf: {p['confidence']:<5} Text: {txt_val}")

print("=" * 90)
matches_phone = [p for p in predictions if "0144" in p["predicted_text"]]
matches_email = [p for p in predictions if "casey.bennett" in p["predicted_text"]]

print(f"\nExact matches for '202-555-0144':")
for m in matches_phone:
    print(f"  -> {m}")

print(f"\nExact matches for 'casey.bennett@example.com':")
for m in matches_email:
    print(f"  -> {m}")
