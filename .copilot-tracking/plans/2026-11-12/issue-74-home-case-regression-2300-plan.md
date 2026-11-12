---
title: #74 home case regression plan
ms.date: 2026-11-12
task_id: issue-74-home-case-regression-2300
---

* [x] P1 `src/api/tests/test_home_case_api.py`: append two HTTP tests after the last test. (a) non-finance staff (sam) gets 200 with `cost_allocation_restricted`, `cost_allocation` None, `costs_restricted`, no `costs` on the building, and neither "6000.00" nor "12000.00" anywhere in the raw body, for both homes. (b) finance staff (pam) gets allocation 6000.00 for ZF-2 and ZF-3 and building cost 12000.00, unrestricted flags. No `funding_confirmed` assertion. Details: [details](../../details/2026-11-12/issue-74-home-case-regression-2300-details.md).
* [x] P2 `src/api/checks/home_case_browser_check.py`: seed ZF-2 with its own document and quality in `home_case_data()`; open ZF-2 then ZF-3; assert per home own document and quality tokens in the home region only and not the sibling's anywhere; assert SYS-1 "Shared ventilation" in the building region only on both homes; keep every existing check.
* [x] P3 Run focused checks under the shared heavy lock: API test file, core `test_home_case.py` (impacted regression), modified browser check with the pinned axe (sha256 880970c0...8bb).
* [x] P4 Scratch-copy mutation controls for each new assertion family; keep adverse outputs; nothing mutated left in the tree.
* [x] P5 Changes record, one author Review, state, result JSON, local commit, no push.

Critique: one independent rubber-duck critique of this plan and the details before P1; see [critique](./issue-74-home-case-regression-2300-critique.md). Out of scope: product source, G5, outcome tuple, criterion 2 tick, funding assertions, full gate.
