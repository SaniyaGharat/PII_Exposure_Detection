# Sample Necessity Classification Audit Reports (8 Representative Documents)

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
---

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
---

# PII Necessity Audit Report: `med_001`
**Domain:** `medical_intake` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **6 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Brian Meyer` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `January 29, 1986` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Phone Number** | `+1-526-618-9141x173` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Home Address** | `6420 Lozano Spurs, Riveratown, AL 8` | 0.50 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Marital Status** | `Single` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Occupation** | `Archaeologist` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Religious Affiliation** | `Buddhism` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **National ID / SSN** | `546-85-7560` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.7%). |
| **Health Insurance Policy Number** | `KSR-20555833` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Emergency Contact** | `Brian Andrews (Sibling) - Phone: 32` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Allergies & Sensitivities** | `Aspirin (bronchospasm), Codeine (na` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Current Medications** | `Albuterol HFA Inhaler 90mcg 2 puffs` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Past Medical History** | `No significant past medical history` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
---

# PII Necessity Audit Report: `med_002`
**Domain:** `medical_intake` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.

**Summary:** Flagged **6 / 13** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Patient Full Name** | `Heather Rhodes` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `September 08, 1972` | 1.00 | 0.99 | **0.99** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 98.3%). |
| **Phone Number** | `001-711-700-2255x7941` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Home Address** | `66746 Marsh Run, North David, VA 08` | 0.50 | 0.08 | **0.08** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 84.5%). |
| **Marital Status** | `Married` | 0.50 | 0.42 | **0.42** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 15.1%). |
| **Occupation** | `Armed forces training and education` | 0.50 | 0.45 | **0.45** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 9.8%). |
| **Religious Affiliation** | `Islam` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **National ID / SSN** | `622-91-2868` | 0.00 | 0.01 | **0.01** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 97.3%). |
| **Health Insurance Policy Number** | `KSR-78444607` | 0.50 | 0.50 | **0.50** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 0.2%). |
| **Emergency Contact** | `Dr. Ashley Pruitt (Sibling) - Phone` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Allergies & Sensitivities** | `Sulfa antibiotics (severe skin reac` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Current Medications** | `Albuterol HFA Inhaler 90mcg 2 puffs` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Past Medical History** | `Mild persistent Asthma, seasonal al` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
---

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
---

# PII Necessity Audit Report: `loan_002`
**Domain:** `loan_application` | **Alpha:** `0.0` | **Flagging Threshold:** `< 0.5`

> **Document Purpose:** To collect financial and personal information required to evaluate an applicant's eligibility and risk for a loan or credit service.

**Summary:** Flagged **4 / 14** fields as **Unnecessary PII Exposure**.

| Field Name | Field Value | $R(f,p)$ | $M(f,p)$ | $N(f,p)$ | Status | Research Justification / Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Applicant Full Name** | `Alex Nelson` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Date of Birth** | `September 08, 1990` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Marital Status** | `Married` | 0.50 | 0.01 | **0.01** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 97.5%). |
| **Religion** | `Judaism` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Phone Number** | `(923)208-3708x164` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Email Address** | `alex.nelson@hotmail.com` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Residential Address** | `63353 Christopher Manor, North Matt` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employment Status** | `Employed Full-Time` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Employer Name** | `Robles Ltd` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Annual Income** | `$192,000.00 USD` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Bank Account Number** | `ACCT-4262396395` | 0.50 | 0.50 | **0.50** | 🟡 CONTEXTUAL | Flagged by learned contextual pattern (Model Confidence: 0.0%). |
| **Credit Score** | `652 (FICO Score 8)` | 1.00 | 1.00 | **1.00** | 🟢 NECESSARY | Flagged by learned contextual pattern (Model Confidence: 100.0%). |
| **Medical History** | `Hypertension (diagnosed 2018), Mild` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
| **Biometric Identifier** | `SHA256:dafb0fc69cd9e7f8c8d695c7 (Bi` | 0.00 | 0.00 | **0.00** | 🔴 **FLAGGED** | Flagged by learned contextual pattern (Model Confidence: 99.9%). |
---

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
---

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
---
