"""
PII Exposure Detection - Necessity Policy Engine
Defines standardized document purpose policies, field definitions, necessity labels,
and academically defensible justifications for research evaluation.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple


class NecessityLabel(str, Enum):
    """Standardized 3-tier necessity classification labels."""
    NECESSARY = "necessary"
    CONTEXTUAL = "contextual"
    UNNECESSARY = "unnecessary"


@dataclass(frozen=True)
class FieldPolicy:
    """Represents the necessity policy and research rationale for a single PII field."""
    field_type: str
    field_name: str
    document_type: str
    document_purpose: str
    necessity_label: NecessityLabel
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_type": self.field_type,
            "field_name": self.field_name,
            "document_type": self.document_type,
            "document_purpose": self.document_purpose,
            "necessity_label": self.necessity_label.value,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class DocumentPurposePolicy:
    """Represents a document type, its explicit purpose statement, and its field policies."""
    document_type: str
    display_name: str
    purpose: str
    fields: Dict[str, FieldPolicy]

    def get_field_policy(self, field_type: str) -> Optional[FieldPolicy]:
        return self.fields.get(field_type)


# --- Explicit Document Purpose Definitions ---
DOCUMENT_PURPOSES: Dict[str, str] = {
    "job_application": "To evaluate a candidate's qualifications, skills, education, and professional experience for potential employment.",
    "medical_intake": "To collect relevant patient information required for medical assessment, diagnosis, treatment, and healthcare administration.",
    "loan_application": "To collect financial and personal information required to evaluate an applicant's eligibility and risk for a loan or credit service.",
    "rental_agreement": "To collect information required to evaluate a tenant and establish a rental relationship between the tenant and property owner.",
}


# --- Detailed Policy Specifications for Each Document Type ---

JOB_APPLICATION_FIELDS: Dict[str, FieldPolicy] = {
    "full_name": FieldPolicy(
        field_type="full_name",
        field_name="Full Name",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required to unambiguously identify the candidate, manage application tracking, and conduct hiring correspondence."
    ),
    "email": FieldPolicy(
        field_type="email",
        field_name="Email Address",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required as a primary electronic communication channel for interview scheduling and official employment notifications."
    ),
    "phone": FieldPolicy(
        field_type="phone",
        field_name="Phone Number",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for direct contact, telephone screening sessions, and urgent recruitment updates."
    ),
    "work_history": FieldPolicy(
        field_type="work_history",
        field_name="Work History",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for evaluating candidate's prior professional experience, relevant responsibilities, and career trajectory."
    ),
    "education": FieldPolicy(
        field_type="education",
        field_name="Education",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for verifying required academic degrees, institutional background, and formal qualifications."
    ),
    "skills": FieldPolicy(
        field_type="skills",
        field_name="Skills & Competencies",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Directly reflects technical, operational, and domain competencies required for job performance."
    ),
    "job_title": FieldPolicy(
        field_type="job_title",
        field_name="Position Applied For",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Specifies the target role against which candidate qualifications and criteria are evaluated."
    ),
    "date_of_birth": FieldPolicy(
        field_type="date_of_birth",
        field_name="Date of Birth",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Date of birth is generally not required for evaluating qualifications during initial employment screening and may create discrimination concerns."
    ),
    "marital_status": FieldPolicy(
        field_type="marital_status",
        field_name="Marital Status",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Marital status is irrelevant to assessing job competence and creates potential exposure to marital status or gender discrimination."
    ),
    "national_id": FieldPolicy(
        field_type="national_id",
        field_name="National ID / SSN",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Government national identification numbers are unnecessary at initial screening and introduce high identity theft exposure."
    ),
    "religion": FieldPolicy(
        field_type="religion",
        field_name="Religion",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Religious beliefs are completely irrelevant to job performance and introduce unlawful bias risks under employment regulations."
    ),
    "home_address": FieldPolicy(
        field_type="home_address",
        field_name="Home Address",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Full street address is unnecessary for initial screening (city/region suffices), but may be required for local payroll tax jurisdictions or commute assessment."
    ),
    "gender": FieldPolicy(
        field_type="gender",
        field_name="Gender",
        document_type="job_application",
        document_purpose=DOCUMENT_PURPOSES["job_application"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Gender is not required for qualification evaluation, though occasionally collected under optional equal employment opportunity (EEO) demographic monitoring."
    ),
}


MEDICAL_INTAKE_FIELDS: Dict[str, FieldPolicy] = {
    "full_name": FieldPolicy(
        field_type="full_name",
        field_name="Patient Full Name",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for patient identification, medical record linkage, and preventing catastrophic misidentification in clinical care."
    ),
    "date_of_birth": FieldPolicy(
        field_type="date_of_birth",
        field_name="Date of Birth",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Crucial for clinical safety, age-dependent pharmaceutical dosage calculations, developmental assessment, and primary patient record matching."
    ),
    "phone": FieldPolicy(
        field_type="phone",
        field_name="Phone Number",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for appointment reminders, urgent clinical test result notifications, and post-procedure follow-ups."
    ),
    "emergency_contact": FieldPolicy(
        field_type="emergency_contact",
        field_name="Emergency Contact",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Vital in acute medical situations, patient incapacitation, or urgent medical decisions where patient proxy consent is needed."
    ),
    "medical_history": FieldPolicy(
        field_type="medical_history",
        field_name="Past Medical History",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential clinical context for differential diagnosis, identifying chronic comorbidities, and planning safe therapeutic interventions."
    ),
    "current_medications": FieldPolicy(
        field_type="current_medications",
        field_name="Current Medications",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Critical for preventing adverse drug-drug interactions, polypharmacy complications, and dosage conflicts."
    ),
    "allergies": FieldPolicy(
        field_type="allergies",
        field_name="Allergies & Sensitivities",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="High-priority safety data required to prevent life-threatening anaphylaxis, drug allergies, and cross-reactive interventions."
    ),
    "insurance_number": FieldPolicy(
        field_type="insurance_number",
        field_name="Health Insurance Policy Number",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Necessary for healthcare claims billing and insurance verification, but not strictly required for emergency or direct self-pay clinical triage."
    ),
    "home_address": FieldPolicy(
        field_type="home_address",
        field_name="Home Address",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Used for patient billing, demographic analysis, and local public health reporting, though secondary to immediate clinical diagnosis."
    ),
    "national_id": FieldPolicy(
        field_type="national_id",
        field_name="National ID / SSN",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Standard government national IDs are unnecessary when unique Medical Record Numbers (MRN) or insurance IDs exist, creating avoidable exposure."
    ),
    "marital_status": FieldPolicy(
        field_type="marital_status",
        field_name="Marital Status",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="May provide helpful context regarding home support network and surrogate decision-makers, but not universally necessary for diagnostics."
    ),
    "religion": FieldPolicy(
        field_type="religion",
        field_name="Religious Affiliation",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Contextual in clinical settings to respect medical restrictions (e.g., blood transfusions, dietary rules, end-of-life pastoral care), but optional."
    ),
    "occupation": FieldPolicy(
        field_type="occupation",
        field_name="Occupation",
        document_type="medical_intake",
        document_purpose=DOCUMENT_PURPOSES["medical_intake"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Provides relevant context for evaluating occupational exposures, repetitive stress injuries, or physical disability accommodations."
    ),
}


LOAN_APPLICATION_FIELDS: Dict[str, FieldPolicy] = {
    "full_name": FieldPolicy(
        field_type="full_name",
        field_name="Applicant Full Name",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Mandatory for establishing legal borrower identity and executing legally binding credit agreements."
    ),
    "date_of_birth": FieldPolicy(
        field_type="date_of_birth",
        field_name="Date of Birth",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required to verify legal age of majority for credit contracts and pull accurate consumer credit bureau reports."
    ),
    "phone": FieldPolicy(
        field_type="phone",
        field_name="Phone Number",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for customer identity verification, fraud prevention multi-factor authentication, and account servicing."
    ),
    "email": FieldPolicy(
        field_type="email",
        field_name="Email Address",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for delivery of mandated Truth in Lending disclosures, electronic contract execution, and official statements."
    ),
    "home_address": FieldPolicy(
        field_type="home_address",
        field_name="Residential Address",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Mandatory under Know Your Customer (KYC) and Anti-Money Laundering (AML) regulations to establish legal residential domicile."
    ),
    "employment_status": FieldPolicy(
        field_type="employment_status",
        field_name="Employment Status",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for evaluating income continuity, employment stability, and the borrower's recurring repayment capacity."
    ),
    "employer_name": FieldPolicy(
        field_type="employer_name",
        field_name="Employer Name",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for independent employment verification and underwriting validation of stated income sources."
    ),
    "annual_income": FieldPolicy(
        field_type="annual_income",
        field_name="Annual Income",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Fundamental metric for calculating Debt-to-Income (DTI) ratio and determining loan affordability and credit limits."
    ),
    "bank_account_number": FieldPolicy(
        field_type="bank_account_number",
        field_name="Bank Account Number",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Contextual during pre-qualification screening; necessary later for direct loan disbursement and automated clearing house (ACH) repayments."
    ),
    "credit_score": FieldPolicy(
        field_type="credit_score",
        field_name="Credit Score",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Primary quantitative metric reflecting historical credit risk, default probability, and determining loan interest pricing."
    ),
    "marital_status": FieldPolicy(
        field_type="marital_status",
        field_name="Marital Status",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Relevant in community property jurisdictions or joint loan applications, but restricted under fair lending laws for individual applications."
    ),
    "religion": FieldPolicy(
        field_type="religion",
        field_name="Religion",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Religious affiliation is completely irrelevant to credit risk assessment and its collection violates the Equal Credit Opportunity Act (ECOA)."
    ),
    "medical_history": FieldPolicy(
        field_type="medical_history",
        field_name="Medical History",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Health and medical conditions are irrelevant to financial solvency evaluation and collecting them exposes high-liability sensitive health data."
    ),
    "biometric_information": FieldPolicy(
        field_type="biometric_information",
        field_name="Biometric Identifier",
        document_type="loan_application",
        document_purpose=DOCUMENT_PURPOSES["loan_application"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Biometric markers are disproportionate and unnecessary for standard consumer credit evaluation, posing severe privacy risks."
    ),
}


RENTAL_AGREEMENT_FIELDS: Dict[str, FieldPolicy] = {
    "full_name": FieldPolicy(
        field_type="full_name",
        field_name="Tenant Full Name",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required to identify the legal tenant and execute an enforceable residential lease contract."
    ),
    "phone": FieldPolicy(
        field_type="phone",
        field_name="Phone Number",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for property management communication, maintenance requests, and emergency notifications."
    ),
    "email": FieldPolicy(
        field_type="email",
        field_name="Email Address",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required for electronic lease execution, rent payment portal access, and digital delivery of legal notices."
    ),
    "current_address": FieldPolicy(
        field_type="current_address",
        field_name="Current Residential Address",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Required to verify current tenancy, assess residency stability, and contact previous landlords for reference checks."
    ),
    "employment_status": FieldPolicy(
        field_type="employment_status",
        field_name="Employment Status",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Directly indicates financial stability and ongoing ability to meet recurring monthly rent obligations."
    ),
    "employer_name": FieldPolicy(
        field_type="employer_name",
        field_name="Employer Name",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Useful for independent employment verification, though verifiable pay stubs or bank statements can serve as alternative proof."
    ),
    "income": FieldPolicy(
        field_type="income",
        field_name="Monthly / Annual Income",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Essential for determining rent-to-income ratio (standard industry threshold of monthly income >= 2.5x to 3x rent)."
    ),
    "rental_history": FieldPolicy(
        field_type="rental_history",
        field_name="Previous Rental History",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.NECESSARY,
        reason="Critical for evaluating past tenancy behavior, timely rent payment record, lease compliance, and eviction history."
    ),
    "emergency_contact": FieldPolicy(
        field_type="emergency_contact",
        field_name="Emergency Contact",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Valuable in urgent property situations, abandonment, or tenant emergencies, but secondary to initial financial qualification."
    ),
    "bank_account_number": FieldPolicy(
        field_type="bank_account_number",
        field_name="Bank Account Number",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Full banking account numbers are unnecessary during rental application screening and expose the applicant to financial fraud risks."
    ),
    "religion": FieldPolicy(
        field_type="religion",
        field_name="Religion",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Religious beliefs are completely irrelevant to rental qualifications and collecting them violates the Fair Housing Act."
    ),
    "medical_history": FieldPolicy(
        field_type="medical_history",
        field_name="Medical History",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Medical history has no bearing on tenancy eligibility and exposes private health data in violation of fair housing privacy principles."
    ),
    "marital_status": FieldPolicy(
        field_type="marital_status",
        field_name="Marital Status",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.UNNECESSARY,
        reason="Marital status is irrelevant to rental qualification and introduces unlawful discrimination risks under fair housing standards."
    ),
    "national_id": FieldPolicy(
        field_type="national_id",
        field_name="National ID / SSN",
        document_type="rental_agreement",
        document_purpose=DOCUMENT_PURPOSES["rental_agreement"],
        necessity_label=NecessityLabel.CONTEXTUAL,
        reason="Often requested for credit and criminal background checks, but can be replaced by direct third-party screening services to reduce exposure."
    ),
}


DOCUMENT_POLICIES: Dict[str, DocumentPurposePolicy] = {
    "job_application": DocumentPurposePolicy(
        document_type="job_application",
        display_name="Job Application",
        purpose=DOCUMENT_PURPOSES["job_application"],
        fields=JOB_APPLICATION_FIELDS,
    ),
    "medical_intake": DocumentPurposePolicy(
        document_type="medical_intake",
        display_name="Medical Intake Form",
        purpose=DOCUMENT_PURPOSES["medical_intake"],
        fields=MEDICAL_INTAKE_FIELDS,
    ),
    "loan_application": DocumentPurposePolicy(
        document_type="loan_application",
        display_name="Loan/Credit Application",
        purpose=DOCUMENT_PURPOSES["loan_application"],
        fields=LOAN_APPLICATION_FIELDS,
    ),
    "rental_agreement": DocumentPurposePolicy(
        document_type="rental_agreement",
        display_name="Rental Application / Agreement",
        purpose=DOCUMENT_PURPOSES["rental_agreement"],
        fields=RENTAL_AGREEMENT_FIELDS,
    ),
}


# --- Sub-Condition Affected Fields Mapping ---
# Fields where necessity genuinely varies depending on document-level context / sub-conditions
AFFECTED_FIELDS: Dict[str, List[str]] = {
    "job_application": ["home_address"],
    "medical_intake": ["home_address"],
    "loan_application": ["marital_status"],
    "rental_agreement": ["emergency_contact"],
}


def get_field_policy(document_type: str, field_type: str) -> Optional[FieldPolicy]:
    """Retrieve static default policy definition for a given document type and field name."""
    doc_policy = DOCUMENT_POLICIES.get(document_type)
    if not doc_policy:
        return None
    return doc_policy.get_field_policy(field_type)


def get_contextual_necessity_policy(
    document_type: str,
    field_type: str,
    sub_conditions: Optional[Dict[str, Any]] = None,
) -> Tuple[NecessityLabel, str]:
    """
    Computes genuine ground-truth necessity label based on both (field_type, document_type)
    AND document-level context sub-conditions.

    Args:
        document_type: Domain of document.
        field_type: Specific PII field type.
        sub_conditions: Dictionary of contextual flags (e.g. is_remote_role, is_telehealth, is_joint_applicant, has_guarantor).

    Returns:
        Tuple of (NecessityLabel, detailed_justification_reason).
    """
    sub_conditions = sub_conditions or {}
    static_policy = get_field_policy(document_type, field_type)

    # 1. Job Application: home_address varies with work_modality (remote vs onsite)
    if document_type == "job_application" and field_type == "home_address":
        if sub_conditions.get("is_remote_role", False):
            return (
                NecessityLabel.UNNECESSARY,
                "Full street address is unnecessary for initial screening for 100% remote roles; state/country jurisdiction suffices.",
            )
        else:
            return (
                NecessityLabel.NECESSARY,
                "Required for assessing commute feasibility, physical facility access, and local payroll tax withholding jurisdiction.",
            )

    # 2. Medical Intake: home_address varies with encounter_type (telehealth vs in-person)
    if document_type == "medical_intake" and field_type == "home_address":
        if sub_conditions.get("is_telehealth", False):
            return (
                NecessityLabel.UNNECESSARY,
                "Physical residential street address is unnecessary for remote telehealth encounters; electronic communication channels suffice.",
            )
        else:
            return (
                NecessityLabel.NECESSARY,
                "Necessary for physical clinical admission, outpatient billing dispatch, and local public health reporting.",
            )

    # 3. Loan Application: marital_status varies with application_type (joint vs individual)
    if document_type == "loan_application" and field_type == "marital_status":
        if sub_conditions.get("is_joint_applicant", False):
            return (
                NecessityLabel.NECESSARY,
                "Necessary for joint/co-borrower credit applications to establish joint spousal liability and community property asset evaluation.",
            )
        else:
            return (
                NecessityLabel.UNNECESSARY,
                "Unnecessary for individual credit applications under the Equal Credit Opportunity Act (ECOA).",
            )

    # 4. Rental Agreement: emergency_contact varies with tenancy_type (guarantor/student vs individual)
    if document_type == "rental_agreement" and field_type == "emergency_contact":
        if sub_conditions.get("has_guarantor", False):
            return (
                NecessityLabel.NECESSARY,
                "Mandatory emergency contact and legal proxy communication for guarantor-supported or student lease agreements.",
            )
        else:
            return (
                NecessityLabel.UNNECESSARY,
                "Unnecessary for standard independent direct adult leases during initial rental screening.",
            )

    # Default to static policy for unaffected fields
    if static_policy:
        return static_policy.necessity_label, static_policy.reason

    return NecessityLabel.CONTEXTUAL, f"Field '{field_type}' has no explicit policy in '{document_type}'."


def get_all_policies() -> Dict[str, DocumentPurposePolicy]:
    """Retrieve all document purpose policies."""
    return DOCUMENT_POLICIES


def validate_necessity_label(label: str) -> bool:
    """Validate if a string is a recognized necessity label."""
    return label in {item.value for item in NecessityLabel}

