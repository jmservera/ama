---
title: Critique, open-PR admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

* Executed once by an independent rubber-duck agent at harness default (read-only). Verdict: Revise, 3 findings. Not repeated.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | Blocking | Drain state underspecified across ticks and when unknown | Applied: details define initialise, persist in ledger, read before admission, fail closed when unknown |
| 2 | Blocking | Drain could stick below 10 if clearing needs 10 to 15 | Applied: clear at a confirmed count of 15 or fewer, including a jump below 10 |
| 3 | Non-blocking | Scenarios could miss a multi-tick trajectory | Applied: scenario G trajectory 21, 20, 16, 15 and jump below 10 |

* Target grep found no other restatement of the 16 to 20 band.
