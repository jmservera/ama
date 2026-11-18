<!-- markdownlint-disable-file -->
# RPI Plan: Resolve Coordinator Handoff Guard Review Defects RV-001 through RV-003 (Issue #1204 Child Loop)

## Task Metadata

* Task ID: issue-1204-rv-fixes
* Task slug: delivery-1204-coordinator-guard-rv-fixes
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan-critique.md

## Executive Summary

Parent review `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` identified three bounded hardening defects (`RV-001` High, `RV-002` Medium, `RV-003` Medium) before local commit on `fix/delivery-1204-coordinator-guard`. This child plan closes every reproduced bypass across `tools/check-coordinator-handoff.py` (`check_handoff_text`, `_validate_section`, `_has_non_bare_self_link`, `check_agent_instructions`) and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (including PR-filtered `gh api --paginate` saturation handling and write-time `--expect-*`/`--open-issues` flags), locks adversarial regression subtests in `tools/test_check_coordinator_handoff.py`, refreshes the SHA-256-anchored HVE assessment while retaining parent SHA-256 lineage, and preserves the original parent review log untouched.

### User Decisions and Requirements Highlights

* Resolve routed findings `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` while keeping the original parent review artifact unmodified (`Preserve original critique/Review outcomes`).
* Keep Focused validation (`python3 -m unittest tools/test_check_coordinator_handoff.py -q`, `python3 -m ruff check`, `python3 -m ruff format --isolated --line-length 100 --check`), do not run `tools/rpi-checks.py`, and do not push or open a PR.

### What You May Not Know

* Clause-scoping negation (`_is_claim_negated(line, match.start())`) prevents trailing instructions such as `"Nothing changed; do not launch anything"` from masking an unguarded leading `"Nothing changed"` claim while still honoring prohibition rules like `"Never claim 'nothing changed'"`.
* Evaluating classification completeness per summary line using only classification tables that end before that summary line (`tbl.end_line < lineno`, plus flagging any classification table placed after the summary line) closes split-table ordering bypasses.

### Unresolved Decisions or Blockers

* None

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Preserve all four Issue #1204 acceptance criteria (`AC1` through `AC4`), Focused validation tier, no `tools/rpi-checks.py` execution, and clean local frozen `HEAD` commit on `fix/delivery-1204-coordinator-guard` without push/PR (caller prompt, 2026-11-15).
* Close `RV-001`, `RV-002`, and `RV-003` routed to `rpi-implement` from `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` without modifying parent review/critique logs.

## Goals

* Eliminate clause-unscoped negation, `"Waiting for ..."` phrasing gaps, post-summary split classification tables, absent cited-blocker (`ref_row is None`) gaps, and broken local `#anchor` blocker links in `tools/check-coordinator-handoff.py` (`RV-001`).
* Enforce prohibition polarity in `check_agent_text` and add write-time `--expect-*`/`--open-issues` validator flags plus saturated-limit (`--limit 500` / `--limit 200`) full pagination rules in `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`RV-002`).
* Lock deterministic adversarial unit tests in `tools/test_check_coordinator_handoff.py` and refresh `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` (`RV-003`).

## Scope and Non-Goals

### In Scope

* `tools/check-coordinator-handoff.py` (`RV-001`, `RV-002`)
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`RV-002`)
* `tools/test_check_coordinator_handoff.py` and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` (`RV-003`)

### Non-Goals

* Modifying `.copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md` or `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-plan-critique.md`
* Modifying or running `tools/rpi-checks.py`
* Pushing to `origin` or opening/modifying a pull request

## Functional Requirements

* Clause-scoped negation and expanded waiting/pause/stale-carry detection (`RV-001`, `PC-002`):
  * Observable acceptance criteria: `_validate_section` treats an `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, `STALE_CARRY_RE`, or `CITED_BLOCKER_REF_RE` match as negated only when a prohibition/guard token precedes that match within the same clause (splitting `line[:match_start]` at `[;.!?:]` or whitespace-bounded `\s+--\s+` so CLI flags like `--state` are never split and no cross-clause prefix override masks `"Do not launch: nothing changed"`), and matches both `"waiting on ..."` and `"waiting for ..."`.
* Pre-summary table completeness, standalone/absent cited-blocker rejection, and local `#anchor` verification (`RV-001`, `PC-002`):
  * Observable acceptance criteria: `_validate_section` flags `summary-before-classification-table` if any issue-state classification table ends after a summary line (`tbl.end_line > lineno`); runs unnegated `CITED_BLOCKER_REF_RE` checks even on standalone `blocked on #N` lines without requiring `is_idle`/`is_waiting_or_pause`, flagging `unverified-blocker-reference` unless `ref_row` exists with state in `{"active session", "human-blocked", "dependency-blocked"}` (and `has_valid_blocker_link` when blocked); strips `MD_LINK_RE` spans before `ISSUE_REF_RE` matching (with `(?![A-Za-z0-9_-])` on `ISSUE_REF_RE` so `[bad](#999-missing)` never falls through to `#999`), and rejects local `#anchor` links that are neither GitHub comment/review fragments (`#issuecomment-<n>`, `#pullrequestreview-<n>`, `#discussion_r<n>`) nor present in the handoff document's heading slugs.
* Polarity-aware `check_agent_instructions` and PR-filtered `gh api --paginate` / CLI hardening (`RV-002`, `PC-001`, `PC-003`):
  * Observable acceptance criteria: `check_agent_instructions` normalizes wrapped paragraph/bullet clauses (`\s+` -> `" "` across hard-wrapped ~80-column lines split on `\n\s*\n` and `[.;!?]`), verifies prohibition polarity (`never|cannot|must\s+not|do\s+not|forbid\w*|prohibit\w*`) for `"nothing changed"` + `"unclassified"` and `"unverified blocker"`, rejects any affirmative single-section inversion clause pairing those terms outside `"permitted only when ... zero open issues unclassified"`, requires `--expect-open-issues`, `--open-issues`, and `gh api --paginate` in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, documents PR-excluding REST `/issues` pagination (`select(.pull_request == null)`) cross-referenced from `Stabilization checkpoints` and step 5, and accepts `gh api --paginate` provenance alongside `gh issue list` and `gh pr list` in `_validate_section`.
* Adversarial regression tests and HVE qualification refresh (`RV-003`, `PC-004`):
  * Observable acceptance criteria: `tools/test_check_coordinator_handoff.py` (`<= 12` test methods total, `0` test removals, extending `test_agent_instruction_guard_rejects_missing_contracts` and adding adversarial `RV-001`/`PC-002` subtests) proves every vector fails closed, and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` records both the superseded parent `.agent.md` SHA-256 (`6bca3f75...`) and the refreshed SHA-256 plus expanded scenarios.

## Non-Functional Requirements

* Zero third-party dependencies, offline determinism, and Ruff compliance:
  * Objective threshold or evaluation condition: Python 3.12 stdlib only; `< 1s` unit suite runtime; `0` diagnostics under `python3 -m ruff check` and `python3 -m ruff format --isolated --line-length 100 --check`; plain ASCII (`ord(c) <= 127`) and AMA Markdown rules in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
  * Observable acceptance criteria: Focused validation commands exit `0`.

## Acceptance Criteria

* `AC-RV1`: Trailing-clause negation (`"Nothing changed; do not launch anything"`) and `"Waiting for stakeholder feedback"` fail closed when unclassified or `ready to start` open issues exist (`RV-001`).
* `AC-RV2`: Split classification tables placed after an idle/waiting summary, cited blockers absent from the classification table (`Waiting on #999`), and nonexistent local `#anchor` blocker links all emit deterministic violations (`RV-001`).
* `AC-RV3`: Polarity-inverted coordinator instructions (`"always say nothing changed when unclassified"`, `"pause on an unverified blocker"`) fail `check_agent_text`, and `.github/agents/ama-backlog-delivery-coordinator.agent.md` documents write-time `--expect-*`/`--open-issues` flags and saturated-limit `gh api --paginate` handling (`RV-002`).
* `AC-RV4`: `tools/test_check_coordinator_handoff.py` (`unittest`), `ruff check`, `ruff format --isolated --line-length 100 --check`, `test_rpi_phase_witness.py`, and Markdown/ASCII checks exit `0`, and HVE assessment records exact updated SHA-256 (`RV-003`).

## Test Ownership and Validation Lock

* Canonical test file: `tools/test_check_coordinator_handoff.py` (`0` removals; maximum `2` new test methods added to the existing `10`, keeping total `<= 12` test methods using `self.subTest(...)`).
* Generated targets: `none`.
* Semantic vs regression coverage: Semantic behavior tests verify clause-scoped negation, `waiting for` detection, pre-summary table completeness, absent cited-blocker rejection, local `#anchor` verification, and polarity-enforced agent rules; regression tests confirm existing 10 positive/negative test groups and `tools/test_rpi_phase_witness.py` remain green.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md |
| Latest critique | .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan-critique.md with Revise disposition resolved directly (`PC-001` through `PC-004`) |
| Relevant research | .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md and .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement` |
| Continuation context | Parent automatic RPI Agent loop (`issue-1204-rv-fixes`, child of `issue-1204`) |

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md: Defines routed defects `RV-001`, `RV-002`, and `RV-003`.
* .copilot-tracking/research/2026-11-15/delivery-1204-coordinator-guard-research.md: Baseline coordinator architecture and validation constraints (`C1`-`C9`).
* tools/check-coordinator-handoff.py, .github/agents/ama-backlog-delivery-coordinator.agent.md, tools/test_check_coordinator_handoff.py: Exact files under remediation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Coordinator Handoff Validator, Instruction Hardening, and Adversarial Regression Suite

* Intent: Resolve `RV-001`, `RV-002`, and `RV-003` in one cohesive Focused-tier batch and re-verify all checks.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `tools/check-coordinator-handoff.py` and `.github/agents/ama-backlog-delivery-coordinator.agent.md` (`RV-001`, `RV-002`)

* Requirement and evidence: `RV-001` and `RV-002` in .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md
* Expected result: `check_handoff_text` and `check_agent_text` close all five `RV-001` bypass vectors and polarity-inverted instruction mutations, and `.github/agents/ama-backlog-delivery-coordinator.agent.md` documents write-time `--expect-*`/`--open-issues` flags and saturated-limit `gh api --paginate` handling.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend `tools/test_check_coordinator_handoff.py`, Refresh HVE Assessment, and Run Focused Validation (`RV-003`)

* Requirement and evidence: `RV-003` in .copilot-tracking/reviews/logs/2026-11-15/delivery-1204-coordinator-guard-review.md
* Expected result: Adversarial unit tests fail closed on every `RV-001`/`RV-002` vector, Focused validation (`unittest`, `ruff check`, `ruff format --isolated --line-length 100 --check`, `test_rpi_phase_witness.py`, Markdown/ASCII checks) passes with `0` errors, and `.copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-hve-assessment.md` is updated with the new `.github/agents/ama-backlog-delivery-coordinator.agent.md` SHA-256.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-phase-details.md

## Dependencies

* `P01-T02` depends on `P01-T01` so unit tests and HVE SHA-256 identity validate the finalized validator and agent Markdown.

## Critique Disposition

Single-pass critique executed at .copilot-tracking/reviews/2026-11-15/delivery-1204-coordinator-guard-rv-fixes-plan-critique.md (`Verdict: Revise`; `0` Critical, `2` High, `1` Medium, `1` Low; `User response required: no`). All four compatible planner-owned findings were applied directly:

* `PC-001` (`High`): Preserved `check_agent_instructions` public signature, specified whitespace-collapsed clause splitting across hard-wrapped ~80-column sentences (`\n\s*\n` and `[.;!?]`), added affirmative single-section polarity-inversion rejection alongside positive prohibition checks, and required `--expect-open-issues`, `--open-issues`, and `gh api --paginate` in `check_agent_instructions`.
* `PC-002` (`High`): Applied match-scoped `_is_claim_negated` across `STALE_CARRY_RE`, `IDLE_CLAIM_RE`, `WAITING_OR_PAUSE_RE`, `UNVERIFIED_BLOCKER_RE`, and `CITED_BLOCKER_REF_RE` splitting only on `[;.!?:]` and whitespace-bounded `\s+--\s+` with no cross-clause prefix carryover; evaluated standalone `blocked on #N` citations even outside `is_idle`/`is_waiting_or_pause`; and stripped `MD_LINK_RE` spans + tightened `ISSUE_REF_RE` (`(?![A-Za-z0-9_-])`) in `_has_non_bare_self_link` so digit-prefixed broken anchors (`[bad](#999-nonexistent)`) never fall through.
* `PC-003` (`Medium`): Specified PR-excluding REST `/issues` pagination (`select(.pull_request == null)`) cross-referenced from `Stabilization checkpoints` and step 5 in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and accepted `gh api --paginate` issue/PR provenance alongside `gh issue list` and `gh pr list` in `_validate_section`.
* `PC-004` (`Low`): Referenced the exact method `test_agent_instruction_guard_rejects_missing_contracts`, added `python3 tools/check-coordinator-handoff.py` plus Markdown link/style and plain-ASCII checks to `P01-T02` validation expectations, and required preserving the superseded parent SHA-256 (`6bca3f75...`) in the refreshed HVE assessment.

## Follow-Up Items

* Wire `python3 tools/check-coordinator-handoff.py` into `tools/rpi-checks.py` static checks in a separate gate-tooling PR validated under the full gate tier (`#1294`).
