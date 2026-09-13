# PII Necessity Audit Report: `rent_001`
**Domain:** `rental_agreement` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect information required to evaluate a tenant and establish a rental relationship between the tenant and property owner.

**Summary:** Flagged **6 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Tenant Full Name** | `Eric Fitzgerald` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `(616)510-7051` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Email Address** | `eric.fitzgerald@hotmail.com` | 1.00 | 0.99 | **0.99** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 97.3%). |
| **National ID / SSN** | `596-54-9231` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.5%). |
| **Marital Status** | `Divorced` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Religion** | `Agnostic` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Current Residential Address** | `5295 Shelia Lodge, Monroeton, CA 25` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employment Status** | `Self-Employed` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employer Name** | `Kramer and Sons` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Flagged by learned contextual pattern (Model Confidence: 0.0%). |
| **Monthly / Annual Income** | `$9,383.00 / month` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Bank Account Number** | `ACCT-1772303297` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.8%). |
| **Previous Rental History** | `Previous Address: 70493 Thompson Su` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Emergency Contact** | `John Huff (Sibling) - Tel: 797-211-` | 0.50 | 0.28 | **0.28** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 43.9%). |
| **Medical History** | `Mild persistent Asthma, seasonal al` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |