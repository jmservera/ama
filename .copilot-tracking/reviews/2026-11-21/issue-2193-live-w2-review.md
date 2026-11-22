---
title: Issue 2193 review, wave 2
ms.date: 2026-11-21
---

Review executed once. Outcome: Conformant locally; two items remain unproven.

* Source diff is a DOM reorder plus one test; behaviour of chart and states unchanged. 71 web tests and mypy pass.
* Live proof recorded without credentials in probe output.
* Routed later work: deploy the reorder when production change is authorised (rank 1); observe stale, offline and withheld homes live when one exists (rank 2).
