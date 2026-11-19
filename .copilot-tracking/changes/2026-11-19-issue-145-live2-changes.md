---
title: Issue 145 live2 changes
ms.date: 2026-11-19
---

Added docs/reference/research/issue-145-live-20261119T1419Z-2026-11-19.md, an index row and a log entry. No source, infra or Azure change; no resource created. Tier: focused, documentation only. Validation: Git diff review; new note links resolve.

| # | Criterion | Status |
| --- | --- | --- |
| C1 to C3 | Parameters, PITR, objectives | Proven (ticked) |
| C4 | Redundancy and retention match #121 | Unproven, production-only (Legal period deferred to #1906) |
| R1 | Actual backup with document and audit state | Partly proven; no new drill authorised |
| R2 | Reconcile, reapply tombstones and holds | Partly proven; no hold state in demo |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven; code gap on the release-authority path needs FULL tier |
| R4 | DPO and record-owner approval | Waived for the demo |
| R5 | Independent qualified witness | Unproven, human |
| R6 to R8 | Disposable limits, labelling, counts only | Proven (ticked) |
