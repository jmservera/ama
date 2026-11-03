---
title: Issue 117 round 1 plan
ms.date: 2026-11-03
---

Stacked slices for criterion 1: (1) this slice, visible warning for synthetic scanner on Blob; (2) infrastructure: enable Defender for Storage and set `ZF_SCANNER=defender` (coordinator gate, deployment); (3) real-account evidence.

## Phase 1 (this PR)

* [x] Warning in `open_scanner` when `ZF_SCANNER` is local and the store is Azure Blob.
* [x] Unit test for warning and no-warning cases; README note.
* [x] Focused tests, ruff, mypy.

Final-candidate critique: executed once, verdict compatible. Applied: no hard failure, warning only, so the current deployment is not broken. Details: [details](../../details/2026-11-03/issue-117-r1-details.md).
