---
title: Issue 116 live round 4 critique
ms.date: 2026-11-19
---

Executed once on the final candidate plan.

* Verdict: compatible, apply directly.
* Finding 1: bar only the `Contractor` role in `reason_roles()`. `RESIDENT_ROLES` contains staff roles (Resident Liaison Officer, Retrofit Coordinator), so reusing it would wrongly remove a default reason role. Applied.
* Finding 2: the change touches `src/core`, so the FULL tier applies by rule, but the heavy lock is held and the owner forbids `rpi-checks.py --all`. Record the full gate as not run and unmet. Applied.
* Finding 3: do not claim criterion 1 as ticked beyond the demo; DPO and Legal approval stays a production gate. Applied.
