---
title: Issue 145 changes (1409Z)
ms.date: 2026-11-19
---

Refs #145. No source change; tier FOCUSED (documentation only). Files: research note, README index row, log entry, RPI artifacts.

| # | Criterion | Status |
| --- | --- | --- |
| C1 to C3 | Ticked on the issue | Proven |
| C4 | Backup redundancy and retention match #121 | Unproven, production-only: no approved decision (#1906) |
| R1 | Actual backup restore with document and audit state | Partly proven; drills not authorised |
| R2 | Reconcile and reapply tombstones and holds | Partly proven; no hold state in demo |
| R3 | No resurrection | Unproven; FULL tier needed |
| R4 | DPO approval | Waived for the demo |
| R5 | Independent witness | Unproven |
| R6 to R8 | Disposable limits, labelling, counts only | Proven |

Validation: link and diff review only; no src, mypy or ruff run applicable. Azure: read-only `az sql` calls, nothing created.
