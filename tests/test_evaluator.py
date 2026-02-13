from acquia_ai_governance_gate.evaluator import evaluate_content


def test_content_passes_with_source_and_no_risky_patterns() -> None:
    content = "This draft summarizes trends [Source](https://example.com/report)."
    result = evaluate_content(content)

    assert result.approved is True
    assert result.score == 100
    assert result.failures == []


def test_content_fails_when_multiple_violations_exist() -> None:
    content = (
        "Guaranteed outcomes for all customers. Contact user 123-45-6789. "
        "No explicit source is provided."
    )
    result = evaluate_content(content)

    assert result.approved is False
    assert result.score == 0
    assert set(result.failures) == {
        "missing_source_attribution",
        "unqualified_guarantee_claim",
        "contains_ssn_like_pii",
    }
