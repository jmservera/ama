<!-- markdownlint-disable-file -->
# Implementation Changes: Resolve RV-001 through RV-007 Quoted Prohibition Attribute Fix, Linear Bridge/Session Indexing, Causal Blocker Verification, Bare Pause Enforcement, Comma Timing Lookahead, and Contiguous Lifecycle Chains (Issue #1204 Child Loop 9)

## Metadata

* Task ID: issue-1204-rv9-fixes
* Task slug: delivery-1204-coordinator-guard-rv9-fixes
* Plan: .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan-critique.md
* Declared scope: Full plan (`P01`: `P01-T01` through `P01-T02`)
* Execution status: Complete

## Phase Execution Summary

### P01: Quoted Prohibition Fix, Linear Bridge and Session Indexing, Causal/Pause Blocker Guards, and Subtest Coverage

#### P01-T01: Implement `RV-001`..`RV-007` Fixes in `tools/check-coordinator-handoff.py`

* Fixed `_fallback_prohibition_check` integer `pm.end` slice indexing (`RV-001`), added `_mask_inline_literal_interior` (`clause_split_masked`) in `_build_clause_index` so colons/semicolons/periods inside closed inline literals do not split outer clauses (`PC-002`), restricted `_fallback_prohibition_check` on literal interiors to inner prohibitions (`pm.inside_literal_end == only_literal_end`) with no intervening `CLAUSE_SPLIT_RE` match, and evaluated outer prohibitions at `lit_s` via the indexed token path in `_is_claim_negated_at`.
* Replaced regex backtracking in multi-trigger bridge stripping with deterministic linear `_strip_trailing_trigger_bridge` (`RV-002`, `PC-001`), covering both coordinating (`as well as`, `and`, `or`, `also`, `plus`) and causal (`because of`, `due to`, `owing to`, `because`) connectors, and aligned `INTRO_PREFIX_BETWEEN_RE`.
* Pre-extracted integer tokens once from `custom_non_rpi_tokens` via `STANDALONE_ISSUE_NUM_RE` into `custom_session_issue_nums: set[int]` (`O(S + M)`) before scanning `active_session_rows` (`RV-003`).
* Extended `PAUSE_HEAD_PAT`, `CLAUSE_SPLIT_RE`, `WAITING_OR_PAUSE_RE`, `DIRECT_GLOBAL_WAIT_RE`, and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` (ordered `paus(?:ed|ing|e)\b` with optional `WAIT_INTRODUCER_TAIL_PAT`) to enforce table presence and blocker verification on `Status: paused.`, `paused summary`, `all lanes paused`, and `(?:scheduled )?check|run|delivery|schedule|tick paused` (`RV-005`, `PC-001`).
* Updated `COORDINATED_WAIT_SPLIT_RE` so `NEXT_CHECK_NOUN_LOOKAHEAD_PAT` sits immediately after `,` with explicit optional post-comma coordinating/causal/non-timing-`pending` consumption (`RV-006`), bounded non-comma splits by non-whitespace (`(?<=\S)[ \t]+...(?=[ \t]+\S)`), and added copular/aspectual negative lookbehinds before `[ \t]+(?:pending|awaiting)\b` (`RV-004`, `PC-001`).
* Extended `SHARED_REF_LIFECYCLE_SEG_RE` with optional leading `of` and bounded lifecycle predicate tails, and replaced single-hop neighbor copying with two linear sweeps (`life_attached`) across contiguous `SHARED_REF_LIFECYCLE_SEG_RE` runs (`RV-007`).

#### P01-T02: Add `RV-001`..`RV-007` Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Preserved the exact `11` `def test_*` methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods) and added `self.subTest` blocks covering multi-token and colon-containing quoted prohibitions plus negative controls (`RV-001`, `PC-002`), `20,000`-space bridge scaling (`< 0.15s`, `RV-002`), `1,200` custom non-RPI worker sessions scaling (`< 0.25s`, `RV-003`), causal uncited vs cited blocker subclauses (`RV-004`, `PC-001`, `PC-003`), bare and tableless `Status: paused.` enforcement plus valid `Status: paused on/due to/pending ...` (`RV-005`), comma-prefixed `, until the next check` / `, pending the next check` capacity and drain waits (`RV-006`), and 3-item contiguous lifecycle chains (`RV-007`).

## Implementation Discoveries and Updates

* Local judgment: Renamed loop-unpacked `ClauseIndex` binding to `c_idx` in `check_handoff_text` so `mypy` cleanly distinguishes it from an earlier integer loop index `idx` in the same function scope.

## Validation Summary

* `python3 tools/check-coordinator-handoff.py` -> exit `0` (`Coordinator handoff guard check passed (1 target(s), 0 violations).`).
* `python3 -m unittest tools/test_check_coordinator_handoff.py -q` -> exit `0` (`Ran 11 tests in 0.721s`, `OK`).
* `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> exit `0` (`All checks passed!`).
* `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> exit `0` (`2 files already formatted`).
* `python3 -m mypy tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py` -> exit `0` (`Success: no issues found in 2 source files`).
* `python3 -m unittest tools/test_rpi_phase_witness.py -q` -> exit `0` (`Ran 33 tests in 2.837s`, `OK`).
* Invariant checks: exact `11` `def test_*` methods in `tools/test_check_coordinator_handoff.py`, valid JSON across all `.copilot-tracking/rpi-sessions/2026-11-15/*.json` state files, zero `.copilot-tracking` string literals in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`, and `git --no-pager diff --check` exit `0`.
* Explicit skip: `tools/rpi-checks.py` intentionally not executed per user Focused-tier instruction (`Do NOT run tools/rpi-checks.py`).

## Remaining Work and Blockers

* Remaining active-plan tasks: none (`P01`, `P01-T01`, and `P01-T02` complete).
* Blockers: none.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).

## Handoff

Ready for single-pass `rpi-review` at .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-review.md.
