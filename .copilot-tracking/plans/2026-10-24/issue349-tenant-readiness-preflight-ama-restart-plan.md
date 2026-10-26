<!-- markdownlint-disable-file -->
---
title: Issue 349 ama-restart plan
description: Bounded plan for diagnosis-only continuation
ms.date: 2026-10-24
---

## Plan

Research: ../../research/2026-10-24/issue349-tenant-readiness-preflight-ama-restart-research.md
Details: ../../details/2026-10-24/issue349-tenant-readiness-preflight-ama-restart-phase-details.md

* [x] Phase 1: Record read-only diagnosis (research complete).
* [x] Phase 2: Independent critique executed before implementation (rubber-duck): verdict Revise. PC-001 applied (direct header provenance, qualified wording); PC-002 applied (scope wording); PC-003 rejected as owner explicitly requires commit and gate for a changed candidate. Critique is not repeated.
* [ ] Phase 3: Implement: no source, infra or live change; write changes evidence and an exact owner intervention plan.
* [ ] Phase 4: Independent review, then commit dated artifacts, rebase only if needed, one external-receipt gate.

## Success criteria

* No source change to the preflight or its tests (no defect found).
* Public 403 cause and prerequisite status recorded without identifiers.
* All live #349 criteria remain unticked; prior reviews and logs untouched.
* Stop before push, PR update or merge.

## Out of scope

Graph/Entra/Azure writes, ingress rule edit, replica change, consent,
credentials, roster, #360 repair, #126 approvals.
