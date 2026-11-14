<!-- markdownlint-disable-file -->
# RPI Plan: Surface Retained Sensor Values and Ground Quality AI Review Flags (Issue #1288)

## Task Metadata

* Task ID: quality-1288-sensor-ai-2142
* Task slug: quality-1288-sensor-ai-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-plan-critique.md

## Executive Summary

This plan completes end-to-end retained sensor value surfacing, conflict blocking, and source provenance grounding for Quality AI review flags (`Issue #1288`) across `src/core` and `src/api`. While the worktree already starts identical-timestamp conflict detection in `sensor_view.capture_source()`, downstream `grounding()`, `reading_health()`, `advisory()`, `trend_summary()`, case chat, API badges, employee UI panels, and Quality AI `review_flag()` still pick a winning reading or omit structured source provenance for cited evidence. We propagate conflict handling through every read projection (without altering the coarse 6-hour `sensor_view.signature()` rate-limit bucket), suppress single-reading `Latest:` promotion and directional 7-day trend averaging on clashes, enrich Quality AI `review_flag` payloads and plain-language employee UI blocks with per-citation locator/hash and synthetic reading source grounding, and verify both `src/core` and `src/api` with bare `mypy`, `ruff`, sibling `#1288` suites, and touched browser checks.

### User Decisions and Requirements Highlights

* Reuse existing `quality-evidence`, retained sensor storage, and Quality UI surfaces without adding a new service, simulator, or ingestion engine (`Issue #1288`) -> all changes stay inside `src/core` and `src/api`.
* Conflicting retained readings must never pick a winning value silently or generate an autonomous L4 `review-suggested` flag (`Issue #1288` AC 4, AC 6) -> `grounding()`, `reading_health()`, `advisory()`, `sensor_badges`, `eligible()`, and `review_flag()` explicitly surface a conflict state and manual quality route.
* Quality AI review flags must ground every finding with retained sensor values and source provenance (`Caller prompt`, `Issue #1288` AC 3, AC 5) -> `review_flag()` projects per-reading synthetic source metadata plus a `source_provenance` list covering all `cited_ids` (`sensor:*` and `source:*`).
* Verify with bare `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` (and `src/api` when touched), commit cleanly with the Copilot trailer, and do not push (`Caller prompt`).

### What You May Not Know

* `Assistants._view()` preserves proactive flag actionability (`keeps`) when new readings arrive within the same 6-hour scheduling bucket; checking both captured `sensors["conflicting_readings"]` and `current["sources"]["sensors"]["conflicting_readings"]` inside `review_flag()` prevents a newly-arrived conflicting row from leaving an autonomous L4 flag active.
* `src/api/tests/test_content_standard.py` strictly forbids internal jargon (`provenance`, `snapshot`, `gate`, `hold`, `trace`, `envelope`) and unowned `BLOCKED_WORDS` (`unavailable`, `cannot`, `failed`, etc.) in `src/api/src/zava_forward/api/web/*.js` literal strings, so UI labels must use plain English (`"Source:"`, `"Cited source records:"`, `"Conflicting readings"`).

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for `Issue #1288` (`feat(quality): show retained sensor values and ground Quality AI review flags`) on branch `feat/quality-1288-sensor-ai-2142` (`Caller prompt`).
* Ensure retained sensor values are surfaced with synthetic provenance, units, observation timestamps, uncalibrated/non-diagnostic framing, and explicit `mould_risk_index` non-retention disclosure (`Issue #1288` AC 1, AC 2; `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md` `C1`, `C2`, `C10`).
* Ensure Quality AI consumes identical authorized reading IDs/values and bounded checklist/document evidence, and ground Quality AI review flags with source provenance (`locator`, `content_hash`, synthetic `provenance_class` / plain-language source description, `source_time`, model/version, and unapproved status) (`Caller prompt`, `Issue #1288` AC 3, AC 4, AC 5; research `C5`, `C6`, `C10`).
* Missing, stale, rejected, withdrawn, or conflicting readings must produce an explicit non-normal state and human manual route without generating an autonomous L4 flag (`Issue #1288` AC 6; research `C2`, `C3`, `C5`, `C6`, `C9`).
* Reuse existing `quality-evidence`, retained storage, and employee UI surfaces; follow Web Development Guidance (plain-language content standard, Fluent 2, WCAG 2.2 AA) for any `web/*.js` edits (`Issue #1288`, `.github/copilot-instructions.md`; research `C11`).
* Write all 4 `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), verify with bare `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api`, commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do NOT push (`Caller prompt`).

## Goals

* Propagate retained sensor conflict detection end-to-end across `sensor_view`, deterministic case chat, API badges, and Quality AI review flags so conflicting readings never appear normal or trigger autonomous L4 flags.
* Ground Quality AI `review_flag` payloads and employee UI rendering with structured source provenance (captured snapshot locators, content hashes, synthetic reading provenance classes, plain-language source descriptions, and invocation event modes) alongside retained sensor values.
* Prove behavior and regression safety across `src/core` and `src/api` with focused unit/API correlation tests, bare `mypy`, and `ruff`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/sensor_view.py` (`conflicts`, `capture_source`, `grounding`, `reading_health`, `advisory`, `trend_summary`, `_view`; leaving `signature` unchanged to preserve the 6-hour proactive rate-limit bucket).
* `src/core/src/zava_forward/core/chat_case_answers.py` and `src/core/src/zava_forward/core/chat_panel.py` (sensor conflict and grounded reading source facts and `decision-rule` citations).
* `src/core/src/zava_forward/core/assistants.py` (`eligible`, `review_flag`, and `_view` conflict gating + structured `source_provenance` and per-reading source grounding, preserving `review_flag(..., actionable=True, ...)` signature defaults).
* `src/api/src/zava_forward/api/sensor_badges.py` and `src/api/src/zava_forward/api/web/{ops.js,assistants.js,chat.js}` (`conflict` badge, `next_action`, plain-language conflict notice, and grounded review-flag source display).
* Focused tests in `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py`, and `src/api/tests/test_sensor_staleness_ui_badge.py`.

### Non-Goals

* Building new sensor simulators, telemetry ingestion pipelines, or standalone agent microservices.
* Changing database schemas, infrastructure Bicep templates, Dockerfiles, dependency manifests, or CI workflows.
* Pushing commits to `origin` or opening/modifying a remote PR.

## Functional Requirements

* Conflicting retained sensor readings for the same `(sensor_id, observed_at)` with distinct `(temperature_c, humidity_pct)` must be surfaced without choosing one value.
  * Observable acceptance criteria: `sensor_view.reading_health()` returns `state="conflict"`, `sensor_view.grounding()` sets `citation=None, values=None` with `conflicting_citations`, `sensor_view.advisory()` withholds `"Sensor watch"` with conflict explanation, `chat_case_answers` cites the conflict notice and manual check, and `/api/cases/<id>/sensors` emits a `"conflict"` badge and plain-language `next_action`.
* Grounded non-conflicting retained sensor readings must carry both exact values and synthetic source provenance.
  * Observable acceptance criteria: `sensor_view.grounding()` preserves `values={"temperature_c", "humidity_pct", "observed_at"}` while adding `provenance_class` and plain-language `source_text`, and `ops.js` renders retained readings, provenance descriptions, non-retained `mould_risk_index` notice, and any `conflict_notice`.
* Quality AI proactive eligibility and `review_flag` projection must ground cited evidence with source provenance and refuse autonomous L4 flags on conflicting readings.
  * Observable acceptance criteria: `assistants.eligible()` skips sensor-only proactive triggers when `conflicting_readings` is non-empty; `assistants.review_flag()` downgrades captured or current same-bucket conflicts to `status="conflicting-readings"`, `autonomous=False`, `level=None`; each entry in `flag["readings"]` includes `provenance_class`, `source_text`, `locator`, and `content_hash`; and `flag["source_provenance"]` maps every ID in `flag["cited_ids"]` (`sensor:*` and `source:*`) to its captured snapshot `locator` and `content_hash` (plus synthetic provenance on sensor readings), while consent withdrawal still withholds all sensor IDs/values.
* Employee UI Quality AI review flag rendering must display conflict status and cited source records in plain language.
  * Observable acceptance criteria: `assistants.js` maps `"conflicting-readings"` in `FLAG_TITLES`, appends reading source descriptions and cited source locators, and renders `conflict_notice` when present without violating `test_content_standard.py`.

## Non-Functional Requirements

* Static type safety, lint cleanliness, and formatting compliance across touched packages.
  * Objective threshold or evaluation condition: Zero errors from bare `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in both `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Execute directly from `src/core` and `src/api` directories in this worktree.
  * Observable acceptance criteria: Exit code `0` for all six static check commands.
* Plain-language, Fluent 2, WCAG 2.2 AA, and privacy/consent-withdrawal invariants.
  * Objective threshold or evaluation condition: Zero banned jargon (`provenance`, `snapshot`, `gate`, `hold`, `trace`, `envelope`) or unowned blocked words in `web/*.js`, zero consent-withdrawn reading leaks, and 6-hour proactive scan rate limit preserved.
  * Operating condition or verification approach, if needed: Run worktree-scoped `unittest` suites covering `test_content_standard`, `test_design_system`, `test_accessibility_baseline`, `test_quality_sensors`, `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_sensor_staleness_ui_badge`, and `src/core/tests`.
  * Observable acceptance criteria: All targeted `src/core` and `src/api` unit tests pass with exit code `0`.

## Acceptance Criteria

* `/api/cases/<id>/sensors` and `ops.js` surface retained `temperature_c` and `humidity_pct` values, units, observation timestamps, synthetic provenance descriptions, `mould_risk_index` non-retention disclosure, and explicit `"conflict"` badge + `next_action` + `conflict_notice` when identical-timestamp readings disagree.
* `sensor_view.grounding()`, `reading_health()`, `advisory()`, and case chat (`chat_case_answers`) refuse to pick a single reading on conflict and preserve exact backward-compatible `values` keys plus `provenance_class`/`source_text` when non-conflicting.
* `assistants.review_flag()` enriches `readings` with `provenance_class`, `source_text`, `locator`, and `content_hash`, projects `cited_provenance_classes`, `source_provenance` (for all `cited_ids`), and `invocation_modes`, blocks autonomous L4 `review-suggested` status on captured or current conflicting readings (`status="conflicting-readings"`, `autonomous=False`), and withholds all reading data on consent withdrawal.
* Focused tests (max 4 test files updated/created, zero test removals) prove semantic conflict propagation, source provenance grounding, UI plain-language compliance, and API/snapshot correlation.
* Bare `mypy`, `ruff check .`, and `ruff format --check .` pass in `src/core` and `src/api`, all four `.copilot-tracking/` artifacts exist, and all changes are committed cleanly on `feat/quality-1288-sensor-ai-2142` with the Copilot trailer and empty `git status --short` (unpushed).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-plan.md                                                                   |
| Phase details                    | .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md                                                        |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-plan-critique.md with Revise disposition (`PC-001`–`PC-006` resolved in plan and details) |
| Relevant research                | .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md                                                            |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md is created by implementation as its evidence record          |
| Planning execution and readiness | Complete and Ready for implementation (`focused` validation tier recorded; hosted CI not yet observed on unpushed branch)                |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `Implement` (`rpi-implement`)                                                 |

## Sources

* `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md`: Codebase evidence `C1`–`C12`, gap analysis, contrarian findings, and selected Option A architecture.
* `GitHub Issue #1288`: Acceptance criteria `1`–`7` and `9`, governance constraints, and reuse boundaries.
* `.github/copilot-instructions.md`: Validation tier classification (focused tier for bounded app/UI refinement), Web Development Guidance, plain-language and Fluent 2 / WCAG baseline rules, and privacy-safe git commit rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Retained Sensor Conflict Propagation and Provenance Grounding

* Intent: Ensure `sensor_view` and case-chat fact projection propagate identical-timestamp reading conflicts without selecting an arbitrary reading, and attach synthetic source provenance to grounded non-conflicting readings.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Propagate `conflicting_readings` and reading provenance across `sensor_view.py`

* Requirement and evidence: Research `C1`–`C4`; Issue #1288 AC 1, AC 2, AC 4, AC 6; Critique `PC-001`, `PC-004`.
* Expected result: `capture_source()` records `conflicting_readings` and `conflict_notice`; `reading_health()` returns `state="conflict"` on clash; `grounding()` reuses `dict(out, ...)` (`NOT_RETAINED`) to clear `citation`/`values` and list `conflicting_citations` on clash while adding sibling `provenance_class` and `source_text` when non-conflicting; `advisory()` withholds watch on clash; `trend_summary()` and `_view()` return `direction="insufficient"` rather than averaging conflicting values; `signature()` stays unchanged so the 6-hour proactive bucket is preserved.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Surface sensor conflict and reading source provenance in deterministic case chat

* Requirement and evidence: Research `C7`; Issue #1288 AC 2, AC 6; Critique `PC-003`.
* Expected result: `chat_case_answers.sensor_facts()` sets `sensor.detail` fallback, `sensor.conflict`, and `sensor.source`; `chat_panel.SENSOR_RULE_PATHS` marks both as `decision-rule`; `_sensor()` checks `r.fact("sensor.conflict")` first when `not cite` (emitting `decision-rule` citations without claiming no readings are shown) and binds `{case_id}/sensor.source` via `r.fact("sensor.source")` on clean readings.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Quality AI Review Flag Source Provenance and Conflict Gating

* Intent: Ground Quality AI `review_flag` findings with per-reading and per-citation snapshot provenance, and prevent conflicting readings from triggering proactive sensor scans or projecting autonomous L4 flags.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Gate conflicting readings in `eligible()` and ground `review_flag()` with `source_provenance`

* Requirement and evidence: Research `C5`, `C6`; Issue #1288 AC 3, AC 4, AC 5, AC 6; Critique `PC-001`, `PC-006`.
* Expected result: `assistants.eligible()` skips sensor-only proactive triggers when `conflicting_readings` is truthy; `assistants.review_flag()` preserves `actionable=True` positional defaults, downgrades actionable captured conflicts and same-bucket `current_conflicts` (even when `provenance_class` sets widen) to `status="conflicting-readings"` (`autonomous=False`, `level=None`), adds `provenance_class`, `source_text`, `locator`, and `content_hash` to each item in `readings`, adds `cited_provenance_classes`, `source_provenance` (covering all `cited_ids`), and `invocation_modes` (`e.get("kind") == "invocation"`), and preserves complete redaction when `withheld=True`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: API Badges, Plain-Language Employee UI Surfacing, and Verification

* Intent: Surface sensor conflicts and Quality AI source provenance in `/api/cases/<id>/sensors` and employee web scripts while complying with Fluent 2, WCAG 2.2 AA, and plain-language content standards, and verify with focused tests, sibling `#1288` suites, touched browser checks, `mypy`, and `ruff`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `"conflict"` badge/guidance in `sensor_badges.py` and plain-language UI surfacing in `web/*.js`

* Requirement and evidence: Research `C8`–`C11`; Issue #1288 AC 1, AC 5, AC 6, AC 7; `.github/copilot-instructions.md` Web Development Guidance; Critique `PC-002`, `PC-005`.
* Expected result: Load `web-design-guidelines` and `redesign-existing-projects` first (disclosing any remote source-fetch limitation); `sensor_badges.py` adds `"conflict"` health badge and `next_action` with precedence ahead of `"offline"` for context-only clashes; `ops.js` suppresses single-reading `Latest:` promotion on conflict while keeping `sensorTable` and rendering `v.conflict_notice`; `assistants.js` maps `"conflicting-readings"` in `FLAG_TITLES` and renders per-reading `source_text`, cited source record locators, and `conflict_notice` in plain English; `chat.js` mirrors `sensor.source` and `sensor.conflict` in `RULE_PARTS`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Extend focused `src/core` and `src/api` tests and run static, sibling `#1288`, and browser verification

* Requirement and evidence: Research `C11`, `C12`; Issue #1288 AC 8, AC 9; Critique `PC-005`, `PC-006`.
* Expected result: Strict-typed (`-> None`) semantic and regression tests pass in `src/core/tests/test_sensor_view_conflicts.py`, `src/api/tests/test_quality_sensor_grounding.py`, `src/api/tests/test_quality_sensors_correlation.py`, and `src/api/tests/test_sensor_staleness_ui_badge.py`, plus sibling `#1288` suites (`test_quality_sensors`, `test_quality_sensors_{c7,e1,e2}`, `test_sensor_trend_summary`), UI/content suites, touched browser checks (`checks.quality_sensors_browser_check`, `checks.employee_chat_browser_check` without `/tmp`), and bare `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api`; validation tier (`focused`) and unobserved hosted CI are recorded.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-phase-details.md

## Dependencies

* `P01` precedes `P02` and `P03`: `assistants.py`, `sensor_badges.py`, and `ops.js` consume `sensor_view` fields (`conflicting_readings`, `conflict_notice`, `health.state == "conflict"`, `grounding.provenance_class`, `grounding.source_text`).
* Web Development Guidance skills (`web-design-guidelines`, `redesign-existing-projects`) precede `P03-T01` edits to `src/api/src/zava_forward/api/web/*.js`.
* Worktree `PYTHONPATH` prefixing (`PYTHONPATH=src:tests` in `src/core`; `PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests` in `src/api`) is required when running `unittest` so global editable installs from `/home/azureuser/source/ama` do not shadow worktree code.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 — `PC-001` [High]  | resolved    | Kept `sensor_view.signature()` unchanged (preserving the 6-hour rate-limit bucket), preserved `review_flag(..., actionable=True, ...)` positional defaults, and updated `P02-T01` so same-bucket `current_conflicts` take precedence over `"not-current"` even when `provenance_class` sets widen. |
| Run 1 — `PC-002` [High]  | resolved    | Guarded `ops.js:88` (`v.latest`) on conflict while retaining `sensorTable`, and prioritized `"conflict"` ahead of `"offline"` in `sensor_badges.py` (`health_state` and `next_action`) for context-only (`latest=None`) clashes. |
| Run 1 — `PC-003` [High]  | resolved    | Updated `P01-T02` so `_sensor()` checks `r.fact("sensor.conflict")` first when `not cite` and binds `{case_id}/sensor.source` via `r.fact("sensor.source")` on clean readings. |
| Run 1 — `PC-004` [Medium]| resolved    | Replaced nonexistent `OMITTED`/`OMITTED_REASON` in `P01-T01` with `dict(out, ...)` (`NOT_RETAINED`) and withheld directional 7-day `trend_summary()` averaging (`direction="insufficient"`) when readings conflict. |
| Run 1 — `PC-005` [Medium]| resolved    | Added `web-design-guidelines` pre-edit/review workflow, sibling `#1288` suites (`test_quality_sensors_{c7,e1,e2}`, `test_sensor_trend_summary`), touched browser checks (no `/tmp` paths, explicit prerequisite disclosure), and validation-tier (`focused`) + unobserved hosted-CI recording to `P03`. |
| Run 1 — `PC-006` [Low]   | resolved    | Filtered `e.get("kind") == "invocation"` for `invocation_modes` in `P02-T01` and required strict `mypy` annotations (`-> None`, typed helpers) on modified test files in `P03-T02`. |

## Follow-Up Items

* Pre-existing `origin/main` (`f5f76b6cc`) `#employee-chat-question` `target-size` (`partiallyObscured`) axe violation in `checks.employee_chat_browser_check` `demo-disclaimer-model-answer` state on a 720px-tall viewport after plain-language toggle/alert header additions (`#1690` / `#1718`): adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` in a dedicated UX follow-up.
* Add an automated browser scenario in `src/api/checks/quality_sensors_browser_check.py` exercising live same-bucket conflicting-reading arrival (`data-sensor-conflict`, `data-flag-conflict`, `data-flag-sources`) under pinned `axe-core` 4.10.3.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` completed; ready for `Review`)
* Remaining provisional question or blocker: None; hosted CI remains unobserved locally because pushing is explicitly prohibited by caller instructions.
