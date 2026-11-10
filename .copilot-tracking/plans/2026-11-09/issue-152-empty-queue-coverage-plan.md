<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-empty-queue-coverage

| Field | Value |
|---|---|
| Task ID | issue-152-empty-queue-coverage |
| Date | 2026-11-09 |
| Branch / base | feat/workbench-empty-coverage-152 from b46a9ad9a9619db535368d1b2cbbddec8110e122, target main |
| Research | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md |
| Phase details | .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-phase-details.md |
| Changes record (owned by Implement) | .copilot-tracking/changes/2026-11-09/issue-152-empty-queue-coverage-changes.md |
| Tier | focused (re-checked: web client copy and tests only; no auth, SQL, deployment, consent, data) |

## Executive Summary

The My cases screen will give three different explanations for an empty list: a search/filter that matched nothing; an empty default queue whose scenario coverage is Unknown; and, only when a validated, version-bound server declaration exists, a declared-unrepresented perspective. Today no server produces such a declaration, so the shipped default is the explicit Unknown wording. A producer would need a dataset-owned declaration with SQL parity (full-tier) and is recorded as a follow-up, not built. Node tests exercise the decision logic for the Programme Manager `ZF-5` default, the Coordinator empty default, no-match, valid declaration and absent/stale/mismatched declarations; browser check text is added but cannot run now. This is partial progress on C5 (`Refs #152`); it is not AC-034/043 acceptance.

## User Decisions and Requirements

* Bounded partial C5: meaningful empty-queue explanations; test PM default `ZF-5` and Coordinator empty default (caller brief).
* Declared-unrepresented only on trustworthy version-bound metadata; missing, stale, mismatched, unavailable or untrusted gives explicit Unknown; never infer from empty queue, identity or synthetic labels (caller brief).
* Stop and report rather than invent authority, data, permissions or schema; stop for tier reassessment if auth/SQL/deployment is touched (caller brief).
* Preserve own-queue authorization, native semantics, keyboard path, non-colour status, reduced motion, resident choice, human approvals; no role simulator; supported widths remain an owner decision (caller brief).
* Run only lightweight unit/static checks; no browser, SQL, Docker, changed/full gates; no push/PR (caller brief).
* Use `Refs #152` only (caller brief).

## Goals

* Empty queue explanations that never over-claim coverage.
* A fail-closed contract for a future version-bound coverage declaration.
* Regression tests runnable without a browser, plus browser-check expectations for the coordinator-admitted gate.

## Scope and Non-Goals

* In: `app.js` listView empty copy and a pure helper; `test_workbench.py` or a new node-based test file; `workbench_browser_check.py` expectations; docs note in `src/api/README.md` if it lists the contract.
* Out: server, Store, SQL, taskqueues, manifest changes, auth, runtime producer, full profile coverage, #1219 320px fix, supported-device decision, #440 checkpoint.

## Functional Requirements

* FR-A: with active non-sort filters and zero results, text says no cases match, names it a search result, not a coverage statement, and points to reset.
* FR-B: with no active filters, empty own queue and no valid declaration, text says coverage for this perspective is Unknown and the empty list does not mean the programme has no work.
* FR-C: with no active filters, empty own queue and a valid declaration, text says no representative scenario is supplied for this perspective in the declared fixture version, states it is a declared demonstration gap, and does not claim complete coverage elsewhere.
* FR-D: a declaration is valid only when `status` is `unrepresented`, `contract` equals `work_queues.version`, `as_of` and `policy_version` equal the page, `perspective` equals the signed-in role, and `fixture_version` and `source` are non-empty strings; any other shape yields Unknown.
* FR-E: the declaration never changes which records are shown, the role, or access; the empty `all` view keeps its current wording.

## Non-Functional Requirements

* Native list, button and live regions retained; empty state is plain text in the existing live region; no colour-only signal; no new animation.
* Plain-language copy per `docs/reference/research/ux/content-standard.md`; ASCII punctuation.
* No new dependency; no framework change.

## Acceptance Criteria

* AC1: node tests assert text/state for no-match, unknown (PM `ZF-5` non-empty default yields no empty state; Coordinator empty default yields Unknown), declared-unrepresented, and absent, stale as_of, stale policy version, contract mismatch, wrong role, wrong status, blank fixture, non-object declaration.
* AC2: node test asserts a populated queue and the `all` view never show coverage wording.
* AC3: existing test_workbench and manifest tests still pass; static checks (ruff, node syntax) exit 0.
* AC4: browser check expectations for reset-focus, no-match text, Unknown text for the Coordinator, ordered IDs and count are added and reported as not executed.
* AC5: no file outside scope changed; no claim of AC-034/043 completion.

## Phase Checklist

* [x] P01 Pure empty-state helper and client wiring
* [x] P02 Regression tests (node, runnable) and browser-check expectations (not runnable)
* [x] P03 Static validation, web-design-guidelines review, docs note

<!-- P01 -->
### P01 Pure empty-state helper and client wiring

* [x] P01-T01 Add `queueEmptyExplanation` and `trustedCoverage` pure functions in `app.js`.
* [x] P01-T02 Keep `asOf` from the cases page and call the helper from the empty `li`.

<!-- P02 -->
### P02 Regression tests and browser expectations

* [x] P02-T01 Add `src/api/tests/test_queue_empty_state.py` (node `vm`, extracts the two functions from `app.js` by name).
* [x] P02-T02 Extend `workbench_browser_check.py` Coordinator and no-match steps with the expected text (unexecuted).

<!-- P03 -->
### P03 Validation, review of web files, docs

* [x] P03-T01 Run ruff, mypy if configured for tests, `node --check`, targeted unittest.
* [x] P03-T02 Fetch web-design-guidelines source, review changed web files, record `file:line` findings.
* [x] P03-T03 Add a short contract note in `src/api/README.md` if a suitable section exists.

## Critique Disposition

Critique executed once on the final candidate: .copilot-tracking/challenges/2026-11-09/issue-152-empty-queue-coverage-critique.md, verdict Revise (8 planner-owned findings, no user decision needed). No second critique runs. All findings were applied directly; PC-001 was independently re-verified by grep (employee_briefing_browser_check.py:70, store.py:881, test_ai_tasks.py:141).

| Finding | Disposition | Plan change |
|---|---|---|
| PC-001 (High) other consumers of existing empty copy | Accepted | Unknown copy begins with the exact sentence "No open cases are assigned to you. This does not mean the programme has no work." and the no-match copy begins with "No cases match these filters."; affected checks listed in P02. The server briefing sentence in store.py is a separate surface and is not changed. |
| PC-002 (High) null/empty equality passes | Accepted | FR-D requires non-empty strings (typeof checks) for every bound field; tests added for missing/empty/non-string variants. |
| PC-003 (Medium) wiring untested | Accepted | The filtered/empty/view gate lives inside `queueEmptyExplanation`, called with `rowsLength`; the render passes it unconditionally of copy. Test asserts non-empty rows yield no explanation. |
| PC-004 (Medium) provenance shown | Accepted | Declared copy names source, fixture version and as-of date. |
| PC-005 (Medium) fetch before edit | Accepted | Fetch of web-design-guidelines is a precondition of P01. |
| PC-006 (Medium) overstated trust | Accepted | Wording changed to "validated and version-consistent"; tripwire test that `taskqueues.contract` has no `coverage` key; declared state is stated unreachable until an authorised producer (F1) exists. |
| PC-007 (Low) thin browser expectations | Accepted | Browser expectations: Coordinator Unknown and not "unrepresented"; no empty element for the PM default; no-match wording. Unexecuted. |
| PC-008 (Low) publication boundaries | Accepted | Handoff states `Refs #152` with unmet items (owner device decision, full AC-034/043, producer); publication blocked until focused gate, independent review and CI; `journey_acceptance` stays `partial`. |

## Follow-Up Items

* F1: dataset-owned fixture/coverage declaration served via `/api/me`, with JSON and SQL store parity and owner approval (full-tier; needs coordinator reassessment).
* F2: reconcile the two manifests' differing status semantics (workbench `partial` vs scenario `unavailable`).
* F3: run exact-head `--changed` gate and Playwright after the heavy lock is free.

## Handoff

Implement per phase details; Review once afterwards. Publication is blocked until the coordinator-admitted focused `--changed` gate with Playwright, independent exact-head review and hosted CI. Use `Refs #152`; unmet: owner supported-device decision, full AC-034/043, runtime producer. `journey_acceptance` AC-034/043 stay `partial`.
