---
title: Issue 1300 C2 Review
description: One post-implementation code review of the C2 diff (2026-11-10)
ms.date: 2026-11-10
---

Executed once (code-review agent, read-only) on the uncommitted diff. Outcome: one Medium finding.

* Medium: `bound_elsewhere` also ran in default in-tree mode, so a committed in-tree log read from another checkout path would be refused or flagged, changing default behaviour. Valid and caused by this change.
* Disposition: fixed before commit as a recorded post-review amendment (binding applies only with `--evidence-dir`) with an in-tree moved-checkout regression. This amendment was NOT re-reviewed; no second Review ran. The independent exact-head assessment by Root remains required.
* After amendment: 31 unit tests, Ruff check and format on the two files pass. Mistake preserved: a whole-`tools/` formatter run touched 16 unrelated files and was reverted with `git checkout --` on exactly those paths; nothing unrelated is in the diff.
* Limits: the check-to-open race on the trusted evidence directory is not closed; records are local observations, not attestation; synthetic regressions are not native RPI or HVE fidelity.
