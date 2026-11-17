---
title: Fieldwork variation named-owner C1 research (#132)
ms.date: 2026-11-14
---

## Research disposition

Executed against independent review `independent-direct-132-variation-0290f27cc.md`. Planning Readiness: Ready.

## Evidence

* `staff-intake.js` showed escalations but had no raise form and hardcoded the non-instruction cell.
* `projection.hold_notes` overwrites every `NOTE_KEYS` entry, including the `note` that carried `NON_INSTRUCTION_NOTICE`, and left `summary` raw. `staff_intake.view` returned raw `summary` to roles without `can_see_reason`.
* `escalate` coerced `kind` and `summary` with `str(...)`, did not guard closed cases or withdrawn orders, and did not use `_read_dependency`.
* `reject_instruction_claim` used `not in (None, False, "")`, and `0 == False` let a numeric zero pass.
* The role endpoint inventory lacked `field-escalate`, and the guard test ran only on the SQLite store.
* Editable installs resolve to another checkout, so validation used `PYTHONPATH` to this worktree's `src/*/src`.
