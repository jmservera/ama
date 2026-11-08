---
title: Issue 1231 r17 plan critique
description: Prospective one-pass author-only critique of the r17 cf5f57a00 merge plan
ms.date: 2026-11-07
---

Critique execution: Complete, author-run, NOT independent. Written before any mutation. Verdict: proceed.

| ID | Severity | Concern | Disposition |
| --- | --- | --- | --- |
| C-01 | High | A parent move can make a conflict-free merge hide a semantic change. | Parent src delta is only src/api/checks/case_journey_browser_check.py; verify by raw diff and blob identity, not hash of an obsolete tree. |
| C-02 | High | Child privacy (0600), stage_retained diagnostics and winner metadata must survive, alongside the parent's hash, future-date and blocked-exit guards. | Blob identity to 5f904c29 plus the unchanged tests; no assertion edits. |
| C-03 | Medium | docs/reference/log.md is append-only and parent-owned. | Require zero deleted lines; do not edit it. |
| C-04 | Medium | Selector drift: guessed class names. | Selectors are the r16 modules (70 core, 18 API); report actual counts. |
| C-05 | Medium | Import origin could be another checkout. | Print module __file__ for each package. |
| C-06 | Medium | Masked pipelines hide failing exits. | Capture each command's exit code directly. |
| C-07 | Low | The changed browser check is untestable without a browser. | Static checks only; stated as unrun. |
| C-08 | Low | Receipts: the merge invalidates r14, g79 and any stacked claim. | Say so; no current-receipt claim. |

Residual: author critique and Review are not independent; cross-UID permissions, real unsupported mount and directory-sync audit remain unproven. No decision for the owner is needed.
