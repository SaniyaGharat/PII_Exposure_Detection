# PII Necessity Audit Report: `loan_001`
**Domain:** `loan_application` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect financial and personal information required to evaluate an applicant's eligibility and risk for a loan or credit service.

**Summary:** Flagged **3 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Applicant Full Name** | `Frederick Clark` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `September 27, 1963` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Marital Status** | `Widowed` | 0.50 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 99.1%). |
| **Religion** | `Islam` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Phone Number** | `301.476.5636x004` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Email Address** | `frederick.clark@yahoo.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Residential Address** | `7118 Jennifer Mill Apt. 742, Port A` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employment Status** | `Self-Employed` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employer Name** | `Figueroa, Jackson and Powers` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Annual Income** | `$112,000.00 USD` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Bank Account Number** | `ACCT-9415119956` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Flagged by learned contextual pattern (Model Confidence: 0.0%). |
| **Credit Score** | `798 (FICO Score 8)` | 1.00 | 0.86 | **0.86** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 71.7%). |
| **Medical History** | `Gastroesophageal Reflux Disease (GE` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Biometric Identifier** | `SHA256:c3782a44e413c018bba78315 (Bi` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |