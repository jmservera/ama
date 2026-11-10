---
title: Run state, coordinator behavior run 009 (issue 1204)
ms.date: 2026-11-06
---

* Run type: final fixture-only round, full fresh (report 009 verdict Revise; reuse ineligible). Owner granted exactly one extra round.
* Target blob acefb44a4d254ede6d86413343127b763dec42cb, HEAD 769d620b8ff4aec520fffac1a43e50a45d3b4954 (planning commit), tree 593c7d9f8c1190d7278a9a170701391b24b28006.
* Profile: High responsibility inference, not backend identity. Subagents use harness defaults (no overrides).
* Containment: read-only executor, lead-only writes, all actions emulated.
* Lead pre-execution validation: arithmetic, canonical paths, supplied facts and launch outcomes recomputed (see test-log.md).
