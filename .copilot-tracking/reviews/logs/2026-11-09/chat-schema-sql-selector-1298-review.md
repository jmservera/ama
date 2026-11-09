<!-- markdownlint-disable-file -->
# RPI Review: chat-schema-sql-selector-1298

| Field | Value |
|---|---|
| Date | 2026-11-09 |
| Task ID | issue-1298-fresh-demo |
| Reviewed boundary | implementation commit 58efcaa50536557954388890e024808f598a1092 on base 9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939 (pre-source evidence commit 52c3ec4f507a6129372e0ce747ed176d9ed9a61a) |
| Reviewer | implementing-agent pass through rpi-review; not an independent review |
| Review execution | Complete |
| Outcome | Residual work (no defects found in the delivered change) |

## Compared artifacts

* .copilot-tracking/research/2026-11-09/chat-schema-sql-selector-1298-research.md
* .copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md (all P01 to P03 markers checked, critique dispositions PC-001 to PC-007 resolved)
* .copilot-tracking/details/2026-11-09/chat-schema-sql-selector-1298-phase-details.md
* .copilot-tracking/reviews/plans/2026-11-09/chat-schema-sql-selector-1298-plan-critique.md (single critique, verdict Revise, applied directly, not repeated)
* .copilot-tracking/changes/2026-11-09/chat-schema-sql-selector-1298-changes.md
* .copilot-tracking/rpi-sessions/2026-11-09/chat-schema-sql-selector-1298-state.json

## Reconciliation

* Plan markers, details, changes record, state and validation agree. Ordering evidence: research, plan, details and critique are committed at 52c3ec4f5, before the first source edit; the changes record and Implement state were written before the source edit; the regression was run failing (3 failures) before the selector change.
* Source diff is limited to one set member and its comment in tools/rpi-checks.py, and tests in tools/test_rpi_checks.py. No SQL command, discovery-exception, required-test or receipt-verification code changed. src/README.md:183-192 re-read and still accurate.
* Correction budget: zero prior review-correction cycles on #1298, no grant, five remaining; this attempt was the initial implementation. Original adverse evidence on fix/chat-schema-sql-gate-1298 (fef352e0) is untouched.

## Acceptance criteria matrix (issue #1298)

| Criterion | Status | Evidence |
|---|---|---|
| Reproduce omitted MSSQL selection and the exercised SQL initialization dependency | Proven | research C1 to C8; repro-before `mssql selected: False`, repro-after `True`; AST regression |
| Smallest fail-closed change preserving discovery exception, SQL command, execution evidence and receipt checks | Proven for the selector | diff limited to one set member; module 103 tests pass |
| Regression for changed-path selection and receipt expectations including rejection of missing or failed sensor SQL evidence | Proven | new test, extended per-path loop asserting flagged command, flag and pinned count; existing mutation tests (tools/test_rpi_checks.py receipt mutation test) pass unchanged |
| Record remaining transitive limitation and broader coverage or cost decision | Proven (recorded) | code comment, plan, changes record, RV-001 |
| Isolated RPI, independent exact-head review, applicable full local gate, hosted checks | Unproven | full gate not run under the owner demo tier; independent review and hosted CI pending |

## Validation evidence

Owner-selected demo-targeted tier (no `rpi-checks --all`/`--changed`, no SQL waiver, no cloud fallback). Commands, exits and counts are in the changes record: targeted unittest Ran 3 OK; full tools module Ran 103 OK, 0 skipped; Ruff check and format (isolated gate arguments) exit 0; mypy --strict exit 0; `git diff --check` exit 0. Ruff 0.17.3 and mypy 2.4.1 differ from the gate pins 0.17.1 and 2.4.0, so they are not gate-equivalent. No SQL container was started and no shared SQL lock taken, because path selection is the only changed invariant. Hosted CI was not observed.

## Findings

| ID | Severity | Finding | Destination |
|---|---|---|---|
| RV-001 | Medium | Coverage is explicit, not exhaustive. `sqlstore.py` (imported by `mssqlstore.py`) has at least fourteen top-level sibling imports plus function-local imports; a change to one of them alone can still omit `mssql` if its code runs in the sensor fixture. Only `chatthreads.py` is demonstrated here. | Distinct follow-up: owner decision on transitive coverage versus cost |
| RV-002 | Medium | Real sensor MSSQL execution at this head and the literal full-gate acceptance criterion are unproven by this attempt, by owner demo policy. | Distinct follow-up: independent exact-head review and hosted CI; any full gate only if the owner requires it; `Refs #1298`, no closing keyword |
| RV-003 | Low | The new test asserts the alias references through any `ast.Name` in `mssqlstore.py`, not specifically inside `MssqlStore` methods; it proves the names are used, not that the sensor fixture's constructor path reaches them. The call-path claim rests on the C6 and C7 reading. | Residual work; optional for a later implementation |
| RV-004 | Low | This review is by the implementing agent family and the critique worker is a same-family subagent; neither substitutes for independent exact-head review. | Coordinator: independent review |

No High findings. No defects requiring `rpi-implement`, no decision gaps for `rpi-plan`, no research gaps.

## Routing and follow-ups

1. Independent exact-head review and hosted CI on the frozen head (RV-002, RV-004).
2. Owner decision on transitive dependency coverage versus cost (RV-001).
3. Optional strengthening of the AST usage assertion (RV-003).
