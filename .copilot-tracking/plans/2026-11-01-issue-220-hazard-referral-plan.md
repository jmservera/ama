# Plan: issue 220 hazard referral follow-up, 2026-11-01

* Add optional `hazard_concern` to `record_digital` and `record_staff`: record `hazard_referral` to the named owner on receipt; no clock, sanction, refusal or consent field.
* Add `hazard_referrals()` listing open flagged challenges.
* Add two tests; document in `src/core/README.md`.
* Critique: executed once, self-critique; compatible finding applied (referral must not depend on review status). Verdict: proceed.
* Validation: unittest `test_challenges`, ruff check, ruff format --check, mypy. CI is the evidence.
* PR wording: `Refs #220`, naming criterion 5 as unmet.

## Correction cycle (PR 693)

* Validate handoff evidence before mutating the referral; extend the rejection test to assert the referral stays listed and `referred_on_receipt`.
