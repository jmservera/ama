---
title: "Implementation Changes: Live Release Admission & Readiness Hardening (#218 Child)"
description: "Execution log and validation record for child task rai-218-release-admission-hardening"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

* Task ID: `issue-218-rai-release-admission-hardening`
* Task Slug: `rai-218-release-admission-hardening`
* Plan: `.copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md`
* Critique: `.copilot-tracking/reviews/2026-11-15/rai-218-release-admission-hardening-plan-critique.md`
* Declared Scope: Full plan (`P01`, `P02`)
* Status: `Complete`
* Review readiness: `Ready`

## Opening Implementation State

* Active plan scope: `P01` (`P01-T01`, `P01-T02`) and `P02` (`P02-T01`, `P02-T02`)
* Starting item: `P01-T01`
* Blockers: None

## Completed Work

### Live Release Binding and Dispatch Hardening (`P01`, `P01-T01`, `P01-T02`)

* `src/core/src/zava_forward/core/rai_release.py`: Removed inner key-presence guards inside `if live and ("approved_by" in record or "named_approval_id" in record):` in `missing_binding` so supplying either `OQ-017` field requires both `valid_named_human_approver` and `valid_named_approval_id` while preserving isolated 4-key unit test contracts (`RV-001`).
* `src/core/src/zava_forward/core/assistant_release.py`: Normalized every SQL-loaded record in `assessment(..., live=True)` with `rec.setdefault("approved_by", None)` and `rec.setdefault("named_approval_id", None)` prior to `invalidate_changed` and `rai_release.select` so pre-existing or out-of-band SQL rows cannot bypass `OQ-017` at live dispatch or readiness inspection (`RV-001`).
* `src/core/src/zava_forward/core/rai_control_plane.py`: Replaced raw SQL row field checks in `_inspect_sql_live_releases` with read-only `_assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` against `_assistants.runtime_binding` and `_ai_registry.legacy_binding` (with default-safe route/deployment lookup and DB-clock resolution) and removed unused `sqlite3` import (`RV-002`, `PC-001`).

### Focused Regression Tests and Package Validation (`P02`, `P02-T01`, `P02-T02`)

* `src/core/tests/test_rai_control_plane_218.py`: Extended `missing_binding` assertions for partial `OQ-017` keys and `expires=True`, and added `test_stored_sql_row_without_oq017_or_with_drifted_binding_is_denied_live` proving stored SQL rows lacking `OQ-017` fields or having drifted `prompt_version` fail live admission and readiness while remaining `"active"` under `read_only()`.
* `src/api/tests/test_rai_release_readiness_api_218.py`: Verified `verify_traceability_targets()["all_resolved"] is True` and added `test_ai_report_rejects_drifted_or_legacy_unapproved_sql_release_rows_read_only` (`PC-002`), staying at 2 new test methods total (`<= 6` budget in `NFR-H03`).

## Implementation Discoveries and Plan Updates

* Local judgment: Addressed test assertion nesting path (`real_ai_delivery_gate.checks.oq017_named_live_releases_recorded.unapproved_live_tasks`) to match `exercise_acceptance_report` schema. No plan amendments or divergences required.

## Validation Evidence

* `python3 -m ruff format --isolated --line-length 100 --check` on touched `#218` source and test files: Passed (`4 files already formatted`)
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`: Passed (`0` lint/format errors; `Success: no issues found in 357 source files`)
* `cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy`: Passed (`0` lint/format errors; `Success: no issues found in 298 source files`)
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest` across 12 `src/core` and `src/api` RAI/release/governance/continuity suites: Passed (`Ran 281 tests in 92.153s — OK (skipped=23)`)
* `python3 tools/rpi-checks.py`: Skipped per explicit caller focused-tier instruction

## Blockers, Remaining Work, and Follow-Up Items

* Blockers: None
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`)
* Follow-Up Items: None
* Review Handoff: Ready for single post-implementation `rpi-review` at `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-admission-hardening-review.md`
