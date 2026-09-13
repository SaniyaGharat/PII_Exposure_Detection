"""
PII Exposure Detection - Necessity Rule Engine (R Component)
Direct deterministic policy lookup mapping (field_type, document_type/purpose)
to an ordinal necessity score in {0.0, 0.5, 1.0} and its policy justification.
"""

from typing import Dict, Optional, Tuple
from src.policies.necessity_policy import (
    DOCUMENT_POLICIES,
    DOCUMENT_PURPOSES,
    NecessityLabel,
    get_field_policy,
)

# Standard ordinal mapping
LABEL_TO_SCORE: Dict[str, float] = {
    "unnecessary": 0.0,
    "contextual": 0.5,
    "necessary": 1.0,
}

SCORE_TO_LABEL: Dict[float, str] = {
    0.0: "unnecessary",
    0.5: "contextual",
    1.0: "necessary",
}


class RuleEngine:
    """Deterministic policy-based necessity evaluator (R component)."""

    def __init__(self):
        self.policies = DOCUMENT_POLICIES

    def evaluate(self, field_type: str, document_type: str) -> Tuple[float, str, str]:
        """
        Evaluates the rule score for a given field and document type.

        Args:
            field_type: Standardized PII field type (e.g., 'date_of_birth', 'full_name').
            document_type: Document domain ('job_application', 'medical_intake', etc.).

        Returns:
            Tuple of (rule_score in {0.0, 0.5, 1.0}, label_str, justification_reason).
        """
        policy = get_field_policy(document_type, field_type)
        if policy:
            label = policy.necessity_label.value
            score = LABEL_TO_SCORE.get(label, 0.5)
            reason = policy.reason
            return score, label, reason

        # Fallback for unmapped / general fields
        return 0.5, "contextual", f"Field '{field_type}' has no explicit policy in '{document_type}'; treated as contextual by default."

    def __call__(self, field_type: str, document_type: str) -> Tuple[float, str, str]:
        return self.evaluate(field_type, document_type)
