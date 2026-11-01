# Research: affected-person challenge and correction route (issue 220), 2026-11-01

* Task: issue-220-affected-person-challenge; Research disposition: executed (targeted).
* Requirements: PRD FR-052 and AC-071 (constructed challenge; digital and staff-recorded non-digital routes; permitted AI/source/policy explanation, human owner, next-update commitment, resolution evidence; no consent, refusal, sanction, unrelated closure or hazard-clock inference), FR-043 (exactly dependent proposals, calculations, reviews stale; prior versions and unrelated decisions preserved).
* Related: #130 (nomination and challenge route, open, not evidenced), #86, #88, #154; parent #218.
* Codebase: `src/core/src/zava_forward/core/` has no challenge module. `form_review.py` and `taskqueues.py` hold stale handling for forms and queues, coupled to JSON/SQL/MSSQL stores. `change_provenance.py` shows the named-staff actor rule. Tests live in `src/core/tests/`, run with unittest; ruff line length 100, mypy strict.
* Decision: deliver a store-independent domain module (`challenges.py`) with an injected dependency graph, so the slice is demonstrable now and storage/API/UI wiring follows under #130/#218. This keeps scope to the acceptance criteria.
* Constraints: tests outside package, no mvp/prototype code, pip only, synthetic data only, no secrets.
* Unmet by design: criterion 5 (no retaliation, inferred refusal or delayed hazard response) needs live workflow and hazard-referral integration and human review; this slice only proves the record cannot alter hazard clocks, consent or sanctions.
* Planning Readiness: Ready.

## Correction cycle 2 (2026-11-01)

Review thread: pending hazard referrals must stay visible after challenge resolution until an evidenced human handoff. Valid; no new external evidence needed. Planning Readiness: Ready.
