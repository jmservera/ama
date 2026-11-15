---
title: Fieldwork variation named-owner C1 plan (#132)
ms.date: 2026-11-14
---

## Steps

* [x] Store the notice as `contract_notice`, redact `summary` in `projection.hold_notes` and `staff_intake.view` without a recorded need.
* [x] Require text `kind` and `summary`, refuse closed cases and withdrawn orders, run the write inside `_read_dependency`, and fix the `0 == False` bypass.
* [x] Add the `intakeEscalate` form and a fail-closed `intakeNotInstruction` check in `staff-intake.js` (no `innerHTML`, no `aria-invalid`).
* [x] Test SQLite and JSON stores, redaction, validation and a node vm screen test; add the route to `POST_ENDPOINTS`.
* [x] Update `src/core/README.md` and `src/api/README.md`.

## Critique

One critique pass: compatible, no decision conflicts. Focused validation tier; no `--all` gate.
