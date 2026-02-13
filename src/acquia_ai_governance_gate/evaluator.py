from __future__ import annotations

import re
from dataclasses import dataclass

PII_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
SOURCE_PATTERN = re.compile(r"\[[^\]]+\]\([^)]+\)")


@dataclass(frozen=True)
class EvaluationResult:
    score: int
    approved: bool
    failures: list[str]


def evaluate_content(content: str) -> EvaluationResult:
    failures: list[str] = []

    if not SOURCE_PATTERN.search(content):
        failures.append("missing_source_attribution")

    lowered = content.lower()
    if "guaranteed" in lowered:
        failures.append("unqualified_guarantee_claim")

    if PII_PATTERN.search(content):
        failures.append("contains_ssn_like_pii")

    score = max(0, 100 - (len(failures) * 35))
    approved = not failures
    return EvaluationResult(score=score, approved=approved, failures=failures)
