---
title: Fieldwork variation named-owner plan (#132)
ms.date: 2026-11-14
---

## Steps

* [x] Add `acts_as_contract_instruction=False` and shared notice to `job_pack.escalation`; add `reject_instruction_claim`.
* [x] Add `field-escalate` action: staff only, required `named_owner` matching a registered staff member holding `owner_role`, persisted on the case, audited.
* [x] Stamp view payload, boundaries and staff UI with the non-instruction notice and list raised escalations.
* [x] Add `src/api/tests/test_fieldwork_variation_owner_guard.py`.

## Critique

One pass: no instruction-capable path is added; claims of binding or approved variations are rejected with 400. A new work order version stays a separate contract manager and procurement action.

## Validation tier

Focused. No `aria-invalid` added.
