<!-- markdownlint-disable-file -->

# Review Log: issue-152-empty-queue-coverage

| Field | Value |
|---|---|
| Date | 2026-11-09 (04:13-04:20 UTC) |
| Execution status | Complete for the static boundary below; browser, SQL, gate and CI evidence unavailable by direction |
| Outcome | Residual work (no defect open in the implemented scope; no complete AC-034/043 or #152 C5 claim) |
| Reviewed boundary | working tree on b46a9ad9a9619db535368d1b2cbbddec8110e122, uncommitted diff of app.js, workbench_browser_check.py, README.md and new test_queue_empty_state.py |

## Compared artifacts

* Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-plan.md (P01-P03 and tasks checked; critique dispositions PC-001..PC-008 recorded)
* Details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md
* Critique: .copilot-tracking/challenges/2026-11-09/issue-152-empty-queue-coverage-critique.md (executed once, verdict Revise, applied directly)
* Changes: .copilot-tracking/changes/2026-11-09/issue-152-empty-queue-coverage-changes.md (includes a dated late amendment found before this review)
* Research: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md

## Reconciliation

Plan markers, phase details, changes evidence and handoff prose agree. Plan P03-T02 was checked on the strength of the implementation-time fetch and pass; this Review refreshed the source and re-reviewed (below). Follow-ups F1-F3 remain outside the active plan. No critique repetition occurred.

## Requirement and acceptance comparison

| Item | Evidence | Result |
|---|---|---|
| FR-A no-match is a search result | app.js:478; test_no_match_is_a_search_result_even_with_a_valid_declaration | met (node) |
| FR-B empty default is Unknown | app.js:484; Coordinator test | met (node) |
| FR-C declared gap needs valid bound declaration | app.js:464-473, 480-483; declared test | met (node), unreachable at runtime (RV-002) |
| FR-D fail closed on missing/stale/mismatched/blank/non-string | 11 variants + 4 empty page values | met (node) |
| FR-E no change to role, access, records, all-scope wording | diff touches only the empty `li` text and `asOf`; all-scope test | met by inspection and node |
| AC2 populated queue (PM `ZF-5`) no explanation | node test with manifest default | met (node); real-data check stays in test_workbench_live_defaults (not run) |
| Own-queue authorization, native semantics, reset, focus, live regions, reduced motion | no code touched; reset/focus remain in pre-existing browser checks | preserved by inspection; unexecuted |
| Server/SQL/auth/schema untouched | `git diff --stat` shows web client, browser check, README, test only | met; tier stays focused |

## Validation evidence

* Actual commands and exits are in the changes record (node v24.21.0, Python 3.12.3, ruff 0.17.3, mypy 2.4.1; 51 related unit tests OK; re-run after the amendment: 13 tests OK; ruff and py_compile exit 0).
* web-design-guidelines source refreshed at 2026-11-09 04:12:47 UTC, HTTP 200, 8055 bytes, byte-identical to the earlier fetch. Applicable rules checked against the changed web file: empty states handled; async update inside existing `aria-live=polite` region; no new controls, focus, animation, colour-only signal, images or forms. Findings: RV-001 only. Visual rendering and screen-reader behaviour were not performed.
* Unavailable by direction: Playwright/browser (`workbench_browser_check`, `test_workbench_live_defaults` Playwright and HTTP classes), SQL, Docker, `rpi-checks --changed/--all`. No prior receipt used.

## Findings

| ID | Severity | Finding | Evidence | Destination |
|---|---|---|---|---|
| RV-001 | Low | Declared copy prints the ISO `as_of` rather than a locale-formatted date (guideline: use `Intl`) | src/api/src/zava_forward/api/web/app.js:482 | later user-selected rpi-implement, optional; the raw value is the version-binding identifier |
| RV-002 | Medium | "Declared unrepresented" cannot occur at runtime: no authorised producer exists and a dataset-owned declaration needs data/SQL/API schema (full-tier) | src/core/src/zava_forward/core/taskqueues.py:59; tripwire test | rpi-plan (owner/coordinator tier reassessment) as F1; not a defect |
| RV-003 | Medium | New browser expectations (Coordinator Unknown, no `li.empty` for PM default, no-match wording) and existing reset/focus/live-status checks are unexecuted | src/api/checks/workbench_browser_check.py:258-272 | residual F3: coordinator-admitted exact-head `--changed` gate with Playwright |
| RV-004 | Low | Node tests extract functions from `app.js` by source text, so a refactor to another declaration style breaks the test | src/api/tests/test_queue_empty_state.py:17-27 | accepted; failure is loud, not silent |
| RV-005 | Low | `ruff format --check` reports pre-existing drift in workbench_browser_check.py outside the diff | changes record | unrelated, not fixed |
| RV-006 | Info | Workbench manifest `partial` vs scenario manifest `unavailable` semantics still differ; neither is used as runtime provenance | research Contradictions | F2 |
| RV-007 | Info | Supported devices/widths remain an owner decision; 320/1280 checks are engineering only; journey_acceptance AC-034/043 remain `partial` | manifest `supported_devices`; journey_acceptance.py | owner |

No finding is a High defect. Nothing here proves AC-034, AC-043, the #152 C5 criterion, assistive-technology, human or live Azure acceptance; use `Refs #152`.

## Routing

* rpi-plan: F1 producer design with owner tier decision.
* Residual/distinct: F3 gate and Playwright; F2 manifest reconciliation; RV-001 optional.
* Publication remains blocked until the focused gate, independent exact-head review and hosted CI.
