---
title: Issue 530 focused actual SQL and chat browser route critique
ms.date: 2026-11-08
---

* Execution: one independent read-only rubber-duck pass (agent `critique-c3`) before any check. Verdict: Revise. Not repeated.

## Findings and dispositions

* F1 Blocking, applied: the unit suite's loopback `/healthz` call is explicitly authorised and recorded; it is not an external or live call.
* F2 Blocking, applied: lock ownership is explicit. The runner acquires the canonical lock itself with `--lock-timeout 0`; an inherited lock needs `--heavy-lock-fd`, to be named at admission.
* F3 Non-blocking, applied: selection is not execution; browser and SQL need separate evidence and 21 unique `ok` SQL headers.
* F4 Non-blocking, applied: the 3 GiB container limit, Chromium and axe downloads, capacity and short output path are admission requirements.
* F5 Non-blocking, applied: record test-module origins and the final freeze; LIGHT results are source-equivalent, not exact-final-head.
