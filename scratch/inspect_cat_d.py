import json
from pathlib import Path

res_path = Path("validation/real_world_samples/real_world_validation_results.json")
data = json.loads(res_path.read_text(encoding="utf-8"))

print(f"Total Category (d) items: {data['false_positive_taxonomy']['d_unannotated_pii']['count']}\n")

for doc in data["per_document_metrics"]:
    doc_id = doc["doc_id"]
    print(f"============================== {doc_id} ==============================")
    for fp in doc["false_positive_details"]:
        if fp["category"] == "d_unannotated_pii":
            print(f"Field: {fp['field_type']:<22} Entity: {fp['entity_type']:<22} Conf: {fp['confidence']:<5} Text: {repr(fp['predicted_text'])}")
    print()
