<!-- markdownlint-disable-file -->
# RPI Changes: Surface Retained Sensor Values and Ground Quality AI Review Flags (Issue #1288)

## Metadata

* Task ID: quality-1288-sensor-ai-2142
* Related plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: None
* Status basis: Every phase and task in full-plan scope has completed source and test changes with passing static, unit, correlation, content-standard, and Quality sensor browser verification.

## Execution Summary

Delivered end-to-end retained sensor value surfacing, identical-timestamp reading conflict blocking, and Quality AI review-flag source provenance grounding for Issue #1288 across `src/core` and `src/api`. Conflicting readings for the same `(sensor_id, observed_at)` now propagate through `sensor_view`, deterministic case chat, `/api/cases/<id>/sensors` badges, employee UI panels, and Quality AI `eligible()` / `review_flag()` without picking an arbitrary reading, averaging conflicting 7-day trends, or leaving an autonomous L4 `review-suggested` flag active. Non-conflicting grounded readings and Quality AI `review_flag` findings carry structured synthetic provenance (`provenance_class`, `source_text`) and captured snapshot evidence identity (`locator`, `content_hash`, `source_provenance`, `invocation_modes`), while consent withdrawal continues to withhold all reading IDs and values.

## Completed Work

### Core Retained Sensor Conflict Propagation and Grounding (`P01`, `P01-T01`, `P01-T02`)

* `src/core/src/zava_forward/core/sensor_view.py`:
  * Retained `conflicts(rows)` and `capture_source()` attachment of `conflicting_readings` and plain-language `conflict_notice`, while keeping `signature()` unchanged so the 6-hour proactive scheduling bucket is preserved (`PC-001`).
  * Updated `grounding(sensors)` to return `citation=None`, `values=None`, and `conflicting_citations` on conflict (reusing `NOT_RETAINED` via `dict(out, ...)`), and added sibling `provenance_class` and plain-language `source_text` alongside exact 3-key `values` when non-conflicting (`PC-004`).
  * Updated `reading_health(sensors)` to return `state="conflict"` on `conflicting_readings`, `advisory(sensors)` to return `label="No watch"`, `watch=False` with conflict explanation, and `trend_summary()` / `_view()` to report `direction="insufficient"` instead of averaging disagreeing 7-day readings (`PC-004`).
* `src/core/src/zava_forward/core/chat_case_answers.py` and `src/core/src/zava_forward/core/chat_panel.py`:
  * Added `sensor.detail` fallback to `conflict_notice`, `sensor.conflict`, and `sensor.source` in `sensor_facts()`; registered `"sensor.source"` and `"sensor.conflict"` in `SENSOR_RULE_PATHS`; updated `_sensor(r)` to check `r.fact("sensor.conflict")` first when `not cite` (routing to the ordinary quality check with `decision-rule` citations and zero numeric values) and bind `{case_id}/sensor.source` on clean readings (`PC-003`).

### Quality AI Review Flag Source Provenance and Conflict Gating (`P02`, `P02-T01`)

* `src/core/src/zava_forward/core/assistants.py`:
  * Updated `eligible()` so sensor-only proactive scans skip snapshots with `conflicting_readings`.
  * Added `_sensor_bucket_key()` and updated `Assistants._view()` and `review_flag()` (preserving `actionable=True` positional defaults) so captured conflicts and same-bucket newly-arrived conflicts (even when `provenance_class` sets widen) resolve to `status="conflicting-readings"`, `autonomous=False`, `level=None` while keeping `withheld=True` highest priority (`PC-001`).
  * Enriched each entry in `review_flag["readings"]` with `provenance_class`, `source_text`, `locator`, and `content_hash`, and added `source_provenance` across all `cited_ids` (`sensor-reading` and `case-evidence`), `cited_provenance_classes`, and `invocation_modes` (`e.get("kind") == "invocation"`, `PC-006`).

### API Badges, Employee Web Surfacing, and Verification (`P03`, `P03-T01`, `P03-T02`)

* `src/api/src/zava_forward/api/sensor_badges.py`:
  * Added `"conflict"` to `_HEALTH` (`"Conflicting readings"`) and `_NEXT_ACTION`, and prioritized `"conflict"` ahead of `"offline"` (after `"withheld"` and `"unavailable"`) in `health_state()` and `next_action()` (`PC-002`).
* `src/api/src/zava_forward/api/web/ops.js`, `assistants.js`, and `chat.js`:
  * Loaded `web-design-guidelines` (fetched live rules from `vercel-labs/web-interface-guidelines`) and `redesign-existing-projects` prior to editing.
  * Updated `ops.js` to suppress `v.latest` promotion when `conflicting_readings` or `conflict_notice` is present while keeping `sensorTable` visible and rendering `data-sensor-conflict` (`PC-002`).
  * Updated `assistants.js` to map `"conflicting-readings"` in `FLAG_TITLES` and render `data-flag-conflict`, per-reading `Source: ${r.source_text}`, `data-flag-sources` (`Cited source records: ...`), and `cited_provenance_classes` in plain English without triggering `test_content_standard.py` jargon/blocked-word violations.
  * Updated `chat.js` `RULE_PARTS` to include `"sensor.source"` and `"sensor.conflict"`.
* Focused strict-typed (`-> None`) tests extended in 4 files:
  * `src/core/tests/test_sensor_view_conflicts.py`
  * `src/api/tests/test_quality_sensor_grounding.py`
  * `src/api/tests/test_quality_sensors_correlation.py`
  * `src/api/tests/test_sensor_staleness_ui_badge.py`

## Implementation-Time Plan and Detail Updates

* Updated `## Follow-Up Items` and `## Handoff` in `.copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md` and marked `P01`–`P03` `completed` in `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md`.
* Discovery classification: Running `checks.employee_chat_browser_check` uncovered a pre-existing `origin/main` (`f5f76b6cc`, after `#1690`/`#1718`) `target-size` (`partiallyObscured`) axe violation on `#employee-chat-question` in the `demo-disclaimer-model-answer` state at 720px viewport height (unrelated to our 2-token `RULE_PARTS` data list addition in `chat.js`, whereas `test_chat_panel` Chromium check and `checks.quality_sensors_browser_check` pass 100%). Classified as `follow-up-only` per repository `<rules_for_code_changes>` ("Don't fix unrelated pre-existing issues") and `rpi-implement`.

## Validation Record

* Validation tier classification: `focused tier` (owner decision D4 / issue #1294). Basis: bounded application and employee UI refinement in `src/core` and `src/api` with zero edits to infrastructure, Bicep, SQL schema/migrations, Dockerfiles, dependency manifests, GitHub workflows, or gate tools.
* Hosted CI status: Not yet observed locally (branch `feat/quality-1288-sensor-ai-2142` is intentionally unpushed per caller instruction `"Do NOT push"`).

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `Success: no issues found in 317 source files`; `All checks passed!`; `264 files already formatted` |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `Success: no issues found in 280 source files`; `All checks passed!`; `196 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -k "sensor\|chat\|quality"` | `src/core` | Passed | `303` sensor tests OK (`skipped=34`), `188` chat tests OK, `159` quality tests OK (`650` total, `0` failures) |
| `PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -m unittest ...` | `src/api` (`test_quality_sensors*`, `test_sensor_*`, `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_assistants`) | Passed | `542` sensor/grounding/correlation/UX/content tests OK (`skipped=179`) + `138` `test_assistants` tests OK (`skipped=60`) |
| `python3 -m checks.quality_sensors_browser_check --axe axe-4.10.3.min.js --out ...` | `src/api` Chromium + pinned axe 4.10.3 (non-`/tmp` scratch) | Passed | `42 checks passed`, zero page errors, zero serious/critical axe violations across all 9 scanned sensor/flag states |
| `ZF_BROWSER_TESTS=1 python3 -m unittest -v test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log` | `src/api` Chromium chat panel | Passed | `Ran 1 test in 3.153s - OK` |
| `python3 -m checks.employee_chat_browser_check --axe axe-4.10.3.min.js --out ...` | `src/api` Chromium employee chat | Pre-existing `origin/main` failure disclosed | Fails on `demo-disclaimer-model-answer` `#employee-chat-question` `target-size` (`partiallyObscured`, 18px < 24px at 720px height) due to `#1690`/`#1718` header height on `origin/main`; `chat.js` change in this task only adds `"sensor.source"` and `"sensor.conflict"` strings to `RULE_PARTS`; routed as follow-up |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all `[x]` in plan and `completed` in phase details).
* Completed-work evidence and handoff prose: Reconciled across plan, phase details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining tasks, `2` evidence-grounded follow-up items recorded).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md, `## Follow-Up Items`
* Adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` to clear the pre-existing `origin/main` (`#1690`/`#1718`) `#employee-chat-question` `target-size` (`partiallyObscured`) axe violation in `checks.employee_chat_browser_check` (`demo-disclaimer-model-answer`).
* Extend `src/api/checks/quality_sensors_browser_check.py` with a live conflicting-reading browser state check (`data-sensor-conflict`, `data-flag-conflict`, `data-flag-sources`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full_plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`; remaining None
* Validation coverage: Static (`mypy`, `ruff check`, `ruff format --check` in `src/core` and `src/api`), unit/correlation/content/UX (`src/core` and `src/api`), and Chromium + pinned axe (`quality_sensors_browser_check`, `test_chat_panel` browser test; pre-existing `employee_chat_browser_check` CSS target-size overflow disclosed and routed)
* Blockers: None
* Current plan and detail updates: All phases marked completed; 2 follow-up items recorded in plan
* Planning and critique state: Complete (`PC-001`–`PC-006` resolved)
* Follow-up items: 2 items recorded in canonical plan `## Follow-Up Items`
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent transitions directly to `Review` (`rpi-review`)
