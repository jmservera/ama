"""Policy checks: Copilot Code Review stays advisory and outside cancelling CI concurrency."""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOWS = Path(__file__).resolve().parents[2] / "workflows"
REVIEW_MARKERS = ("copilot-pull-request-reviewer", "copilot_code_review")


def test_given_workflows_when_scanned_then_no_copilot_review_in_cancelling_concurrency():
    # Arrange
    offenders = []
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        concurrency = data.get("concurrency")
        cancelling = isinstance(concurrency, dict) and bool(concurrency.get("cancel-in-progress"))
        if cancelling and any(marker in text for marker in REVIEW_MARKERS):
            offenders.append(path.name)

    # Assert
    assert offenders == []


def test_given_ci_concurrency_group_when_read_then_it_is_pull_request_scoped_and_not_review_named():
    # Arrange
    data = yaml.safe_load((WORKFLOWS / "src-ci.yml").read_text(encoding="utf-8"))

    # Act
    group = data["concurrency"]["group"]

    # Assert
    assert "review" not in group.lower()
