<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-005 Subclause Indexing, Capacity-Aware Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Active-Row Session Matching (Issue #1204 Child Loop 6)

## Metadata

* Task ID: issue-1204-rv6-fixes
* Task slug: delivery-1204-coordinator-guard-rv6-fixes
* Parent task ID: issue-1204-rv5-fixes (`delivery-1204-coordinator-guard-rv5-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md) routed five findings: `RV-001` (`_launches_ready_issue_in_current_tick` rescanning `SUBCLAUSE_SPLIT_RE` across the full clause on every `READY_LAUNCH_RE` match, taking `~7.44s` on `"while will be starting #1310 " * 4000`), `RV-002` (lane-specific waiting accepting *any* single launched `ready to start` issue even when additional `ready to start` issues and open session capacity remain), `RV-003` (generic waiting/pause claims such as `"Pausing the run due to an approval from another stakeholder."` passing when they cite zero blocker references), `RV-004` (`[PR #999](https://github.com/jmservera/ama/pull/1641)` in a table blocker cell crediting the mismatched `#999` label as verified blocker evidence), and `RV-005` (`active session` rows in the table not verified against live `--active-sessions` / declared `rpi-<issue>` tokens, and live `rpi-<issue>` sessions missing from the table not flagged). Preserving all closed review and critique logs immutable, this single-phase plan resolves `RV-001`..`RV-005` across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md: Routed findings `RV-001`..`RV-005`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation boundary.
* .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/check-coordinator-handoff.py, and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria with `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py` (`unittest`).
* Use Focused validation only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Keep all closed critique and review artifacts immutable; commit locally on `fix/delivery-1204-coordinator-guard` without pushing or opening a PR.

## Goals

* Precompute `subclause_starts` and `subclause_ends` once per `ClauseIndex` so ready-launch scanning runs in strict `O(N)` time (`< 0.15s` on 4,000-repetition adversarial inputs).
* Require lane-specific waiting summaries below capacity to actively launch every actionable `ready to start` issue up to available session/PR admission capacity.
* Reject any unnegated waiting/pause span that fails to cite at least one verified blocker reference (issue, PR, or URL) from the classification table unless genuinely waiting on declared session-slot saturation or active PR-drain hysteresis.
* Credit only verified link-target references (and flag mismatched `#<n>` link labels) when extracting table blocker evidence, and cross-check `active session` rows bidirectionally against live `--active-sessions` and declared `rpi-<issue>` tokens.

## Scope and Non-Goals

* In scope: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md`, and dated `2026-11-15` `rv6-fixes` RPI artifacts.
* Non-goals: Editing `tools/rpi-checks.py`, modifying closed review/critique files, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`): Precompute `subclause_starts: tuple[int, ...]` and `subclause_ends: tuple[int, ...]` in `_build_clause_index` (splitting each clause `[c_start, c_end)` via `SUBCLAUSE_SPLIT_RE.finditer(span_masked, c_start, c_end)`) and memoize `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` per subclause index in `_launched_ready_issues_in_current_tick` so `"while will be starting #1310 " * 4000` runs in `O(N)` (`< 0.15s`).
* `FR-02` (`RV-002`): Replace boolean `_launches_ready_issue_in_current_tick` with `_launched_ready_issues_in_current_tick(...) -> set[int]`, align `.agent.md` wording (`actively starting each ready to start issue up to available session capacity in the current check`), and in `_validate_section` compute `required_launches = min(len(ready_issue_nums), session_slots)` (where `session_slots = max(0, session_cap - declared_active_sessions)` when `declared_active_sessions is not None`, else `len(ready_issue_nums)`), rejecting waiting summaries when `not at_capacity_or_draining` and the section launches fewer than `required_launches` distinct `ready to start` issues.
* `FR-03` (`RV-003`): Expand wait/pause span extraction (`WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` with consolidated optional trailing prepositions) across all unnegated wait/pause claims (`waiting on/for/until`, `status: waiting`, `waiting summary`, `all lanes waiting`, `paus* ...`, `blocked on/by`), track generic non-GitHub URLs as `("url", normalized_url)` in `BlockerRef = tuple[str, int | str]`, and emit one `unverified-blocker-pause` violation per prose block whenever `has_unverified_phrase` holds or an unnegated wait/pause span cites zero blocker references without `at_session_capacity` + `SESSION_CAPACITY_WAIT_RE` or `pr_drain_active` + `PR_DRAIN_WAIT_RE`.
* `FR-04` (`RV-004`): Parameterize `_extract_refs_from_fragment(..., include_label_refs: bool = True)` so table blocker evidence extraction passes `include_label_refs=False` (never crediting unverified Markdown link labels as blocker evidence) while prose citation extraction keeps `include_label_refs=True`, and record `mismatched_links` on `IssueRow` blocker cells (`mismatched-blocker-link` at `row.lineno`) when a Markdown link `[label](target)` embeds a `#<n>` reference in `label` (`n != row.issue_number`) that is absent from `target`'s resolved issue/PR references.
* `FR-05` (`RV-005`): In `_validate_section`, verify session-to-table consistency bidirectionally with per-section deduplication across `listed_session_tokens` and `active_sessions`:
  * For every `rpi-<issue>` token in `listed_session_tokens` or `active_sessions`, flag `stale-session-classification` if `classified_by_num.get(issue)` is missing (when classification tables exist) or has `state != "active session"`.
  * When `active_sessions is not None` (or when `listed_session_tokens` is non-empty and `not has_non_issue_session_token`), flag `stale-session-classification` on any `active session` row `#N` whose issue number `N` is absent from the active `rpi-<issue>` session issue set (unless a non-`rpi-<issue>` live session token embeds bounded `(?<!\d)N(?!\d)`).
* `FR-06` (Test Ownership Lock): Preserve all `11` test methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods; add `self.subTest` cases inside existing methods covering `RV-001`..`RV-005`).

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, strict linear `O(N)` worst-case scaling, passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` string literals in `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, comments, docstrings, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-005` regression subtests pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and exit code `0` across Focused validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Subclause Indexing, Multi-Ready Launch Guard, Mandatory Pause Blocker Evidence, Link-Target Verification, and Active-Row Matching

* Intent: Resolve `RV-001`..`RV-005` across coordinator instructions, validator, HVE SHA record, and unit tests.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Clarify Capacity-Bounded Multi-Ready Concurrent Launch Rule in `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Refresh HVE Assessment SHA

* Requirement and evidence: `FR-02`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Expected result: `.agent.md` states capacity-bounded concurrent launches (`actively starting each ready to start issue up to available session/PR capacity`) cleanly, `test_rpi_phase_witness.py` passes, and `delivery-1204-coordinator-guard-hve-assessment.md` records the current SHA-256.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement Subclause Indexing, Multi-Ready Launch Verification, Uncited Pause Rejection, Target-Only Blocker Link Evidence, and Bidirectional Active-Session Matching in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-05`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Expected result: `RV-001`..`RV-005` resolved in `tools/check-coordinator-handoff.py` with `0` violations on `.agent.md`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Add `RV-001`..`RV-005` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-06`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv5-fixes-review.md
* Expected result: All `11` test methods and all Focused checks exit `0`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`; `P01-T03` depends on `P01-T01` and `P01-T02`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-plan-critique.md (Verdict: `Revise`, `0` Critical, `1` High, `2` Medium, `1` Low; user response required: `no`):

* `PC-001` [High] (`direct_planner_correction`, applied): Computed `required_ready_launches = min(len(ready_issue_nums), session_slots)` without artificially capping launches by `20 - declared_open_prs` when PR drain is inactive (`at_capacity_or_draining` already models `Open PRs > 20` and `Open PRs > 15` drain hysteresis).
* `PC-002` [Medium] (`direct_planner_correction`, applied): Consolidated optional trailing prepositions into `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` branches and emitted at most one `unverified-blocker-pause` violation per prose block when `has_unverified_phrase or has_uncited_non_capacity_wait`.
* `PC-003` [Medium] (`direct_planner_correction`, applied): Recorded `mismatched_links` on `IssueRow` blocker cells (`mismatched-blocker-link` at `row.lineno`) alongside `include_label_refs=False` in `_extract_verified_evidence_refs`.
* `PC-004` [Low] (`direct_planner_correction`, applied): Added per-section deduplication for `stale-session-classification` across `listed_session_tokens` and `active_sessions`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
