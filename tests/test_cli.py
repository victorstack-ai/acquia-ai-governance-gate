from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_returns_success_for_compliant_content(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("Compliant text with citation [Ref](https://example.com).", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "acquia_ai_governance_gate.cli", str(draft)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"approved": true' in result.stdout.lower()


def test_cli_returns_nonzero_for_noncompliant_content(tmp_path: Path) -> None:
    draft = tmp_path / "draft.md"
    draft.write_text("Guaranteed success for everyone.", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "acquia_ai_governance_gate.cli", str(draft)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "missing_source_attribution" in result.stdout
