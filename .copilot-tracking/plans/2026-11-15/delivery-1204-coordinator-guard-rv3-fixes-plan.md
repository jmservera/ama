<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-003 Linear-Time Negation, Ready-Row Launch Guard, and Qualified Blocker Citations (Issue #1204 Child Loop 3)

## Metadata

* Task ID: issue-1204-rv3-fixes
* Task slug: delivery-1204-coordinator-guard-rv3-fixes
* Parent task ID: issue-1204-rv2-fixes (`delivery-1204-coordinator-guard-rv2-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md) confirmed artifact reconciliation and `.agent.md` conformance, and routed three High-severity findings in `tools/check-coordinator-handoff.py`: `RV-001` (ambiguous nested regex repetition in `_PROHIBITION_BODY` causing exponential backtracking on repeated `idle or`), `RV-002` (historical or non-ready launch mentions such as `"Previously launched rpi-1204; waiting on PR #1642"` suppressing `unsupported-waiting-ready-work` when `ready to start` rows remain unstarted), and `RV-003` (intermediate qualifiers such as `"waiting for hosted CI on PR #999"` or `"waiting on parent PR #999"` bypassing `CITED_BLOCKER_REF_RE`). Keeping all prior review logs immutable, this single-phase plan replaces nested regex quantifiers with linear-time `O(N)` suffix parsing, scopes concurrent launch exceptions to non-historical launches of `ready_rows` issue numbers, extracts `#<n>` blocker citations across bounded wait/pause/blocked object spans, and adds regression subtests under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md: Routed findings `RV-001`, `RV-002`, and `RV-003` (all High).
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria and Focused validation scope.
* tools/check-coordinator-handoff.py: `_is_claim_negated`, `_has_unnegated_concurrent_launch`, and `_validate_section`.
* tools/test_check_coordinator_handoff.py: Focused `unittest` suite (`11` test methods).

## User Decisions and Requirements

* Satisfy all four Issue #1204 acceptance criteria on branch `fix/delivery-1204-coordinator-guard` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Use Focused validation only (`python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Keep earlier review and critique files immutable; commit locally without pushing or opening a PR.

## Goals

* Eliminate exponential regex backtracking in negation checking (`O(N)` worst-case runtime per clause).
* Require current-tick, non-historical launch of at least one `ready_rows` issue before permitting a lane-specific `waiting on/for` clause alongside open capacity and `ready to start` rows.
* Extract all `#<n>` issue/PR citations inside governed `waiting on/for`, `blocked on/by`, and `pause/paused/pausing on/for/due to` object phrases, including qualified phrases (`hosted CI on PR #999`, `parent PR #999`).

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and child-loop-3 `.copilot-tracking/` RPI artifacts.
* Non-goals: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` (already conformant at `sha256: cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`), mutating prior review logs, running `tools/rpi-checks.py`, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-004`): Replace `_PROHIBITION_BODY` / `PROHIBITION_SUFFIX_RE` / `HANDOFF_NEGATION_SUFFIX_RE` nested regex quantifiers with a linear-time `O(N)` token scanner `_trailing_clause_has_governing_prohibition(trailing_clause: str, *, allow_conditional_guards: bool) -> bool` that masks inline literals with word-boundary-guarded single quotes (`\"[^\"\n]*\"|(?<![A-Za-z0-9])'[^'\n]*'(?![A-Za-z0-9])|`[^`\n]*``), inspects at most the last 4 prohibition heads, rejects `and`/ungoverned verbs/unrelated nouns, and validates governed verbs + finite continuation tokens in `O(N)` time.
* `FR-02` (`RV-002`, `PC-002`): Replace `_has_unnegated_concurrent_launch(line)` with `_launches_ready_issue_in_current_tick(line: str, ready_issue_nums: set[int]) -> bool`, scanning the full enclosing launch subclause to reject both pre-verb and post-object historical qualifiers (`previously`, `earlier`, `already`, `yesterday`, `formerly`, and `(?<!since\s)(?<!since\sthe\s)\b(?:last|prior|previous)\s+(?:tick|check|run|turn|wave)\b`), hold prepositions (`before`, `until`, `without`, `instead of`, `prior to`), participle negations (`not`, `*n't`), and launches whose `#<n>` or `rpi-<n>` number is not in `ready_issue_nums`.
* `FR-03` (`RV-003`, `PC-003`): Replace single-token `CITED_BLOCKER_REF_RE` with `_extract_cited_blocker_numbers(line: str) -> list[int]` using flat `BLOCKER_TRIGGER_RE` (`paus(?:e|ed|ing)\s+(?:(?:the\s+)?(?:run|schedule|delivery|check|tick)\s+)?(?:on|for|due\s+to)|blocked\s+(?:on|by)|waiting\s+(?:on|for)`) and `BLOCKER_SPAN_STOP_RE` (`[.;!?:]`, `\s+--\s+`, `,\s+(?:so|but|yet|then|while|whereas)\b`, `\bwhile\b`, `(?:before|until|instead\s+of|then|to|and(?:\s+now)?)\s+(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)`, and negation heads), extracting both GitHub `/issues/` or `/pull/` URL numbers and prose `#<n>` numbers.
* `FR-04` (`PC-001`, `PC-002`): Lock test ownership in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new test methods keeping `11` methods total, adding `self.subTest` cases inside existing methods) covering:
  * Bounded `< 0.5s` runtime on both `"Never claim " + ("idle or " * 80) + "and nothing changed."` (failing-suffix ReDoS path asserting `unsupported-idle-ready-work`) and `"Never claim " + ("idle or " * 80) + "nothing changed."` (`RV-001`, `PC-001`).
  * Rejection of `"Previously launched rpi-1204; waiting on PR #1641."`, `"Previously started #1310; waiting on PR #1641."`, `"Started #1310 last tick; waiting on PR #1641."`, `"Not starting #1310; waiting on PR #1641."`, and `"Launched rpi-1204; waiting on PR #1641."` when `#1310` is `ready to start` with spare capacity (`RV-002`, `PC-002`).
  * Rejection of `"Waiting for hosted CI on PR #999."` and `"Waiting on parent PR #999."` when `#999` is absent from verified table evidence (`RV-003`).

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, zero nested variable-length regex quantifiers, passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` path literals in code, tests, docstrings, comments, or commit messages.

## Acceptance Criteria

* Live `.github/agents/ama-backlog-delivery-coordinator.agent.md` passes `python3 tools/check-coordinator-handoff.py` with `0` violations.
* Pathological `idle or ` repetition completes in `< 0.5s` (`O(N)` linear time), historical/non-ready launches no longer mask `unsupported-waiting-ready-work`, and qualified unlisted PR citations (`waiting for hosted CI on PR #999`, `waiting on parent PR #999`) trigger `unverified-blocker-reference`.
* All Focused validation checks (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`) pass with exit code `0`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Linear-Time Prohibition Scanner, Ready-Row Launch Check, Qualified Blocker Extraction, and Subtests

* Intent: Resolve `RV-001`, `RV-002`, and `RV-003` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement Linear-Time Prohibition Scanner, Ready-Row Launch Guard, and Qualified Blocker Extraction in `tools/check-coordinator-handoff.py`

* Requirement and evidence: `FR-01`..`FR-03`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md
* Expected result: `O(N)` negation parsing, current-tick `ready_issue_nums` launch guard, and bounded blocker-span `#<n>` extraction implemented without regex backtracking.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add Performance and Behavioral Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-04`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv2-fixes-review.md
* Expected result: All `RV-001`..`RV-003` regression subtests pass (`11` test methods total) and Focused validation exits `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-plan-critique.md (`Verdict: Revise`; `0` Critical, `3` High, `1` Medium, `0` Low; `User response required: no`). Applied all four planner-owned dispositions directly:

* `PC-001` (`High`): Added the failing-suffix ReDoS test case `"Never claim " + ("idle or " * 80) + "and nothing changed."` (`< 0.5s`, asserting `unsupported-idle-ready-work`) alongside the positive repetition test.
* `PC-002` (`High`): Extended `_launches_ready_issue_in_current_tick` to scan the full enclosing launch subclause for pre- and post-object historical qualifiers (excluding `since [the] last/prior/previous ...`) and reject participle `not`/`*n't` negations (`"Not starting #1310"`, `"Started #1310 last tick"`).
* `PC-003` (`High`): Pinned `BLOCKER_TRIGGER_RE` to flat `paus(?:e|ed|ing)\s+(?:(?:the\s+)?(?:run|schedule|delivery|check|tick)\s+)?(?:on|for|due\s+to)` and added `:`, `, so/but/yet/then/while/whereas`, `to launch/start/...`, and negation stop boundaries to `BLOCKER_SPAN_STOP_RE`.
* `PC-004` (`Medium`): Guarded single-quote literal masking with `(?<![A-Za-z0-9])'[^'\n]*'(?![A-Za-z0-9])` so paired English possessives cannot swallow intermediate `and`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
