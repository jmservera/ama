---
title: Issue 1231 r20 author review
description: One author Review of the r20 merge of parent79 0a8ecd50
ms.date: 2026-11-07
---

Execution: Complete, author-written, not independent. Outcome: Conformant for local merge; residual work remains.

| ID | Severity | Finding | Route |
| --- | --- | --- | --- |
| RV-001 | Info | Conflict-free merge; delta equals the parent's; child blobs unchanged; targeted checks pass. | None |
| RV-002 | Low | Wider tools/ Ruff diagnostics are baseline from main, not introduced here, and not reformatted. | Main owner |
| RV-003 | Medium | Parent Mediums unconfirmed; cross-UID, unsupported mount, directory-sync and future-date gaps remain; skipped SQL is not acceptance. | Independent review |
| RV-004 | High (process) | Receipts invalid; sole FULL with --lock-timeout 0 on exact head, independent review, hosted checks, new parent integration FULL needed. | Coordinator |
