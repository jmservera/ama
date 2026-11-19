---
title: Issue 619 live demo plan details
ms.date: 2026-11-18
---

## Phase 1

Run `employee_proof.py`, `employee_followup.py` in the evidence folder.

## Phase 2

Run `resident_proof.py`; keep failures; do not retry inside the 600 second limiter window.

## Phase 3

Criteria: (1) screen reader, keyboard and zoom recorded by a person; (2) consent step proven with a real resident journey; (#550) consent before data use; (#552) Fluent 2 and WCAG baselines preserved. Mark each proven for the demo, partly proven or unproven with the reason.

## Phase 4

Literal scan for the three credential values; record that resident chat questions have no browser deletion path (four synthetic questions retained, no personal data); commit with trailers.
