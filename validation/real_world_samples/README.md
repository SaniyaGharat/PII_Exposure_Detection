# Real-World Template Validation Dataset (Sanity-Check Samples)

## 📌 Overview & Purpose

This directory (`validation/real_world_samples/`) contains a curated, coarse real-world validation benchmark dataset created for the **PII Exposure Detection & Necessity Minimization Framework**.

The primary objective of this validation set is to provide a realistic "out-of-distribution" sanity check to evaluate how well the PII detection pipeline (Presidio + OCR) and necessity classification engines generalize to authentic, publicly used industry document layouts, formatting conventions, and field structures.

---

## 🔒 Privacy, Safety & Ethical Compliance

> [!IMPORTANT]
> **Strict Privacy Guarantee**:
> - **Zero Real Personal Data**: No personal data of any real person was used, collected, or stored in this dataset.
> - **Synthetic Completion**: All document fields are populated with entirely synthetic, fictional values.
> - **Safe Domain Placeholders**: All email addresses strictly utilize RFC 2606 reserved domains (`@example.com`).
> - **Fictional Phone Numbers**: All telephone numbers use the North American NANPA 555 fictional exchange prefix (`202-555-XXXX`).
> - **Safe Identifier Masks**: Any sensitive identifiers or member IDs utilize obvious artificial pattern masks (e.g., `SHM-000-12345`, `000-00-0000`, `MRN-00000-X`).
> - **No Sensitive Entity Involvement**: No real patient records, actual bank customers, or live job applicants are represented.

---

## 📄 Publicly Available Underlying Templates (4 Real-World Domains)

The structural layouts and field nomenclatures are directly derived from publicly accessible, standardized blank template documents across all 4 target domains:

| Document ID | Domain | Underlying Public Template Source | Structure Preserved |
| :--- | :--- | :--- | :--- |
| [`real_job_001.txt`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/real_world_samples/real_job_001.txt) | `job_application` | UK ICO / Acas Standard Job Application Form Template | Personal details, education, employment history, supporting statement, references, UK GDPR declaration |
| [`real_bank_001.txt`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/real_world_samples/real_bank_001.txt) | `loan_application` | UCO Bank Retail Credit & Lead Generation Application | Customer identity, regional address/state/district, loan requirement, tentative amount, DNC override consent |
| [`real_medical_001.txt`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/real_world_samples/real_medical_001.txt) | `medical_intake` | Greenlight Med Standard Clinical Patient Intake Form | Patient demographics, contact info, emergency contacts, insurance subscriber & member IDs, health history, medications, allergies, confirmation |
| [`real_rent_001.txt`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/real_world_samples/real_rent_001.txt) | `rental_agreement` | Standard US Residential Lease Application (NARPM / Property Management Format) | Prospective tenant identity, current landlord info, employment & supervisor verification, checking account details, FCRA credit disclosure |

---

## 🏷️ Annotations & Summary Statistics ([`dataset_summary.json`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/real_world_samples/dataset_summary.json))

- **Total Documents**: 4 (1 Job Application, 1 Bank Loan, 1 Medical Intake, 1 Rental Agreement)
- **Total Hand-Labeled PII Fields**: 51

---

## 📈 Final Real-World Performance & Generalization Findings

Execution of [`validation/run_real_world_check.py`](file:///c:/Users/Saniya%20Gharat/Desktop/Projects/PII_Exposure_Detection/validation/run_real_world_check.py) evaluates both baseline detection and the unmodified pre-filter across all 4 templates:

| Document ID | Domain | Baseline Precision / Recall | Pre-Filtered Precision / Recall | Measured FP Reduction | Generalization Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `real_bank_001` | `loan_application` | 33.3% / 60.0% ($12\text{ FP}$) | **54.5% / 60.0%** ($5\text{ FP}$) | **-7 FPs (-58.3%)** | *Tuned sample* |
| `real_job_001` | `job_application` | 43.5% / 92.3% ($26\text{ FP}$) | **62.5% / 92.3%** ($12\text{ FP}$) | **-14 FPs (-53.8%)** | *Tuned sample* |
| `real_medical_001` | `medical_intake` | 52.4% / 82.4% ($20\text{ FP}$) | **73.3% / 82.4%** ($8\text{ FP}$) | **-12 FPs (-60.0%)** | *Tuned sample* |
| **`real_rent_001`** | `rental_agreement` | 45.5% / 87.5% ($24\text{ FP}$) | **48.8% / 87.5%** ($21\text{ FP}$) | **-3 FPs (-12.5%)** | **Unseen Held-Out Template** |
| **MICRO AGGREGATE** | **All 4 Domains** | **45.33% / 84.31%** ($82\text{ FP}$) | **59.65% / 84.31%** ($46\text{ FP}$) | **-36 FPs (-43.90%)** | Full Corpus |

> [!WARNING]
> **Key Scientific Takeaway on Pre-Filter Generalization**:
> - On the 3 templates from which stopwords were derived, the filter reduced false positives by **~57%**.
> - On the completely unseen 4th template (`real_rent_001`), the stopword filter reduced false positives by only **12.5%** (only capturing generic duration regexes like `"2 years"` and `"4 years"`).
> - **Conclusion**: Lexical stopword filtering is a **documented, template-dependent heuristic**, not a universal fix. Universal PII detection recall remains strong (**84.31%**), but general layout filtering requires structural/visual boundary awareness rather than static wordlists.



