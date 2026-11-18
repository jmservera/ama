<!-- markdownlint-disable-file -->
# Changes: Resolve RV-001 through RV-003 Linear-Time Negation, Ready-Row Launch Guard, and Qualified Blocker Citations (Issue #1204 Child Loop 3)

## Metadata

* Task ID: issue-1204-rv3-fixes
* Task slug: delivery-1204-coordinator-guard-rv3-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Execution status: Complete

## Opening Implementation State

* Interpreted implementation goal: Implement `P01-T01` and `P01-T02` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` to resolve `RV-001`..`RV-003` and `PC-001`..`PC-004`.
* Declared scope: Full child plan (`P01`, `P01-T01`, `P01-T02`)
* First ready item: `P01-T01`
* Active blockers: none

## Completed Work

### P01-T01: Linear-Time Prohibition Scanner, Ready-Row Launch Guard, and Qualified Blocker Extraction (`tools/check-coordinator-handoff.py`)

* Replaced nested variable-length prohibition regexes with linear-time `O(N)` `_trailing_clause_has_governing_prohibition`, using word-boundary-guarded single-quote literal masking (`INLINE_LITERAL_SPAN_RE`), reverse-bounded (`[-4:]`) `PROHIBITION_HEAD_RE` inspection, governed verb checks (`GOV_VERB_TOKEN_RE`), and finite `GOV_CONTINUATION_TOKENS` (excluding `and`) to eliminate exponential backtracking (`RV-001`, `PC-004`).
* Replaced `_has_unnegated_concurrent_launch` with `_launches_ready_issue_in_current_tick(line, ready_issue_nums)`, requiring target issue membership in `ready_issue_nums`, rejecting pre-verb negations/holds (`LAUNCH_NEG_OR_HOLD_PREFIX_RE`, including `not` and `*n't`), and rejecting historical qualifiers across the full enclosing `while`-bounded launch subclause (`HISTORICAL_LAUNCH_SUBCLAUSE_RE`, preserving `since [the] last ...`) (`RV-002`, `PC-002`).
* Replaced single-token `CITED_BLOCKER_REF_RE` with `_extract_cited_blocker_numbers(line)` using flat `BLOCKER_TRIGGER_RE` and `BLOCKER_SPAN_STOP_RE` so qualified citations (`Waiting for hosted CI on PR #999.`, `Waiting on parent PR #999.`) extract `999` and trigger `unverified-blocker-reference` when unlisted (`RV-003`, `PC-003`).

### P01-T02: Performance and Behavioral Regression Subtests (`tools/test_check_coordinator_handoff.py`)

* Added regression `self.subTest` cases inside `test_adversarial_rv001_handoff_bypasses_rejected` (`11` test methods total, zero net additions) verifying `< 0.5s` execution on both failing-suffix (`"Never claim " + ("idle or " * 80) + "and nothing changed."`) and positive (`"Never claim " + ("idle or " * 80) + "nothing changed."`) repetition, possessive apostrophe non-bridging, historical/participle-negated/non-ready launch rejection, and qualified unlisted PR blocker rejection.

## Implementation-Time Plan and Detail Updates

* Local judgment: Bounded launch subclauses across `\bwhile\b` boundaries inside `_launches_ready_issue_in_current_tick` so an active `while starting #1310 next` subclause is evaluated cleanly without cross-contaminating adjacent `while` subclauses.

## Validation Record

* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> passed (`All checks passed!`)
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> passed (`2 files already formatted`)
* `python3 tools/check-coordinator-handoff.py` -> passed (`Coordinator handoff guard check passed (1 target(s), 0 violations).`)
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` -> passed (`Ran 11 tests in 0.608s - OK`)
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` -> passed (`Ran 33 tests in 8.095s - OK`)
* `git --no-pager diff --check` -> passed
* `tools/rpi-checks.py` -> intentionally not executed per explicit Focused-tier instruction (`Do NOT run tools/rpi-checks.py`).

## Blockers and Remaining Work

* Blockers: none
* Remaining work: none (`P01`, `P01-T01`, `P01-T02` complete; ready for `Review`)

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
