<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-007 Quoted Prohibition Attribute Fix, Linear Bridge/Session Indexing, Causal Blocker Verification, Bare Pause Enforcement, Comma Timing Lookahead, and Contiguous Lifecycle Chains (Issue #1204 Child Loop 9)

## Metadata

* Task ID: issue-1204-rv9-fixes
* Task slug: delivery-1204-coordinator-guard-rv9-fixes
* Parent task ID: issue-1204-rv8-fixes (`delivery-1204-coordinator-guard-rv8-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md) routed seven findings: `RV-001` (`_fallback_prohibition_check` calls integer `pm.end` as `pm.end()`, raising `TypeError` on multi-token quoted prohibition prose such as `Never say "we are waiting on PR #1641".`), `RV-002` (`TRAILING_NEXT_TRIGGER_BRIDGE_RE` backtracks quadratically over whitespace between triggers), `RV-003` (custom non-RPI session token matching scans quadratically across active rows and custom sessions), `RV-004` (causal blocker clauses after `because`/`due to`/`owing to`/`pending`/`awaiting` piggyback on a cited PR without independent verification), `RV-005` (`Status: paused.` / `paused summary` / `all lanes paused` / `check paused` bypass `WAITING_OR_PAUSE_RE` and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`), `RV-006` (comma-prefixed `, until the next check` backtracks `\s*` in `COORDINATED_WAIT_SPLIT_RE` and false-splits), and `RV-007` (contiguous 3+ item lifecycle chains such as `PR #1641 and its hosted CI and status checks` reject beyond distance 1). Preserving all closed review and critique logs immutable, this single-phase plan resolves `RV-001`..`RV-007` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md: Routed findings `RV-001`..`RV-007`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation tier.
* tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria across `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `tools/check-coordinator-handoff.py`, and `tools/test_check_coordinator_handoff.py` (`unittest`).
* Run Focused validation only (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Leave all closed critique and review artifacts untouched; commit locally on `fix/delivery-1204-coordinator-guard` without pushing or opening a PR.

## Goals

* Fix `_fallback_prohibition_check` integer `pm.end` slice indexing (`RV-001`).
* Replace regex backtracking in multi-trigger bridge trimming and per-pair regex scanning in custom session coverage with linear `O(N)` / `O(S + M)` indexing (`RV-002`, `RV-003`).
* Split and verify causal blocker subclauses (`because`, `because of`, `due to`, `owing to`, and non-timing `pending`/`awaiting`) while preventing comma-whitespace backtracking on valid `, until the next check` tails and propagating contiguous lifecycle chains (`RV-004`, `RV-006`, `RV-007`).
* Enforce classification-table presence and blocker citation on bare pause headers and summaries (`Status: paused.`, `Paused summary`, `All lanes paused`, `Scheduled check paused`) (`RV-005`).
* Add regression `self.subTest` cases inside the existing `11` test methods in `tools/test_check_coordinator_handoff.py`.

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and dated `2026-11-15` `rv9-fixes` RPI artifacts.
* Non-goals: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` (already conformant), running or editing `tools/rpi-checks.py`, editing closed review/critique artifacts, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-002`): Fix `pm.end` integer slice indexing in `_fallback_prohibition_check`, mask interior characters of closed `INLINE_LITERAL_SPAN_RE` spans (`clause_split_masked`) during `_build_clause_index` so colons/semicolons/periods inside quoted prohibition examples do not split outer clauses, evaluate outer prohibitions at `lit_s` via the indexed token fast path when `match_start` lies inside a quoted literal `[lit_s, lit_e)`, and evaluate inner prohibitions (`pm.inside_literal_end == lit_e`) only when `CLAUSE_SPLIT_RE.search(clause_raw, pm.end, rel_pos) is None`.
* `FR-02` (`RV-002`, `PC-001`): Remove `TRAILING_NEXT_TRIGGER_BRIDGE_RE` and implement a deterministic `O(tail_len)` backward string scan `_strip_trailing_trigger_bridge(span_masked: str, start: int, end: int) -> int` that trims trailing whitespace, strips a trailing coordinating or causal connector (`and`, `or`, `also`, `plus`, `as well as`, `because`, `because of`, `due to`, `owing to`) when preceded by whitespace or comma, or strips a trailing comma, with zero regex backtracking; include the same causal connectors in `INTRO_PREFIX_BETWEEN_RE`.
* `FR-03` (`RV-003`): Pre-extract integer tokens once from `custom_non_rpi_tokens` via `STANDALONE_ISSUE_NUM_RE = re.compile(r"(?<!\d)(\d+)(?!\d)")` into `custom_session_issue_nums: set[int]` (`O(S)`) before iterating `active_session_rows`, replacing the inner `any(re.search(...))` loop with `if row_num in custom_session_issue_nums: continue`.
* `FR-04` (`RV-004`, `RV-006`, `RV-007`, `PC-001`): Update `COORDINATED_WAIT_SPLIT_RE` so the negative lookahead sits immediately after `,` with explicit optional post-comma coordinating/causal/non-timing-`pending` consumption, require non-comma connector branches to be bounded by non-whitespace (`(?<=\S)[ \t]+...(?=[ \t]+\S)`), and guard non-timing `pending|awaiting` with copular/aspectual negative lookbehinds (`(?<!\bis)(?<!\bare)(?<!\bwas)(?<!\bwere)(?<!\bbe)(?<!\bbeen)(?<!\bstill)(?<!\bremain)(?<!\bremains)`) so predicative `"#1288#issuecomment-10 is pending"` and `"its checks are pending"` never split into trailing empty segments. Allow optional leading `(?:of\s+)?` and bounded lifecycle predicate tails (`is running`, `are pending`, `to pass`) in `SHARED_REF_LIFECYCLE_SEG_RE`, and propagate citation adjacency across contiguous runs of `SHARED_REF_LIFECYCLE_SEG_RE` segments via two linear sweeps (left-to-right and right-to-left).
* `FR-05` (`RV-005`, `PC-001`): Extend `CLAUSE_SPLIT_RE`, `WAITING_OR_PAUSE_RE`, `DIRECT_GLOBAL_WAIT_RE`, and `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE` (using `paus(?:ed|ing|e)\b` ordering and optional `on|for|until|due to|because(?: of)?|owing to` introducer tails) to recognize `status:\s*paus(?:ed|ing|e)\b`, `paused\s+summary\b`, `all\s+lanes\s+paused\b`, and `(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+(?:is\s+)?paus(?:ed|ing)\b`.
* `FR-06` (`PC-002`, `PC-003`, Test Ownership Lock): Preserve all `11` existing `def test_*` methods in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new `def test_*` methods) and add `self.subTest` cases inside existing methods covering all `RV-001`..`RV-007` and `PC-001`..`PC-003` positive, negative, non-coincidental quoted-prohibition, and scaling scenarios.

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, strict `O(N)` worst-case runtime across whitespace-padded multi-trigger spans and large active-session tables (`< 0.25s`), clean `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` string literals in `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, comments, docstrings, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-007` checks pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and exit code `0` across Focused validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Quoted Prohibition Fix, Linear Bridge and Session Indexing, Causal/Pause Blocker Guards, and Subtest Coverage

* Intent: Resolve `RV-001`..`RV-007` across `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `RV-001`..`RV-007` Fixes in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-05`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md
* Expected result: Quoted prohibition prose evaluates without error, whitespace bridge trimming and custom session matching scale linearly, causal blockers and bare pause headers are enforced, comma timing tails do not false-split, and contiguous lifecycle chains pass.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `RV-001`..`RV-007` Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-06`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv8-fixes-review.md
* Expected result: All `11` test methods and all Focused checks exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv9-fixes-plan-critique.md (Verdict: `Revise`, `0` Critical, `2` High, `0` Medium, `1` Low; user response required: `no`):

* `PC-001` [High] (`direct_planner_correction`, applied): Bounded non-comma `COORDINATED_WAIT_SPLIT_RE` splits by non-whitespace (`(?<=\S)[ \t]+...(?=[ \t]+\S)`), added copular/aspectual negative lookbehinds before `pending|awaiting` (`is/are/was/were/be/been/still/remain/remains`) plus post-comma non-timing `pending|awaiting` consumption, ordered `paus(?:ed|ing|e)\b` with optional `on|for|until|due to|because(?: of)?|owing to` introducer tails in `WAIT_OR_BLOCKER_SPAN_TRIGGER_RE`, and added causal connectors (`because`, `because of`, `due to`, `owing to`) to `_strip_trailing_trigger_bridge` and `INTRO_PREFIX_BETWEEN_RE`.
* `PC-002` [High] (`direct_planner_correction`, applied): Masked interior characters of closed `INLINE_LITERAL_SPAN_RE` spans during `_build_clause_index` clause/sentence splitting, evaluated outer prohibitions at `lit_s` via the indexed token path while restricting `_fallback_prohibition_check` on literal interiors to inner prohibitions without intervening `CLAUSE_SPLIT_RE` boundaries, and upgraded `P01-T02` quoted-prohibition subtests to test uncited/ready-work targets plus negative controls.
* `PC-003` [Low] (`direct_planner_correction`, applied): Aligned `P01-T02` `RV-004` positive subtest anchor `#1288#issuecomment-10` with `_valid_handoff_markdown` and added companion subtests for `, pending #1288#issuecomment-10`, `and its checks are pending`, `because blocked on #1288#issuecomment-10`, and `Status: paused due to PR #1641.`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
