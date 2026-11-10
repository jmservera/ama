---
title: Issue 149 parent correction 3 research
ms.date: 2026-11-07
---

## Evidence

Start 0d8c39f1; origin/main now bcd86707 (b284d0d3 was the integrated base; not merged). Admitted browser run failed at `data_operator_browser_check.py:213` after 48 PASS. Earlier data-operator raw data holds one queue-page axe 4.10.3 scan (0 violations, incomplete []); it is not complete per-home coverage, and the earlier no-axe wording stays as corrected history.

Diagnosis, reproduced without a browser by running the actual helper on the real rendered register (`/tmp/zf149-correction3-1107/red.log`): the renderer's Reference cell (cell 0) holds the exception item ID (`EX-001`, `EX-002`); the synthetic IDs `SYN-AI-QUARANTINED` and `SYN-AI-FALLBACK` appear in cell 6 (Source or run reference). Kind selection finds both rows correctly (2 failed rows), but the checker compares cell 0 to the SYN IDs, so the once-each assertion is false. The hand-built stub in `test_kind_label_selects...` put the SYN ID in cell 0, which hid the mismatch. This is a checker and test-helper contract error, not a product defect; product code is unchanged.

Planning readiness: Ready.
