# PII Necessity Audit Report: `rent_002`
**Domain:** `rental_agreement` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect information required to evaluate a tenant and establish a rental relationship between the tenant and property owner.

**Summary:** Flagged **6 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Tenant Full Name** | `Dana Stevens` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `001-734-832-4064x2429` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Email Address** | `dana.stevens@gmail.com` | 1.00 | 0.99 | **0.99** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 97.4%). |
| **National ID / SSN** | `897-45-1959` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Marital Status** | `Widowed` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Religion** | `Unaffiliated` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Current Residential Address** | `3244 Baker Overpass, Bethstad, WI 8` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employment Status** | `Self-Employed` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employer Name** | `Willis-Watson` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Flagged by learned contextual pattern (Model Confidence: 0.0%). |
| **Monthly / Annual Income** | `$7,088.00 / month` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Bank Account Number** | `ACCT-5293274004` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.8%). |
| **Previous Rental History** | `Previous Address: 96289 Victoria Me` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Emergency Contact** | `Michael Gordon (Sibling) - Tel: 001` | 0.50 | 0.03 | **0.03** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 93.5%). |
| **Medical History** | `Type 2 Diabetes Mellitus (managed v` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |