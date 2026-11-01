# Plan: affected-person challenge and correction route (issue 220), 2026-11-01

Research: `.copilot-tracking/research/2026-11-01-issue-220-affected-person-challenge-research.md`

## Phases

* [x] 1. Add `src/core/src/zava_forward/core/challenges.py`: `ChallengeRegister` with `record_digital`, `record_staff`, `review`, `resolve`, `view`.
  * Routes: `digital` (self-service, no staff needed) and `staff_recorded` (non-digital channel phone, in person, paper, with named recording staff).
  * Each record: subject (kind source/policy/proposal, id, version), human decision reference, plain-language statement, human owner, accessible-route statement, next-update due date, status, resolution evidence, explanations with a permitted flag (only permitted visible).
  * Dependency graph injected as `{item_id: [upstream ids]}`; staleness marks only transitive dependents of the challenged subject, preserving prior versions.
  * Explicit non-inference flags: consent, refusal, sanction, unrelated closure, hazard clock are never read or written; a test proves they are unchanged.
* [x] 2. Add `src/core/tests/test_challenges.py` covering AC-071 for both routes, explanation visibility, owner/next-update/resolution, exact stale set, and non-inference.
* [x] 3. Validate: unittest for the new tests, ruff check, ruff format --check, mypy in `src/core`.
* [x] 4. Document in `src/core/README.md` briefly and the change log.

## Critique (single pass, final candidate)

* Verdict: proceed. Risk: scope creep into stores; rejected. Risk: criterion 5 over-claim; resolved by Refs, not Closes.

## Correction cycle 2 (2026-11-01)

Copilot thread on challenges.py: resolving a challenge dropped a pending hazard referral from the listing. Fix: `hazard_referrals()` lists referrals with status `referred_on_receipt` regardless of challenge status; new `confirm_hazard_handoff()` (named owner, non-empty evidence) marks `handed_off`. Test and README contract updated. Validation: ruff check, ruff format --check, mypy clean; tests.test_challenges 14 pass. Human review remains required.
