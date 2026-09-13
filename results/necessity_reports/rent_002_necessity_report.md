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