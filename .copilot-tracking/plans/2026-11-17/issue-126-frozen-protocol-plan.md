---
title: Issue 126 plan, work-package breach pause
ms.date: 2026-11-17
---

# Plan

Details: [issue-126-frozen-protocol-details.md](../../details/2026-11-17/issue-126-frozen-protocol-details.md)

* [ ] P1 Add a failing regression test: a `work package` breach pauses case events for a case with an active work order in that package, and the pause lifts after authorised restart. Record fail-before.
* [ ] P2 Extend `guard_case_event` in `src/core/src/zava_forward/core/governance.py` to check `work package` scopes from the case's active work orders.
* [ ] P3 Update the breach paragraph in `src/core/README.md` (work package enforced; workstream recorded, not enforceable).
* [ ] P4 Run targeted core tests, ruff format check and mypy for `src/core`; record in the changes file.
* [ ] P5 Review, append the knowledge-base log entry, commit.

Out of scope: #1818/#1641 (mssqlstore, chat grounding), SQL, ticks of the human/cloud-gated criteria.
