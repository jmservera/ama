---
title: Issue 132 contractor variation and escalation research
date: 2026-11-14
---

## Findings

* `job_pack.escalation` already requires a named owner holding a manager or Building Safety Liaison role, and sets `contract_instruction` and `acts_as_contract_instruction` to False.
* `job_pack.reject_instruction_claim` rejects truthy instruction claims; `staff_intake.escalate` calls it. API guard tests exist in `src/api/tests/test_fieldwork_variation_owner_guard.py`.
* Gap: no `is_contract_instruction` field and that key was not rejected as a claim.
* `role-screens.js` is out of scope and untouched.

Planning Readiness: Ready. Research disposition: executed.
