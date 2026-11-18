<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-006 Single-Subclause Hold Indexing, Independent Multi-Trigger Spans, Strict Capacity/Drain Anchors, Bare Self-URL Rejection, Tableless Blocker Checks, and Mixed Declared Session Matching (Issue #1204 Child Loop 7)

## Metadata

* Task ID: issue-1204-rv7-fixes
* Task slug: delivery-1204-coordinator-guard-rv7-fixes
* Parent task ID: issue-1204-rv6-fixes (`delivery-1204-coordinator-guard-rv6-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md) routed six findings in `tools/check-coordinator-handoff.py`: `RV-001` (quadratic `O(K^2)` prefix rescanning inside a single long subclause when `READY_LAUNCH_RE` matches repeat before `after approval` or a hold keyword), `RV-002` (`Waiting on PR #1641 because pausing the run for stakeholder approval.` passing when `#1641` is verified because `covered_until` masks the subsequent uncited trigger), `RV-003` (loose `SESSION_CAPACITY_WAIT_RE` / `PR_DRAIN_WAIT_RE` keyword checks excusing `"Waiting for stakeholder approval of the capacity plan."` at full session capacity), `RV-004` (bare self-issue GitHub URLs like `https://github.com/jmservera/ama/issues/1288` without a `#fragment` counting as valid blocker evidence on `#1288`), `RV-005` (`"Blocked on stakeholder approval."` with no classification table bypassing both `unverified-blocker-pause` and `missing-classification-table`), and `RV-006` (mixed declared session lists like `rpi-1302, maintenance` disabling offline `active session` row coverage checks). Preserving all closed review and critique records immutable, this single-phase plan resolves `RV-001`..`RV-006` in `tools/check-coordinator-handoff.py` and adds `self.subTest` regression cases inside existing `11` test methods in `tools/test_check_coordinator_handoff.py` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md: Routed findings `RV-001`..`RV-006`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation boundary.
* tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria with `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py` (`unittest`).
* Use Focused validation only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Preserve all closed critique and review logs immutable; commit locally on `fix/delivery-1204-coordinator-guard` without pushing or opening a PR.

## Goals

* Guarantee strict `O(N)` worst-case runtime in `_launched_ready_issues_in_current_tick` even when thousands of launch matches occur inside a single subclause (`RV-001`).
* Validate every substantive wait/pause/blocker trigger independently in `_extract_wait_and_blocker_spans` while preserving introductory prefix chaining (`Status: waiting — blocked on #1641`), and restrict capacity/PR-drain exemptions strictly to slot-saturation or PR-drain waits (`RV-002`, `RV-003`).
* Reject bare self-issue GitHub URLs without `#fragment` on `human-blocked` and `dependency-blocked` rows, enforce `unverified-blocker-pause` and table-presence checks on uncited `blocked on/by` claims, and require active-row session coverage even when mixed non-issue declared tmux sessions are present (`RV-004`, `RV-005`, `RV-006`).

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and dated `2026-11-15` `rv7-fixes` RPI artifacts.
* Non-goals: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` (already conformant in `rv6-fixes`), editing `tools/rpi-checks.py`, altering closed critique/review logs, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-004`): In `_launched_ready_issues_in_current_tick`, check memoized `non_current_by_subclause` (`si not in non_current_by_subclause`, scanning `idx.span_masked_text[sub_start:sub_end]`) before hold/negation checks, and memoize `min_hold_end_by_subclause: dict[int, int]` using integer sentinel `-1` (`si not in min_hold_end_by_subclause`, scanning `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.finditer(idx.span_masked_text, sub_start, sub_end)`) once per subclause index `si` so `min_hold_end != -1 and min_hold_end <= m.start()` executes in `O(1)` per match (`O(N)` total across the prose block without hold-free cache misses or backtick token false matches).
* `FR-02` (`RV-002`): In `_extract_wait_and_blocker_spans`, collect all unnegated `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` matches `triggers`, compute each trigger's `natural_end` via `BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end())`, delegate `triggers[i]` to `triggers[i + 1]` only when `triggers[i + 1].start() < natural_end` and `text[tm.end():triggers[i + 1].start()]` matches pure introductory punctuation/whitespace (`^[\s:,\-\u2013\u2014]*$`), and otherwise clamp `end_pos = min(natural_end, triggers[i + 1].start())` so every substantive trigger is checked independently in `O(N)`.
* `FR-03` (`RV-003`, `PC-002`): Evaluate `_is_exempt_capacity_or_drain_wait` on the post-trigger slice `target_span = text[tm.end():end_pos]`, anchoring `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` to the head of `target_span`, rejecting coordinating or causal extra-blocker tails (`\b(?:and|or|plus|because|due\s+to)\b`) inside `target_span`, and rejecting non-capacity blocker phrases (`approv*`, `stakeholder*`, `owner*`, `review*`, `human*`, `sign-off*`, `decision*`, `feedback`, `input`, `repl*`, `response*`, `clearance*`, `permission*`, `legal`, `security`, `outage*`, `upstream`, `ci`, plural `checks`, `(?:ci|pr|hosted|status|required|merge)\s+check`, `plan*`) without false-triggering on singular coordinator `"next check"` prose.
* `FR-04` (`RV-004`, `PC-001`): Add `_is_bare_self_issue_url(url, issue_number, self_repo_key="")` aligned with `_normalize_repo_key(DEFAULT_LOCAL_REPO) == ""`, matching fragment-free or `#<self>`-fragment GitHub/relative `issues/<self>` URLs (`https://github.com/<owner>/<repo>/issues/<self>`, `/issues/<self>`, `./issues/<self>`, `issues/<self>`) when `_normalize_repo_key(repo) == _normalize_repo_key(self_repo_key)` (while preserving real `#issuecomment-...` / review / heading fragments, `/pull/<n>` URLs, and cross-repository `/issues/<self>` URLs), and exclude bare self-issue URLs from both `_inspect_blocker_links` and `_extract_verified_evidence_refs`.
* `FR-05` (`RV-005`, `PC-003`): In `_validate_section`, emit `unverified-blocker-pause` unconditionally whenever `has_unverified_phrase or has_uncited_non_capacity_wait` holds (even when `first_table_end is None`), define `has_blocker_or_wait_claim = is_waiting_or_pause or bool(cited_blocker_refs) or has_uncited_non_capacity_wait or has_unverified_phrase` to gate `missing-classification-table`, `summary-before-classification-table`, `unsupported-idle-unclassified`, and `unsupported-waiting-ready-work`, and include `\bblocked\s+(?:on|by)\b` alongside `WAITING_ON_FOR_RE` before `HOLD_CONTINUATION_RE` in `_has_global_wait_or_pause`.
* `FR-06` (`RV-006`): Pass `require_active_rows_covered=True` to `_verify_sessions_against_table` whenever `listed_session_tokens` is non-empty so mixed declared session lists (e.g. `rpi-1302, maintenance`) still require every `active session` issue row `#N` to match an active `rpi-<N>` or custom `(?<!\d)N(?!\d)` session token, while preserving zero-`active session`-row validity when only non-issue sessions run.
* `FR-07` (Test Ownership Lock): Preserve all `11` existing `def test_*` methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods; add `self.subTest` cases inside existing methods covering `RV-001`..`RV-006`).

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, strict `O(N)` worst-case time complexity (`< 0.25s` on 2,000+ repeated single-subclause launch phrases), passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` string literals in `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, comments, docstrings, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-006` regression subtests pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and exit code `0` across Focused validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Single-Subclause O(N) Hold Indexing, Per-Trigger Wait Spans, Strict Capacity Anchors, Bare Self-URL Rejection, Tableless Blocker Guard, and Mixed Session Matching

* Intent: Resolve `RV-001`..`RV-006` in `tools/check-coordinator-handoff.py` and add focused `self.subTest` regression coverage in `tools/test_check_coordinator_handoff.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `RV-001`..`RV-006` Fixes in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-06`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md
* Expected result: `RV-001`..`RV-006` resolved in `tools/check-coordinator-handoff.py` with `0` violations on `.agent.md` and `0` regressions on existing unit tests.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `RV-001`..`RV-006` Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-07`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv6-fixes-review.md
* Expected result: All `11` test methods and all Focused checks exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv7-fixes-plan-critique.md (Verdict: `Revise`, `0` Critical, `2` High, `2` Medium, `0` Low; user response required: `no`):

* `PC-001` [High] (`direct_planner_correction`, applied): Aligned `self_repo_key` comparison with `_normalize_repo_key(DEFAULT_LOCAL_REPO) == ""`, allowed slashless or `./` relative `issues/<self>` targets in `BARE_GITHUB_ISSUE_URL_RE`, and rejected trivial `#<self>` fragments while preserving `#issuecomment-...` and cross-repository `/issues/<self>` URLs.
* `PC-002` [High] (`direct_planner_correction`, applied): Anchored `SESSION_CAPACITY_WAIT_SPAN_RE` and `PR_DRAIN_WAIT_SPAN_RE` to the post-trigger head `text[tm.end():end_pos]`, rejected coordinating/causal extra-blocker tails (`and|or|plus|because|due to`), and narrowed `check` in `NON_CAPACITY_BLOCKER_WORD_RE` to plural `checks` or `(?:ci|pr|hosted|status|required|merge)\s+check`.
* `PC-003` [Medium] (`direct_planner_correction`, applied): Gated `unsupported-waiting-ready-work` on `has_blocker_or_wait_claim` and included `\bblocked\s+(?:on|by)\b` before `HOLD_CONTINUATION_RE` in `_has_global_wait_or_pause`.
* `PC-004` [Medium] (`direct_planner_correction`, applied): Used integer sentinel `-1` with explicit `si not in min_hold_end_by_subclause` membership checks and scanned `idx.span_masked_text` so hold-free multi-launch subclauses never cache-miss and backticked session tokens never match hold words.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
