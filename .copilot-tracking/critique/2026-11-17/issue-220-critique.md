---
title: Issue 220 plan critique
ms.date: 2026-11-17
---

# Critique (single pass, final candidate)

* Verdict: proceed. Scope is one test plus a documentation note; no store, legal approval, hazard-clock or #1818/#1641 change.
* Risk: the new test may expose a real defect; if so, the smallest fix in `src/core` or `src/api` follows, with the test as regression.
* Criterion 5 must stay unticked; the note must not claim representative acceptance or measured delay.
* Disposition: all findings compatible, applied directly.
