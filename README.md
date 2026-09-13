# An Intelligent Blockchain-Assisted Framework for Detecting Unnecessary PII Exposure in Document Sharing

## 📌 Research Overview & Objective

In modern digital document workflows (e.g., employment screening, healthcare admissions, consumer credit evaluations, and residential tenancy agreements), organizations frequently collect sensitive Personally Identifiable Information (PII) beyond what is strictly required for the specific business objective. This unnecessary data exposure increases privacy risks, identity theft vulnerabilities, and compliance liabilities under data privacy frameworks (e.g., GDPR, CCPA/CPRA, HIPAA).

This research project introduces an intelligent, privacy-preserving framework to:
1. Detect PII entities within shared digital and scanned documents.
2. Formally classify each extracted PII element as **Necessary**, **Contextual**, or **Unnecessary** relative to the explicit, declared purpose of the document.
3. Establish auditable, tamper-evident cryptographic verification via blockchain-assisted document hashing.

---

## 🎯 Phase 1 Objective: Dataset Preparation

Phase 1 establishes the benchmark synthetic dataset and research ground truth required for training, evaluating, and validating the subsequent components of the framework.

Key highlights of Phase 1:
- **4 Real-World Document Domains**: Job Application, Medical Clinical Intake, Loan/Credit Application, and Residential Rental Application.
- **Strictly Grounded Necessity Policies**: Academic justifications and purpose-dependent classification policies for every PII attribute.
- **Multi-Modal Document Representations**:
  - Raw Text format (`.txt`)
  - Formatted digital PDF documents (`.pdf` via ReportLab)
  - Degraded scanned document simulations (`.png` via Pillow for OCR robustness evaluation)
  - Detailed ground truth annotations (`.json`) with exact character-level span boundaries `[start, end]`.
- **Reproducible Dataset Splits**: Stratified 70% Train, 15% Validation, and 15% Test splits stored in JSON format with deterministic random seeds.
- **Comprehensive Integrity Validation**: 10 automated consistency checks ensuring zero orphan files, exact span matching, valid labels, and disjoint splits.

---

## 📂 Project Structure

```text
PII_Exposure_Detection/
│
├── dataset/
│   │
│   ├── job_application/
│   │   ├── text/           # Raw .txt documents
│   │   ├── pdf/            # Digital .pdf documents
│   │   ├── scanned/        # Simulated scanned .png images (OCR testing)
│   │   └── labels/         # Ground truth .json labels with exact spans
│   │
│   ├── medical_intake/
│   │   ├── text/
│   │   ├── pdf/
│   │   ├── scanned/
│   │   └── labels/
│   │
│   ├── loan_application/
│   │   ├── text/
│   │   ├── pdf/
│   │   ├── scanned/
│   │   └── labels/
│   │
│   ├── rental_agreement/
│   │   ├── text/
│   │   ├── pdf/
│   │   ├── scanned/
│   │   └── labels/
│   │
│   └── splits/             # Stratified dataset splits
│       ├── train.json
│       ├── validation.json
│       └── test.json
│
├── src/
│   │
│   ├── generator/
│   │   ├── __init__.py
│   │   └── generate_documents.py   # Synthetic generator & dataset splitter
│   │
│   ├── policies/
│   │   ├── __init__.py
│   │   └── necessity_policy.py     # Purpose definitions & necessity policies
│   │
│   └── utils/
│       ├── __init__.py
│       ├── pdf_generator.py        # ReportLab PDF rendering
│       ├── scanner_simulator.py    # Pillow OCR degradation simulator
│       └── dataset_validator.py    # 10-point dataset validation suite
│
├── templates/
│   ├── job_application.txt
│   ├── medical_intake.txt
│   ├── loan_application.txt
│   └── rental_agreement.txt
│
├── requirements.txt
├── main.py                         # CLI entrypoint
└── README.md
```

---

## 🏷️ Necessity Classification Policies

The framework defines three standardized necessity tiers:

| Necessity Label | Definition | Research Context |
| :--- | :--- | :--- |
| `necessary` | Indispensable for fulfilling the core declared purpose of the document. | Exclusion hinders primary processing (e.g., Patient Name and Medical History in Medical Intake). |
| `contextual` | Conditionally relevant depending on jurisdiction, billing, or specific operational workflows. | Not universally required for core evaluation (e.g., Home Address in Job Applications, Insurance Policy Number in emergency triage). |
| `unnecessary` | Irrelevant or disproportionate to the declared purpose, creating privacy risks or bias exposure. | PII that should be redacted/minimized (e.g., Date of Birth or Religion in Job Applications, Bank Account Numbers in Rental Applications). |

### Purpose-Driven Policy Comparison Matrix

| PII Field | Job Application | Medical Intake | Loan Application | Rental Agreement |
| :--- | :--- | :--- | :--- | :--- |
| **Full Name** | `necessary` | `necessary` | `necessary` | `necessary` |
| **Date of Birth** | `unnecessary` | `necessary` | `necessary` | `unnecessary` |
| **Phone / Email** | `necessary` | `necessary` | `necessary` | `necessary` |
| **Home Address** | `contextual` | `contextual` | `necessary` | `necessary` |
| **National ID / SSN** | `unnecessary` | `unnecessary` | `necessary` | `contextual` |
| **Marital Status** | `unnecessary` | `contextual` | `contextual` | `unnecessary` |
| **Religion** | `unnecessary` | `contextual` | `unnecessary` | `unnecessary` |
| **Medical History** | `unnecessary` | `necessary` | `unnecessary` | `unnecessary` |
| **Bank Account No.** | `unnecessary` | `unnecessary` | `contextual` | `unnecessary` |
| **Credit Score** | `unnecessary` | `unnecessary` | `necessary` | `contextual` |
| **Employment / Income** | `necessary` | `contextual` | `necessary` | `necessary` |

---

## 🏷️ Ground Truth Label Structure

Each generated document is paired with a ground truth JSON file in `dataset/<doc_type>/labels/<doc_id>.json`:

```json
{
    "document_id": "job_001",
    "document_type": "job_application",
    "document_purpose": "To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.",
    "fields": [
        {
            "field_type": "full_name",
            "field_name": "Full Name",
            "field_value": "Sarah Jenkins",
            "necessity_label": "necessary",
            "reason": "Required to unambiguously identify the candidate, manage application tracking, and conduct hiring correspondence.",
            "span": {
                "start": 268,
                "end": 281
            }
        },
        {
            "field_type": "date_of_birth",
            "field_name": "Date of Birth",
            "field_value": "April 14, 1993",
            "necessity_label": "unnecessary",
            "reason": "Date of birth is generally not required for evaluating qualifications during initial employment screening and may create discrimination concerns.",
            "span": {
                "start": 304,
                "end": 318
            }
        }
    ]
}
```

---

## 🚀 Setup & Installation (Windows)

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Create and Activate Virtual Environment (Optional but Recommended)
Open PowerShell in the project directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(If script execution is restricted, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 💻 CLI Usage

### Generate Complete Dataset (Default: 400 documents, 100 scanned, 70/15/15 split, & validation)
```powershell
python main.py
```

### Customize Document Count
To generate a custom number of documents per type (e.g. 50 per type = 200 total):
```powershell
python main.py --count 50
```

### Validate Existing Dataset
Runs the 10-point structural, semantic, and span validation suite without regenerating files:
```powershell
python main.py --validate
```

### Clean Dataset
Removes all generated files and resets the `dataset/` directory:
```powershell
python main.py --clean
```

### Advanced Options
```powershell
# Custom scanned percentage (e.g., 30%) and custom random seed
python main.py --count 100 --scanned-ratio 0.30 --seed 12345 --clean
```

---

## 🔍 Phase 2: PII Detection & Multi-Strategy Evaluation

Phase 2 integrates **Microsoft Presidio** (`presidio-analyzer`, `presidio-anonymizer`) backed by **spaCy** (`en_core_web_sm`) and domain-specific custom recognizers to detect PII entities in both clean digital text and scanned/degraded documents.

### 🧠 Custom Domain Recognizers
In addition to Presidio's default recognizers (e.g. `PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `LOCATION`, `US_SSN`), custom pattern and context-aware recognizers are registered for domain-specific fields defined in `src/policies/necessity_policy.py`:
- **Financial & Legal**: `bank_account_number`, `credit_score`, `annual_income`/`income`, `biometric_information`
- **Demographics & Personal**: `marital_status`, `religion`, `gender`, `date_of_birth`, `national_id`
- **Employment & Experience**: `employment_status`, `employer_name`, `job_title`, `education`, `work_history`, `skills`
- **Medical & Tenancy**: `medical_history`, `current_medications`, `allergies`, `insurance_number`, `emergency_contact`, `rental_history`

### 📊 Multi-Strategy Evaluation Protocol
Because optical character recognition (OCR) and layout reflow can cause character offset shifts in scanned documents, the framework evaluates detection performance across three distinct matching criteria:

1. **Exact Span Match**: Predicted entity type matches ground truth AND character offsets match exactly (`pred_span == gt_span`).
2. **Partial Overlap Match**: Predicted entity type matches ground truth AND character spans overlap (`min(pred_end, gt_end) - max(pred_start, gt_start) > 0`).
3. **Field Presence Match**: Evaluates document-level recall—whether a field type present in ground truth is successfully identified anywhere within the document.

### 📉 Clean vs. OCR Degradation Analysis
Detection performance is computed separately on:
- **Clean Text Documents**: Evaluates baseline NER and pattern accuracy on digital text.
- **Scanned OCR Documents**: Quantifies the empirical accuracy penalty ($\Delta F_1 = F_{1,\text{Clean}} - F_{1,\text{OCR}}$) introduced by optical noise, skew, blur, and OCR transcription errors.

---

## 💻 Running Detection and Evaluation

### Run Detection & Evaluation Pipeline (Default)
```powershell
python main.py --detect --evaluate
```

### Run Only Detection
Generates predictions and saves per-document JSON records to `results/predictions/clean/` and `results/predictions/ocr/`:
```powershell
python main.py --detect
```

### Run Only Evaluation
Evaluates existing prediction files against ground truth labels and exports report files:
```powershell
python main.py --evaluate
```

### Run Full End-to-End Workflow (Phase 1 + Phase 2)
Generates the dataset, creates stratified splits, validates integrity, runs Presidio + OCR detection, and outputs evaluation reports:
```powershell
python main.py --run-all
```

---

## ⚖️ Phase 3: Necessity Classification (Rule + ML Hybrid Engine)

Phase 3 implements the hybrid necessity assessment formula:

$$N(f, p) = \alpha \cdot R(f, p) + (1 - \alpha) \cdot M(f, p)$$

where:
- **$R(f, p) \in \{0.0, 0.5, 1.0\}$**: Deterministic rule lookup based on the domain policy in `src/policies/necessity_policy.py`.
- **$M(f, p) \in [0.0, 1.0]$**: Learned continuous/ordinal regressor (Random Forest with TF-IDF context embeddings) weighted by inverse class frequency.
- **$\alpha \in [0.0, 1.0]$**: Optimal weighting parameter chosen via grid search on the validation set.
- **$N(f, p)$**: Final ordinal necessity score:
  - **$N(f,p) < 0.5$**: Flagged as **Unnecessary PII Exposure** (e.g. National ID or Religion in Job Applications).
  - **$0.5 \le N(f,p) < 0.67$**: Categorized as **Contextual PII** (e.g. Home Address in Job Applications).
  - **$N(f,p) \ge 0.67$**: Categorized as **Necessary PII** (e.g. Full Name, Email, Medical History in Medical Intake).

---

## 💻 Running Phase 3 (Necessity Classification)

### Run Complete Phase 3 Pipeline
Executes ML training on `train` split, Alpha grid search on `validation` split, held-out evaluation on `test` split, end-to-end compounding error test, and generates 8 sample audit reports:
```powershell
python main.py --necessity
```

### Generate Audit Report for a Specific Document
```powershell
python main.py --report job_001
python main.py --report med_001
```

### Run Full End-to-End Pipeline (Phases 1, 2, and 3)
```powershell
python main.py --run-all
```

---

## 📁 Phase 3 Output Files & Artifacts

| File | Description |
| :--- | :--- |
| `results/necessity_alpha_grid_search.csv` | Validation set Alpha ($\alpha$) vs. MAE/RMSE grid search table. |
| `results/necessity_evaluation_metrics.json` | Complete evaluation metrics comparing Rule-only, ML-only, and Hybrid models on the test set, per-domain breakdowns, disagreement analyses, and compounding error stats. |
| `results/necessity_reports/<doc_id>_necessity_report.json` | Per-document machine-readable JSON necessity audit report. |
| `results/necessity_reports/<doc_id>_necessity_report.md` | Per-document human-readable Markdown privacy audit report displaying $R(f,p)$, $M(f,p)$, $N(f,p)$, flagging status, and research rationale. |
| `results/necessity_reports/all_sample_necessity_reports.md` | Combined audit report artifact across 8 representative documents (2 per domain). |
