---
title: Run state, coordinator behavior run 010 (issue 1204)
ms.date: 2026-11-06
---

* Run type: admission-threshold correction validation (owner "fix 1204 and merge"); fresh evidence bound to the new instruction blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5 at HEAD 72cfd55e0662f819b98ab7e075e68897611c9711. Prior sandboxes, reports 005 to 010 are historical and not reused as passes.
* Design was authored against intermediate blob aa175c95c23fe92eddb1b9db1fb611e9b40f6783 (commit 4d1cff62). The final edit (F1 to F3 of the independent static review) changed only unavailable-state wording and clearing record; lead found every scenario expectation unchanged except that an unavailable drain record now means: rebuild from evidence and admit none while a confirmed count is above 15, and an unavailable count means admit none and re-read.
* Profile: High responsibility inference; subagents at harness default; no overrides.
* Lead arithmetic rechecked: N-01 7 to 8 each at 15, 16 and 20 PRs; N-02 21 to 20 PRs, 7 to 6 assignments; N-03 20, 16, 15 (6 to 7), 9 (5 to 6); N-04 8 to 8; N-05 6 to 7; N-06 6 to 7 with #746 counted; N-07 7 to 8; N-08 6 to 7. 13 forty-hex and 9 sixty-four-hex values verified.
* Lead prompt edits: removed the common line "No scenario supplies an outcome for an admission that should be barred" and the N-05 sentence "Under the dependency rule, #730 may only run as a stack ...". Mapped requirements, signals and arithmetic tables were not given to the executor.
