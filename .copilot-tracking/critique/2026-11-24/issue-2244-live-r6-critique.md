---
title: Issue 2244 live run 6 critique
ms.date: 2026-11-24
---

Executed once on the final candidate plan. Verdict: proceed.

* Finding 1: forcing the lock to prove C4 is a drill the owner excluded. Applied: C4 and C5 are recorded unproven, no Azure change.
* Finding 2: copying the whole test file from the other branch would delete tests present on this base. Applied: add only the new test class.
* Finding 3: a src change takes the full tier. Applied: targeted core tests plus mypy and ruff for src/core; no `rpi-checks.py --all`; the coordinator runs gates.
* Finding 4: deployment is a production change reserved to the owner. Applied: stays a follow-up.
