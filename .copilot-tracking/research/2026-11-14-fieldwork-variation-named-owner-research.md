---
title: Fieldwork variation named-owner research (#132)
ms.date: 2026-11-14
---

## Question

Which part of issue #132 ("Variations and escalations reach a named owner and never act as a contract instruction") is unmet?

## Evidence

* `src/core/src/zava_forward/core/job_pack.py` had `escalation()` (named owner, `contract_instruction=False`) but nothing used it.
* `src/core/src/zava_forward/core/staff_intake.py` only exposed a configured destination; no API action raised, persisted or audited a variation.
* `src/api/src/zava_forward/api/web/staff-intake.js` showed a static note and no raised escalations.

## Planning Readiness

Ready. Disposition: executed. Scope: core guard, `field-escalate` action, staff view, focused tests.
