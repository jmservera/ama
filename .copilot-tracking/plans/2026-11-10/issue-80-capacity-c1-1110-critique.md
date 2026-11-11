---
title: Issue 80 capacity browser check time-status expectation, critique
description: Single pre-implementation critique of the C1 plan
ms.date: 2026-11-10
---

Critique executed once on the final candidate plan and details (native author critique, not independent). Verdict: proceed with direct amendments.

* K1 (Medium, applied): a bare "Owner and Next action present" regex in the generic branch could match unrelated text. Amendment: the regex also requires a leading reason sentence (`\S\. Owner:`), and the maintained fixture state uses the exact sentence instead.
* K2 (Low, rejected): add an assertion that the raw API `reason` is not shown. Rejected: that copy contract belongs to `test_timecapture_copy.py`; adding it widens this one-expectation correction.
* K3 (Low, applied): scope guard. Success criteria require reaching `empty capacity`, because the old pass at the `#/time` stage would otherwise hide a later failure.
* No conflict with a confirmed Root decision; no significant or divergent issue needing a user decision.
