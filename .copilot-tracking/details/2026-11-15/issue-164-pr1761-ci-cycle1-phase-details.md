<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #164 PR #1761 Cycle 1 Hosted CI `src-api` Fix

## Metadata

* Task ID: issue-164-pr1761-ci-cycle1
* Task slug: issue-164-pr1761-ci-cycle1
* Related plan: .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-164-pr1761-ci-cycle1-research.md (`C1`–`C4`)

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Align Held Manager Report Test Contract and Validate `src/api` | ready | P01, P01-T01 |

<!-- rpi:phase id=P01 -->
## P01: Align Held Manager Report Test Contract and Validate `src/api`

### Context

In PR #1761 (`feat/ai-164-chat-revocation-0042`), commit `7124ab572` added `"chat_evaluation": chat_eval.run_eval()` to `GET /api/ai/report` in `src/api/src/zava_forward/api/server.py` (`C2`). Hosted `src-api` CI failed in `test_manager_report_local_http_and_bad_period` (`src/api/tests/test_ai_consumption_api.py`) because the consumption-hold loop still checked `set(held) == {"evaluation", "live", "registry", "consumption"}` (`C1`).

### Intent

Update `test_manager_report_local_http_and_bad_period` so held `/api/ai/report` responses require `"chat_evaluation"` alongside `"evaluation"`, `"live"`, `"registry"`, and `"consumption"`, and verify `held["chat_evaluation"]` parity and disabled enablement state across all targeted `src/api` checks.

### Boundaries

* Included: `src/api/tests/test_ai_consumption_api.py`.
* Excluded: Application runtime modules (`server.py`, `chat_eval.py`, `ai_eval.py`), live task enablement, and full-gate `tools/rpi-checks.py --all`.

### Likely Targets

* `src/api/tests/test_ai_consumption_api.py`: Update `set(held)` expectation in `test_manager_report_local_http_and_bad_period` and add `held["chat_evaluation"]` key, `version`, and `enablement["state"] == "disabled"` assertions mirroring `held["evaluation"]`.

### Dependencies

* None.

### Validation Expectations

* `PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py` passes in `src/api`.
* `python3 -m ruff check src tests`, `python3 -m ruff format --check src tests`, and `python3 -m mypy tests/test_ai_consumption_api.py` pass in `src/api`.

### Completion Evidence

* Both `"meter-capacity-reached"` and `"meter-evidence-invalid"` subtests in `test_manager_report_local_http_and_bad_period` pass and confirm `chat_evaluation` presence and parity, with `ruff` and `mypy` clean.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update held `/api/ai/report` assertions in `src/api/tests/test_ai_consumption_api.py` and run focused validation

#### Context

When `app.assistants.consumption.report(...)` raises `ai_consumption.DispatchHeld`, `GET /api/ai/report` returns HTTP 200 with unavailable `consumption` while preserving `evaluation`, `chat_evaluation`, `live`, and `registry` (`C2`). `test_manager_report_local_http_and_bad_period` already checks `set(held["evaluation"]) == set(result["evaluation"])` and `held["evaluation"]["version"] == result["evaluation"]["version"]` (`C3`).

#### Intent

Include `"chat_evaluation"` in `set(held)` and assert `set(held["chat_evaluation"]) == set(result["chat_evaluation"])`, `held["chat_evaluation"]["version"] == result["chat_evaluation"]["version"]`, and `held["chat_evaluation"]["enablement"]["state"] == "disabled"`.

#### Boundaries

* Edit only `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py`; keep line formatting compliant with `ruff format --check` (`line-length = 100` in `src/api/pyproject.toml`).

#### Validation

* Run the exact caller-specified `unittest` (`-B`), `ruff check`, `ruff format --check`, and `mypy` command from `src/api`.
