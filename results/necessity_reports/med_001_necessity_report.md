# PII Necessity Audit Report: `med_001`
**Domain:** `medical_intake` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **6 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Brian Meyer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `January 29, 1986` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `+1-526-618-9141x173` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Home Address** | `6420 Lozano Spurs, Riveratown, AL 8` | 0.50 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Marital Status** | `Single` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Occupation** | `Archaeologist` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Religious Affiliation** | `Buddhism` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **National ID / SSN** | `546-85-7560` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Health Insurance Policy Number** | `KSR-20555833` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Emergency Contact** | `Brian Andrews (Sibling) - Phone: 32` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Allergies & Sensitivities** | `Aspirin (bronchospasm), Codeine (na` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Current Medications** | `Albuterol HFA Inhaler 90mcg 2 puffs` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Past Medical History** | `No significant past medical history` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |