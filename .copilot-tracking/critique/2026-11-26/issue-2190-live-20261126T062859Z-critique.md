---
title: Critique issue 2190 run 20261126T062859Z
ms.date: 2026-11-26
---

Executed once. Verdict: proceed.

* Finding: the first browser-check run failed at the `select option` count (1 of 6) 5 s after the dialog opened; 6 of 7 runs passed. The option list is appended only after `/api/chat/skills` and `/api/chat/status` resolve, so the assertion races the API under load. Compatible disposition: wait for the question input to be enabled (the app's own "loaded" signal) before the count assertion. The count and every other assertion stay unchanged, so no check is relaxed.
* Risk: a longer timeout could hide a real slow API. Mitigation: the wait is bounded at 20 s and fails loudly.
* No deterministic regression test is feasible for a load-dependent timing race; record as unproven.
