"""
PII Exposure Detection - Synthetic Document & Label Generator
Generates realistic, purpose-driven synthetic documents across 4 domains with
automatic ground-truth necessity labeling and exact character span annotations.
"""

import json
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from faker import Faker

from src.policies.necessity_policy import (
    DOCUMENT_POLICIES,
    DOCUMENT_PURPOSES,
    get_field_policy,
)
from src.utils.pdf_generator import generate_pdf_from_text
from src.utils.scanner_simulator import simulate_scanned_document


class DocumentGenerator:
    """Generates synthetic documents and annotated ground-truth labels."""

    def __init__(self, seed: int = 42, templates_dir: Path = None):
        self.seed = seed
        self.rng = random.Random(seed)
        self.fake = Faker()
        Faker.seed(seed)

        if templates_dir is None:
            self.templates_dir = Path(__file__).resolve().parent.parent.parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)

        # Pre-load templates
        self.templates: Dict[str, str] = {
            "job_application": (self.templates_dir / "job_application.txt").read_text(encoding="utf-8"),
            "medical_intake": (self.templates_dir / "medical_intake.txt").read_text(encoding="utf-8"),
            "loan_application": (self.templates_dir / "loan_application.txt").read_text(encoding="utf-8"),
            "rental_agreement": (self.templates_dir / "rental_agreement.txt").read_text(encoding="utf-8"),
        }

        # Domain specific data pools for realistic generation
        self._init_data_pools()

    def _init_data_pools(self) -> None:
        """Initialize domain-specific knowledge pools for realistic generation."""
        self.job_titles = [
            "Senior Software Engineer", "Data Scientist", "DevOps Engineer",
            "Financial Analyst", "Clinical Research Coordinator", "Marketing Specialist",
            "Product Manager", "Database Administrator", "Systems Architect",
            "Cybersecurity Analyst", "HR Operations Generalist", "Account Executive"
        ]

        self.universities = [
            "University of Washington", "Georgia Institute of Technology",
            "University of Michigan", "University of Illinois Urbana-Champaign",
            "University of Texas at Austin", "Purdue University", "UC San Diego",
            "Carnegie Mellon University", "Columbia University", "Cornell University"
        ]

        self.skills_pool = [
            "Python, SQL, PyTorch, Docker, Kubernetes, AWS Cloud Architecture",
            "Financial Modeling, Risk Analysis, Bloomberg Terminal, Advanced Excel, CFA Level II",
            "Clinical Trial Management, GCP Compliance, Electronic Health Records (EHR), HIPAA",
            "React, TypeScript, Node.js, GraphQL, CI/CD Pipelines, Microservices",
            "Network Security, Penetration Testing, SIEM, Incident Response, ISO 27001",
            "Statistical Analysis, R, Tableau, Data Pipelines, Predictive Modeling"
        ]

        self.medical_histories = [
            "Hypertension (diagnosed 2018), Mild Osteoarthritis in right knee.",
            "Type 2 Diabetes Mellitus (managed via diet/medication), Hyperlipidemia.",
            "Mild persistent Asthma, seasonal allergic rhinitis, History of Appendectomy (2015).",
            "Gastroesophageal Reflux Disease (GERD), History of Right Wrist Fracture (2020).",
            "Hypothyroidism (stable on levothyroxine), Migraines with aura.",
            "No significant past medical history. Non-smoker, no past surgeries."
        ]

        self.medications_pool = [
            "Lisinopril 10mg PO daily, Atorvastatin 20mg PO at bedtime.",
            "Metformin 500mg PO BID with meals, Glipizide 5mg daily.",
            "Albuterol HFA Inhaler 90mcg 2 puffs PRN, Fluticasone nasal spray daily.",
            "Omeprazole 20mg PO daily before breakfast, Calcium + Vitamin D supplement.",
            "Levothyroxine 75mcg PO daily in morning, Sumatriptan 50mg PRN for migraine.",
            "None reported / Over-the-counter multivitamins only."
        ]

        self.allergies_pool = [
            "Penicillin (rash, hives), Shellfish (mild itching).",
            "Sulfa antibiotics (severe skin reaction), Latex.",
            "Peanuts (anaphylaxis - carries EpiPen), Tree nuts.",
            "Aspirin (bronchospasm), Codeine (nausea).",
            "No Known Drug Allergies (NKDA), No known environmental allergies."
        ]

        self.religions = [
            "Christianity", "Islam", "Hinduism", "Buddhism", "Judaism",
            "Sikhism", "Agnostic", "Atheist", "Unaffiliated", "Prefer not to disclose"
        ]

        self.marital_statuses = [
            "Single", "Married", "Divorced", "Widowed", "Domestic Partnership"
        ]

        self.employment_statuses = [
            "Employed Full-Time", "Employed Part-Time", "Self-Employed",
            "Contractor / Freelancer", "Retired"
        ]

    def _generate_national_id(self) -> str:
        """Generate realistic synthetic US-style SSN / National ID."""
        area = self.rng.randint(100, 899)
        group = self.rng.randint(10, 99)
        serial = self.rng.randint(1000, 9999)
        return f"{area:03d}-{group:02d}-{serial:04d}"

    def _generate_bank_account(self) -> str:
        """Generate synthetic bank account number."""
        return f"ACCT-{self.rng.randint(1000000000, 9999999999)}"

    def _generate_insurance_number(self) -> str:
        """Generate synthetic health insurance identifier."""
        prefix = self.rng.choice(["MED", "BLU", "AET", "UHC", "KSR"])
        return f"{prefix}-{self.rng.randint(10000000, 99999999)}"

    def _render_with_spans(
        self,
        template_text: str,
        field_values: Dict[str, str],
        doc_type: str,
        doc_id: str,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Substitutes placeholder variables {{field_type}} in the template and
        calculates exact character start and end spans in the final rendered text.
        """
        # Find all placeholders in order of appearance
        pattern = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
        rendered_pieces: List[str] = []
        fields_metadata: List[Dict[str, Any]] = []

        last_idx = 0
        current_char_len = 0

        for match in pattern.finditer(template_text):
            placeholder_start, placeholder_end = match.span()
            field_key = match.group(1)

            # Append text preceding this placeholder
            preceding_text = template_text[last_idx:placeholder_start]
            rendered_pieces.append(preceding_text)
            current_char_len += len(preceding_text)

            # Value to insert
            val = field_values.get(field_key, f"[{field_key.upper()}]")
            val_start = current_char_len
            val_end = current_char_len + len(val)

            rendered_pieces.append(val)
            current_char_len += len(val)
            last_idx = placeholder_end

            # Retrieve policy definition
            policy = get_field_policy(doc_type, field_key)
            if policy:
                field_name = policy.field_name
                necessity_label = policy.necessity_label.value
                reason = policy.reason
            else:
                field_name = field_key.replace("_", " ").title()
                necessity_label = "contextual"
                reason = "General metadata field."

            fields_metadata.append({
                "field_type": field_key,
                "field_name": field_name,
                "field_value": val,
                "necessity_label": necessity_label,
                "reason": reason,
                "span": {
                    "start": val_start,
                    "end": val_end,
                },
            })

        # Append remaining text after last placeholder
        remaining_text = template_text[last_idx:]
        rendered_pieces.append(remaining_text)
        final_text = "".join(rendered_pieces)

        # Verification assertion: verify every span matches exact value
        for entry in fields_metadata:
            s = entry["span"]["start"]
            e = entry["span"]["end"]
            extracted = final_text[s:e]
            assert extracted == entry["field_value"], (
                f"Span calculation error for {entry['field_type']} in {doc_id}: "
                f"expected '{entry['field_value']}', got '{extracted}'"
            )

        label_data = {
            "document_id": doc_id,
            "document_type": doc_type,
            "document_purpose": DOCUMENT_PURPOSES[doc_type],
            "fields": fields_metadata,
        }

        return final_text, label_data

    def generate_job_application(self, doc_id: str) -> Tuple[str, Dict[str, Any]]:
        """Generates a synthetic job application document and corresponding labels."""
        gender = self.rng.choice(["Female", "Male", "Non-Binary", "Prefer not to disclose"])
        first_name = self.fake.first_name_female() if gender == "Female" else self.fake.first_name_male()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"

        job_title = self.rng.choice(self.job_titles)
        degree = self.rng.choice(["B.S. in Computer Science", "B.A. in Economics", "M.S. in Data Analytics", "MBA", "B.S. in Information Systems"])
        university = self.rng.choice(self.universities)
        grad_year = self.rng.randint(2010, 2023)
        education_str = f"{degree} - {university} (Graduated {grad_year})"

        company1 = self.fake.company()
        company2 = self.fake.company()
        work_str = (
            f"1. {job_title} at {company1} ({self.rng.randint(2021, 2023)} - Present)\n"
            f"   - Led cross-functional initiatives, improving project throughput by 28%.\n"
            f"2. Associate Specialist at {company2} ({self.rng.randint(2017, 2020)} - {self.rng.randint(2020, 2021)})\n"
            f"   - Managed key deliverables, analyzed system data, and automated workflows."
        )

        dob = self.fake.date_of_birth(minimum_age=22, maximum_age=58).strftime("%B %d, %Y")
        phone = self.fake.phone_number()
        email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
        address = f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"

        field_values = {
            "full_name": full_name,
            "date_of_birth": dob,
            "gender": gender,
            "marital_status": self.rng.choice(self.marital_statuses),
            "religion": self.rng.choice(self.religions),
            "national_id": self._generate_national_id(),
            "email": email,
            "phone": phone,
            "home_address": address,
            "job_title": job_title,
            "education": education_str,
            "work_history": work_str,
            "skills": self.rng.choice(self.skills_pool),
        }

        template_text = self.templates["job_application"]
        return self._render_with_spans(template_text, field_values, "job_application", doc_id)

    def generate_medical_intake(self, doc_id: str) -> Tuple[str, Dict[str, Any]]:
        """Generates a synthetic medical clinical intake document and labels."""
        full_name = self.fake.name()
        dob = self.fake.date_of_birth(minimum_age=18, maximum_age=82).strftime("%B %d, %Y")
        phone = self.fake.phone_number()
        address = f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"

        emergency_contact_name = self.fake.name()
        relation = self.rng.choice(["Spouse", "Parent", "Sibling", "Adult Child", "Partner"])
        emergency_phone = self.fake.phone_number()
        emergency_str = f"{emergency_contact_name} ({relation}) - Phone: {emergency_phone}"

        field_values = {
            "full_name": full_name,
            "date_of_birth": dob,
            "phone": phone,
            "home_address": address,
            "marital_status": self.rng.choice(self.marital_statuses),
            "occupation": self.fake.job(),
            "religion": self.rng.choice(self.religions),
            "national_id": self._generate_national_id(),
            "insurance_number": self._generate_insurance_number(),
            "emergency_contact": emergency_str,
            "allergies": self.rng.choice(self.allergies_pool),
            "current_medications": self.rng.choice(self.medications_pool),
            "medical_history": self.rng.choice(self.medical_histories),
        }

        template_text = self.templates["medical_intake"]
        return self._render_with_spans(template_text, field_values, "medical_intake", doc_id)

    def generate_loan_application(self, doc_id: str) -> Tuple[str, Dict[str, Any]]:
        """Generates a synthetic credit/loan application document and labels."""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        dob = self.fake.date_of_birth(minimum_age=21, maximum_age=65).strftime("%B %d, %Y")
        phone = self.fake.phone_number()
        email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
        address = f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"

        income_val = self.rng.randint(48, 195) * 1000
        credit_score_val = self.rng.randint(590, 830)
        bio_hash = f"SHA256:{self.fake.sha256()[:24]} (Biometric Minutiae Key)"

        field_values = {
            "full_name": full_name,
            "date_of_birth": dob,
            "marital_status": self.rng.choice(self.marital_statuses),
            "religion": self.rng.choice(self.religions),
            "phone": phone,
            "email": email,
            "home_address": address,
            "employment_status": self.rng.choice(self.employment_statuses),
            "employer_name": self.fake.company(),
            "annual_income": f"${income_val:,.2f} USD",
            "bank_account_number": self._generate_bank_account(),
            "credit_score": f"{credit_score_val} (FICO Score 8)",
            "medical_history": self.rng.choice(self.medical_histories),
            "biometric_information": bio_hash,
        }

        template_text = self.templates["loan_application"]
        return self._render_with_spans(template_text, field_values, "loan_application", doc_id)

    def generate_rental_application(self, doc_id: str) -> Tuple[str, Dict[str, Any]]:
        """Generates a synthetic residential lease application document and labels."""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        phone = self.fake.phone_number()
        email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
        current_addr = f"{self.fake.street_address()}, {self.fake.city()}, {self.fake.state_abbr()} {self.fake.zipcode()}"

        monthly_inc = self.rng.randint(3500, 12500)
        prev_landlord = self.fake.name()
        prev_rent = self.rng.randint(1400, 3200)
        rental_hist_str = (
            f"Previous Address: {self.fake.street_address()}, {self.fake.city()}\n"
            f"Tenancy: 2021 - 2024 | Landlord: {prev_landlord} | Rent: ${prev_rent}/mo\n"
            f"Reason for Leaving: Job relocation | Full security deposit returned: Yes"
        )

        emergency_contact_str = f"{self.fake.name()} (Sibling) - Tel: {self.fake.phone_number()}"

        field_values = {
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "national_id": self._generate_national_id(),
            "marital_status": self.rng.choice(self.marital_statuses),
            "religion": self.rng.choice(self.religions),
            "current_address": current_addr,
            "employment_status": self.rng.choice(self.employment_statuses),
            "employer_name": self.fake.company(),
            "income": f"${monthly_inc:,.2f} / month",
            "bank_account_number": self._generate_bank_account(),
            "rental_history": rental_hist_str,
            "emergency_contact": emergency_contact_str,
            "medical_history": self.rng.choice(self.medical_histories),
        }

        template_text = self.templates["rental_agreement"]
        return self._render_with_spans(template_text, field_values, "rental_agreement", doc_id)


def generate_full_dataset(
    dataset_dir: Path,
    count_per_type: int = 100,
    scanned_ratio: float = 0.25,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Coordinates the generation of synthetic text documents, JSON ground truth labels,
    ReportLab PDFs, and simulated scanned PNG images.
    """
    generator = DocumentGenerator(seed=seed)
    rng = random.Random(seed)

    dataset_dir = Path(dataset_dir)
    dataset_dir.mkdir(parents=True, exist_ok=True)

    type_mapping = {
        "job_application": ("job", generator.generate_job_application),
        "medical_intake": ("med", generator.generate_medical_intake),
        "loan_application": ("loan", generator.generate_loan_application),
        "rental_agreement": ("rent", generator.generate_rental_application),
    }

    generated_stats = {
        "total_documents": 0,
        "text_count": 0,
        "pdf_count": 0,
        "scanned_count": 0,
        "label_count": 0,
    }

    for doc_type, (prefix, gen_func) in type_mapping.items():
        type_dir = dataset_dir / doc_type
        text_dir = type_dir / "text"
        pdf_dir = type_dir / "pdf"
        scanned_dir = type_dir / "scanned"
        labels_dir = type_dir / "labels"

        for d in [text_dir, pdf_dir, scanned_dir, labels_dir]:
            d.mkdir(parents=True, exist_ok=True)

        scanned_count_target = int(count_per_type * scanned_ratio)
        scanned_indices = set(rng.sample(range(1, count_per_type + 1), scanned_count_target))

        for idx in range(1, count_per_type + 1):
            doc_id = f"{prefix}_{idx:03d}"
            text_content, label_data = gen_func(doc_id)

            # 1. Save text document
            text_path = text_dir / f"{doc_id}.txt"
            text_path.write_text(text_content, encoding="utf-8")
            generated_stats["text_count"] += 1

            # 2. Save JSON ground truth label
            label_path = labels_dir / f"{doc_id}.json"
            with open(label_path, "w", encoding="utf-8") as f:
                json.dump(label_data, f, indent=4)
            generated_stats["label_count"] += 1

            # 3. Save PDF document
            pdf_path = pdf_dir / f"{doc_id}.pdf"
            generate_pdf_from_text(text_content, pdf_path, title=f"{doc_type.replace('_', ' ').title()} - {doc_id}")
            generated_stats["pdf_count"] += 1

            # 4. Save Scanned PNG document (for sampled subset)
            if idx in scanned_indices:
                scanned_path = scanned_dir / f"{doc_id}.png"
                simulate_scanned_document(text_content, scanned_path, seed=seed + idx)
                generated_stats["scanned_count"] += 1

            generated_stats["total_documents"] += 1

    return generated_stats


def split_dataset(
    dataset_dir: Path,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> Dict[str, int]:
    """
    Creates stratified reproducible dataset splits (Train 70%, Validation 15%, Test 15%).
    Saves metadata to dataset/splits/{train, validation, test}.json.
    """
    rng = random.Random(seed)
    dataset_dir = Path(dataset_dir)
    splits_dir = dataset_dir / "splits"
    splits_dir.mkdir(parents=True, exist_ok=True)

    doc_types = ["job_application", "medical_intake", "loan_application", "rental_agreement"]

    train_docs: List[Dict[str, str]] = []
    val_docs: List[Dict[str, str]] = []
    test_docs: List[Dict[str, str]] = []

    for dt in doc_types:
        text_dir = dataset_dir / dt / "text"
        if not text_dir.exists():
            continue

        doc_ids = sorted([p.stem for p in text_dir.glob("*.txt")])
        rng.shuffle(doc_ids)

        n_total = len(doc_ids)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        train_subset = doc_ids[:n_train]
        val_subset = doc_ids[n_train:n_train + n_val]
        test_subset = doc_ids[n_train + n_val:]

        for doc_id in train_subset:
            train_docs.append({"document_id": doc_id, "document_type": dt})
        for doc_id in val_subset:
            val_docs.append({"document_id": doc_id, "document_type": dt})
        for doc_id in test_subset:
            test_docs.append({"document_id": doc_id, "document_type": dt})

    splits_data = {
        "train": {
            "split": "train",
            "ratio": train_ratio,
            "seed": seed,
            "total_count": len(train_docs),
            "documents": train_docs,
        },
        "validation": {
            "split": "validation",
            "ratio": val_ratio,
            "seed": seed,
            "total_count": len(val_docs),
            "documents": val_docs,
        },
        "test": {
            "split": "test",
            "ratio": test_ratio,
            "seed": seed,
            "total_count": len(test_docs),
            "documents": test_docs,
        },
    }

    for split_name, data in splits_data.items():
        split_file = splits_dir / f"{split_name}.json"
        with open(split_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    return {
        "train": len(train_docs),
        "validation": len(val_docs),
        "test": len(test_docs),
    }
