# PII Necessity Audit Report: `med_002`
**Domain:** `medical_intake` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **1 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Heather Rhodes` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for patient identification, medical record linkage, and preventing catastrophic misidentification in clinical care. |
| **Date of Birth** | `September 07, 1972` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Crucial for clinical safety, age-dependent pharmaceutical dosage calculations, developmental assessment, and primary patient record matching. |
| **Phone Number** | `001-711-700-2255x7941` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for appointment reminders, urgent clinical test result notifications, and post-procedure follow-ups. |
| **Home Address** | `66746 Marsh Run, North David, VA 08` | 0.50 | 0.62 | **0.50** | 🟡 CONTEXTUAL | Used for patient billing, demographic analysis, and local public health reporting, though secondary to immediate clinical diagnosis. |
| **Marital Status** | `Domestic Partnership` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | May provide helpful context regarding home support network and surrogate decision-makers, but not universally necessary for diagnostics. |
| **Occupation** | `Armed forces training and education` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Provides relevant context for evaluating occupational exposures, repetitive stress injuries, or physical disability accommodations. |
| **Religious Affiliation** | `Sikhism` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Contextual in clinical settings to respect medical restrictions (e.g., blood transfusions, dietary rules, end-of-life pastoral care), but optional. |
| **National ID / SSN** | `217-45-4705` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Standard government national IDs are unnecessary when unique Medical Record Numbers (MRN) or insurance IDs exist, creating avoidable exposure. |
| **Health Insurance Policy Number** | `UHC-85291541` | 0.50 | 0.49 | **0.50** | 🟡 CONTEXTUAL | Necessary for healthcare claims billing and insurance verification, but not strictly required for emergency or direct self-pay clinical triage. |
| **Emergency Contact** | `Dr. Ashley Pruitt (Sibling) - Phone` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Vital in acute medical situations, patient incapacitation, or urgent medical decisions where patient proxy consent is needed. |
| **Allergies & Sensitivities** | `No Known Drug Allergies (NKDA), No ` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | High-priority safety data required to prevent life-threatening anaphylaxis, drug allergies, and cross-reactive interventions. |
| **Current Medications** | `Levothyroxine 75mcg PO daily in mor` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Critical for preventing adverse drug-drug interactions, polypharmacy complications, and dosage conflicts. |
| **Past Medical History** | `No significant past medical history` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential clinical context for differential diagnosis, identifying chronic comorbidities, and planning safe therapeutic interventions. |