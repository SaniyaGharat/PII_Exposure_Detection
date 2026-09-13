"""
PII Exposure Detection - Custom Presidio Recognizers
Defines custom pattern- and context-based recognizers for domain-specific fields
from necessity policies that are not caught by baseline out-of-the-box Presidio.
"""

from typing import Dict, List
from presidio_analyzer import Pattern, PatternRecognizer


# Standard entity mapping from Presidio / Custom Entity tags to project field_types
DOMAIN_ENTITY_MAPPING: Dict[str, str] = {
    # Built-in Presidio mappings
    "PERSON": "full_name",
    "EMAIL_ADDRESS": "email",
    "PHONE_NUMBER": "phone",
    "US_SSN": "national_id",
    "LOCATION": "home_address",
    "DATE_TIME": "date_of_birth",

    # Custom domain-specific recognizer mappings
    "CUSTOM_NATIONAL_ID": "national_id",
    "CUSTOM_DOB": "date_of_birth",
    "CUSTOM_GENDER": "gender",
    "CUSTOM_MARITAL_STATUS": "marital_status",
    "CUSTOM_RELIGION": "religion",
    "CUSTOM_HOME_ADDRESS": "home_address",
    "CUSTOM_CURRENT_ADDRESS": "current_address",
    "CUSTOM_JOB_TITLE": "job_title",
    "CUSTOM_EDUCATION": "education",
    "CUSTOM_WORK_HISTORY": "work_history",
    "CUSTOM_SKILLS": "skills",
    "CUSTOM_EMERGENCY_CONTACT": "emergency_contact",
    "CUSTOM_MEDICAL_HISTORY": "medical_history",
    "CUSTOM_MEDICATIONS": "current_medications",
    "CUSTOM_ALLERGIES": "allergies",
    "CUSTOM_INSURANCE_NO": "insurance_number",
    "CUSTOM_OCCUPATION": "occupation",
    "CUSTOM_EMPLOYMENT_STATUS": "employment_status",
    "CUSTOM_EMPLOYER_NAME": "employer_name",
    "CUSTOM_ANNUAL_INCOME": "annual_income",
    "CUSTOM_INCOME": "income",
    "CUSTOM_BANK_ACCOUNT": "bank_account_number",
    "CUSTOM_CREDIT_SCORE": "credit_score",
    "CUSTOM_BIOMETRIC_INFO": "biometric_information",
    "CUSTOM_RENTAL_HISTORY": "rental_history",
}


def build_national_id_recognizer() -> PatternRecognizer:
    """Recognizes US-style Social Security and National ID numbers."""
    patterns = [
        Pattern(name="ssn_standard", regex=r"\b\d{3}-\d{2}-\d{4}\b", score=0.90),
        Pattern(name="ssn_unformatted", regex=r"\b\d{9}\b", score=0.60),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_NATIONAL_ID",
        name="NationalIdRecognizer",
        patterns=patterns,
        context=["national id", "ssn", "social security", "identification", "id number", "ssn:"]
    )


def build_bank_account_recognizer() -> PatternRecognizer:
    """Recognizes synthetic and standard bank account identifier formats."""
    patterns = [
        Pattern(name="bank_account_prefix", regex=r"\bACCT-\d{10}\b", score=0.95),
        Pattern(name="bank_account_num", regex=r"(?i)\b(?:Account|Acct)\s*(?:Number|No\.?)?[:\s]+([A-Z0-9-]{8,16})\b", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_BANK_ACCOUNT",
        name="BankAccountRecognizer",
        patterns=patterns,
        context=["bank account", "account number", "checking", "savings", "routing", "account no"]
    )


def build_insurance_number_recognizer() -> PatternRecognizer:
    """Recognizes health insurance policy identifiers."""
    patterns = [
        Pattern(name="insurance_policy_std", regex=r"\b(?:MED|BLU|AET|UHC|KSR)-\d{8}\b", score=0.95),
        Pattern(name="insurance_policy_gen", regex=r"(?i)\b(?:Insurance|Policy)\s*(?:No\.?|Number|#)?[:\s]+([A-Z0-9-]{8,15})\b", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_INSURANCE_NO",
        name="InsuranceNumberRecognizer",
        patterns=patterns,
        context=["insurance", "policy number", "policy no", "health insurance", "subscriber id", "member id"]
    )


def build_credit_score_recognizer() -> PatternRecognizer:
    """Recognizes credit scores with FICO or numeric score context."""
    patterns = [
        Pattern(name="credit_score_fico", regex=r"\b[3-8][0-9]{2}\s*(?:\(FICO Score \d\)|FICO|Score)\b", score=0.95),
        Pattern(name="credit_score_num", regex=r"(?i)\b(?:Credit Score|FICO)(?:[:\s]+|\s*\([a-zA-Z0-9\s]+\)[:\s]+)([3-8][0-9]{2})\b", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_CREDIT_SCORE",
        name="CreditScoreRecognizer",
        patterns=patterns,
        context=["credit score", "fico", "credit rating", "fico score", "score"]
    )


def build_biometric_recognizer() -> PatternRecognizer:
    """Recognizes biometric keys, hashes, and cryptographic templates."""
    patterns = [
        Pattern(name="biometric_sha", regex=r"\bSHA256:[a-f0-9]{24}\s*\(Biometric Minutiae Key\)", score=0.98),
        Pattern(name="biometric_key", regex=r"(?i)\b(?:Biometric|Minutiae|Iris|Fingerprint|Facial Template)[:\s]+([a-zA-Z0-9:_\-\(\)\s]{10,50})\b", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_BIOMETRIC_INFO",
        name="BiometricInfoRecognizer",
        patterns=patterns,
        context=["biometric", "minutiae", "iris template", "fingerprint", "biometric key", "security identifier"]
    )


def build_marital_status_recognizer() -> PatternRecognizer:
    """Recognizes marital status categories."""
    marital_terms = r"(?i)\b(Single|Married|Divorced|Widowed|Domestic Partnership|Separated)\b"
    patterns = [
        Pattern(name="marital_status_val", regex=marital_terms, score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_MARITAL_STATUS",
        name="MaritalStatusRecognizer",
        patterns=patterns,
        context=["marital status", "marital", "married", "spouse", "single", "civil status"]
    )


def build_religion_recognizer() -> PatternRecognizer:
    """Recognizes religious affiliation mentions."""
    rel_terms = r"(?i)\b(Christianity|Islam|Hinduism|Buddhism|Judaism|Sikhism|Agnostic|Atheist|Unaffiliated|Prefer not to disclose)\b"
    patterns = [
        Pattern(name="religion_val", regex=rel_terms, score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_RELIGION",
        name="ReligionRecognizer",
        patterns=patterns,
        context=["religious belief", "religion", "faith", "religious preference", "belief"]
    )


def build_gender_recognizer() -> PatternRecognizer:
    """Recognizes gender demographic disclosures."""
    gender_terms = r"(?i)\b(Female|Male|Non-Binary|Prefer not to disclose)\b"
    patterns = [
        Pattern(name="gender_val", regex=gender_terms, score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_GENDER",
        name="GenderRecognizer",
        patterns=patterns,
        context=["gender", "sex", "demographic"]
    )


def build_employment_status_recognizer() -> PatternRecognizer:
    """Recognizes employment classification terms."""
    emp_terms = r"(?i)\b(Employed Full-Time|Employed Part-Time|Self-Employed|Contractor / Freelancer|Contractor|Freelancer|Retired|Unemployed)\b"
    patterns = [
        Pattern(name="emp_status_val", regex=emp_terms, score=0.88),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_EMPLOYMENT_STATUS",
        name="EmploymentStatusRecognizer",
        patterns=patterns,
        context=["employment status", "employment", "employed", "work status", "job status"]
    )


def build_income_recognizer() -> PatternRecognizer:
    """Recognizes financial income and salary disclosures."""
    patterns = [
        Pattern(name="income_annual", regex=r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*USD", score=0.90),
        Pattern(name="income_monthly", regex=r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*/\s*month", score=0.90),
        Pattern(name="income_currency", regex=r"(?i)\b(?:Income|Salary|Earnings)[:\s]+\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_ANNUAL_INCOME",
        name="IncomeRecognizer",
        patterns=patterns,
        context=["annual income", "gross income", "monthly income", "income", "salary", "earnings"]
    )


def build_dob_recognizer() -> PatternRecognizer:
    """Recognizes full written date of birth expressions."""
    patterns = [
        Pattern(
            name="dob_written",
            regex=r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
            score=0.90
        ),
        Pattern(
            name="dob_numeric",
            regex=r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b",
            score=0.80
        ),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_DOB",
        name="DateOfBirthRecognizer",
        patterns=patterns,
        context=["date of birth", "dob", "birth date", "born", "birthday"]
    )


def build_address_recognizer() -> PatternRecognizer:
    """Recognizes full US street address formats with street, city, state, zip."""
    patterns = [
        Pattern(
            name="address_full_us",
            regex=r"\b\d{1,5}\s+[A-Za-z0-9\s.,]+(?:Apt\.?|Suite|Unit|St\.?|Street|Ave\.?|Avenue|Rd\.?|Road|Dr\.?|Drive|Blvd\.?|Boulevard|Ln\.?|Lane|Way|Ct\.?|Court)[A-Za-z0-9\s.,]*,\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5}(?:-\d{4})?\b",
            score=0.90
        ),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_HOME_ADDRESS",
        name="AddressRecognizer",
        patterns=patterns,
        context=["home address", "residential address", "current residence", "address", "current address"]
    )


def build_job_title_recognizer() -> PatternRecognizer:
    """Recognizes position applied for and job titles with context."""
    job_titles = (
        r"(?i)\b(Senior Software Engineer|Data Scientist|DevOps Engineer|Financial Analyst|"
        r"Clinical Research Coordinator|Marketing Specialist|Product Manager|Database Administrator|"
        r"Systems Architect|Cybersecurity Analyst|HR Operations Generalist|Account Executive)\b"
    )
    patterns = [
        Pattern(name="job_title_exact", regex=job_titles, score=0.90),
        Pattern(name="job_title_ctx", regex=r"(?i)Position Applied For:\s*([A-Za-z0-9\s/&-]+)", score=0.85),
    ]
    return PatternRecognizer(
        supported_entity="CUSTOM_JOB_TITLE",
        name="JobTitleRecognizer",
        patterns=patterns,
        context=["position applied for", "position", "job title", "role", "applied for", "target position"]
    )


def build_contextual_section_recognizers() -> List[PatternRecognizer]:
    """
    Builds context-aware recognizers for structured form sections
    (Education, Work History, Skills, Medical History, Medications, Allergies, Rental History, Emergency Contact).
    """
    recognizers = []

    # 1. Emergency Contact
    rec_emerg = PatternRecognizer(
        supported_entity="CUSTOM_EMERGENCY_CONTACT",
        name="EmergencyContactRecognizer",
        patterns=[
            Pattern(
                name="emerg_contact_line",
                regex=r"(?i)[A-Za-z\s.'-]+\s*\((?:Spouse|Parent|Sibling|Adult Child|Partner|Friend|Relative)\)\s*-\s*(?:Phone|Tel)[:\s]+[0-9+().\-\s]+",
                score=0.92
            )
        ],
        context=["emergency contact", "primary emergency contact", "in case of emergency", "next of kin"]
    )
    recognizers.append(rec_emerg)

    # 2. Medical History
    rec_med_hist = PatternRecognizer(
        supported_entity="CUSTOM_MEDICAL_HISTORY",
        name="MedicalHistoryRecognizer",
        patterns=[
            Pattern(
                name="med_hist_conditions",
                regex=r"(?i)\b(?:Hypertension|Osteoarthritis|Diabetes Mellitus|Hyperlipidemia|Asthma|rhinitis|Appendectomy|GERD|Reflux|Fracture|Hypothyroidism|Migraines|No significant past medical history)[^\n\r]+",
                score=0.90
            )
        ],
        context=["past medical history", "medical history", "diagnosed conditions", "surgeries", "clinical history"]
    )
    recognizers.append(rec_med_hist)

    # 3. Medications
    rec_meds = PatternRecognizer(
        supported_entity="CUSTOM_MEDICATIONS",
        name="MedicationsRecognizer",
        patterns=[
            Pattern(
                name="medications_list",
                regex=r"(?i)\b(?:Lisinopril|Atorvastatin|Metformin|Glipizide|Albuterol|Fluticasone|Omeprazole|Calcium|Levothyroxine|Sumatriptan|None reported)[^\n\r]+",
                score=0.90
            )
        ],
        context=["current medications", "active prescriptions", "medications & dosages", "prescriptions", "supplements"]
    )
    recognizers.append(rec_meds)

    # 4. Allergies
    rec_allergies = PatternRecognizer(
        supported_entity="CUSTOM_ALLERGIES",
        name="AllergiesRecognizer",
        patterns=[
            Pattern(
                name="allergies_list",
                regex=r"(?i)\b(?:Penicillin|Shellfish|Sulfa antibiotics|Latex|Peanuts|Tree nuts|Aspirin|Codeine|No Known Drug Allergies|NKDA)[^\n\r]+",
                score=0.90
            )
        ],
        context=["allergies", "known drug & environmental allergies", "sensitivities", "allergic", "allergy"]
    )
    recognizers.append(rec_allergies)

    # 5. Education
    rec_edu = PatternRecognizer(
        supported_entity="CUSTOM_EDUCATION",
        name="EducationRecognizer",
        patterns=[
            Pattern(
                name="edu_degree_line",
                regex=r"(?i)\b(?:B\.S\.|B\.A\.|M\.S\.|MBA|Ph\.D\.|Bachelor|Master)\s+(?:in\s+)?[A-Za-z\s]+-\s+[A-Za-z\s]+(?:\(Graduated\s+\d{4}\))?",
                score=0.92
            )
        ],
        context=["highest degree", "education & academic credentials", "degree", "major", "university", "education"]
    )
    recognizers.append(rec_edu)

    # 6. Skills
    rec_skills = PatternRecognizer(
        supported_entity="CUSTOM_SKILLS",
        name="SkillsRecognizer",
        patterns=[
            Pattern(
                name="skills_block",
                regex=r"(?i)\b(?:Python|SQL|PyTorch|Docker|Financial Modeling|Clinical Trial|React|TypeScript|Network Security|Statistical Analysis)[^\n\r]+",
                score=0.90
            )
        ],
        context=["technical & professional skills", "skills & core competencies", "skills", "competencies"]
    )
    recognizers.append(rec_skills)

    # 7. Rental History
    rec_rental_hist = PatternRecognizer(
        supported_entity="CUSTOM_RENTAL_HISTORY",
        name="RentalHistoryRecognizer",
        patterns=[
            Pattern(
                name="rental_hist_block",
                regex=r"(?i)Previous Address:[^\n\r]+\n\s*Tenancy:[^\n\r]+\n\s*Reason for Leaving:[^\n\r]+",
                score=0.92
            )
        ],
        context=["previous rental history", "rental history", "tenancy", "previous landlord"]
    )
    recognizers.append(rec_rental_hist)

    return recognizers


def get_custom_recognizers() -> List[PatternRecognizer]:
    """Returns the complete collection of all domain-specific custom Presidio recognizers."""
    recognizers = [
        build_national_id_recognizer(),
        build_bank_account_recognizer(),
        build_insurance_number_recognizer(),
        build_credit_score_recognizer(),
        build_biometric_recognizer(),
        build_marital_status_recognizer(),
        build_religion_recognizer(),
        build_gender_recognizer(),
        build_employment_status_recognizer(),
        build_income_recognizer(),
        build_dob_recognizer(),
        build_address_recognizer(),
        build_job_title_recognizer(),
    ]
    recognizers.extend(build_contextual_section_recognizers())
    return recognizers
