# Sample Necessity Classification Audit Reports (8 Representative Documents)

# PII Necessity Audit Report: `job_001`
**Domain:** `job_application` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.

**Summary:** Flagged **4 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Full Name** | `Margaret Johnson` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to unambiguously identify the candidate, manage application tracking, and conduct hiring correspondence. |
| **Date of Birth** | `August 11, 1973` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Date of birth is generally not required for evaluating qualifications during initial employment screening and may create discrimination concerns. |
| **Gender** | `Female` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Gender is not required for qualification evaluation, though occasionally collected under optional equal employment opportunity (EEO) demographic monitoring. |
| **Marital Status** | `Domestic Partnership` | 0.00 | 0.05 | **0.00** | 🔴 **FLAGGED** | Marital status is irrelevant to assessing job competence and creates potential exposure to marital status or gender discrimination. |
| **Religion** | `Agnostic` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious beliefs are completely irrelevant to job performance and introduce unlawful bias risks under employment regulations. |
| **National ID / SSN** | `132-13-2535` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Government national identification numbers are unnecessary at initial screening and introduce high identity theft exposure. |
| **Email Address** | `margaret.johnson@hotmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required as a primary electronic communication channel for interview scheduling and official employment notifications. |
| **Phone Number** | `001-260-501-3389` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for direct contact, telephone screening sessions, and urgent recruitment updates. |
| **Home Address** | `79402 Peterson Drives Apt. 511, Dav` | 0.50 | 0.57 | **0.50** | 🟡 CONTEXTUAL | Full street address is unnecessary for initial screening (city/region suffices), but may be required for local payroll tax jurisdictions or commute assessment. |
| **Position Applied For** | `Senior Software Engineer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Specifies the target role against which candidate qualifications and criteria are evaluated. |
| **Education** | `M.S. in Data Analytics - University` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for verifying required academic degrees, institutional background, and formal qualifications. |
| **Work History** | `1. Senior Software Engineer at Sanc` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for evaluating candidate's prior professional experience, relevant responsibilities, and career trajectory. |
| **Skills & Competencies** | `Financial Modeling, Risk Analysis, ` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Directly reflects technical, operational, and domain competencies required for job performance. |
---

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
---

# PII Necessity Audit Report: `med_001`
**Domain:** `medical_intake` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **1 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Brian Meyer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for patient identification, medical record linkage, and preventing catastrophic misidentification in clinical care. |
| **Date of Birth** | `January 28, 1986` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Crucial for clinical safety, age-dependent pharmaceutical dosage calculations, developmental assessment, and primary patient record matching. |
| **Phone Number** | `+1-526-618-9141x173` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for appointment reminders, urgent clinical test result notifications, and post-procedure follow-ups. |
| **Home Address** | `6420 Lozano Spurs, Riveratown, AL 8` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Used for patient billing, demographic analysis, and local public health reporting, though secondary to immediate clinical diagnosis. |
| **Marital Status** | `Divorced` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | May provide helpful context regarding home support network and surrogate decision-makers, but not universally necessary for diagnostics. |
| **Occupation** | `Archaeologist` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Provides relevant context for evaluating occupational exposures, repetitive stress injuries, or physical disability accommodations. |
| **Religious Affiliation** | `Sikhism` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Contextual in clinical settings to respect medical restrictions (e.g., blood transfusions, dietary rules, end-of-life pastoral care), but optional. |
| **National ID / SSN** | `206-83-9313` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Standard government national IDs are unnecessary when unique Medical Record Numbers (MRN) or insurance IDs exist, creating avoidable exposure. |
| **Health Insurance Policy Number** | `BLU-30767532` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Necessary for healthcare claims billing and insurance verification, but not strictly required for emergency or direct self-pay clinical triage. |
| **Emergency Contact** | `Brian Andrews (Partner) - Phone: 32` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Vital in acute medical situations, patient incapacitation, or urgent medical decisions where patient proxy consent is needed. |
| **Allergies & Sensitivities** | `Aspirin (bronchospasm), Codeine (na` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | High-priority safety data required to prevent life-threatening anaphylaxis, drug allergies, and cross-reactive interventions. |
| **Current Medications** | `Metformin 500mg PO BID with meals, ` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Critical for preventing adverse drug-drug interactions, polypharmacy complications, and dosage conflicts. |
| **Past Medical History** | `Hypertension (diagnosed 2018), Mild` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential clinical context for differential diagnosis, identifying chronic comorbidities, and planning safe therapeutic interventions. |
---

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
---

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
---

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
---

# PII Necessity Audit Report: `rent_001`
**Domain:** `rental_agreement` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect information required to evaluate a tenant and establish a rental relationship between the tenant and property owner.

**Summary:** Flagged **4 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Tenant Full Name** | `Eric Fitzgerald` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to identify the legal tenant and execute an enforceable residential lease contract. |
| **Phone Number** | `(616)510-7051` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for property management communication, maintenance requests, and emergency notifications. |
| **Email Address** | `eric.fitzgerald@hotmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for electronic lease execution, rent payment portal access, and digital delivery of legal notices. |
| **National ID / SSN** | `492-21-2678` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Often requested for credit and criminal background checks, but can be replaced by direct third-party screening services to reduce exposure. |
| **Marital Status** | `Single` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Marital status is irrelevant to rental qualification and introduces unlawful discrimination risks under fair housing standards. |
| **Religion** | `Sikhism` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious beliefs are completely irrelevant to rental qualifications and collecting them violates the Fair Housing Act. |
| **Current Residential Address** | `5295 Shelia Lodge, Monroeton, CA 25` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to verify current tenancy, assess residency stability, and contact previous landlords for reference checks. |
| **Employment Status** | `Self-Employed` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Directly indicates financial stability and ongoing ability to meet recurring monthly rent obligations. |
| **Employer Name** | `Kramer and Sons` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Useful for independent employment verification, though verifiable pay stubs or bank statements can serve as alternative proof. |
| **Monthly / Annual Income** | `$4,660.00 / month` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for determining rent-to-income ratio (standard industry threshold of monthly income >= 2.5x to 3x rent). |
| **Bank Account Number** | `ACCT-9078786223` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Full banking account numbers are unnecessary during rental application screening and expose the applicant to financial fraud risks. |
| **Previous Rental History** | `Previous Address: 70493 Thompson Su` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Critical for evaluating past tenancy behavior, timely rent payment record, lease compliance, and eviction history. |
| **Emergency Contact** | `John Huff (Sibling) - Tel: 797-211-` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Valuable in urgent property situations, abandonment, or tenant emergencies, but secondary to initial financial qualification. |
| **Medical History** | `Type 2 Diabetes Mellitus (managed v` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Medical history has no bearing on tenancy eligibility and exposes private health data in violation of fair housing privacy principles. |
---

# PII Necessity Audit Report: `rent_002`
**Domain:** `rental_agreement` | **Alpha:** `1.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect information required to evaluate a tenant and establish a rental relationship between the tenant and property owner.

**Summary:** Flagged **4 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Tenant Full Name** | `Dana Stevens` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to identify the legal tenant and execute an enforceable residential lease contract. |
| **Phone Number** | `001-734-832-4064x2429` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for property management communication, maintenance requests, and emergency notifications. |
| **Email Address** | `dana.stevens@gmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required for electronic lease execution, rent payment portal access, and digital delivery of legal notices. |
| **National ID / SSN** | `871-27-3340` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Often requested for credit and criminal background checks, but can be replaced by direct third-party screening services to reduce exposure. |
| **Marital Status** | `Single` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Marital status is irrelevant to rental qualification and introduces unlawful discrimination risks under fair housing standards. |
| **Religion** | `Unaffiliated` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Religious beliefs are completely irrelevant to rental qualifications and collecting them violates the Fair Housing Act. |
| **Current Residential Address** | `3244 Baker Overpass, Bethstad, WI 8` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Required to verify current tenancy, assess residency stability, and contact previous landlords for reference checks. |
| **Employment Status** | `Retired` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Directly indicates financial stability and ongoing ability to meet recurring monthly rent obligations. |
| **Employer Name** | `Willis-Watson` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Useful for independent employment verification, though verifiable pay stubs or bank statements can serve as alternative proof. |
| **Monthly / Annual Income** | `$9,770.00 / month` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Essential for determining rent-to-income ratio (standard industry threshold of monthly income >= 2.5x to 3x rent). |
| **Bank Account Number** | `ACCT-9626333315` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Full banking account numbers are unnecessary during rental application screening and expose the applicant to financial fraud risks. |
| **Previous Rental History** | `Previous Address: 96289 Victoria Me` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Critical for evaluating past tenancy behavior, timely rent payment record, lease compliance, and eviction history. |
| **Emergency Contact** | `Michael Gordon (Sibling) - Tel: 001` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Valuable in urgent property situations, abandonment, or tenant emergencies, but secondary to initial financial qualification. |
| **Medical History** | `No significant past medical history` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Medical history has no bearing on tenancy eligibility and exposes private health data in violation of fair housing privacy principles. |
---
