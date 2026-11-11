---
title: Issue 80 capacity C5 critique
description: One native critique of the C5 plan (not independent)
ms.date: 2026-11-10
---

Executed once on the final candidate plan; native author critique, not independent. Verdict: proceed with dispositions.

* Considered and rejected: guarding `null` in app code (`? exportLink : ""`); production already tolerates `null` and an app change would be a fallback around a fixture gap.
* Considered and rejected: loosening the failing assertion; the failure is a stub crash, not an assertion.
* Risk, accepted: other test stubs for `show` may share the gap; only the one that fails is changed, and the whole `test_case_journey` module is run to find any other.
* Risk, accepted: the browser run is carried (source unchanged, hashes recorded), not repeated; valid because no served file changes.
* No conflict with a confirmed Root decision.
