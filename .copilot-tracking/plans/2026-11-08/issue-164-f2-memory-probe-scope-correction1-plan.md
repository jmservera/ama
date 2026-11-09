---
title: Issue 164 F2 correction1 plan
description: Prospective plan for corrective RPI correction1, written before the critique and implementation
ms.date: 2026-11-08
---

## Scope

Edit `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/tests/test_chat_eval.py` and the memory paragraph of `src/agents/README.md`; add correction1 tracking records. Original records are untouched.

## Phases

* [x] Phase 1: Research ([research](../../research/2026-11-08/issue-164-f2-memory-probe-scope-correction1-research.md)).
* [x] Phase 2: Plan, details and one independent prospective critique ([critique](../../challenges/2026-11-08/issue-164-f2-memory-probe-scope-correction1-critique.md)); CR1-001 to CR1-004 accepted into the details.
* [x] Phase 3: Implement and record changes.
* [x] Phase 4: Focused validation, one Review, commit.

Details: [phase details](../../details/2026-11-08/issue-164-f2-memory-probe-scope-correction1-details.md).

## Constraints

* Outcomes, rates, gates, bindings and task state unchanged; only descriptive memory fields change.
* New regression cases must fail on `b2f35d06`; verify by running them against the base blob.
* Focused tier only with external caches and `PYTHONDONTWRITEBYTECODE=1`; actual exit codes captured. Hosted checks and independent exact-head assessment remain gates.
