"""Transient GitHub 5xx handling in the baseline refresh step (issue 2381, run 45659656937)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_record_workflow as rw

steps = rw.steps
recording_repo = rw.recording_repo
remote_ref = rw.remote_ref
run_refresh = rw.run_refresh

BRANCH = "rubric/baseline-refresh"


@pytest.mark.parametrize(
    ("failing", "existing_pr"),
    [("pr list", None), ("pr edit", "1"), ("pr view", None)],
)
def test_transient_pull_request_api_failure_is_retried(
    steps: Any, tmp_path: Path, failing: str, existing_pr: str | None
) -> None:
    root, remote, out, _, scored = recording_repo(tmp_path)
    result, calls = run_refresh(
        steps, tmp_path, root, remote, out, scored, GH_FAIL_ONCE=failing, GH_EXISTING_PR=existing_pr
    )
    assert result.returncode == 0, result.stderr
    assert sum(call.startswith(failing + " ") for call in calls) >= 2
    assert sum(call.startswith("pr merge ") for call in calls) == 1
    assert sum(call.startswith("pr create ") for call in calls) == (0 if existing_pr else 1)


def test_persistent_pull_request_view_failure_fails_closed(steps: Any, tmp_path: Path) -> None:
    root, remote, out, _, scored = recording_repo(tmp_path)
    result, calls = run_refresh(
        steps, tmp_path, root, remote, out, scored, GH_FAIL_ALWAYS="pr view"
    )
    assert result.returncode != 0
    assert sum(call.startswith("pr view ") for call in calls) == 5
    assert not any(call.startswith("pr merge ") for call in calls)
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is not None
