<!-- markdownlint-disable-file -->
# Research: Issue #164 PR #1761 Cycle 1 Hosted CI `src-api` Fix

## Metadata

* Task ID: issue-164-pr1761-ci-cycle1
* Parent task: issue-164-chat-eval-revocation
* Date: 2026-11-15
* Research disposition: satisfied-and-skipped
* Planning Readiness: Ready

## Evidence Summary

* **C1 — Hosted CI failure (`src-api` on PR #1761, commit `7124ab572`)**: `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py` (line 2089) failed with `AssertionError: Items in the first set but not the second: 'chat_evaluation'` on `self.assertEqual(set(held), {"evaluation", "live", "registry", "consumption"})`.
* **C2 — Endpoint contract (`src/api/src/zava_forward/api/server.py`, lines 930-938)**: `GET /api/ai/report` returns `{"evaluation": ai_eval.run_eval(), "chat_evaluation": chat_eval.run_eval(), "live": s.ai_live_report(), "registry": ai_registry.registry(), "consumption": consumption}` both normally and when `ai_consumption.DispatchHeld` is caught during `"meter-capacity-reached"` or `"meter-evidence-invalid"` holds.
* **C3 — Repository-wide blast radius**: Grep across `src/` confirms line 2089 of `src/api/tests/test_ai_consumption_api.py` is the sole exact key-set assertion on `/api/ai/report` that omitted `"chat_evaluation"`. Adjacent assertions on lines 2090-2092 verify `held["evaluation"]` keys/version and `held["registry"]` against `result`; matching assertions for `held["chat_evaluation"]` keys, `version`, and `enablement` (`state == "disabled"`) confirm `chat_evaluation` is preserved identically when metering is held.
* **C4 — Validation tier**: Focused tier applies (test-only regression alignment for an existing API field, with zero workflow, permission, image, dependency, SQL, infrastructure, or security-control changes). Planned checks are the exact `src/api` `unittest` (`tests/test_ai_consumption_api.py`, `tests/test_ai_tasks.py`), `ruff check src tests`, `ruff format --check src tests`, and `mypy tests/test_ai_consumption_api.py` suite.
