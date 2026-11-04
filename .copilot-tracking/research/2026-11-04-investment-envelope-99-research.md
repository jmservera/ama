---
title: Research for #99 investment envelope and downside controls
ms.date: 2026-11-04
---

* Research disposition: reused (existing evidence adequate); Planning Readiness: Ready.
* Merged evidence: #885 (limits record, assess, pause signal), #1028 (read-only `FinanceMixin.exposure_signal` over a person-supplied limits file), #510 (held ledger entries for OD-12/OD-15).
* Gap found: no API route serves `exposure_signal`, so a Finance user cannot see the pause signal (criterion 2 surface).
* Criterion 1 needs the Board envelope and tolerances (BRD RULE-011, RULE-012, OD-12, OD-15); the closure audit of 2026-10-31 records them as null. This is a human step and stays unmet.
* Slice 1 (this PR): `GET /api/finance/exposure`, role inventory and loopback tests, API README note. Later slices: workbench display and Board-supplied limits file (human).
* Tier: focused; no security, infrastructure, SQL or deployment change beyond reuse of the existing finance-queue permission.
