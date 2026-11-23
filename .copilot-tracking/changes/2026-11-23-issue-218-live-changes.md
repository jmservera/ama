# Changes: issue 218 live (2026-11-23)

Tier FULL (src change), local commit only, no push, no `rpi-checks.py --all`.

## Files

* `src/core/src/zava_forward/core/rai_control_plane.py`: `test_tree_present`, `target_verification` and honest check detail, so a deployment without a test tree no longer fails exercise acceptance falsely; unresolved targets with a test tree still fail closed.
* `src/core/tests/test_rai_control_plane_218.py`: new test and extended fail-closed assertion.
* `docs/reference/research/issue-218-live-rai-readiness-recheck-2026-11-23.md`, `docs/reference/log.md`: evidence note and log entry.
* `.copilot-tracking/evidence/2026-11-23/issue-218-live/`: probe script, outputs, screenshot.

## Validation

Core 218 tests 8 OK; core rai/governance/assistant suites OK; api 218 readiness test 5 OK; ruff check and isolated format clean; mypy unchanged (3 pre-existing errors). Not run: hosted CI, redeploy. Live `/api/ai/report` gave 503/500 under shared SQL write contention (unproven).

## Per-criterion proven or unproven

| Criterion | Status | Why |
| --- | --- | --- |
| Stabilization checkpoint (#440) | Unproven | Owner approval of triage and deferrals, plus a PR and independent review, are required |
| Children closed or deferred by owner | Unproven | #220 and #223 open; no owner deferral; #223 needs real reviewers and OQ-017 holders |
| No live AI activation without named approval | Proven (live gate, offline test) | 0 approved, 11 unapproved live tasks |
| Requirements trace to check or deferral | Proven offline; live fix undeployed | 15 of 15 resolved in repo |
| RAI checks separate from real-AI gate | Proven live | Two independent sections |
