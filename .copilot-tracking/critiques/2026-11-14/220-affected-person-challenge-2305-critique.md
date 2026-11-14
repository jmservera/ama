---
title: RPI Plan Critique - 220-affected-person-challenge-2305
description: Single-pass plan critique for Issue 220 affected-person challenge non-retaliation, non-refusal, and non-delayed hazard response controls in src/core
ms.date: 2026-11-14
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-220-criterion-5-affected-person-challenge-2305
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the remaining locally verifiable acceptance criterion for Issue #220 in `src/core` (`No retaliation, inferred refusal or delayed hazard response` when an affected person submits or updates a challenge or correction request against a source, policy, proposal version, or human decision), with deterministic unit tests in `src/core/tests/test_issue_220_challenge_route.py` covering recording, updating, escalating, and resolving across all safeguard dimensions; write all 4 `.copilot-tracking/` RPI stage artifacts dated `2026-11-14`; run only targeted `src/core` checks (`mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*challenge*.py' -v`); leave `pyproject.toml` untouched; commit cleanly on `feat/ai-220-affected-person-challenge-2305` without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md (`C1`-`C12`), .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md, .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md, src/core/src/zava_forward/core/challenges.py, src/core/src/zava_forward/core/resident_decisions.py, src/core/src/zava_forward/core/sqlstore.py, src/core/tests/test_challenges.py.
* Decisions, dependencies, and acceptance criteria considered: Dual-surface hardening across `ChallengeRegister` (`challenges.py`) and `Store`/`SqlStore` (`resident_decisions.py`); `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, and `AC-1` through `AC-6`; honest `Refs #220` commit boundary preserving external human operational gates (`max_days` policy approval, resident/staff comprehension sign-off, live workflow audit).
* Assessment boundary: Evaluates deterministic `src/core` domain logic, transactional `Store`/`SqlStore` persistence and replay (`validate_sql`), typing/lint compatibility, and targeted unit test design from the supplied artifacts and source files. It cannot validate live operational governance sign-off or `src/api` UI surfaces excluded from scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-1 / AC-1 (`source`, `policy`, `proposal`, `human_decision` targets and versioned staleness) | Covered | `C1`, `C4`, `C9`: `ChallengeRegister` `SUBJECT_KINDS` and `resident_decisions._dependency` / `priority_challenge_state` / `SqlStore._priority_correction_rows` cleanly bind `human_decision` to `priority_binding(rec)[1]` when `resolved_by` is present. |
| FR-2 (`ChallengeRegister.update` digital and non-digital channels, immutable opening statement, hazard referral ageing) | Partial | `C1`, `C2`: lifecycle is well structured, but `PC-002` identifies unpermitted explanation leakage via `rec["updates"]` in `view(cid)` and `PC-003` identifies ambiguous `received_on=None` preservation on active `referred_on_receipt` referrals. |
| FR-3 (`ChallengeRegister.escalate` to distinct named human owner preserving active hazard referral) | Covered | `C1`, `C2`: refuses resolved and same-owner escalation, transfers `owner` and `hazard_referral["to"]`, records `originally_referred_to` via `setdefault`, and preserves `received_on`. |
| FR-4 / AC-5 (Fail-closed `ChallengeSafeguardError` on forbidden inputs and tampered case snapshots) | Partial | `C5`, `C7`, `C8`: `PC-001` identifies case fields affecting priority/retaliation/unrelated closure in `sqlstore.py:975-986` (`resident`, `service_requests`, `appointments`, `funding`, `wave`) and pre-schema `ChallengeSafeguardError` ordering in `_res_challenge_*`. |
| FR-5 / AC-2 / AC-3 / AC-4 (`Store` and `SqlStore` `challenge_open`, `challenge_update`, `challenge_escalate`, `challenge_resolve` safeguards) | Partial | `C4`-`C9`: `FOLLOWUP_ACTIONS` + `_operation` + `validate_sql` replay and monotonic `version = record["version"] + 1` are sound; tightening `PC-001` closes the remaining case-snapshot and input-error gaps. |
| NFR-1 / NFR-2 / AC-6 (Strict `mypy`, `ruff`, targeted `-p 'test_*challenge*.py'`, untouched `pyproject.toml`, 4 RPI artifacts, `README.md`) | Covered | `C10`, `C11`: `P02-T01` and `P02-T02` align with caller constraints, `Any`-bridged strict typing, and honest `Refs #220` documentation. |
| P01 / P01-T01 | Partial | Needs surgical clarifications for `PC-001`, `PC-002`, and `PC-003`. |
| P01 / P01-T02 | Partial | Needs pre-schema `FORBIDDEN_ADVERSE_FIELDS` check raising `ChallengeSafeguardError` (`PC-001`). |
| P02 / P02-T01 / P02-T02 | Partial | Needs focused assertions for update-explanation filtering (`PC-002`), `received_on=None` preservation (`PC-003`), and `Store`/`SqlStore` `ChallengeSafeguardError` + non-`affected_challenges` mutation detection (`PC-001`). |

## Verdict

* Verdict: Revise
* Rationale: The dual-surface architecture across `challenges.py` and `resident_decisions.py` (`Store`/`SqlStore`) is strongly grounded in codebase evidence, compatible with `validate_sql` transactional replay and `SqlStore` JSON indexing, and faithful to every caller constraint, but three concrete edge-case gaps in `P01-T01`, `P01-T02`, and `P02-T01` (`PC-001` through `PC-003`) should be tightened directly by the planning parent before implementation so safeguard and visibility guarantees are airtight.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Incomplete case-mutation coverage in `assert_no_adverse_challenge_effects` and `ValueError` shadowing in `_res_challenge_*`

* Related IDs: FR-4, FR-5, AC-2, AC-5, P01-T01, P01-T02, P02-T01, C5, C7, C8
* Evidence: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md, .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md, src/core/src/zava_forward/core/resident_decisions.py:1502-1536, src/core/src/zava_forward/core/sqlstore.py:975-986
* Concern: Two gaps weaken the fail-closed `ChallengeSafeguardError` contract in `AC-5` and `FR-4`. First, `SqlStore._row` (`src/core/src/zava_forward/core/sqlstore.py:975-986`) derives priority ranking and resident/service state from `c["resident"]` (`ranking._support(c)`), `c["wave"]`, `c["funding"]`, `c["appointments"]`, and `c["service_requests"]` (where closing an open repair or complaint request is an unrelated closure), whereas `P01-T01` only lists `closed`, `stage`, `days_in_stage`, `priority_penalty`, `decision`, `measure_decisions`, `resident_reviews`, and `hazards`, and does not state that nested dicts inside `after_case["affected_challenges"]` are scanned for `FORBIDDEN_ADVERSE_FIELDS` or that any mutation to case keys outside `affected_challenges` fails closed. Second, `_res_challenge_open` and `_res_challenge_resolve` (`src/core/src/zava_forward/core/resident_decisions.py:1504,1533`) and planned `_res_challenge_update` / `_res_challenge_escalate` enforce `set(body) != fields` raising plain `ValueError`; unless `FORBIDDEN_ADVERSE_FIELDS` is checked on `body` before `set(body) != fields`, adverse keys passed to `Store.resident_action` raise plain `ValueError` instead of `ChallengeSafeguardError`.
* Impact: A retaliatory downgrade to `resident` support flags (which lowers `ranking.rank` and `ranking.sql_key`), `funding`, or `wave`, or an unrelated closure/cancellation in `service_requests` or `appointments`, could pass `assert_no_adverse_challenge_effects`, and `Store`/`SqlStore` adverse-input callers would not receive `ChallengeSafeguardError` (`AC-5`). Since `ChallengeSafeguardError` subclasses `ValueError`, checking forbidden adverse keys first preserves 100% backward compatibility with existing `ValueError` callers.
* Smallest useful change: Update `P01-T01` so `assert_no_adverse_challenge_effects(before_case, after_case)` explicitly checks `resident`, `service_requests`, `appointments`, `funding`, and `wave` alongside `closed`, `stage`, `days_in_stage`, `decision`, `measure_decisions`, `resident_reviews`, and `hazards`, scans `after_case` (including nested dicts in `affected_challenges`) for `FORBIDDEN_ADVERSE_FIELDS`, and fails closed with `ChallengeSafeguardError` if any top-level key other than `affected_challenges` differs between `before_case` and `after_case`. Update `P01-T02` and `P02-T01` so `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_escalate`, and `_res_challenge_resolve` reject `FORBIDDEN_ADVERSE_FIELDS` in `body` with `ChallengeSafeguardError` before the generic `set(body) != fields` check.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01`, `P01-T02`, and `P02-T01` sections in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md specifying full non-`affected_challenges` case immutability, recursive `affected_challenges` adverse-key inspection, and pre-schema `ChallengeSafeguardError` rejection in `_res_challenge_*`, with matching negative unit test cases.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Person-facing `ChallengeRegister.view(cid)` can leak non-permitted explanations recorded via `update(...)`

* Related IDs: FR-1, FR-2, P01-T01, P02-T01, C1, C10
* Evidence: src/core/src/zava_forward/core/challenges.py:272-277, src/core/tests/test_challenges.py:80-84, .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Concern: `ChallengeRegister.view(cid)` (`src/core/src/zava_forward/core/challenges.py:272-277`) deep-copies the full challenge record and filters `permitted` items only on top-level `rec["explanations"]`. `P01-T01` adds `rec["updates"]` and accepts `explanations` in `ChallengeRegister.update(...)`. If update entries store `explanations` (or raw explanation dicts) without `view(cid)` filtering `explanations` inside `rec["updates"]`, internal notes with `permitted=False` supplied on `update(...)` will be exposed in `view(cid)["updates"]`.
* Impact: Breaks Issue #220's person-facing permitted-explanation visibility boundary (`challenges.py:273`, `test_challenges.py:80-84`) whenever staff or automated workflows attach internal non-permitted triage notes during a challenge update.
* Smallest useful change: Specify in `P01-T01` that `ChallengeRegister.view(cid)` filters any `explanations` list inside `rec.get("updates", [])` to `[e for e in u["explanations"] if e["permitted"]]` (or stores update explanations on `rec["explanations"]` and filters any per-update copy in `view(cid)`), and add an assertion in `P02-T01` passing `permitted=False` to `update(...)` and verifying its absence from `view(cid)` everywhere.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P02-T01` sections in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md explicitly filtering non-permitted explanations across `view(cid)` including `updates`, paired with a test assertion.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Ambiguous preservation of `received_on=None` on active `referred_on_receipt` hazard referrals during `update(...)`

* Related IDs: FR-2, AC-4, P01-T01, P02-T01, C2, C10
* Evidence: src/core/src/zava_forward/core/challenges.py:249-256, src/core/tests/test_challenges.py:209-221, .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Concern: In `src/core/src/zava_forward/core/challenges.py:249-256`, an unhanded `hazard_referral` with `received_on=None` has `age = None` and is immediately flagged by `hazard_referrals_overdue(today, max_days)` (`src/core/tests/test_challenges.py:213-220`). `P01-T01` states that on `update(..., hazard_concern=True)` when `status == "referred_on_receipt"`, the register `"strictly preserves existing received_on (never overwrites an existing date with a later date or None)"`. That phrasing leaves open overwriting `received_on=None` with a newly supplied date (such as `today`), which would turn `referral_age_days` from `None` into `0` and silently drop an already-flagged unknown-age referral from `hazard_referrals_overdue`.
* Impact: Updating an open challenge that carried an unknown-age unhanded hazard referral could mask overdue safety follow-up (`AC-4`).
* Smallest useful change: Clarify in `P01-T01` and `P02-T01` that any supplied `received_on` argument on `update(...)` is still date-validated when non-`None`, and while an existing `hazard_referral` has `status == "referred_on_receipt"`, `referral["received_on"]` is unconditionally preserved unchanged whether its prior value was an ISO date string or `None`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P01-T01` and `P02-T01` sections in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md stating unconditional immutability of `hazard_referral["received_on"]` while `status == "referred_on_receipt"` (including `None`) and testing both dated and `None` cases.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong dual-surface design: Extending both `ChallengeRegister` (`challenges.py`) and `ResidentDecisionMixin` (`resident_decisions.py`) ensures no drift between store-independent challenge dependency graphs and transactional JSON `Store` / SQLite `SqlStore` case workflows.
* Transactional SQLite safety verified: Routing `challenge_update` and `challenge_escalate` through `FOLLOWUP_ACTIONS` and `_operation` preserves `resident_decisions.validate_sql` replay under `SqlStore.save()`, while `SqlStore._row` and `SqlStore._priority_correction_rows` index `target.kind == "human_decision"` automatically without schema changes.
* Monotonic concurrency and version binding: Replacing hardcoded `version=2` with `record["version"] + 1` in `_res_challenge_resolve` preserves `version=2` for direct open-to-resolve flows while keeping `expected_version` optimistic locking sound across updates and escalations.
* Accepted residual risk: Live operational non-retaliation audits, resident/staff comprehension studies, `src/api` workbench form exposure, and an owner-approved `max_days` hazard follow-up threshold remain separate governance/follow-up items outside `src/core`; the plan appropriately scopes commits to `Refs #220`.

## Questions or Blocking Evidence Gaps

* None. All three findings are deterministic planner refinements fully resolved by the supplied `src/core` evidence.

## Limitations

* Critique stayed strictly read-only over the supplied artifacts and four referenced `src/core` files without running full test suites or inspecting out-of-scope `src/api` files.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, and `PC-003` to .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md (and update critique disposition / readiness in .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md), then finalize the plan for implementation without a second critique pass.
* User response required: no
