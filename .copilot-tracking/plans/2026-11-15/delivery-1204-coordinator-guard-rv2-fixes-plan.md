<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve Validator Edge-Case Defects RV-001 through RV-003 (Issue #1204 Child Loop 2)

## Metadata

* Task ID: issue-1204-rv2-fixes
* Task slug: delivery-1204-coordinator-guard-rv2-fixes
* Parent task ID: issue-1204-rv-fixes (`delivery-1204-coordinator-guard-rv-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md) confirmed closure of `.github/agents/ama-backlog-delivery-coordinator.agent.md` requirements and earlier structural bypasses, and routed three remaining validator edge cases in `tools/check-coordinator-handoff.py` (`RV-001` coordinated-conjunction negation bypass, `RV-002` false positives on table-evidenced PR blocker numbers and concurrent active-launch lane waits, and `RV-003` Markdown-linked Issue column IDs plus regression tests). Keeping both prior review logs immutable, this single-phase plan updates `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` under Focused validation with zero changes needed to `.github/agents/ama-backlog-delivery-coordinator.agent.md`.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md: Routed findings `RV-001` (High), `RV-002` (Medium), and `RV-003` (Medium).
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria and Focused validation boundaries.
* tools/check-coordinator-handoff.py: `_is_claim_negated`, `_extract_classification_tables`, and `_validate_section`.
* tools/test_check_coordinator_handoff.py: Focused `unittest` suite (`11` test methods currently).

## User Decisions and Requirements

* Satisfy all four Issue #1204 acceptance criteria on branch `fix/delivery-1204-coordinator-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Use Focused validation (`python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`, `python3 -m ruff format --isolated --line-length 100 --check tools/check-coordinator-handoff.py tools/test_check_coordinator_handoff.py`); do not run `tools/rpi-checks.py`.
* Preserve all prior critique and review artifacts untouched (`Preserve original critique/Review outcomes`).
* Commit all changes and `.copilot-tracking/` RPI artifacts locally with the Copilot `Co-authored-by` trailer without pushing or opening a PR.

## Goals

* Bind negation guards directly to the governed claim at `match_start` so coordinated conjunctions (`"Never skip verification and nothing changed"`, `"Never skip verification and always claim nothing changed when issues are unclassified"`) never mask an unnegated claim (`RV-001`).
* Accept table-evidenced PR/blocker numbers (`Waiting on #1641` when a valid blocking row records `PR #1641` or `/pull/1641`) while still rejecting uncited or `ready to start`/`merged` issue citations, and distinguish concurrent active-launch lane-wait reports (`Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 next`) from global stall/waiting claims (`RV-002`).
* Parse Markdown-linked issue IDs (`[#1288](https://github.com/jmservera/ama/issues/1288)`) in the `Issue` column and add regression subtests in `tools/test_check_coordinator_handoff.py` (`RV-003`).

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and child-loop `.copilot-tracking/` RPI artifacts.
* Non-goals: Mutating prior review/critique artifacts, modifying `tools/rpi-checks.py`, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-001`): `_is_claim_negated` returns `True` only when the suffix of `trailing_clause` immediately preceding `match_start` matches an anchored prohibition-governance pattern (`PROHIBITION_SUFFIX_RE` for agent instructions and `HANDOFF_NEGATION_SUFFIX_RE` for handoff prose) covering literal masked `` `[^`]*` `` code spans, inflected claim/report/pause/wait/copy/rely verbs, coordinated list items, and optional trailing determiners/prepositions/opening quotes (`on`, `for`, `a`, `an`, `the`, `any`, `global`, `"`, `'`, `` ` ``) right before `match_start`, with no intervening affirmative override (`always`, `may`, `still`) or unrelated coordinated verb phrase (`skip verification and`). `check_agent_instructions` inspects every occurrence via `re.finditer` across each clause.
* `FR-02` (`RV-002`, `PC-002`): `_validate_section` indexes verified blocker reference numbers (`verified_blocker_evidence_nums`) from GitHub `/issues/<n>` and `/pull/<n>` URLs/link targets and URL/link-stripped prose `#<n>` references inside `non_issue_cells` of valid blocking rows (`active session`, or `human-blocked`/`dependency-blocked` with `has_valid_blocker_link=True`), preventing URL `#fragment` digits from leaking. `CITED_BLOCKER_REF_RE` includes optional `PR`/`pull request` qualifiers (`waiting on PR #1641`, `Waiting on #1641`); `classified_by_num` is checked first, and non-issue numbers succeed if and only if present in `verified_blocker_evidence_nums`.
* `FR-03` (`RV-002`, `PC-002`): `_validate_section` distinguishes unnegated `GLOBAL_WAIT_OR_PAUSE_RE` (`status: waiting`, `waiting summary`, `all lanes waiting`, `nothing ready to start`, `pause/paused/pausing ...`, `waiting ... before/until/prior to/instead of continuing/starting/launching/proceeding`) from lane-specific `\bwaiting\s+(?:on|for)\b` mentions. Both require the classification table ahead of the summary and zero unclassified open issues, while `unsupported-waiting-ready-work` fires on `GLOBAL_WAIT_OR_PAUSE_RE` unconditionally (below cap/drain) and on lane-specific `waiting on/for` unless the same line records an unnegated target-scoped concurrent launch (`CONCURRENT_LAUNCH_RE` requiring `#<n>` or `rpi-<n>` target so `"Check started at 12:00Z; waiting..."` never bypasses).
* `FR-04` (`RV-003`, `PC-003`): `_extract_classification_tables` parses single-issue cells in either bare `#?<num>` form (`^\s*#?(\d+)\s*$`) or full-cell Markdown link form (`^\s*\[([^\]]+)\]\(([^)\s]+)\)\s*$`), rejecting multi-issue cells, `javascript:`/`data:` targets, mismatched `/issues/<other>` URLs, and non-heading self/broken `#anchor` links.
* `FR-05` (`RV-003` & Locked Test Plan):
  * Test owner: `tools/test_check_coordinator_handoff.py` (`CoordinatorHandoffGuardTests`).
  * Removals: `none` (`0` tests removed).
  * Maximum additions: `0` new test methods (extend existing `test_agent_instruction_guard_rejects_missing_contracts`, `test_valid_active_and_multi_role_stacked_handoffs_pass`, `test_valid_waiting_and_idle_summaries_pass_when_all_open_issues_classified`, and `test_adversarial_rv001_handoff_bypasses_rejected` with focused `self.subTest` cases, keeping total test methods at `11`).
  * Canonical targets: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py` (no generated files; `.github/agents/ama-backlog-delivery-coordinator.agent.md` remains at SHA-256 `cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b` unless critique requires an edit).

## Non-Functional Requirements

* Python 3.12 stdlib only, deterministic offline execution (`< 1s`), clean `ruff check` and `ruff format --isolated --line-length 100 --check`, and zero `.copilot-tracking/` references in `tools/`.

## Acceptance Criteria

* Coordinated-conjunction negation bypasses (`"Never skip verification and nothing changed."` and `"Never skip verification and always claim nothing changed when issues are unclassified."`) fail closed in `check_handoff_text` and `check_agent_instructions`.
* Table-evidenced PR blocker citations (`Waiting on #1641 for parent PR merge` when `#1302 | dependency-blocked | PR #1641` is in the table), concurrent active-launch lane-wait lines (`Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 next`), and Markdown-linked Issue column cells (`[#1288](https://github.com/jmservera/ama/issues/1288)`) pass with `0` violations, while uncited blockers (`Waiting on #999`) and global waiting stalls (`Waiting for stakeholder feedback before starting #1310`) still fail closed.
* All Focused validation checks exit `0`, and plan, phase-details, and changes status fields are fully synchronized before Review.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Governed Negation Binding, Table-Evidenced PR Blockers, Concurrent Lane Waits, and Regression Subtests

* Intent: Resolve `RV-001`, `RV-002`, and `RV-003` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update `tools/check-coordinator-handoff.py` for `RV-001`, `RV-002`, and `RV-003`

* Requirement and evidence: `FR-01`..`FR-04`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md
* Expected result: Anchored negation governance, table-evidenced PR blocker verification, concurrent active-launch lane-wait differentiation, and Markdown-linked Issue cell parsing implemented cleanly.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-05`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-review.md
* Expected result: Regression subtests cover all `RV-001`..`RV-003` positive and negative cases (`11` test methods total) and all Focused validation commands exit `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-plan-critique.md (`Verdict: Revise`; `0` Critical, `1` High, `1` Medium, `1` Low; `User response required: no`). Applied all three planner-owned dispositions directly:

* `PC-001` (`High`): Modeled literal `` `[^`]*` `` code spans, inflected verbs, and optional trailing determiners/prepositions/quotes before `match_start` in `PROHIBITION_SUFFIX_RE` / `HANDOFF_NEGATION_SUFFIX_RE`, and scanned all occurrences per clause via `re.finditer` in `check_agent_instructions`.
* `PC-002` (`Medium`): Scoped `CONCURRENT_LAUNCH_RE` to explicit `#<n>` or `rpi-<n>` delivery targets, guarded `GLOBAL_WAIT_OR_PAUSE_RE` with `_is_claim_negated` plus `before`/`until`/`prior to`/`instead of` forms, added `PR #<n>` support to `CITED_BLOCKER_REF_RE`, and stripped URLs/link targets before `ISSUE_REF_RE` when building `verified_blocker_evidence_nums`.
* `PC-003` (`Low`): Enforced full-cell single-issue matching (`#?<num>` or `[#?<num>](target)`) in `_parse_issue_cell`, rejecting multi-issue cells, `javascript:`/`data:` schemes, mismatched `/issues/<other>` URLs, and invalid `#anchor` targets.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
