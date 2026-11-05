---
title: Issue 82 corrupted replacement plan (2026-11-05, continuation)
ms.date: 2026-11-05
---

* [ ] Phase 1: tests first that fail before the change (details: `../../details/2026-11-05/issue-82-corrupted-replacement-details.md`).
* [ ] Phase 2: narrow `submit_quality` change.
* [ ] Phase 3: ordinary merge of origin/main bb3a3b03c, light checks (JSON/pure only, external caches, bytecode off).
* [ ] Phase 4: commit; full gate and SQL selectors pending coordinator admission.

## Critique (single pass, self-run)

* Replacement allowed only when every in-progress record for the measure is corrupted (gaps or unreadable); any valid in-progress record keeps the refusal. Applied.
* Caller must hold a quality role (QUALITY_ROLES) for this route; other callers keep the refusal. Applied (conservative reading of "existing authorized roles").
* Fresh evidence validated exactly as today; binding required as today. Applied.
* No edit of originals; replacement starts Submitted and goes through independent acceptance. Applied.
* SQL store shares the code path; SQL selectors are planned for the final gate (`test_quality_procurement.SqlFlows`), not run now.
