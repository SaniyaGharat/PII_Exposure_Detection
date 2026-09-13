# PII Necessity Audit Report: `loan_001`
**Domain:** `loan_application` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect financial and personal information required to evaluate an applicant's eligibility and risk for a loan or credit service.

**Summary:** Flagged **3 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Applicant Full Name** | `Frederick Clark` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Mandatory for establishing legal borrower identity and executing legally binding credit agreements. |
| **Date of Birth** | `September 26, 1963` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to verify legal age of majority for credit contracts and pull accurate consumer credit bureau reports. |
| **Marital Status** | `Single` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Relevant in community property jurisdictions or joint loan applications, but restricted under fair lending laws for individual applications. |
| **Religion** | `Christianity` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious affiliation is completely irrelevant to credit risk assessment and its collection violates the Equal Credit Opportunity Act (ECOA). |
| **Phone Number** | `301.476.5636x004` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for customer identity verification, fraud prevention multi-factor authentication, and account servicing. |
| **Email Address** | `frederick.clark@yahoo.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for delivery of mandated Truth in Lending disclosures, electronic contract execution, and official statements. |
| **Residential Address** | `7118 Jennifer Mill Apt. 742, Port A` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Mandatory under Know Your Customer (KYC) and Anti-Money Laundering (AML) regulations to establish legal residential domicile. |
| **Employment Status** | `Contractor / Freelancer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for evaluating income continuity, employment stability, and the borrower's recurring repayment capacity. |
| **Employer Name** | `Figueroa, Jackson and Powers` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for independent employment verification and underwriting validation of stated income sources. |
| **Annual Income** | `$103,000.00 USD` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Fundamental metric for calculating Debt-to-Income (DTI) ratio and determining loan affordability and credit limits. |
| **Bank Account Number** | `ACCT-9863781331` | 0.50 | 0.52 | **0.50** | 🟡 CONTEXTUAL | Contextual during pre-qualification screening; necessary later for direct loan disbursement and automated clearing house (ACH) repayments. |
| **Credit Score** | `738 (FICO Score 8)` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Primary quantitative metric reflecting historical credit risk, default probability, and determining loan interest pricing. |
| **Medical History** | `Hypertension (diagnosed 2018), Mild` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Health and medical conditions are irrelevant to financial solvency evaluation and collecting them exposes high-liability sensitive health data. |
| **Biometric Identifier** | `SHA256:c3782a44e413c018bba78315 (Bi` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Biometric markers are disproportionate and unnecessary for standard consumer credit evaluation, posing severe privacy risks. |