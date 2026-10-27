<!-- markdownlint-disable-file -->
# RPI Plan: Resident sensors

## Task Metadata

* Task ID: 468; slug: resident-sensors; date: 2026-10-27.
* Planning status: Ready; single critique completed, compatible findings resolved.
* Details: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md

## Executive Summary

Expose existing generated temperature/humidity readings through the same
resident SQL view and signed-session projection. Show latest recorded values,
two labelled static history plots and an equivalent native data table.
No live data claim, safety judgement, new dependencies or deployed changes.
Sensor tables may be absent: the source view must remain usable with an explicit
empty sensor result. A later authorised view apply is an operational dependency,
not part of this local task. No current blocker to source implementation.

## User Decisions and Requirements

* Implement #468, sub-issue of #466, full native ordered automatic RPI.
* Resident sees only their own home; sensor data must be synthetic from existing generator.
* Accessible gauges/history with text alternative, keyboard support, non-colour signals and no motion.
* Leave #467 header and #465 mapping cap untouched.
* No Azure access, SQL execution/change, registry work, private datasets, secrets, .env or verifier file.
* Source SQL projection edits are required for the requested view boundary; never apply them here.
* Use pip, affected-project tests, ruff/mypy on changed Python and focused Playwright.
* Stack on feat/resident-interactive, Refs only, no force push and no merge.

## Goals

* Deliver own-home sensor visibility without widening database or HTTP authority.

## Scope and Non-Goals

* In scope: source-only view projection, SQL reader shaping, domain allowlist,
  resident JS/CSS, core/API regressions, local constructed browser harness, README.
* Excluded: live SQL/infra operations, sensor generation on requests, health
  recommendations, controls, private snapshots, header and unrelated pages.

## Functional Requirements

* Join readings to home.stock_id, never assume case ID equals home ID.
* Return at most 48 latest stored rows, chronological, with timestamp and numeric
  temperature/humidity; strip sensor/home/reading IDs from resident response.
* No data yields clear empty copy. Missing/invalid/faulty values are not normal.
* Always label synthetic historical readings and state they are not live/safety advice.

## Non-Functional Requirements

* SQL principal retains SELECT on only existing resident view; app still fetches
  case by signed session and reauthorises every request.
* Static responsive SVGs with native table equivalent; semantic meters for valid
  values; dates/numbers via Intl; existing Fluent tokens.
* Bounded 48 rows; finite numbers and UTC timestamps; no heavy dependency.

## Acceptance Criteria

* Two residents with distinct stock histories see only their own values.
* Forged home/case query/header/path does not change sensor ownership.
* Latest values, timestamps and table agree; no history is invented.
* Empty, malformed, missing, out-of-range and fault states have explicit text.
* Local browser checks cover keyboard, 320/390/1280 widths, reduced motion and SVG/table.
* Affected project unit tests, changed-file ruff/mypy and browser checks recorded honestly.

## Sources

* .copilot-tracking/research/2026-10-27/resident-sensors-research.md: C1-C7/W1.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Own-home sensor boundary

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Source view and strict projection

Add optional stored-history projection, typed reading model, strict validation,
and cross-home/unit tests. No SQL statements will be executed.

<!-- rpi:phase id=P02 -->
### [x] P02: Accessible sensor presentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Gauges, history and table

Add static semantic section below home, no header edits; reuse tokens.

<!-- rpi:phase id=P03 -->
### [x] P03: Verification and documentation

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Local tests, browser and source documentation

Run complete core/API unit discovery, targeted sensor regressions and changed-file
ruff/mypy; start real HTTP app over constructed reader, use Playwright.

## Test Ownership and Change Budget

Core owns parsing/projection/SQL query tests, API owns session isolation, browser
harness owns rendered states. Removals: none. Maximum additions: 20 test methods
and one bounded browser harness. Canonical targets: existing source files and
tests; generated targets: temporary fresh synthetic fixture and browser results
only, no private input. Semantic coverage: ownership, values, units, timestamps,
fault/empty states. Regression: existing core/API suites. No full local gate.

## Dependencies

Installed editable core/agents/API with pip. Local SQL execution is excluded;
SQL integration remains an explicitly unrun operational verification.

## Critique Disposition

Original independent verdict: Revise. No second critique.

| Finding | Disposition | Correction |
| --- | --- | --- |
| PC-001 High | Resolved directly | Binary exact case/register/reading home match and both synthetic labels; retain reading home internally; negative tests |
| PC-002 Medium | Resolved directly | Explicit nullable JSON contract and channel unavailable states; latest never silently falls back |
| PC-003 Medium | Resolved directly | Controlled test environment removes all inherited ZF_* settings; no SQL/integration opt-ins |

## Follow-Up Items

* RV-001 was implemented in a subsequent bounded P01 invocation with source/
  parser regressions. Independent hosted assessment of the final head remains;
  original complete/Not accepted Review is unchanged. No second local Review.
* Authorised operator may later apply reviewed view and verify populated sensor
  tables; no deployment or data population is part of this task.
* Human screen-reader acceptance remains distinct from engineering checks.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/resident-sensors-changes.md.
P01-P03 complete; original Review complete/Not accepted and preserved. Subsequent
P01 invocation implemented RV-001 and passed 114 focused tests (19 skips), changed
Python Ruff/mypy and 23 browser assertions. P02/P03 original suite evidence
retained; no full-suite rerun after SQL-source/test/docs-only correction.
Publish draft stacked PR for hosted independent assessment. T-SQL compile,
populated SQL integration and human acceptance remain explicitly unrun.
