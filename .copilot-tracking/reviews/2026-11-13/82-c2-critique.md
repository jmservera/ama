---
title: Issue 82 C2 plan critique
ms.date: 2026-11-13
---

* Executed once (rubber-duck). Verdict: one blocking finding, applied.
* Blocking: a non-string oid normalises to empty, so independence could pass; `_complete` now rejects a supplied non-string oid.
* Non-blocking: tests per field and per person, applied. Invalid `on` is out of scope.
