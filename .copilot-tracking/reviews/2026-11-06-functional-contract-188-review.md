---
title: Review for #188 functional findings F1 and F2
ms.date: 2026-11-06
---

* Review execution: once, author-only, after checks and after reading the final diff (3 files, +45/-10). Not independent. Human checkbox unchecked. Independent finding file not modified.
* F1: reproduced, corrected, regression added. F2: reproduced, corrected, regression added including no replay writes. Indoor exact-schema check keeps independent of consumer admission; weather acceptance untouched.
* Limitations: the seed `-0` branch of the new test only exercises that spelling when the generated seed is "0"; the equal-seed ("184") case is the actual coverage and `-0` equivalence follows from `int()` but is not separately exercised. Distinct seeds do not authenticate independent provenance. SQLite/constructed only; no owned SQL rerun. Fresh FULL and independent assessment required on the new head.
* Chronology: Research, Plan and details were committed before the RED and edits. Earlier adverse records preserved unchanged.
