---
title: Ranking archive ancestor durability 1258 continuation review
description: Author review of the boundary and API coverage additions
ms.date: 2026-11-08
---

Review execution: Complete (author review, once). Outcome: Residual work. The original review (Residual work) is preserved and not regraded.

* R2/DV-3 addressed for non-root: direct non-writable boundary test; root-run covered by a mock only.
* R3/DV-2 addressed: API-level parent-fault 409, audit, original bytes and sound retry.
* Still open: R1 real crash durability, R4 extra-sync visibility, FULL receipt and verification, independent exact-head assessment, hosted checks, named approvals. Issue criteria not proven; Refs only.
