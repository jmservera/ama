<!-- markdownlint-disable-file -->
# Implementation Plan: Resolve RV-001 through RV-004 Constant-Time Suffix Guard, Deferred/Negated Launch Qualification, and URL-Safe Blocker Spans (Issue #1204 Child Loop 4)

## Metadata

* Task ID: issue-1204-rv4-fixes
* Task slug: delivery-1204-coordinator-guard-rv4-fixes
* Parent task ID: issue-1204-rv3-fixes (`delivery-1204-coordinator-guard-rv3-fixes`)
* Research: .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md (`satisfied-and-skipped`)
* Routed review source: .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan-critique.md
* Downstream changes path: .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-changes.md
* Planning execution status: complete
* Planning status: complete

## Executive Summary

Parent review (.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md) confirmed closure of the `idle or ` ReDoS (`PC-001`) and possessive single-quote non-bridging (`PC-004`), and routed four narrow validator findings in `tools/check-coordinator-handoff.py`: `RV-001` (quadratic whitespace scanning in `CONDITIONAL_GUARD_SUFFIX_RE` and `\s+--\s+` on 4,000–8,000 spaces), `RV-002` (deferred future-tick/modal launches such as `"Starting #1310 next tick"` or `"Will be starting #1310"` and adverb-separated negations such as `"Not actually starting #1310"` suppressing `unsupported-waiting-ready-work`), `RV-003` (`BLOCKER_SPAN_STOP_RE` stopping at `https:` before URL masking and missing unlisted full-URL blockers such as `https://.../pull/999`), and `RV-004` (`BLOCKER_SPAN_STOP_RE` and `READY_LAUNCH_RE` handling of coordinated subject-verb launch clauses such as `", and #1310 is starting now"`). Preserving all prior review logs immutable, this single-phase plan resolves `RV-001`..`RV-004` and single-pass critique refinements `PC-001`..`PC-003` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` under Focused validation.

## Sources and Evidence

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md: Routed findings `RV-001`..`RV-004`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Issue #1204 acceptance criteria 1–4 and Focused validation boundaries.
* .github/agents/ama-backlog-delivery-coordinator.agent.md: Live coordinator instructions (`sha256: cbe27e1616b101a313482ec2fc3cdd72977e68309497b53e9223aaab8a96457b`).
* tools/check-coordinator-handoff.py and tools/test_check_coordinator_handoff.py.

## User Decisions and Requirements

* Prove all four Issue #1204 acceptance criteria:
  1. Update delivery coordinator instructions so scheduled checks cannot claim `"nothing changed"` or pause on an unverified blocker while open issues remain unclassified in the current run.
  2. Require an explicit five-category issue-state classification table (`merged`, `active session`, `human-blocked` with link, `dependency-blocked` with link, `ready to start`) before any idle or waiting summary.
  3. Require handoff and checkpoint notes to refresh open-issue counts, open-PR counts, and active session status from live commands at the time of writing.
  4. Provide `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py` (`unittest`) enforcing all of the above and flagging stale count/SHA handoff blocks.
* Use Focused validation only (`python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check`); do NOT run `tools/rpi-checks.py`.
* Keep earlier review and critique files immutable; commit locally without pushing or opening a PR.

## Goals

* Replace regex-based conditional suffix scanning with constant-time tail word-token slicing (`O(1)` on tail after `rstrip`).
* Reject deferred future-tick/modal launches and adverb-separated negations inside `_launches_ready_issue_in_current_tick`.
* Mask URLs and inline code spans before `BLOCKER_SPAN_STOP_RE` scanning and stop blocker extraction at coordinated subject-verb launch clauses.

## Scope and Non-Goals

* In scope: `tools/check-coordinator-handoff.py`, `tools/test_check_coordinator_handoff.py`, and child-loop-4 `.copilot-tracking/` RPI artifacts.
* Non-goals: Modifying `.github/agents/ama-backlog-delivery-coordinator.agent.md` (already conformant), mutating prior review logs, running `tools/rpi-checks.py`, or pushing/opening a PR.

## Functional Requirements

* `FR-01` (`RV-001`, `PC-001`): Replace `\s+--\s+` with `(?<=\s)--\s+` in `CLAUSE_SPLIT_RE` and `BLOCKER_SPAN_STOP_RE`, delete `CONDITIONAL_GUARD_SUFFIX_RE`, and implement `_has_conditional_guard_suffix(trailing_clause: str) -> bool` via pure Python `trailing_clause.rstrip(" \t\"'`").rsplit(None, 8)` whitespace-token slicing (preserving `#<n>` and numeric tokens rather than stripping non-letters), popping up to 4 exact `TRAILING_PREP_DET_TOKENS` tokens and checking `(len(tokens) >= 2 and tokens[-2].lstrip("\"'`([") == "only" and tokens[-1] == "after") or (len(tokens) >= 3 and tokens[-3].lstrip("\"'`([") == "permitted" and tokens[-2:] == ["only", "when"])` in linear time.
* `FR-02` (`RV-002`, `PC-003`): Update `_launches_ready_issue_in_current_tick` to:
  * Split subclauses on `SUBCLAUSE_SPLIT_RE = re.compile(r"\bwhile\b|,\s+and\b", re.IGNORECASE)` and recognize both verb-first (`starting #1310`) and subject-first (`#1310 is starting`) active `-ed`/`-ing` launch forms in `READY_LAUNCH_RE`.
  * Check unanchored `LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE` anywhere in `prefix = line[sub_start : m.start()]`, rejecting `not`, `*n't`, `no`, `never`, `without`, `before`, `until`, `instead of`, `prior to`, `unless`, `if`, `unable to`, `fail(ed|ing|s)? to`, `defer*`, `postpon*`, `skip*`, `(?:hold(?:ing)?|held) off(?:\s+on)?`, and irrealis/deferred auxiliaries (`will`, `would`, `could`, `should`, `might`, `may`, `(?:plan(?:ning|ned|s)?|intend(?:ing|ed|s)?)\s+(?:to|on)`, `going to`).
  * Expand `NON_CURRENT_LAUNCH_SUBCLAUSE_RE` across `line[sub_start:sub_end]` to reject future/deferred qualifiers (`later`, `tomorrow`, `eventually`, `soon`, and `(?:next|future|following|subsequent|upcoming)\s+(?:tick|check|run|turn|wave|slot|window|cycle|pass)`) in addition to historical qualifiers.
* `FR-03` (`RV-003`, `RV-004`, `PC-002`): Update `_extract_cited_blocker_numbers` to:
  * Slice `span = line[tm.end() : tm.end() + 300]`, mask `BACKTICK_TOKEN_RE` to `_` and mask `URL_RE` while preserving trailing `.;!?:,` punctuation (`core = m.group(0).rstrip(".;!?:,")`, `"_" * len(core) + m.group(0)[len(core):]`), and run `BLOCKER_SPAN_STOP_RE.search(masked_span)` so `https://.../pull/999 before continuing` is not truncated at `https:` while `https://.../pull/1641; #1310 is starting` still stops at `;`.
  * Extend `BLOCKER_SPAN_STOP_RE` with a constrained coordinated subject-verb launch stop `,\s+and\s+(?:(?:now|meanwhile|concurrently)\s+)?(?:(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b|(?:we|coordinator|delivery|independent\s+(?:lanes?|work|issues?)|(?:(?:issue|worker|session)\s+)?(?:#\d+|_+|rpi-\d+(?:-[A-Za-z0-9_.-]+)?))\s+(?:(?:is|are|has|have)\s+(?:now\s+)?)?(?:launch(?:ed|ing|es)|start(?:ed|ing|s)|dispatch(?:ed|ing|es)|spawn(?:ed|ing|s)|running|continu(?:e|es|ed|ing)|proceed(?:s|ed|ing))\b)` (excluding bare noun `run` and `before/until/to` bridges).
* `FR-04`: Lock test ownership in `tools/test_check_coordinator_handoff.py` (`0` removals, `0` new test methods keeping `11` methods total; add `self.subTest` cases inside existing methods) covering:
  * `< 0.1s` execution on both `(" " * 8000) + "nothing changed."` and `"only after" + (" " * 8000) + "x nothing changed."`, plus rejection of `"Only after #1204 nothing changed."` (`RV-001`, `PC-001`).
  * Rejection of `"Starting #1310 next tick; waiting on PR #1641."`, `"Not actually starting #1310; waiting on PR #1641."`, `"Will be starting #1310; waiting on PR #1641."`, `"Will start #1310; waiting on PR #1641."`, `"Planning on starting #1310; waiting on PR #1641."`, and `"Held off starting #1310; waiting on PR #1641."`, plus below-capacity acceptance of `"Waiting on PR #1641 without force-pushing, and starting #1310 now."` and `"Waiting on PR #1641, and #1310 is starting now."` (`RV-002`, `PC-003`).
  * Rejection of `"Waiting on https://github.com/jmservera/ama/pull/999 before continuing."`, `"Waiting on PR #1641, and #999 before continuing."`, and `"Waiting on PR #1641, and PR #999 check run."` (`unverified-blocker-reference`, `RV-003`, `PC-002`).
  * Acceptance of `"Waiting on PR #1641, and #1310 is starting now."` and `"Waiting on https://github.com/jmservera/ama/pull/1641; #1310 is starting now."` during PR drain (`18 (draining until <= 15)`) without misclassifying `#1310` as an unverified blocker (`RV-004`, `PC-002`).

## Non-Functional Requirements

* `NFR-01`: Stdlib-only Python 3.12+, linear `O(N)` worst-case line scanning, passing `ruff check` and `ruff format --isolated --line-length 100 --check`.
* `NFR-02`: Zero `.copilot-tracking/` path literals in code, tests, docstrings, comments, or commit messages.

## Acceptance Criteria

* All four Issue #1204 acceptance criteria and all `RV-001`..`RV-004` regression subtests pass with `0` violations on `.github/agents/ama-backlog-delivery-coordinator.agent.md` and Focused validation exit code `0`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Constant-Time Conditional Suffix, Subclause Launch Qualification, URL-Safe Blocker Spans, and Subtests

* Intent: Resolve `RV-001`..`RV-004` in `tools/check-coordinator-handoff.py` and `tools/test_check_coordinator_handoff.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update `tools/check-coordinator-handoff.py` for `RV-001` through `RV-004`

* Requirement and evidence: `FR-01`..`FR-03`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md
* Expected result: Constant-time conditional suffix slicing, subclause-wide negation/deferred launch rejection, and URL-masked coordinated-stop blocker extraction implemented cleanly.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add Regression Subtests in `tools/test_check_coordinator_handoff.py` and Run Focused Validation

* Requirement and evidence: `FR-04`; .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-rv3-fixes-review.md
* Expected result: All `RV-001`..`RV-004` regression subtests pass (`11` test methods total) and Focused validation exits `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01`.

## Critique Disposition

Single-pass critique (.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv4-fixes-plan-critique.md) completed with verdict `Revise` (`0` Critical, `2` High, `1` Medium, `0` Low; no user decision required):

* `PC-001` [High] (`Applied directly`): Replaced `\s+--\s+` with `(?<=\s)--\s+` in `CLAUSE_SPLIT_RE` and `BLOCKER_SPAN_STOP_RE`, switched `_has_conditional_guard_suffix` to `rsplit(None, 8)` whitespace tokenization so `#<n>` and numeric tokens are preserved rather than stripped, and added both 8,000-space and `"Only after #1204 nothing changed."` subtests in `FR-01`, `FR-04`, `P01-T01`, and `P01-T02`.
* `PC-002` [High] (`Applied directly`): Preserved trailing `.;!?:,` punctuation when masking `URL_RE` in `_extract_cited_blocker_numbers` and constrained the `, and` stop branch in `BLOCKER_SPAN_STOP_RE` to coordinated subject-verb launch clauses (excluding bare noun `run` and `before/until/to` bridges), adding regression subtests in `FR-03`, `FR-04`, `P01-T01`, and `P01-T02`.
* `PC-003` [Medium] (`Applied directly`): Updated `_launches_ready_issue_in_current_tick` to split subclauses on `\bwhile\b|,\s+and\b`, recognize subject-first `#<n> is/has starting/started`, cover `(?:hold(?:ing)?|held)\s+off(?:\s+on)?` and `(?:plan...|intend...)\s+(?:to|on)`, and test non-vacuous `-ing` modal/deferred forms (`"Will be starting #1310..."`) plus below-capacity `, and` concurrent launches in `FR-02`, `FR-04`, `P01-T01`, and `P01-T02`.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static validation in a dedicated gate-tooling PR validated under the full gate tier (`#1294`).
