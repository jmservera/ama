<!-- markdownlint-disable-file -->
# RPI Plan: select MSSQL for the chat schema dependency of the sensor store (#1298)

## Task Metadata

* Task ID: issue-1298-fresh-demo
* Task slug: chat-schema-sql-selector-1298
* Planning status: ready
* Plan date: 2026-11-09
* Phase details: .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-09/chat-schema-sql-selector-1298-plan-critique.md

## Executive Summary

The local focused gate selects the `mssql` group from path keywords and an explicit dependency set. `src/core/src/zava_forward/core/chatthreads.py` is neither, yet `MssqlStore`, which the retained-sensor fixture constructs, imports and executes its SQL definitions. A change limited to that file therefore passes selection without the sensor SQL run, while project-core discovery accepts the ten sensor opt-in skips. The plan adds that one path to the explicit set, with a focused regression, and records that the set stays explicit and not exhaustive.

This is the initial implementation on a fresh branch from main `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939`. It does not adopt or alter the earlier branch `fix/chat-schema-sql-gate-1298` (`fef352e0`), whose process findings stay as adverse evidence.

### User Decisions and Requirements Highlights

* Owner demo-targeted validation replaces the blanket full gate for this push, so the literal issue full-gate criterion stays unproven and the deliverable uses `Refs #1298`.
* Source is bounded to `tools/rpi-checks.py` and `tools/test_rpi_checks.py`; no expanded matrix, no exhaustive dependency claim.

### What You May Not Know

* `sqlstore.py`, also imported by `mssqlstore.py`, has at least fourteen top-level sibling imports plus function-local ones; any of them could have the same gap. Only `chatthreads.py` is demonstrated (research C6 to C8, C14). That is recorded as a limitation and an owner decision, not fixed here.
* Issue text says eight sensor tests; current main pins ten (research C3). The plan does not change the count.
* Correction budget: zero spent review-correction cycles on #1298, five remaining under the standing default; this attempt is not a correction cycle.

### Unresolved Decisions or Blockers

* None blocking. Open for the owner: broader transitive coverage versus cost.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Fresh prospective attempt from main `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` on `fix/demo-chat-sql-selector-1298-1109`; never modify, adopt or rewrite `fix/chat-schema-sql-gate-1298`; preserve the original High and three Medium process findings. Source: coordinator brief.
* Reproduce the `chatthreads.py`-only omission, make the smallest fail-closed selector fix, preserve discovery exception, execution and receipt controls. Source: issue #1298.
* Add a regression for changed-path selection and receipt expectations; record the remaining transitive-dependency limitation and cost decision explicitly. Source: issue #1298.
* Owner demo-targeted validation: tool selector and receipt regressions and directly impacted tests; bounded actual SQL only if the changed invariant needs it, under the owned non-queued shared lock; no `rpi-checks --all`, no SQL skip waiver, no cloud fallback. Source: coordinator brief.
* `Refs #1298` only; no closing keyword and no relaxation of acceptance criteria. Source: coordinator brief.
* Correction history established before any correction; a fresh attempt does not reset it. Source: coordinator brief; research section Correction budget.
* Commit research, plan, details and critique before any source edit; no push, PR or board writes. Source: coordinator brief.

## Goals

* A `chatthreads.py`-only change selects `mssql`, so the flagged sensor SQL command with its pinned tests and zero-skip count runs.
* The selector stays explicit, fail-closed and documented as not exhaustive.

## Scope and Non-Goals

### In Scope

* One path added to the sensor MSSQL dependency set in `tools/rpi-checks.py` with its comment updated.
* Regression changes in `tools/test_rpi_checks.py`.
* Tracking evidence for research, plan, critique, changes and review.

### Non-Goals

* Transitive closure over `sqlstore.py` imports or any runtime import walker.
* Changes to the SQL command, discovery-exception tuple, receipt verification, skip handling or required-test pinning.
* `rpi-checks --all`, `--changed` receipts, SQL skip waivers, cloud fallback, source migration, README rewrite, the #184 ten-test integration.

## Functional Requirements

* `changed_groups(["src/core/src/zava_forward/core/chatthreads.py"], [])` includes `mssql`.
  * Observable acceptance criteria: the new regression fails on main and passes after the change.
* A path that `mssqlstore.py` does not import, such as `chat_panel.py`, does not select `mssql` through the dependency rule.
  * Observable acceptance criteria: a negative assertion in the regression.
* The selected group yields the existing flagged sensor command with the pinned count.
  * Observable acceptance criteria: the existing per-path command assertion includes the new path.

## Non-Functional Requirements

* Fail closed and bounded: the diff in source is one set member and its comment; no existing control is loosened.
  * Objective threshold or evaluation condition: `git diff` of `tools/rpi-checks.py` touches only the set and its comment.
  * Observable acceptance criteria: the existing receipt-mutation test and the full `test_rpi_checks.py` module still pass.
* Lint, format and strict typing for the two files are clean.
  * Verification approach: run Ruff lint, Ruff format check and strict mypy locally. The gate pins ruff 0.17.1 and mypy 2.4.0 while this environment has ruff 0.17.3 and mypy 2.4.1, so results are labelled unpinned and are not equivalent to the gate; no global install.

## Acceptance Criteria

* Reproduction recorded on main before the change and passing after it.
* Regression asserts the exercised dependency from the code (imports and use in `MssqlStore`), the selection, the negative control and the flagged command.
* Existing path-independent receipt tests (mutation test at tools/test_rpi_checks.py:643-760 and the sensor command/count assertions) are unchanged and pass; they, not a duplicate, cover rejection of missing, substituted or failed sensor SQL evidence.
* The new test derives `chatthreads.py` from the `mssqlstore.py` import and asserts it is in the explicit set and matches no path keyword, so the set entry is tied to the evidence.
* `src/README.md:183-192` was re-read and stays accurate; it is not edited.
* The limitation and tier are documented in the changes record, review, code comment and handoff.
* The literal full-gate criterion is reported as unproven; hosted CI and independent exact-head review remain required.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                          |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md                                            |
| Phase details                    | .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-09/chat-schema-sql-selector-1298-plan-critique.md, dispositions below       |
| Relevant research                | .copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-09/chat-schema-sql-selector-1298-changes.md is created by implementation          |
| Planning execution and readiness | complete; ready                                                                                                     |
| Continuation context             | confirmed automatic parent continues to Implement after critique dispositions                                       |

## Sources

* .copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md: C1 to C15 and correction budget.
* Issue #1298 and #1297 read through `gh` as data; coordinator brief and `demo-rpi-common.md`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Reproduce and add the failing regression

* Intent: demonstrate the omission against unchanged source and pin it in a test.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Record the reproduction and add the regression

* Requirement and evidence: reproduce the omission (research C1, C4); regression and receipt expectations (C9 to C11).
* Expected result: the new test fails on unchanged source for the stated reason.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Make the selector change

* Intent: smallest fail-closed source change.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Add `chatthreads.py` to the explicit sensor MSSQL dependency set

* Requirement and evidence: C2, C6 to C8.
* Expected result: the regression and the adjusted exact-set pin pass; comment states the set is explicit, not exhaustive.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md

<!-- rpi:phase id=P03 -->
### [ ] P03: Targeted validation and evidence

* Intent: owner demo-targeted tier evidence with exact commands, counts and exits.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run the targeted tool checks and record the tier

* Requirement and evidence: owner demo tier; C9 to C13.
* Expected result: unittest module passes with recorded counts; formatter and strict typing results or their unavailability recorded; SQL need decision recorded.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md

## Dependencies

* Merged #1299 is an ancestor of the base `9f9aacc8b`: #1297 integration is present; no stack needed.
* Owned non-queued SQL admission is needed only if the plan's SQL decision changes (see P03-T01).

## Critique Disposition

Critique executed once (Complete), verdict Revise, 0 High, 3 Medium, 4 Low. All findings are planner-owned and applied directly; no user decision was required and no second critique runs.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 Medium | resolved | Validation now runs Ruff lint, Ruff format check and strict mypy; versions unpinned versus gate (ruff 0.17.3/mypy 2.4.1 vs 0.17.1/2.4.0), labelled not gate-equivalent |
| PC-002 Medium | resolved | Pin test edit derives the entry from the AST import of `mssqlstore.py` and asserts set membership and keyword non-match |
| PC-003 Medium | resolved | Wording changed to at least fourteen top-level plus function-local imports (plan and research) |
| PC-004 Low | resolved | Receipt-rejection coverage named; research C11 cite corrected to 643-760 |
| PC-005 Low | resolved | Details specify AST usage sites and which assertions fail before the fix |
| PC-006 Low | resolved | README re-read, unchanged, recorded in acceptance criteria |
| PC-007 Low | resolved | Residual unselected imports and SQL-not-run rationale carried to the changes record and review; real sensor SQL execution at this head is unproven by this attempt |

## Follow-Up Items

* Owner decision: broader transitive dependency coverage versus cost (`sqlstore.py` has at least fourteen top-level sibling imports plus function-local ones). Outside this plan; owner is the decision maker.
* Process follow-up #1300 for prospective recording gaps is separate.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-09/chat-schema-sql-selector-1298-changes.md
* Ready phase or task: P01-T01 after the pre-edit commit
* Remaining provisional question or blocker: none
