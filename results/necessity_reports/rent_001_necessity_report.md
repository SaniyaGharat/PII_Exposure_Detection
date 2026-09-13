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