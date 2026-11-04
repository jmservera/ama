---
title: Issue 111 round 4 research
ms.date: 2026-11-04
---

Research disposition: reused (rounds 1 to 3 plus a fresh PR and issue check on 2026-11-04).

* Merged: #871 (pure exercise analysis), #996 and #1032 (scenario consumers), #1031 (derivation from retained SQL readings). Open: #1075 (status text mirror, slice 3), #1087 (scenario tests).
* Issue comments: bounded read-only slice authorised in principle; closure audit of 2026-10-31 records all three criteria unmet and no ticks.
* Remaining work for the issue: (1) a named human rule approval bound to the policy version, so `SENSOR_REVIEW_DUE` can be proposed; (2) R1 open, R2 competent method sign-off and R3 miss and false-alert limits; (3) SQL Server run of the retained-reading path; (4) UI use plus screen-reader and copy review of #1075.
* Every remaining item needs a human, Azure or legal step. Task creation without an approved rule would break FR-050 (only approved signals create tasks), and a placeholder approval would be fabricated evidence.
* Planning readiness: no coherent unmet-criterion code slice. Docs-only record.
