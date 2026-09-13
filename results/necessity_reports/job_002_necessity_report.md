# PII Necessity Audit Report: `job_002`
**Domain:** `job_application` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.

**Summary:** Flagged **5 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Full Name** | `Renee Blair` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `April 22, 1992` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Gender** | `Female` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.0%). |
| **Marital Status** | `Single` | 0.00 | 0.01 | **0.01** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 98.9%). |
| **Religion** | `Hinduism` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **National ID / SSN** | `814-64-6574` | 0.00 | 0.01 | **0.01** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 98.9%). |
| **Email Address** | `renee.blair@yahoo.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `001-831-603-4131` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Home Address** | `55341 Amanda Gardens Apt. 764, Lake` | 0.50 | 0.71 | **0.71** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 42.0%). |
| **Position Applied For** | `Systems Architect` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Education** | `B.A. in Economics - Columbia Univer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Work History** | `1. Systems Architect at Martinez, N` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Skills & Competencies** | `Clinical Trial Management, GCP Comp` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |