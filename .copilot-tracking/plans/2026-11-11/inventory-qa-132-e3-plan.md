---
title: Inventory-managed staff intake and independent QA 132 extension E3 plan
ms.date: 2026-11-11
---

Forward adoption plan for the existing unpublished draft `3c395740`. Refs #132. All boxes are unchecked: nothing in this plan has been implemented. The plan precedes every E3 verification run, which is the point of E3; it does not retroactively change E2.

* [ ] Phase 1: freeze and assert identity. Confirm head, tree, the 53-line diff and the test file SHA-256 above, and that the only worktree changes are the E3 records; any other difference stops the stage.
* [ ] Phase 2: private venv with editable core, agents and api from this worktree, import-origin assertion for each, then the exact E2 focused selectors on the unchanged draft (new cases, full `test_staff_intake_api`, Core `-k inventory`, Core gate selectors, API `-k inventory`, role endpoint inventory and dependency rule, Ruff check, format check, mypy for the api project, `git diff --check`). Retain every raw log and exit; keep failed attempts.
* [ ] Phase 3: current-main compatibility. Fetch is read-only; build a throwaway detached trial merge of `origin/main` in a separate scratch worktree (no commit on the topic branch, no push) and rerun the new cases plus the full `test_staff_intake_api` there with the same import assertions pointing at the scratch tree. If the merge conflicts or fails, record it as a finding; do not resolve by editing the draft.
* [ ] Phase 4: sensitivity diagnostic. In `/tmp` only, a subclass of the committed class (no edit of the committed file) that, after the real `declare_inventory`, patches `Store.require_resident_clear` to a no-op, and runs both cases on the SQLite and JSON classes. Expected: the held accept or handover assertions fail because the call returns 200 or the state moves. Classify each as `sensitive` (failure at the held-accept or held-handover assertion), `inconclusive` (another guard refuses first or the setup fails earlier) or `insensitive` (assertions still pass, which would be a real finding). Do not weaken fixtures, do not manufacture a failure. No MSSQL, cloud or live.
* [ ] Phase 5: bounded browser observation optional and independent, only if the heavy lock is free by `flock -n`; skip otherwise with the reason. Not an acceptance claim.
* [ ] Phase 6: record changes with an honest divergence section, one review after implementation, freeze new E3 records with the original `3c395740` ancestry preserved.

Constraints: no new test or application code; no edit to `test_staff_intake_api.py` or to any existing RPI record or log; no manifest, permission or infrastructure change; no blanket full gate; no push, PR, issue or board write; no MSSQL. If any verification motivates a source edit, stop and route it as a finding; an admitted amendment needs Root's explicit admission and a divergence record, and the original 53-line patch stays byte-identical otherwise.

Stage boundary: this launch stops after the critique and freeze of research, plan, details and critique for Root's prospective plan admission. Details: [details](../../details/2026-11-11/inventory-qa-132-e3-details.md).
