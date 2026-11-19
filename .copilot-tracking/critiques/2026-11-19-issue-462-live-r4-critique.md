---
title: Issue 462 live r4 critique
ms.date: 2026-11-19
---

Single final-candidate critique, executed. Verdict: proceed.

* Risk: stricter validation could break existing fixtures. Mitigation: the builder and tests already write string ids; run the api preview tests.
* Risk: scope creep into other fixture checks (`_load_fixture`). Disposition: out of scope; only the reviewed comparison changes.
* Risk: blank-string handling is beyond the review text. Disposition: accepted, it is the same "incompletely marked" class and costs one condition.
* Criterion 2 will remain partly unmet after this change (manual score-edit absence and hosted rerun cannot be proven locally); the note must say so.
