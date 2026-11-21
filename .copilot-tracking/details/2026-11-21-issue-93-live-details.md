---
title: Issue 93 live plan details (2026-11-21)
ms.date: 2026-11-21
---

* Phase 3: from src/core, `PYTHONPATH=src:tests:../agents/src:../agents/tests python3 -m unittest` over test_finance_no_automated_path_93, test_finance_match_controls, test_finance_signoffs, test_grant_lifecycle_controls, test_exposure_limits, test_funding_automation_boundary, test_form_staging, test_form_review, test_form_review_pack, test_form_dependencies, test_form_export, test_form_criteria_5_6. Run alone, sequentially.
* Phase 4: research note with per-criterion table; link from docs/reference/README.md; append an entry to docs/reference/log.md.
* Phase 5: if a failure shows a real defect, add a regression test and fix, then take the full tier.
