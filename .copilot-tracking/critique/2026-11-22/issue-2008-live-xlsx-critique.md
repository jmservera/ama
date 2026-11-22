---
title: Issue 2008 critique, 2026-11-22
ms.date: 2026-11-22
---

Executed once on the final candidate plan. Verdict: proceed with changes applied directly.

* Risk: moving modules breaks `mock.patch("zava_forward.importer.mapping...")` targets. Mitigation: alias via `sys.modules` so one module object; run all importer tests.
* Risk: base64 payload exceeds 8 MB body limit. Mitigation: client checks size (5 MB) and shows a plain message; server returns 400 on bad base64.
* Risk: row preview leaks cell content into errors. Mitigation: reuse importer's fixed reasons; show values only as the user's own file content in their own session; cap rows at 200.
* Risk: formula and macro workbooks. Mitigation: `read_workbook` guards and `LocalSignatureScanner` reused unchanged.
* Risk: scope creep to quarantine staging. Mitigation: preview only, nothing stored.
* Dependency rule: api must not import importer; core only. Add a core-module test.
* Conflict with decisions: none.
