# PII Necessity Audit Report: `job_001`
**Domain:** `job_application` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.

**Summary:** Flagged **5 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Full Name** | `Margaret Johnson` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `August 12, 1973` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Gender** | `Female` | 0.50 | 0.48 | **0.48** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 3.1%). |
| **Marital Status** | `Single` | 0.00 | 0.10 | **0.10** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 80.4%). |
| **Religion** | `Christianity` | 0.00 | 0.02 | **0.02** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 96.6%). |
| **National ID / SSN** | `195-37-4811` | 0.00 | 0.03 | **0.03** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 93.7%). |
| **Email Address** | `margaret.johnson@hotmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `001-260-501-3389` | 1.00 | 0.99 | **0.99** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 98.3%). |
| **Home Address** | `79402 Peterson Drives Apt. 511, Dav` | 0.50 | 0.55 | **0.55** | 🟡 CONTEXTUAL | Flagged by learned contextual pattern (Model Confidence: 9.9%). |
| **Position Applied For** | `Senior Software Engineer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Education** | `M.S. in Data Analytics - University` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Work History** | `1. Senior Software Engineer at Sanc` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Skills & Competencies** | `Network Security, Penetration Testi` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |