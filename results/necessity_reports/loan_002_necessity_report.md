# PII Necessity Audit Report: `loan_002`
**Domain:** `loan_application` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect financial and personal information required to evaluate an applicant's eligibility and risk for a loan or credit service.

**Summary:** Flagged **3 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Applicant Full Name** | `Alex Nelson` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Mandatory for establishing legal borrower identity and executing legally binding credit agreements. |
| **Date of Birth** | `September 07, 1990` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to verify legal age of majority for credit contracts and pull accurate consumer credit bureau reports. |
| **Marital Status** | `Widowed` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Relevant in community property jurisdictions or joint loan applications, but restricted under fair lending laws for individual applications. |
| **Religion** | `Christianity` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious affiliation is completely irrelevant to credit risk assessment and its collection violates the Equal Credit Opportunity Act (ECOA). |
| **Phone Number** | `(923)208-3708x164` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for customer identity verification, fraud prevention multi-factor authentication, and account servicing. |
| **Email Address** | `alex.nelson@hotmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for delivery of mandated Truth in Lending disclosures, electronic contract execution, and official statements. |
| **Residential Address** | `63353 Christopher Manor, North Matt` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Mandatory under Know Your Customer (KYC) and Anti-Money Laundering (AML) regulations to establish legal residential domicile. |
| **Employment Status** | `Self-Employed` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for evaluating income continuity, employment stability, and the borrower's recurring repayment capacity. |
| **Employer Name** | `Robles Ltd` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for independent employment verification and underwriting validation of stated income sources. |
| **Annual Income** | `$65,000.00 USD` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Fundamental metric for calculating Debt-to-Income (DTI) ratio and determining loan affordability and credit limits. |
| **Bank Account Number** | `ACCT-2756070122` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Contextual during pre-qualification screening; necessary later for direct loan disbursement and automated clearing house (ACH) repayments. |
| **Credit Score** | `829 (FICO Score 8)` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Primary quantitative metric reflecting historical credit risk, default probability, and determining loan interest pricing. |
| **Medical History** | `Type 2 Diabetes Mellitus (managed v` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Health and medical conditions are irrelevant to financial solvency evaluation and collecting them exposes high-liability sensitive health data. |
| **Biometric Identifier** | `SHA256:dafb0fc69cd9e7f8c8d695c7 (Bi` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Biometric markers are disproportionate and unnecessary for standard consumer credit evaluation, posing severe privacy risks. |