# Research: issue 220 hazard referral follow-up, 2026-11-01

* Task: `issue-220-hazard-referral`. Research disposition: executed. Planning Readiness: Ready.
* Finding: #641 delivered criteria 1 to 4 in `challenges.py`; criterion 5 (no retaliation, inferred refusal or delayed hazard response) was left unproven. Issue comments (closure audit batch 2) confirm it is unmet.
* Gap addressable in code: a challenge describing a hazard has no routing, so it could wait behind routine review.
* Out of scope: store persistence, API/UI, representative human acceptance, operational delay measurement (cannot be proven locally).

## Correction cycle (PR 693)

* Copilot thread: `confirm_hazard_handoff` marked the referral `handed_off` before validating evidence, so a whitespace-only value raised after mutating state. Valid; confirmed by reading the code.
