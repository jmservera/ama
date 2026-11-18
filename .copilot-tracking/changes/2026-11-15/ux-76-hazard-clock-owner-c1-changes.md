<!-- markdownlint-disable-file -->
# RPI Changes: Issue #76 Correction Cycle 1 — PR #1768 `mssql` CI Parity Fix and Rebase onto `#1641`

## Metadata

* Task ID: issue-76-c1
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: None
* Status basis: Rebased cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), implemented staff-order-invariant lookup and fallback in `taskqueues.py` (`MEMBERSHIP_REVISION = 5`), added strictly typed permutation and email-seeded `SqlStore` parity unit tests in `test_hazard_safeguarding_clock_owner.py`, passed all focused validation checks (3,514 `src/core` unit tests, `mypy`, `ruff`, and `#76` API tests), and configured privacy-safe local Git commit identity ready for post-`rpi-review` local commit.

## Execution Summary

All planned phases (`P01` and `P02`) completed without material divergences. `feat/ux-76-hazard-clock-owner` now sits cleanly atop `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), preserving both `#83` (`PR #1769`) handoff SLA escalation arguments and `#76` safety roster projection in `Store._work_context`, while eliminating `staff` row-order sensitivity between JSON/SQLite insertion order and SQL Server clustered primary-key (`email`) order.

## Completed Work

### Rebase onto `#1641` (`0c1fa1da4`) and Resolve `Store._work_context`

* Related phase or task: `P01-T01`
* Files: `src/core/src/zava_forward/core/store.py`
* What changed and why: Rebased `feat/ux-76-hazard-clock-owner` (`5d4c80ee3` -> `8bd8a4f4d`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolving the single merge conflict in `Store._work_context` so `taskqueues.context(...)` receives both `#83`'s `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `#76`'s `staff=staff_list`.
* Completion evidence: `git merge-base --is-ancestor 0c1fa1da4 HEAD` exited `0`; zero conflict markers remain.
* Validation: Passed (`test_handoff_escalation_83.py` 11/11 and `test_hazard_safeguarding_clock_owner_76.py` 3/3).

### Deterministic Staff Lookup, Sorted Role Fallback, and Queue Revision Separation

* Related phase or task: `P01-T02`
* Files: `src/core/src/zava_forward/core/taskqueues.py`, `src/core/README.md`
* What changed and why: Added `_staff_sort_key` and rewrote `_match_staff` to run three separate precedence passes (`code.strip()` across all `staff`, then case-insensitive `email.strip().lower()`, then case-insensitive `name.strip().lower()`) over canonically sorted `staff`, sorted `roster` before role-based fallback scanning in `project_safety_clock_and_owner`, and bumped `MEMBERSHIP_REVISION` to `5` (syncing `src/core/README.md`) so databases created at `#83`'s revision `4` refresh `#76` queue flags.
* Completion evidence: `taskqueues.MEMBERSHIP_REVISION == 5`; `_match_staff` and `project_safety_clock_and_owner` produce identical results across every permutation of `STAFF`.
* Validation: Passed (`mypy`, `ruff check`, `ruff format --check`, and unit test suites).

### Permutation and Email-Ordered SQL Parity Unit Tests and Focused Validation

* Related phase or task: `P02-T01`
* Files: `src/core/tests/test_hazard_safeguarding_clock_owner.py`
* What changed and why: Added strictly typed unit tests (`StaffOrderInvarianceTests`) verifying `_match_staff` field precedence (`code` > `email` > `name`) with whitespace normalization, `project_safety_clock_and_owner` invariance across all `itertools.permutations` of `STAFF` when `case` has `owner_code="PM-01"` and `owner="Sam Example"` (allocated and unallocated), duplicate-role fallback determinism, and end-to-end `Store` (`[Sam, Pam, Kim]`) vs email-seeded `SqlStore` (`[Kim, Pam, Sam]`, matching SQL Server's clustered `email` PK order) parity across `counts`, `page_cases` (`all`/`mine`, `flag="hazard"`, `queue="blocked"`, `queue="overdue"`), and `detail` on `test_sqlreads.make_cases(120)`.
* Completion evidence: `src/core/tests/test_hazard_safeguarding_clock_owner.py` created (1 new test file, 0 test removals, 0 `type: ignore` suppressions).
* Validation: Passed (`test_hazard_safeguarding_clock_owner.py` 4/4, `test_sqlreads.py` 15/15, `mypy` 339 files, `ruff` 286 files, full `src/core` `unittest` 3,514 tests, and `#76` API regression suite 2/2).

### Diff-Boundary Check, Privacy-Safe Git Identity, and Review/Commit Reconciliation

* Related phase or task: `P02-T02`
* Files: `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md`, `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md`, `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md`
* What changed and why: Verified `git diff --name-status` contains only `src/core/src/zava_forward/core/taskqueues.py`, `src/core/README.md`, and new `src/core/tests/test_hazard_safeguarding_clock_owner.py` (plus `.copilot-tracking/` `-c1` artifacts), configured repository-local `user.email` to `8036360+jmservera@users.noreply.github.com` from `gh api user`, and reconciled all plan/detail markers ahead of `rpi-review` and the single post-review local `Refs #76` commit.
* Completion evidence: `git config --local user.email` verified; all `P01` and `P02` checklist markers `[x]`.
* Validation: Passed (`git diff --name-status` and `git status --short` verified).

## Implementation-Time Plan and Detail Updates

None required beyond checking completed `P01` and `P02` markers and updating handoff status.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v` | `src/core` | Passed | `Ran 4 tests in 0.537s — OK` |
| `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_76.py" -v` | `src/core` | Passed | `Ran 3 tests in 0.291s — OK` |
| `python3 -m unittest discover -s tests -p "test_handoff_escalation_83.py" -v` | `src/core` | Passed | `Ran 11 tests in 1.099s — OK` |
| `python3 -m unittest discover -s tests -p "test_sqlreads.py" -v` | `src/core` | Passed | `Ran 15 tests in 49.436s — OK` |
| `mypy` (`strict = true`) | `src/core` (339 source files) | Passed | `Success: no issues found in 339 source files` |
| `ruff check .` & `ruff format --check .` | `src/core` (286 formatted files) | Passed | `All checks passed! 286 files already formatted` |
| `python3 -m unittest discover -s tests -q` | `src/core` (full suite) | Passed | `Ran 3514 tests in 985.644s — OK (skipped=419)` |
| `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner_api_76.py" -v` | `src/api` (`#76` API/DOM guard) | Passed | `Ran 2 tests in 2.587s — OK` |
| Hosted `mssql` CI (`MssqlParity` against live SQL Server container) | GitHub Actions (`ZF_TEST_MSSQL=1`) | Skipped | Local commit only per caller instructions (`Do NOT push or run rpi-checks.py`); mechanism reproduced locally via email-seeded `SqlStore` parity test |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`; Phase Index marked `Complete`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in `Implement`; post-`rpi-review` local commit will capture code + all `-c1` tracking artifacts cleanly with `Refs #76` and the Copilot trailer.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md, `## Follow-Up Items`
* Push rebased `feat/ux-76-hazard-clock-owner` to `origin` (`PR #1768`) once authorized by the owner and verify the hosted GitHub Actions `mssql` job (`MssqlParity`) passes on the new head SHA.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: Focused tier complete (`test_hazard_safeguarding_clock_owner.py`, `test_hazard_safeguarding_clock_owner_76.py`, `test_handoff_escalation_83.py`, `test_sqlreads.py`, `mypy`, `ruff check`, `ruff format --check`, full 3,514-test `src/core` `unittest` suite, and `test_hazard_safeguarding_clock_owner_api_76.py` all passed)
* Blockers: None
* Current plan and detail updates: Checked `P01` and `P02` completion markers and updated handoff to `Review`
* Planning and critique state: Complete (`PC-001`–`PC-003` resolved)
* Follow-up items: Owner-authorized push and hosted `mssql` CI check on `PR #1768`
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
