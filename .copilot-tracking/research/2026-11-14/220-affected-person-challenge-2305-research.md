---
title: Task Research - 220-affected-person-challenge-2305
description: Primary evidence artifact for Issue 220 affected-person challenge non-retaliation, non-refusal, and non-delayed hazard response controls in src/core
ms.date: 2026-11-14
---

| Field | Value |
| --- | --- |
| Date | 2026-11-14 |
| Researcher / agent | rpi-research (via RPI Agent) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md |

## Research Brief

* What to research: Existing `src/core` affected-person challenge and correction route implementation, resident refusal handling, retaliation/sanction safeguards, and statutory/safety hazard clocks or emergency responses to determine what is needed to satisfy and deterministically verify Issue #220 criterion 5 (`No retaliation, inferred refusal or delayed hazard response`).
* Why it matters: Ensures affected persons can submit, update, escalate, or resolve a challenge or correction request against a source, policy, proposal version, or human decision without triggering retaliation flags/penalties, inferred resident refusals, or hazard response delays.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this RPI session, plus PR reviewers on target branch `feat/demo-164-chat-grounding-provenance-0900`.
* Scope: `src/core/src/zava_forward/core/` challenge, refusal, and hazard modules and `src/core/tests/` challenge route unit tests, anchored to Issue #220, PRD FR-052/AC-071/FR-043, and Case Study 48 Addendum.
* Non-goals: Unrelated UI/API changes, infrastructure/SQL changes, full test suite execution without `-p`, pushing to remote, or fabricating live operational workflow evidence.
* Criteria: Deterministic local controls and unit tests in `src/core` verifying that recording, updating, escalating, or resolving an affected-person challenge/correction request across source, policy, proposal version, and human decision targets never triggers retaliation flags/penalties, never records an inferred resident refusal, and never delays or pauses any statutory/safety hazard clock or emergency response.
* Requested outputs: Converged implementation recommendation for `src/core` and `src/core/tests/test_issue_220_challenge_route.py` (plus existing `test_*challenge*.py` compatibility).
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q4 below |
| Codebase scope | `src/core/`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/case_study_48_addendum.md`, `.copilot-tracking/` prior #220 records |
| External scope | none |
| Initial internal candidate areas | `src/core/src/zava_forward/core/challenges.py`, `hazard.py`, `resident_decisions.py`, `complaints_route.py`, `store.py`, `src/core/tests/test_challenges.py`, `test_hazard_referral.py` |
| Initial external candidate areas | none |
| Research posture | focused |
| Posture provenance | caller-specified bounded `src/core` objective |
| Explicit limits / deadline | Targeted tests only (`-p 'test_*challenge*.py'`); no push |
| Posture-specific completion basis | focused scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Keep working tree clean at commit; do not place `.copilot-tracking/` paths in production code or commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches all repository files | Enforces KB/case-study grounding, validation tier classification, commit/trailer rules, and Markdown style | Selected: mandatory repository governance |
| Skill | `rpi-research` | Explicit RPI loop phase 1 | Produces primary research artifact with 3-wave cycle and `C#` evidence log | Selected: canonical RPI research skill |
| Skill | `web-design-guidelines` / frontend skills | Web UI only | Backend `src/core` work is explicitly exempt in repository instructions | Skipped: backend-only `src/core` scope |
| Research specialist | `hve-core-all:rpi-researcher` | General delegated lane worker | Bounded independent lane investigation | Skipped (inline fallback): tightly coupled 3-file `src/core` investigation completed faster and more accurately inline |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive execution with explicit caller objective, target branch, artifact paths, and test selector | Answered by prompt | Proceed in confirmed automatic mode with focused posture |
| Direction change | No scope ambiguity or cross-boundary widening arose during cycle 1 | Not needed | Keep scope strictly inside `src/core` and `src/core/README.md` |
| Convergence | Cycle 1 answered all sub-questions with direct codebase evidence | Not needed | Converge on dual-surface hardening (`challenges.py` + `resident_decisions.py`) and `test_issue_220_challenge_route.py` |

## Scope and Success Criteria

* Scope: `src/core/src/zava_forward/core/challenges.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_issue_220_challenge_route.py`, `src/core/tests/test_challenges.py`, and `src/core/README.md`.
* Assumptions: Verified against code rather than assumed — checked whether `ChallengeRegister` and `Store` already support `human_decision` targets, challenge `update`, challenge `escalate`, and active non-retaliation / non-refusal / non-hazard-delay invariant checks.
* Success criteria:
  * Every research question is answered with exact `path:line` `C#` evidence.
  * Alternatives are compared and one convergence recommendation is selected.
  * Self-check passes and Planning Readiness is `Ready`.

## Task Research Requests

* Explicit requests: Deliver locally verifiable Issue #220 criterion 5 (`No retaliation, inferred refusal or delayed hazard response`) in `src/core` when an affected person submits or updates a challenge or correction request against a source, policy, proposal version, or human decision, with deterministic unit tests in `src/core/tests/test_issue_220_challenge_route.py` verifying recording, escalating, and resolving across all safeguard dimensions.
* Inferred research questions: How do `ChallengeRegister` and `Store` (`resident_decisions.py`) represent challenges, resident refusals, priority/retaliation signals, and hazard clocks (`taskqueues.py`, `store.py`, `hazard.py`), and what lifecycle operations or fail-closed guards are currently missing?
* Caller constraints and non-goals: Run only targeted tests (`-p 'test_*challenge*.py'`), run `mypy`, `ruff check .`, `ruff format --check .` in `src/core`, do not touch `pyproject.toml`, commit cleanly with Copilot trailer, do not push.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| narrow | Restrict validation test runner to `-p 'test_*challenge*.py'` plus `mypy` and `ruff` in `src/core` | Caller prompt | New deterministic test suite must live in `src/core/tests/test_issue_220_challenge_route.py` matching `'test_*challenge*.py'` |
| exclude | No `git push` or remote mutations | Caller prompt | Stop after clean local commit and `git status --short` verification |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | What challenge and correction surfaces exist in `src/core`, and which target kinds and lifecycle transitions do they currently support? | depth | H | answered |
| Q2 | How are retaliation/penalties, resident refusals, and statutory/safety hazard clocks or emergency responses modeled in `src/core`? | depth | H | answered |
| Q3 | What gaps prevent locally verifying non-retaliation, non-refusal, and non-delayed hazard response across submit, update, escalate, and resolve for source, policy, proposal version, and human decision targets? | depth | H | answered |
| Q4 | How can `test_issue_220_challenge_route.py` deterministically test both `ChallengeRegister` and `Store`/`SqlStore` while passing `mypy --strict` without modifying `pyproject.toml`? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-03-issue-220-protection-overdue-research.md`, `.copilot-tracking/research/2026-11-04-issue-220-status-record-research.md`, `.copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`.
* Reused (verified) findings: Criteria 1-4 of Issue #220 were delivered across `ChallengeRegister` (`challenges.py`) and `Store` (`resident_decisions.py`), including digital/staff routes, permitted explanations, exact transitive staleness, immediate `hazard_referral` on receipt, `protection` notice, and `overdue` / `hazard_referrals_overdue` read-only queries (`C1`, `C2`, `C4`).
* Superseded / stale: The 2026-11-04 status note observed that live human/operational acceptance cannot be proven by code alone, which remains true for live workflow sign-off, while deterministic `src/core` lifecycle operations (`update`, `escalate`, `human_decision` target kind) and fail-closed non-retaliation / non-refusal / non-hazard-delay safeguard invariants CAN and MUST be enforced and unit-tested locally in `src/core`.

## Research Cycle Log

### Cycle 1

* Active direction controls: Targeted `src/core` challenge test selector; no remote push; preserve `pyproject.toml`.
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: None blocking; baseline `mypy`, `ruff`, and `test_challenges.py` execute in ~2s.

#### Wave 1: Wider

* Plan and independent lanes: Inline sweep across `docs/prds/`, `docs/case_study_48_addendum.md`, `src/core/README.md`, and `src/core/src/zava_forward/core/` for FR-052, AC-071, FR-043, `ChallengeRegister`, `affected_challenges`, refusal handling, ranking, and hazard clocks.
* Worker evidence relationships or inline fallback: Inline (`C1`-`C9`) mapped Issue #220 requirements to two `src/core` challenge modules: store-independent `challenges.py` and store-backed `resident_decisions.py`, alongside `ranking.py`, `hazard.py`, `store.py`, and `taskqueues.py`.
* Reflection: Identified that both `challenges.py` and `resident_decisions.py` participate in Issue #220 in `src/core`, requiring deeper inspection of target kinds, lifecycle methods, and typing rules.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect exact method contracts in `challenges.py`, `resident_decisions.py`, `taskqueues.py`, `ranking.py`, and `src/core/pyproject.toml`.
* Plan and independent lanes: Inline line-level inspection of `challenges.py`, `resident_decisions.py`, `taskqueues.py`, `ranking.py`, `test_challenges.py`, `test_resident_decisions.py`, and `pyproject.toml`.
* Worker evidence relationships or inline fallback: Inline (`C1`-`C12`) established exact gaps:
  1. `challenges.py` restricts `SUBJECT_KINDS` to `("source", "policy", "proposal")` (omitting `"human_decision"`), lacks `update(...)` and `escalate(...)` lifecycle methods, lacks closed adverse-key input validation, and lacks an explicit deterministic safeguard invariant checker (`C1`).
  2. `resident_decisions.py` restricts `_dependency` `target_kind` to `proposal`, `source`, or `policy` (omitting `human_decision`), lacks `challenge_update` and `challenge_escalate` resident actions, and hardcodes `version=2` in `_res_challenge_resolve` rather than `record["version"] + 1` (`C4`, `C5`).
  3. `pyproject.toml` enforces `mypy` `strict = true` across new test modules (`C11`), while `Store`, `SqlStore`, `ranking`, and `resident_decisions` have `ignore_errors = true`; typing `Store`/`SqlStore` constructors via `Any` bridges in `test_issue_220_challenge_route.py` keeps strict mypy 100% clean without editing `pyproject.toml`.
* Reflection: Candidate design covers all lifecycle verbs (`record`, `update`, `review`, `escalate`, `resolve`) and all four target kinds (`source`, `policy`, `proposal`, `human_decision`). Needs contrarian testing against existing regression expectations and subtle hazard-ageing edge cases.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether adding `"human_decision"`, `update`, and `escalate` could break existing `test_challenges.py`, `test_resident_decisions.py`, or `src/api` callers, or inadvertently reset hazard referral ageing / overwrite opening statements.
* Plan and independent lanes: Grep all references to `SUBJECT_KINDS`, `NOT_INFERRED`, `RESIDENT_ACTIONS`, `FOLLOWUP_ACTIONS`, `target_kind`, and `"Choose proposal, source or policy."` across `src/`; trace hazard referral state transitions on update and escalation.
* Worker evidence relationships or inline fallback: Inline (`C5`, `C10`, `C12`) proved:
  1. No test in `src/` asserts failure on `target_kind="human_decision"` or hardcodes `RESIDENT_ACTIONS` / `NOT_INFERRED` contents (`C12`).
  2. If `ChallengeRegister.update(..., hazard_concern=True)` or `escalate(...)` overwrote an existing unhanded `hazard_referral["received_on"]`, it WOULD reset referral age in `hazard_referrals_overdue(today, max_days)` and mask a delayed hazard handoff! Preserving original `received_on` on active referrals while updating `to` (and recording `originally_referred_to`) prevents any hidden referral-clock reset.
  3. In `_res_challenge_resolve`, changing `version=2` to `version=record["version"] + 1` yields `2` when resolving directly from `version=1` (preserving every existing test in `test_resident_decisions.py` and `test_resident_api.py`) while maintaining strict version monotonicity after `challenge_update` or `challenge_escalate` (`C5`).
* Reflection: Contrarian wave caught two subtle hazards (referral `received_on` preservation across update/escalate and `version=record["version"] + 1` on post-update/post-escalate resolution). No open gaps remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
| --- | --- | --- | --- | --- |
| Extend `ChallengeRegister` with `"human_decision"` subject kind, `update()`, `escalate()`, closed adverse-field rejection, and deterministic safeguard verifier `assert_no_adverse_challenge_effects()` | `C1`, `C2`, `C3`, `C6`, `C7`, `C8` | accepted | Directly implements and enforces non-retaliation, non-refusal, and non-delayed hazard response across submit, update, escalate, and resolve in the typed challenge route | Primary convergence recommendation |
| Extend `resident_decisions.py` (`Store`/`SqlStore`) with `target_kind="human_decision"`, `challenge_update`, `challenge_escalate`, and monotonic `version=record["version"] + 1` | `C4`, `C5`, `C9`, `C12` | accepted | Ensures store-backed `affected_challenges` also supports all 4 target kinds plus update and escalation without mutating `hazards`, `measure_decisions`, `decision`, `ranking`, or unrelated closures | Primary convergence recommendation |
| Modify `pyproject.toml` mypy overrides for `test_issue_220_challenge_route.py` | `C11` | rejected | Repository instructions classify dependency-manifest edits conservatively; typing untyped `Store`/`SqlStore`/`ranking` bindings via `Any` in the test module satisfies `mypy --strict` cleanly with zero manifest edits | Rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All 4 research questions are answered with direct `path:line` evidence, contrarian checks resolved version-monotonicity and hazard-ageing preservation, and baseline checks pass.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded 3-module `src/core` scope where direct `view` and `grep` resolved exact line-level contracts with zero context bloat.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | `ChallengeRegister` defines `SUBJECT_KINDS = ("source", "policy", "proposal")` and `STATUSES = ("received", "under_review", "corrected", "upheld", "withdrawn")`, omitting `"human_decision"`, `update`, and `escalate` | `src/core/src/zava_forward/core/challenges.py:21` | view | high | Lines 19-33 and 59-277 |
| C2 | `ChallengeRegister._record` records immediate `hazard_referral` (`status="referred_on_receipt"`) when `hazard_concern=True` and `hazard_referrals_overdue` flags unhanded referrals read-only without changing any hazard clock | `src/core/src/zava_forward/core/challenges.py:107` | view | high | Lines 107-113 and 236-263 |
| C3 | PRD FR-052, AC-071, FR-043 and Addendum Meaningful oversight and redress require accessible challenge/correction routes against source, policy, proposal version, and human decision without retaliation, inferred refusal, or delayed hazard response | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:455` | grep/view | high | Also `docs/case_study_48_addendum.md:1006` |
| C4 | `resident_decisions._dependency` currently supports `proposal`, `source`, and `policy` target kinds and computes `(proposal_digest, decision_version, decision)` via `priority_binding(rec)` | `src/core/src/zava_forward/core/resident_decisions.py:570` | view | high | Lines 570-610 and 636-651 |
| C5 | `_res_challenge_open` and `_res_challenge_resolve` record `affected_challenges` on cases (`version=1` then `version=2`), with no `challenge_update` or `challenge_escalate` action yet | `src/core/src/zava_forward/core/resident_decisions.py:1498` | view | high | Lines 1498-1547 |
| C6 | Resident refusal is strictly explicit: `measure_decision_view` defaults to `"Not recorded"` and `resident_status` returns `"Declined"` only when every measure has a current explicit `"Declined"` decision | `src/core/src/zava_forward/core/resident_decisions.py:1040` | view | high | Lines 1040-1068 |
| C7 | Deterministic home priority `ranking.rank`, `ranking.sql_key`, and `ranking.reasons` depend only on `safety_open`, `support`, `waiting_days`, `stage_order`, and `case_id` — never penalizing `affected_challenges` | `src/core/src/zava_forward/core/ranking.py:66` | view | high | Lines 66-143 |
| C8 | Statutory/safety hazard clocks and emergency responses live on `case["hazards"]` (`aware_at`, `response_due_at`, `responded_at`, `resident_update_due_at`, `hold`, `released`), surfaced via `taskqueues.case_view(...)["hazard_clocks"]` and audited as `safety_emergency` in `hazard.persist_event` | `src/core/src/zava_forward/core/taskqueues.py:233` | view | high | Also `src/core/src/zava_forward/core/hazard.py:93` |
| C9 | `SqlStore` indexes `priority_correction` where `$.resolution.outcome == 'Correction recorded'` and extracts `(c.id, ch.id, ch.target)` from `$.affected_challenges` | `src/core/src/zava_forward/core/sqlstore.py:984` | grep | high | Lines 984-985 and 1124-1131; works automatically for `target.kind == "human_decision"` |
| C10 | Existing `test_challenges.py` runs 19 unit tests covering routes, visibility, staleness, `NOT_INFERRED`, `hazard_referral`, `PROTECTION`, `overdue`, and `hazard_referrals_overdue` | `src/core/tests/test_challenges.py:53` | view/bash | high | All 19 pass in 0.004s |
| C11 | `src/core/pyproject.toml` sets `[tool.mypy] strict = true` and `[tool.ruff] line-length = 100` while excluding legacy migrated `resident_decisions.py` from `ruff format` and `mypy` errors | `src/core/pyproject.toml:26` | view | high | New test files are checked under strict mypy and ruff |
| C12 | Repository-wide grep confirms no caller or test hardcodes `RESIDENT_ACTIONS`, `FOLLOWUP_ACTIONS`, `NOT_INFERRED`, or rejects `target_kind="human_decision"` | `src/core/src/zava_forward/core/resident_decisions.py:30` | grep | high | Sweep across `src/` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

### Contradictions / Conflicts

* none

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | `src/core` has two challenge modules: `challenges.ChallengeRegister` (constructed challenges) and `resident_decisions.ResidentDecisionMixin` (`Store`/`SqlStore` `affected_challenges`). Neither yet supports `"human_decision"` as a direct subject/target kind, nor `update` / `escalate` transitions. | `C1`, `C4`, `C5` | high | Extend both modules cleanly while keeping existing method signatures backward-compatible. |
| Q2 | Priority penalties/retaliation would appear in `ranking.rank`/`sql_key`/case adverse flags; resident refusals live in `measure_decisions` / `decision` / `resident_status`; statutory/safety hazard clocks live in `case["hazards"]`, `hazard.persist_event` (`safety_emergency`), `taskqueues.case_view()["hazard_clocks"]`, and `ChallengeRegister.hazard_referrals()`. | `C2`, `C6`, `C7`, `C8` | high | Invariant guard and unit tests can deterministically verify zero adverse impact across all three dimensions. |
| Q3 | Adding `"human_decision"` target support, `update` and `escalate` operations (preserving active `hazard_referral["received_on"]` and monotonic versions), closed adverse-key rejection, and `assert_no_adverse_challenge_effects()` makes criterion 5 deterministically enforceable and verifiable in `src/core`. | `C1`, `C2`, `C5`, `C9`, `C12` | high | Ready for implementation plan without external dependencies. |
| Q4 | Placing the comprehensive unit suite in `src/core/tests/test_issue_220_challenge_route.py` matches `-p 'test_*challenge*.py'` and passes `mypy --strict` using typed `ChallengeRegister`/`taskqueues` imports plus `Any`-typed `Store`/`SqlStore`/`ranking` bindings, leaving `pyproject.toml` untouched. | `C10`, `C11` | high | Satisfies validation and manifest rules cleanly. |

## Key Discoveries

* `ChallengeRegister` (`challenges.py`) and `Store` (`resident_decisions.py`) both handle Issue #220 challenges in `src/core`; supporting `"human_decision"` targets, `update`, and `escalate` across both surfaces eliminates any gap between constructed register challenges and store-backed case challenges (`C1`, `C4`, `C5`, `C9`).
* Escalating or updating a challenge with an unhanded `hazard_referral` must never overwrite an existing `received_on` date or clear `referred_on_receipt`, otherwise `hazard_referrals_overdue(today, max_days)` could mask a delayed safety handoff (`C2`).
* `_res_challenge_resolve` in `resident_decisions.py` previously hardcoded `version=2`; using `record["version"] + 1` preserves `version=2` for direct open-to-resolve flows while keeping optimistic concurrency monotonic when updates or escalations precede resolution (`C5`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Enhance `zava_forward.core.challenges` (add `"human_decision"` to `SUBJECT_KINDS`, `"escalated"` to `STATUSES`, `update(...)`, `escalate(...)`, closed adverse-input rejection, `SAFEGUARDS` metadata in `view()`, and deterministic `assert_no_adverse_challenge_effects(before_case, after_case)`) and `zava_forward.core.resident_decisions` (add `"human_decision"` to `_dependency` and `priority_challenge_state`, add `challenge_update` and `challenge_escalate`, fix `_res_challenge_resolve` to use `record["version"] + 1`, and enforce `assert_no_adverse_challenge_effects`), verified by `src/core/tests/test_issue_220_challenge_route.py` and `src/core/tests/test_challenges.py`, plus `src/core/README.md` documentation.
* Rationale: Covers every target kind (`source`, `policy`, `proposal`, `human_decision`), every lifecycle action (`record`, `update`, `review`, `escalate`, `resolve`), and both `ChallengeRegister` and `Store`/`SqlStore` hazard/refusal/ranking integration without touching `pyproject.toml` or breaking any existing caller.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`
* Implementation impact: `src/core/src/zava_forward/core/challenges.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_issue_220_challenge_route.py`, `src/core/tests/test_challenges.py`, `src/core/README.md`.
* Confidence: high: all code paths and static/unit checks were inspected directly in `src/core`.

File tree:

```text
src/core/
  README.md                                      (updated)
  src/zava_forward/core/
    challenges.py                                (updated)
    resident_decisions.py                        (updated)
  tests/
    test_challenges.py                           (retained/compatible)
    test_issue_220_challenge_route.py            (created)
```

### Alternative: Test-only additions on unchanged `challenges.py`

* Approach: Add tests only in `test_issue_220_challenge_route.py` without adding `"human_decision"` subject kind, `update()`, `escalate()`, or fail-closed safeguard invariants.
* Trade-offs: Smaller diff in `src/core/src/`, but cannot exercise updating or escalating challenges or directly challenging a `"human_decision"` subject kind, and provides passive omission checks rather than active fail-closed safeguard enforcement.
* Evidence refs: `C1`, `C4`, `C5`
* Rejection rationale: Incomplete against the objective requiring submission, update, escalation, and resolution coverage across source, policy, proposal version, and human decision targets.

### Alternative: Edit `pyproject.toml` to add `disallow_untyped_calls = false` override for the new test file

* Approach: Add `test_issue_220_challenge_route` to `[[tool.mypy.overrides]]` in `src/core/pyproject.toml`.
* Trade-offs: Allows direct untyped `Store(...)` calls without `Any` annotation, but modifies a dependency manifest (`pyproject.toml`), which repository governance classifies conservatively toward full-gate scrutiny.
* Evidence refs: `C11`
* Rejection rationale: Unnecessary; explicit `Any` constructor/adapter helpers in `test_issue_220_challenge_route.py` keep `mypy --strict` 100% clean with zero `pyproject.toml` edits.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Live operational non-retaliation acceptance, resident/staff comprehension studies, and an owner-approved `max_days` threshold for `hazard_referrals_overdue` remain human governance gates outside unit code (`C3`, `src/core/README.md`). Commit and PR references must therefore use `Refs #220` rather than claiming human operational gates are closed.
* Follow-up: API/UI forms (`panels.js`) can expose `challenge_update`, `challenge_escalate`, and `target_kind="human_decision"` in a separate web slice under web-design-guidelines when requested.
* Residual uncertainty: none within `src/core` scope.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
| --- | --- | --- | --- | --- | --- |
| Harden both `ChallengeRegister` (`challenges.py`) and `Store`/`SqlStore` (`resident_decisions.py`) with `human_decision` target, `update`, `escalate`, and fail-closed non-retaliation / non-refusal / non-hazard-delay invariants | confirmed | evidence / convergence | Satisfies all locally verifiable requirements of Issue #220 criterion 5 without breaking existing tests | `C1`-`C12` | Plan covers `challenges.py`, `resident_decisions.py`, `test_issue_220_challenge_route.py`, and `src/core/README.md` |
| Keep `src/core/pyproject.toml` untouched | confirmed | repository constraint | Avoids manifest changes while passing `mypy --strict` | `C11` | Type `Store`/`SqlStore`/`ranking` test helpers explicitly |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
| --- | --- | --- | --- | --- |
| Live operational workflow acceptance and owner-approved `max_days` hazard referral follow-up threshold | Live pilot workflow audit and named owner decision | Programme / Safety / Resident Engagement owners | Required before closing Issue #220 as operationally proven beyond `src/core` | follow-up (non-blocking for `src/core` slice) |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
| --- | --- | --- | --- | --- | --- |
| L | Web UI exposure for `challenge_update`, `challenge_escalate`, and `human_decision` target in `src/api` | Extends staff workbench forms to match new `src/core` operations | Owner requests `src/api` workbench slice | deferred | `Q1`; `C4`, `C5` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`
* Preconditions met: Baseline `mypy`, `ruff check`, `ruff format --check`, and `test_challenges.py` verified passing; exact line targets and invariants established.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Cycle 1: Wider, Deeper, and Contrarian completed in order |
| Lane evidence or inline fallback | Inline investigation (`C1`-`C12`); bounded `src/core` scope required no subagent fan-out |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C12`) |
| Blockers | none |
| Continuation owner and state | confirmed automatic RPI Agent; automatic continuation to `Plan` |

## Advisory Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C12`) |
| Output mode and planning support | `convergence`; yes — single evidence-backed `src/core` approach selected |
| Acting owner | confirmed automatic RPI Agent |
| Required gates or confirmations | Prior-knowledge gate passed; 3-wave cycle completed; artifact self-check passed; pre-transition state write ready |
| Continuation result | automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md |
| Notes for planning or re-entry | Preserve `received_on` on active `hazard_referral` across `update`/`escalate`, keep `_res_challenge_resolve` version monotonic (`record["version"] + 1`), and verify both JSON `Store` and SQLite `SqlStore` in `test_issue_220_challenge_route.py`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All material `src/core` code paths, schemas, and tests were directly verified; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives, Open Questions, Current/Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none

