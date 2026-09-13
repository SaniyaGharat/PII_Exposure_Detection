# PII Necessity Audit Report: `job_002`
**Domain:** `job_application` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.

**Summary:** Flagged **4 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Full Name** | `Robert Blair` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to unambiguously identify the candidate, manage application tracking, and conduct hiring correspondence. |
| **Date of Birth** | `April 21, 1992` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Date of birth is generally not required for evaluating qualifications during initial employment screening and may create discrimination concerns. |
| **Gender** | `Male` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Gender is not required for qualification evaluation, though occasionally collected under optional equal employment opportunity (EEO) demographic monitoring. |
| **Marital Status** | `Widowed` | 0.00 | 0.03 | **0.00** | 🔴 **FLAGGED** | Marital status is irrelevant to assessing job competence and creates potential exposure to marital status or gender discrimination. |
| **Religion** | `Prefer not to disclose` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious beliefs are completely irrelevant to job performance and introduce unlawful bias risks under employment regulations. |
| **National ID / SSN** | `384-10-3615` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Government national identification numbers are unnecessary at initial screening and introduce high identity theft exposure. |
| **Email Address** | `robert.blair@yahoo.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required as a primary electronic communication channel for interview scheduling and official employment notifications. |
| **Phone Number** | `001-831-603-4131` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for direct contact, telephone screening sessions, and urgent recruitment updates. |
| **Home Address** | `55341 Amanda Gardens Apt. 764, Lake` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Full street address is unnecessary for initial screening (city/region suffices), but may be required for local payroll tax jurisdictions or commute assessment. |
| **Position Applied For** | `Systems Architect` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Specifies the target role against which candidate qualifications and criteria are evaluated. |
| **Education** | `B.S. in Information Systems - Unive` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for verifying required academic degrees, institutional background, and formal qualifications. |
| **Work History** | `1. Systems Architect at Martinez, N` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for evaluating candidate's prior professional experience, relevant responsibilities, and career trajectory. |
| **Skills & Competencies** | `Statistical Analysis, R, Tableau, D` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Directly reflects technical, operational, and domain competencies required for job performance. |