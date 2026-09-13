# PII Necessity Audit Report: `med_002`
**Domain:** `medical_intake` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **6 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Heather Rhodes` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `September 08, 1972` | 1.00 | 0.99 | **0.99** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 98.3%). |
| **Phone Number** | `001-711-700-2255x7941` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Home Address** | `66746 Marsh Run, North David, VA 08` | 0.50 | 0.08 | **0.08** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 84.5%). |
| **Marital Status** | `Married` | 0.50 | 0.42 | **0.42** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 15.1%). |
| **Occupation** | `Armed forces training and education` | 0.50 | 0.45 | **0.45** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 9.8%). |
| **Religious Affiliation** | `Islam` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **National ID / SSN** | `622-91-2868` | 0.00 | 0.01 | **0.01** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 97.3%). |
| **Health Insurance Policy Number** | `KSR-78444607` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Emergency Contact** | `Dr. Ashley Pruitt (Sibling) - Phone` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Allergies & Sensitivities** | `Sulfa antibiotics (severe skin reac` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Current Medications** | `Albuterol HFA Inhaler 90mcg 2 puffs` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Past Medical History** | `Mild persistent Asthma, seasonal al` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |