# Plan 2026-11-24: issue 157 live recheck

Task `issue-157-live-20261124T035902Z`. Research: `.copilot-tracking/research/2026-11-24-issue-157-live-research.md`. Details: `.copilot-tracking/details/2026-11-24-issue-157-live-details.md`. Critique: `.copilot-tracking/plans/2026-11-24-issue-157-live-critique.md`.

## Phases

* [ ] Phase 1: failing-first tests for runtime retention enforcement and live-only memory limit (`src/core/tests/test_chat_privacy.py`, `test_chat_isolation_single_model_route.py` or the isolation test file).
* [ ] Phase 2: implement `ChatPrivacy.sweep_retention` (throttled) and call it from `ChatIsolation.current_user`; count live memory only in `add_memory`.
* [ ] Phase 3: validate (focused core chat tests, focused api chat tests, ruff, mypy for core) and update the storage approval note and knowledge-base index/log.
* [ ] Phase 4: research note under docs/reference/research with the per-criterion table; changes record; review; local commit.

## Tier

Full tier applies because `src/` changes. The coordinator runs the gate; this worker runs only targeted checks and never `rpi-checks.py --all`.
