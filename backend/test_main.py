"""
Unit and Integration Tests for PII Necessity Audit FastAPI Backend
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "contract_address" in data


def test_get_samples():
    response = client.get("/api/samples")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 4
    domains = {s["domain"] for s in samples}
    assert "job_application" in domains
    assert "medical_intake" in domains
    assert "loan_application" in domains
    assert "rental_agreement" in domains
    for s in samples:
        assert "id" in s
        assert "label" in s
        assert "text" in s
        assert len(s["text"]) > 20


def test_analyze_document():
    sample_text = (
        "APPLICANT DETAILS\n"
        "Full name: Alex Morgan\n"
        "Date of birth: 14 February 1994\n"
        "Email: alex.morgan@example.com\n"
        "Phone: +1 (415) 555-0138\n"
        "Home address: 18 Willow Lane, San Francisco, CA\n"
        "Marital status: Single\n"
        "Religion: Not disclosed\n"
        "National ID: 589-42-1630\n"
    )
    payload = {
        "document_text": sample_text,
        "domain": "job_application",
        "purpose": "job_application_review_and_processing",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "document_id" in data
    assert data["domain"] == "job_application"
    assert data["total_fields"] > 0
    assert len(data["fields"]) == data["total_fields"]
    assert data["flagged_count"] >= 0

    field_types = [f["field_type"] for f in data["fields"]]
    assert any("email" in ft or "phone" in ft or "name" in ft or "date_of_birth" in ft for ft in field_types)

    for field in data["fields"]:
        assert 0.0 <= field["N"] <= 1.0
        assert 0.0 <= field["R"] <= 1.0
        assert 0.0 <= field["M"] <= 1.0
        assert field["status"] in ["flagged", "review", "cleared"]
        assert len(field["justification"]) > 0



def test_full_pipeline_anchor_override_verify():
    # 1. Analyze
    sample_text = (
        "PATIENT INTAKE\n"
        "Full name: Jamie Chen\n"
        "Date of birth: 22 July 1987\n"
        "Email: jamie.chen@example.com\n"
        "Phone: +1 (212) 555-0196\n"
        "Emergency contact: Lin Chen — +1 (212) 555-0170\n"
    )
    analyze_res = client.post(
        "/api/analyze",
        json={
            "document_text": sample_text,
            "domain": "medical_intake",
            "purpose": "medical_intake_review_and_processing",
        },
    )
    assert analyze_res.status_code == 200
    doc_id = analyze_res.json()["document_id"]

    # 2. Anchor
    anchor_res = client.post("/api/anchor", json={"document_id": doc_id})
    assert anchor_res.status_code == 200
    anchor_data = anchor_res.json()
    assert anchor_data["transaction_hash"].startswith("0x")
    assert anchor_data["doc_hash"].startswith("0x")
    assert anchor_data["report_hash"].startswith("0x")
    assert anchor_data["block_number"] > 0
    assert anchor_data["gas_used"] > 0

    # 3. Override
    override_res = client.post(
        "/api/override",
        json={
            "document_id": doc_id,
            "field_type": "date_of_birth",
            "justification": "Required for age-specific medical treatment protocol.",
        },
    )
    assert override_res.status_code == 200
    override_data = override_res.json()
    assert override_data["transaction_hash"].startswith("0x")
    assert override_data["gas_used"] > 0

    # 4. Verify
    verify_res = client.get(f"/api/verify/{doc_id}")
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["purpose"] == "medical_intake_review_and_processing"
    assert verify_data["total_field_count"] == analyze_res.json()["total_fields"]
    assert verify_data["flagged_count"] == analyze_res.json()["flagged_count"]
    assert verify_data["overridden"] is True
    assert "timestamp" in verify_data


def test_invalid_document_analyze():
    response = client.post(
        "/api/analyze",
        json={"document_text": "   ", "domain": "job_application", "purpose": "test"},
    )
    assert response.status_code == 400


def test_anchor_nonexistent_document():
    response = client.post("/api/anchor", json={"document_id": "nonexistent_doc_id"})
    assert response.status_code == 404
