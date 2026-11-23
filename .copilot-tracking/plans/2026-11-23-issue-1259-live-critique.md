---
title: Critique, issue 1259 live run 8
ms.date: 2026-11-23
---

Executed once. Verdict: proceed.

* Test-only change keeps the FOCUSED tier; do not touch src.
* The EACCES case must skip under uid 0 and restore permissions in cleanup so the temp dir is removable.
* Reuse the existing `check_unknown` scenario mechanism rather than a parallel test.
* Failing-first: mutate `_require_creatable`/`_names` to prove the new cases fail.
