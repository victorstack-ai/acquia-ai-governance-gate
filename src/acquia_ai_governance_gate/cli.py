from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate_content


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="acquia-governance-gate",
        description="Run governance checks against an AI-generated content draft.",
    )
    parser.add_argument("input_file", type=Path, help="Path to content markdown/text file.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    content = args.input_file.read_text(encoding="utf-8")
    result = evaluate_content(content)

    print(
        json.dumps(
            {"score": result.score, "approved": result.approved, "failures": result.failures},
            indent=2,
        )
    )
    return 0 if result.approved else 2


if __name__ == "__main__":
    raise SystemExit(main())
