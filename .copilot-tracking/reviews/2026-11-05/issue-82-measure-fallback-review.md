---
title: Issue 82 non-string measure fallback review (2026-11-05, correction 3)
ms.date: 2026-11-05
---

* Execution: author Review, one pass. Outcome: conformant for the bounded defect; not independent assessment.
* The guard is explicit, narrow (unrecognised checklist and non-string, non-None measure only), and yields the existing Unknown and controlled GateError. Valid known-checklist, unrecognised-string and null-measure behaviour are preserved by controls.
* Open and routed later: SQL Server parity for the three new inherited tests (MssqlProcurement) is not run, since heavy admission is held by #96; a new full gate and independent exact-head assessment are required. The 2273ec5f receipt is historical for this commit.
* Other non-string metadata (for example non-string `checklist` already returns Unknown) is not speculatively hardened.
* Whole #82 capacity, authority, finance, eligibility and named rule review stay unmet; reviewer text remains an unreviewed exercise rule. Refs #82.
