import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ocr_file = PROJECT_ROOT / "results" / "predictions" / "ocr" / "job_004.json"
clean_file = PROJECT_ROOT / "dataset" / "job_application" / "text" / "job_004.txt"

with open(ocr_file, "r") as f:
    ocr_doc = json.load(f)

print("=== CLEAN TEXT ===")
print(clean_file.read_text())
print("\n=== OCR TEXT ===")
print(ocr_doc["ocr_text"])
