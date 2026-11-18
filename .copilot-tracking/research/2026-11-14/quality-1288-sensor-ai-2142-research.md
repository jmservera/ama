---
description: "Primary evidence artifact for Issue #1288 retained sensor values and Quality AI review flag grounding"
---
<!-- markdownlint-disable-file -->

# Task Research: quality-1288-sensor-ai-2142

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                 |
| Researcher / agent | rpi-research (RPI Agent)                                                   |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md |

## Research Brief

* What to research: Current retained sensor read model (`sensor_view.py`), Quality AI snapshot capture, review flag grounding/provenance, and conflict/missing/stale handling across `src/core` and `src/api` for Issue #1288, including pre-existing uncommitted worktree edits in `sensor_view.py` and `test_sensor_view_conflicts.py`.
* Why it matters: Issue #1288 requires retained sensor values to be surfaced with synthetic provenance and Quality AI review flags to be grounded in identical authorized reading IDs/values while explicitly handling missing, stale, conflicting, rejected, or unavailable readings without silent resolution or zero substitution.
* Audience or intended use: Engineering plan, implementation, and review phases in this RPI session on branch `feat/quality-1288-sensor-ai-2142`.
* Scope: `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/api/src/zava_forward/api/`, `src/api/tests/`, and prior `.copilot-tracking/` evidence for `#1288`.
* Non-goals: Live Azure IoT Hub activation, paid model invocation, new agent services/simulators/ingestion engines, or pushing to remote.
* Criteria: Every acceptance gap in `src/core` and `src/api` (especially conflicting/missing/stale retained readings, provenance grounding, Quality AI snapshot/proactive review flag handling, and `mypy` + `ruff` compliance) is mapped to concrete `path:line` evidence.
* Requested outputs: Convergence recommendation for minimal, complete surgical changes and focused tests in `src/core` (and `src/api` if touched).
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------|
| Research question(s)             | What gaps remain in retained sensor read/grounding and Quality AI review flag handling for #1288, and how do the existing uncommitted `sensor_view.py` conflict edits interact with Quality AI proactive review flags and UI/API surfaces? |
| Codebase scope                   | `src/core`, `src/api`, `.copilot-tracking`                                                      |
| External scope                   | none                                                                                            |
| Initial internal candidate areas | `src/core/src/zava_forward/core/sensor_view.py`, `src/core/tests/test_sensor_view_conflicts.py`, `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/` |
| Initial external candidate areas | none                                                                                            |
| Research posture                 | focused                                                                                         |
| Posture provenance               | default (bounded internal task with named source targets `src/core` and `src/api`)              |
| Explicit limits / deadline       | Do not push; bare `mypy`, `ruff check .`, and `ruff format --check .` must pass                 |
| Posture-specific completion basis| focused scope and materiality                                                                   |
| Edits allowed during research?   | no, research-only                                                                               |
| Resolved evidence root           | `.copilot-tracking/`                                                                            |
| Known constraints / excluded sources | No live Azure writes, model calls, or private datasets                                      |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md`| `applyTo: "**"` matches repository and tracking   | Validation tiers, branch/commit conventions, web rules | Selected: governs repository evidence and testing |
| Skill               | `python-foundational`            | Python typing/linting context                     | Python standards                             | Skipped: repository already defines strict `mypy` and `ruff` conventions |
| Skill               | `web-design-guidelines`          | Required only if web/UI files are edited          | UI rule audit                                | Deferred to Plan/Implement only if `src/api` web templates/CSS/JS need edits |
| Research specialist | `hve-core-all:rpi-researcher`    | General RPI lane researcher                       | Subagent lane artifact                       | Skipped: tightly coupled internal trace across `src/core` and `src/api` fits inline focused investigation |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                     | Answers / unanswered | Resulting decision or selected further research |
|------------------|-------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller scope, branch, worktree, and verify commands | N/A (non-interactive)| Proceed in focused convergence mode across `src/core` and `src/api` |
| Direction change | None yet                                                                                  | N/A                  | Maintain active brief                           |
| Convergence      | Pending Cycle 1 completion                                                                | Pending              | Pending                                         |

## Scope and Success Criteria

* Scope: Inspect existing `#1288` sensor read model, provenance, conflict detection, Quality AI snapshot capture, proactive review flag evaluation, and API/UI display/tests in `src/core` and `src/api`.
* Assumptions: Pre-existing dirty files (`sensor_view.py`, `test_sensor_view_conflicts.py`) in this dedicated worktree represent partial in-progress `#1288` work that must be audited for completeness, propagation into read model / grounding / proactive Quality AI flags / UI, and test coverage before integration.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect Issue #1288 and existing quality/sensor modules in `src/core` and `src/api` to ensure retained sensor values are surfaced and Quality AI review flags are grounded with source provenance and tests; produce research, plan, changes, and review artifacts; verify with bare `mypy` and `ruff`; commit cleanly without pushing.
* Inferred research questions: Why are `sensor_view.py` and `test_sensor_view_conflicts.py` already modified in the worktree, where else do retained sensor values, conflicts, provenance, and Quality AI review flags flow, and what gaps remain against Issue #1288 criteria 1-7 and 9?
* Caller constraints and non-goals: Research-only during this phase; no push; no new agent service, simulator, or ingestion engine.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Reuse existing `quality-evidence`, retained sensor storage, and Quality surfaces; no new service/simulator/ingestion engine | Issue #1288 / Intake | Constrains all waves and alternatives to `src/core` and `src/api` extensions |
| exclude                                                  | Do not push to remote; leave working tree clean after commit | Caller prompt / Intake | Constrains final git action in Implement/Review |

## Research Questions

|  # | Sub-question                                                                                                      | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What does `src/core` currently implement in `sensor_view.py` (including the uncommitted diff) and related quality/assistant modules for retained sensor readings, provenance, citations, and conflicts? | depth           | H        | answered |
| Q2 | How do Quality AI snapshot capture, proactive review flag machinery, and assistant/flag evaluation consume `sensor_view` outputs, and how are conflicting, stale, missing, or rejected readings handled? | depth           | H        | answered |
| Q3 | How does `src/api` (endpoints, templates/UI, and tests) render retained sensor values, provenance, conflicts, and grounded Quality AI review flags, and are any `src/api` gaps remaining? | breadth         | H        | answered |
| Q4 | Do current `src/core` and `src/api` pass bare `mypy`, `ruff check .`, `ruff format --check .`, and unit tests, or do any typing/lint/behavior issues exist? | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/changes/2026-11-14-issue-1288-sensor-grounding-c2-changes.md`, `.copilot-tracking/changes/2026-11-14-issue-1288-ui-snapshot-correlation-0900-changes.md`, `.copilot-tracking/rpi-sessions/2026-11-13/1288-iot-ui-verify-1045-state.json`, Issue #1288 body.
* Reused (verified) findings: Issue #1288 notes that base source delivery merged in PR #1331 (`1b7a1719bee088ce2823bff45242e319bc928295`), while specific refinements around conflict handling, grounding, and correlation tests have been iterated in follow-up branches.
* Superseded / stale: Pre-2026-11-09 claims that Quality AI does not capture retained sensor readings at all are superseded by PR #1331; current code was inspected directly.

## Candidate Research Areas

| Area | Candidate scope | Disposition | Rationale |
|------|-----------------|-------------|-----------|
| Retained sensor model (`src/core`) | `sensor_view.py`, `chat_case_answers.py`, `chat_panel.py`, `core/tests/` | investigated | Core retained reading selection, synthetic provenance classes, conflict detection, and deterministic grounding live here. |
| Quality AI capture & review flags (`src/core`) | `assistants.py` (`capture`, `eligible`, `review_flag`, `_view`, `_withhold_sensors`) | investigated | Governs proactive L4 `review-suggested` flags, citations, staleness, consent withdrawal, and provenance metadata. |
| Quality API & employee UI (`src/api`) | `app.py`, `sensor_badges.py`, `web/ops.js`, `web/assistants.js`, `web/chat.js`, `api/tests/` | investigated | Surfaces `/api/cases/<id>/sensors`, plain-language status badges, manual routes, and Quality AI review flags. |
| Sensor ingestion & simulator (`src/importer`, `infra/`) | External telemetry producers and database ingestion | out-of-scope | Explicitly excluded by Issue #1288 (`reuse existing retained sensor storage`). |

## Research Cycle Log

### Cycle 1

* Selected posture: `balanced` (explicit Issue #1288 acceptance criteria and bounded `src/core` + `src/api` target modules, with adjacent check on case-chat grounding and plain-language UI rules).
* Wave 1 — Wider (inline; tightly coupled `src/core` and `src/api` modules): Mapped all sensor and `quality-evidence` files across `src/core` and `src/api`, inspected `git status`/`git diff` (finding uncommitted additions of `conflicts()` and `conflicting_readings`/`conflict_notice` in `sensor_view.py` plus `test_sensor_view_conflicts.py`), and located API endpoints, UI renderers, and existing Issue #1288 test suites (`C1`–`C6`).
* Wave 2 — Deeper (inline): Traced data flow from `sensor_view.capture_source()` through `grounding()`, `reading_health()`, `advisory()`, `signature()`, `chat_case_answers.sensor_facts()`, `assistants.capture()`, `assistants.eligible()`, `assistants.review_flag()`, `Assistants._view()`, `sensor_badges.annotate()`, `web/ops.js`, and `web/assistants.js` (`C2`–`C11`). Ran baseline `mypy`, `ruff check .`, `ruff format --check .`, and unit tests (`C12`).
* Wave 3 — Contrarian (inline): Challenged whether the existing uncommitted `sensor_view.conflicts()` diff already satisfies Issue #1288 AC 5 and AC 6, and checked whether UI copy or mypy/pyproject constraints could break downstream suites:
  * Counter-finding 1: `capture_source()` sets `conflicting_readings`, but `reading_health()`, `grounding()`, and `advisory()` still pick `window[-1]` (`latest`) and return `state="ok"`, silently choosing one conflicting value instead of blocking normal interpretation (`C2`, `C3`).
  * Counter-finding 2: `Assistants._view()` (`keeps` in the same 6-hour `scheduling_signature` bucket) preserves `actionable=True` on proactive flags when a new reading arrives in the same bucket; without explicit conflict gating in `review_flag()` and `eligible()`, a conflicting reading can still project an autonomous L4 `review-suggested` flag (`C5`, `C6`).
  * Counter-finding 3: `review_flag()` exposes `sensor_cited_ids` and snapshot-wide `provenance_classes`, but omits per-reading `provenance_class`/`source_text`/`locator`/`content_hash` on `flag["readings"]` and lacks a `source_provenance` map grounding all `cited_ids` (both `sensor:*` and `source:*`) to their captured snapshot locators and hashes (`C5`).
  * Counter-finding 4: `src/api/tests/test_content_standard.py` bans internal jargon (`provenance`, `snapshot`, `gate`, `hold`, `trace`, `envelope`) and unowned `BLOCKED_WORDS` (`unavailable`, `cannot`, `failed`, etc.) in `web/*.js` literal strings (`C11`), so UI labels for source grounding and conflict notices must use plain language (`"Source:"`, `"Cited source records:"`, `"Conflicting readings"`).
* Parent synthesis:
  * Accepted: Extend `sensor_view` (`reading_health`, `grounding`, `advisory`, `signature`), `chat_case_answers`, `chat_panel`, `assistants` (`eligible`, `review_flag`), `sensor_badges`, `web/ops.js`, `web/assistants.js`, and `web/chat.js` to propagate conflict states end-to-end and attach structured `source_provenance` grounding to Quality AI review flags, backed by unit and API/UI correlation tests.
  * Rejected: Creating a separate conflict endpoint or new AI task type (violates Issue #1288 reuse boundary); altering `grounding["values"]` key shape when non-conflicting (would break `test_quality_sensor_grounding.py:52`).
  * Deferred: Real-device calibration and automatic conflict arbitration (out of demonstrator scope; synthetic uncalibrated data requires human routing on conflict).
* Re-entry evaluation: All four research questions (`Q1`–`Q4`) and every Issue #1288 acceptance criterion (`AC 1`–`AC 7`, `AC 9`) have verified codebase evidence (`C1`–`C12`). No material uncertainty remains; Cycle 2 is not needed.

## Evidence Log

### Codebase Evidence

| ID  | Path & Line                                                                 | Summary                                                                                                                                                 |
|-----|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/core/src/zava_forward/core/sensor_view.py:420-476`                     | `capture_source()` builds the bounded retained reading window (`before`, `after`, `latest`), `provenance` map (`CLASSES`), `mould_risk_index` omission notice, and uncommitted `conflicting_readings` / `conflict_notice` via `conflicts(window)` (`lines 334-348`). |
| C2  | `src/core/src/zava_forward/core/sensor_view.py:309-331`                     | `grounding(sensors)` always selects `latest = window[-1]` even when `conflicting_readings` is non-empty, and omits `provenance_class` / `source_text` on grounded non-conflicting readings. |
| C3  | `src/core/src/zava_forward/core/sensor_view.py:679-747`                     | `reading_health(sensors)` returns `state="ok"` despite `conflicting_readings`, and `advisory(sensors)` raises/clears `"Sensor watch"` from `window[-1]` despite conflicts. |
| C4  | `src/core/src/zava_forward/core/sensor_view.py:480-496`                     | `signature(sensors)` records 6-hour scheduling bucket identity `(version, state, anchor, bucket, classes)` without a `conflicting` boolean. |
| C5  | `src/core/src/zava_forward/core/assistants.py:213-346`                      | `capture()` hashes `source:*` and `sensor:*` entries into `snapshot["citations"]`, `eligible()` checks `sensors.get("state") == "ok" and sensors.get("readings")` without excluding `conflicting_readings`, and `review_flag()` omits conflict downgrade (`conflicting-readings`) and structured `source_provenance` / per-reading `provenance_class`, `source_text`, `locator`, and `content_hash`. |
| C6  | `src/core/src/zava_forward/core/assistants.py:1020-1056`                    | `Assistants._view()` sets `keeps = newer and ...` inside the same 6-hour `scheduling_signature` bucket and passes `actionable or keeps` plus `current` into `review_flag()`. |
| C7  | `src/core/src/zava_forward/core/chat_case_answers.py:148-168,342-363`       | `sensor_facts()` copies `view.get("detail")` without falling back to `conflict_notice` or recording `sensor.source` / `sensor.conflict`, and `_sensor()` relies on `sensor.latest.citation` or `sensor.detail`. |
| C8  | `src/api/src/zava_forward/api/app.py:863-882`                               | `GET /api/cases/<case_id>/sensors` enforces `case:read` + case scope, calls `cases.sensors(case_id, allow=can_sensors(user))`, and wraps the payload with `sensor_badges.annotate(...)`. |
| C9  | `src/api/src/zava_forward/api/sensor_badges.py:20-85`                       | `_HEALTH` and `_NEXT_ACTION` define `fault` and `out_of_range` badges and plain-language operator guidance, but lack a `conflict` health state and action. |
| C10 | `src/api/src/zava_forward/api/web/ops.js:74-108` & `assistants.js:22-47`    | `sensorPanel()` renders retained values, units, timestamps, provenance list, omission notice, and badges, but does not render `v.conflict_notice`; `reviewFlagBlock()` lacks a `conflicting-readings` title, per-reading source text, and cited source record locators. |
| C11 | `src/api/tests/test_content_standard.py:25-77`                              | Enforces plain-language copy across `web/*.js`: bans `gates?`, `holds?`, `provenance`, `traces?`, `snapshots?`, `envelopes?` in JS string literals and requires `Owner:` + `Next action:` whenever `BLOCKED_WORDS` appear. |
| C12 | `src/core/pyproject.toml:26-73` & `src/api/pyproject.toml:23-62`            | Configures strict `mypy` (`mypy_path` includes `src` and `tests`, plus `../core/src` in `src/api`) and `ruff` lint/format rules; baseline checks and unit tests currently pass. |

### External Evidence

No external sources used.

## Findings Mapped to Questions and Evidence

* **Q1 (`src/core` retained sensor model & uncommitted diff)**: `sensor_view.capture_source()` already bounds readings to 24h before/after anchor plus latest, labels synthetic provenance classes (`CLASSES`), states uncalibrated/non-diagnostic framing, reports `mould_risk_index` as not retained, and detects identical-timestamp value disagreements via the uncommitted `conflicts(window)` helper (`C1`). However, `grounding()`, `reading_health()`, `advisory()`, `signature()`, and `chat_case_answers.sensor_facts()` do not yet honor `conflicting_readings` or expose grounded reading `provenance_class`/`source_text` (`C2`, `C3`, `C4`, `C7`).
* **Q2 (Quality AI capture & proactive review flags)**: `assistants.capture()` feeds the identical `sensor_view.capture_source()` payload and `sensor:<sensor_id>:<reading_id>` citations to `quality-evidence`, enforces 6-hour bucketed proactive scans, and withholds all reading projections on consent withdrawal (`C5`, `C6`). Gaps: `eligible()` can still trigger sensor-only proactive scans on conflicting readings, `review_flag()` does not downgrade captured or newly-arrived conflicting readings to non-autonomous `conflicting-readings` (including under same-bucket `keeps` in `_view()`), and `review_flag()` lacks structured `source_provenance` and per-reading synthetic source fields (`C5`, `C6`).
* **Q3 (`src/api` endpoints, badges, UI, and tests)**: `/api/cases/<id>/sensors` and `ops.js` / `assistants.js` surface retained readings, synthetic classes, staleness/fault badges, and `review_flag` blocks (`C8`–`C10`), but `sensor_badges.py` lacks a `conflict` badge and `next_action`, `ops.js` omits `conflict_notice`, and `assistants.js` omits `conflicting-readings`, per-reading source text, and cited source locators (`C9`, `C10`). All new JS copy must comply with `test_content_standard.py` (`C11`).
* **Q4 (Verification baseline)**: Bare `mypy`, `ruff check .`, and `ruff format --check .` succeed in both `src/core` and `src/api` (`C12`); because global editable installs point at `/home/azureuser/source/ama`, local `unittest` invocations must prefix `PYTHONPATH` with this worktree's `src` and `tests` directories so worktree edits are exercised.

## Key Discoveries

* Same-bucket conflict hazard: `Assistants._view()` keeps proactive flags actionable (`keeps`) when new readings arrive in the same 6-hour bucket (`C6`). Checking both `sensors.get("conflicting_readings")` and `now_sensors.get("conflicting_readings")` inside `review_flag()` is essential so a newly-arrived conflicting reading immediately replaces `review-suggested` with non-autonomous `conflicting-readings`.
* Backward-compatible grounding contract: `src/api/tests/test_quality_sensor_grounding.py:52` asserts exact key equality on `grounding["values"]` (`temperature_c`, `humidity_pct`, `observed_at`), so grounded `provenance_class` and `source_text` belong as sibling fields on `grounding(sensors)` rather than extra keys inside `values`.
* Plain-language enforcement in `web/*.js`: `test_content_standard.py` rejects the literal word `"provenance"` or `"snapshot"` in UI strings (`C11`), so UI elements must render source grounding using plain-English labels (`"Source:"`, `"Cited source records:"`) while API JSON retains `provenance_class` and `source_provenance`.

## Alternatives and Decision State

| Option | Summary | Pros | Cons | Disposition |
|--------|---------|------|------|-------------|
| Option A: Propagate conflict & provenance grounding through existing `sensor_view`, `assistants`, `chat_case_answers`, `sensor_badges`, and `web/*.js` | Keep `capture_source()` as single source of truth; update `reading_health`, `grounding`, `advisory`, `signature`, `chat_case_answers`, `assistants.eligible`/`review_flag`, `sensor_badges`, `ops.js`, and `assistants.js` with focused core + API tests. | Satisfies all Issue #1288 ACs (`1`–`7`, `9`); zero new endpoints or services; preserves consent withdrawal, staleness, and plain-language rules. | Touches both `src/core` and `src/api`, requiring validation in both packages. | **Selected** |
| Option B: Drop conflicting rows silently inside `capture_source()` | Filter out conflicting rows so `readings` appears empty when timestamps clash. | Fewer downstream branches. | Hides retained audit evidence, conflates sensor data disagreement with `"no readings retained"`, and loses conflicting citation keys needed by officers (`C1`, Issue #1288 AC 6). | Rejected |
| Option C: Backend-only metadata without `sensor_badges.py` or `web/*.js` updates | Add `conflicting_readings` and `source_provenance` only in `src/core` JSON. | Avoids frontend JS edits. | Leaves `/api/cases/<id>/sensors` with `"ok"` health badge and no `next_action` on conflicts, and hides source grounding and `conflicting-readings` status in the employee UI (`C9`, `C10`, Issue #1288 AC 1, AC 5, AC 6). | Rejected |

## Open Questions, Risks, and Residual Uncertainty

* Open questions: None blocking planning or implementation.
* Risks and mitigations:
  * Risk: Regressing plain-language, Fluent 2, or accessibility UI gates when editing `ops.js` and `assistants.js`. Mitigation: Load `web-design-guidelines` and `redesign-existing-projects` before editing JS, avoid banned jargon/blocked words (`C11`), and run `test_content_standard.py`, `test_design_system.py`, and `test_accessibility_baseline.py`.
  * Risk: Consent-withdrawal leakage if conflict metadata remains attached after withdrawal. Mitigation: Keep `if withheld:` first in `review_flag()` and verify `_withhold_sensors()` strips `conflicting_readings` and reading IDs (`test_quality_sensors.py`).

## Current Decisions

* Use Option A: propagate `conflicting_readings` across `sensor_view` (`reading_health`, `grounding`, `advisory`, `signature`), `chat_case_answers`/`chat_panel`, `assistants` (`eligible`, `review_flag`), `sensor_badges`, `ops.js`, and `assistants.js`, and ground `review_flag` with per-reading synthetic source metadata plus full `source_provenance` across all `cited_ids`.
* Keep `grounding["values"]` as the exact 3-field dict when non-conflicting, and set `citation=None, values=None, conflicting_citations=[...]` when `conflicting_readings` is non-empty.
* Validate both `src/core` and `src/api` with bare `mypy`, `ruff check .`, `ruff format --check .`, and worktree-scoped `unittest` suites (focused validation tier per `.github/copilot-instructions.md` for bounded application/UI issue refinement without infra, SQL schema, dependency, workflow, or gate-tool changes).

## Unresolved Decisions

* None.

## Potential Next Research

* None required for Issue #1288; post-demonstrator live-device calibration and hardware telemetry authentication remain future production topics outside this issue's scope.

## Planning Readiness

* Readiness: `Ready`
* Research disposition: `executed`
* Justification: Every target file, function contract, invariant, and validation command in `src/core` and `src/api` is verified with line-anchored codebase evidence (`C1`–`C12`).

## Closeout Record

* Execution status: `Complete`
* Research-only constraint: Preserved during Research phase (zero source or test files created or modified by Research; pre-existing dirty worktree files `sensor_view.py` and `test_sensor_view_conflicts.py` left untouched during Research).
* Continuation context: Active confirmed automatic RPI Agent loop (`quality-1288-sensor-ai-2142`) advancing directly to `Plan`.

## Advisory Next Step

* Active automatic RPI Agent transitions to `Plan` (`rpi-plan`) using `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-research.md`.

## Sources

No external sources used.

## Artifact Self-Check

- [x] Brief, posture (`balanced`), extension registry, participation, and direction controls recorded.
- [x] Complete three-wave Cycle 1 (`Wider`, `Deeper`, `Contrarian`) executed in order with parent synthesis and re-entry decision.
- [x] All questions (`Q1`–`Q4`) answered and mapped to `C1`–`C12` `path:line` evidence.
- [x] Convergence recommendation selected (Option A) with rejected alternatives and trade-offs documented.
- [x] Planning Readiness (`Ready`) and Research disposition (`executed`) recorded; research-only boundary respected.

