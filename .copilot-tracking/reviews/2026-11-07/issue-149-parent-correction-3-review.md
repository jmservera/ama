---
title: Issue 149 parent correction 3 original author review
ms.date: 2026-11-07
---

## Outcome

Review executed once by the original author. The failure was a checker and test-stub contract error (cell 0 is the EX item ID; the SYN ID is in the source cell), not a product defect. Kind selection, prefix semantics, exactly-once and all-rows outcome checks are intact and no assertion was weakened. The maintained browser checks pass on the corrected source (194 and 100). Author-only; independent review and all human, AT and whole-issue gates remain pending. Residual: hosted CI, and main has moved to bcd86707 without incorporation.
