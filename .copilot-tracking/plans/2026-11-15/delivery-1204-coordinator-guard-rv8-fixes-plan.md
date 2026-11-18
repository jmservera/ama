<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-005 Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Complete Subtest Coverage (Issue #1204 Child Loop 8)

## Metadata

* Task ID: issue-1204-rv8-fixes
* Task slug: delivery-1204-coordinator-guard-rv8-fixes
* Parent task ID: issue-1204-rv7-fixes (`delivery-1204-coordinator-guard-rv7-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md) routed five findings: `RV-001` (`_is_claim_negated_at` slices `idx.raw_text[ct.start : ct.end]` on every match inside any clause containing a prohibition token, causing `O(K * N)` quadratic runtime on `"never " + "starting #1310 " * N`), `RV-002` (`_extract_wait_and_blocker_spans` accepts `"Waiting on PR #1641 and stakeholder approval."` when `#1641` is verified because coordinated segments under a single wait trigger are not checked independently), `RV-003` (`SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` reject legitimate bounded timing tails like `"Waiting for a free worker session slot until the next check."` at `1/1` capacity), `RV-004` (two planned positive subtests — `"until the next check"` and backticked `` `rpi-1310-no-push` `` — were omitted from `tools/test_check_coordinator_handoff.py`), and `RV-005` (changes prose overstated the tracking-directory literal assertion scope as all of `tools/` instead of the two Issue #1204 target files). Preserving all closed review and critique logs immutable, this single-phase plan resolves `RV-001`..`RV-005` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md: Routed findings `RV-001`..`RV-005`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation tier.
* tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py` (`unittest`).
* Run Focused validation only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Leave all closed critique and review artifacts untouched; commit locally on `fix/delivery-1204-coordinator-guard` without pushing or opening a PR.

## Goals

* Eliminate per-match clause string slicing in `_is_claim_negated_at` by storing `raw: str` once per `ClauseTokens` during `_build_clause_index` (`RV-001`).
* Verify every coordinated wait/blocker segment separated by `and` / `or` / `plus` / `as well as` inside a trigger's `target_span` while preserving shared PR/issue lifecycle tails such as `"PR #1641 CI and status checks"` (`RV-002`).
* Accept bounded next-check/tick/poll timing qualifiers at the tail of `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` while still rejecting arbitrary non-capacity blocker tails (`RV-003`).
* Add all planned `RV-001`..`RV-004` `self.subTest` cases inside existing `11` test methods in `tools/test_check_coordinator_handoff.py` and record exact two-file tracking-literal validation scope in the changes log (`RV-004`, `RV-005`).

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and dated `2026-11-15` `rv8-fixes` RPI artifacts.
* Non-goals: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` (already conformant), running or editing `tools/rpi-checks.py`, editing closed review/critique artifacts, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`): Add `raw: str` to `ClauseTokens`, populate `raw=clause_raw` once inside `_build_clause_tokens`, and use `ct.raw` inside `_is_claim_negated_at` instead of slicing `idx.raw_text[ct.start : ct.end]` per match.
* `FR-02` (`RV-002`, `PC-001`, `PC-002`): In `_extract_wait_and_blocker_spans`, treat compound trigger prefixes (`Paused and waiting on ...` via `INTRO_PREFIX_BETWEEN_RE`) and strip trailing conjunction bridges immediately preceding the next trigger (`TRAILING_NEXT_TRIGGER_BRIDGE_RE` when `stop_m is None` and `i + 1 < len(triggers)` because Python `re.Pattern.search(..., pos, endpos)` bounds lookaheads at `endpos`), mask `MD_LINK_RE` spans over `idx.span_masked_text[tm.end():end_pos]` so `[label](target)` links containing `and`/`or` or commas are never split mid-link, then split `target_span` across `COORDINATED_WAIT_SPLIT_RE` (`(?:,\s*(?:(?:and|or|plus|as\s+well\s+as)\b\s*)?(?!(?:until|before|for|pending|awaiting|till|at|during|under|in|on|with|without)\b)|\b(?:and|or|plus|as\s+well\s+as)\b)`). Require every coordinated segment `seg_j` either to contain at least one blocker reference (`seg_refs`), to satisfy `_is_exempt_capacity_or_drain_wait`, or to match `SHARED_REF_LIFECYCLE_SEG_RE` when adjacent (`j - 1` or `j + 1`) to a cited segment; otherwise set `has_uncited_wait = True`.
* `FR-03` (`RV-003`, `PC-003`): Extend the optional tail of `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` (placed after numeric drain threshold qualifiers and before `[\s)]*$`) to permit bounded scheduling qualifiers (`(?:(?:\s+|,\s*)(?:(?:until|before|for|pending|awaiting|till)\s+(?:(?:a|an|the)\s+)?(?:next\s+)?(?:scheduled\s+|coordinator\s+)?(?:check|tick|run|poll|cycle|pass|turn|window)|at\s+the\s+next\s+(?:scheduled\s+|coordinator\s+)?(?:check|tick|run|poll|cycle|pass|turn|window)))?`) while continuing to reject arbitrary non-capacity tails (`for external vendor`, `and owner approval`).
* `FR-04` (`RV-004`, `PC-001`, `PC-002`, Test Ownership Lock): Preserve all `11` existing `def test_*` methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods) and add `self.subTest` cases inside existing methods covering `"never " + ("starting #1310 " * 4000)` linear scaling, coordinated uncited blockers (`"Waiting on PR #1641 and stakeholder approval."`, `"Waiting on stakeholder approval and PR #1641."`, `"Waiting on PR #1641, stakeholder approval, and PR #1642."`, `"Waiting on PR #1641 or external vendor."`) plus positive `"Waiting on PR #1641 CI and status checks."`, `"Waiting on CI and status checks on PR #1641."`, and `"[CI and checks](https://github.com/jmservera/ama/pull/1641)"`, `"Waiting for a free worker session slot until the next check."` at `1/1` capacity, `"Waiting on PR drain below 15 until the next scheduled check."` during PR drain, and backticked `` `rpi-1310-no-push` `` active launch.
* `FR-05` (`RV-005`): Record the exact two-file tracking-directory literal check scope (`tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`) in `delivery-1204-coordinator-guard-rv8-fixes-changes.md`.

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, strict `O(N)` worst-case runtime (`< 0.25s` on 4,000 repeated prohibited launch phrases in one clause), passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` string literals in `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, comments, docstrings, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-005` checks pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and exit code `0` across Focused validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Pre-Indexed Clause Raw Slices, Coordinated Wait-Segment Verification, Next-Check Capacity/Drain Tails, and Subtest Coverage

* Intent: Resolve `RV-001`..`RV-005` across `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and the `rv8-fixes` changes record.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `RV-001`..`RV-003` Fixes in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-03`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md
* Expected result: `ClauseTokens.raw` eliminates per-match clause copies, coordinated wait segments require independent blocker verification, and `until the next check` capacity/drain waits pass without false positives.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `RV-001`..`RV-004` Subtests in `tools/test_check_coordinator_handoff.py`, Record Exact Two-File Check Scope (`RV-005`), and Run Focused Validation

* Requirement and evidence: `FR-04`, `FR-05`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-review.md
* Expected result: All `11` test methods and all Focused checks exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-plan-critique.md (Verdict: `Revise`, `0` Critical, `1` High, `1` Medium, `1` Low; user response required: `no`):

* `PC-001` [High] (`direct_planner_correction`, applied): Masked `MD_LINK_RE` spans before coordinated wait splitting so `[CI and checks](...)` links are never split mid-link, and allowed `SHARED_REF_LIFECYCLE_SEG_RE` segments adjacent to either the preceding or following cited segment (`CI and status checks on PR #1641`).
* `PC-002` [Medium] (`direct_planner_correction`, applied): Extended `COORDINATED_WAIT_SPLIT_RE` to split non-prepositional serial-comma items so 3-item lists like `"Waiting on PR #1641, stakeholder approval, and PR #1642."` flag the uncited middle blocker.
* `PC-003` [Low] (`direct_planner_correction`, applied): Placed `NEXT_CHECK_TIMING_TAIL_PAT` after numeric drain threshold qualifiers and immediately before `[\s)]*$` in `PR_DRAIN_WAIT_SPAN_RE`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
