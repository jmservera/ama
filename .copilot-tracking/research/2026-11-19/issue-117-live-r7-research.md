---
title: Issue 117 research, pass 7
ms.date: 2026-11-19
---

Task issue-117-live-r7. Research disposition: reused. Planning Readiness: Ready.

* Unticked criterion: "Uploads are scanned before availability" (issue #117, only one).
* Prior evidence: docs/reference/research/issue-117-live-r6-2026-11-19.md (and r2 to r5). Code and tests for the local scanner and Defender adapter exist (src/core doc_controls.py, documents.py, document_rescan.py; src/api tests.test_document_controls).
* Remaining gap: live Defender path needs ZF_SCANNER=defender on the demo API (deployment change) or a storage network-rule change. Both exceed the 2026-11-18 owner authorisation (no production changes). No further buildable code or test is identified.
