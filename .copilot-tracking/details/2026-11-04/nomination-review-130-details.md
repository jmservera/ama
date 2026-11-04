---
title: Issue 130 nomination human review details
ms.date: 2026-11-04
---

## Details

* Fields: `case_id`, `id`, `expected_version`, `outcome`, `rationale`, `evidence_ref`, `next_update`; any other field is refused.
* Outcomes: Accepted for human eligibility review; More evidence needed; Not progressed; resident may challenge.
* Review record keeps `record_version`, `reviewer`, `competing_evidence_versions`, `at`.
* One review per version. A correction adds `stale_from_version` to earlier reviews and requires a new review.
* AI-unavailable and manual paths: the action is staff-recorded, with no AI dependency; non-digital route is already mandatory at intake.
