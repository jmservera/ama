# Research: #132 variations and escalations reach a named owner (2026-11-14)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* `gh issue view 132`: 5/6 ACs ticked; the remaining AC is "Variations and escalations reach a named owner and never act as a contract instruction". Owner comments (2026-11-09/11) authorise only the synthetic staff-mediated slice; no contractor portal, no new permissions, no actual contract instructions.
* `src/core/.../job_pack.py` `escalation()` already required an owner name and role, but accepted placeholder names (for example "Unknown - not configured", "TBC") and the `contract_instruction=False` flag was a literal that nothing enforced.
* `src/core/.../staff_intake.py` `escalation_destination()` returned "Unknown - not configured" with `configured=False` but no explicit owner-needed statement, and nothing routed a variation to that destination.
* `src/api/.../web/staff-intake.js` showed owner/role/contact and a note, with no explicit owner status or advisory-only line.

## Gaps

1. Placeholder or blank owners could be treated as named.
2. No enforcement that a variation record is never a contract instruction.
3. No routing helper that refuses when no named owner is configured.
4. UI/API lacked an explicit owner-assignment status and advisory-only guard.
