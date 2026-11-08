---
title: "Plan and details: refresh PR 1224 onto the advanced parent 149"
description: Prospective plan with one critique for a normal local merge of the declared parent
author: Copilot
ms.date: 2026-11-06
ms.topic: reference
---

Written after the 2026-11-06 Research and before any merge or repair. Research: `../research/2026-11-06-issue-233-parent-refresh-research.md`. Tier FOCUSED (documentation conflict maintenance, no service). No heavy admission.

## Plan

* [ ] Phase 1: commit these two records on `fix/atlas-tensions-233-parent-refresh` with the gh-resolved noreply identity before repair.
* [ ] Phase 2: re-fetch and assert parent `c66f2cdd` and main; run a normal `git merge --no-ff` of `c66f2cdd` (not a rebase, no retarget, no main merge), preserving published `1addf9c3` ancestry.
* [ ] Phase 3: resolve only `docs/reference/README.md` and `docs/reference/log.md` by keeping both sides. Log entries are appended in context and no earlier entry is edited. Stop if any other conflict appears.
* [ ] Phase 4: prove runtime, checker, test and `role-screens.js` blobs are equal to the parent or published side as appropriate, with no source edits.
* [ ] Phase 5: run existing no-service checks with external caches under `/mnt/ama-gates/restart-1106-233-conflict/`: checker and role tests, atlas trace tests, document-control and content-standard tests, strong Ruff check and format (100 columns), strict mypy on the checker and its test, import source-origin checks, `git diff --check`, JSON and link checks for changed records.
* [ ] Phase 6: write Changes and a separate author Review, commit them, confirm ignored-inclusive clean and freeze locally. No push, PR or issue write.

## Details

* Use the existing own venv only if imports resolve to `/tmp/a233f`; otherwise install with pip into an own external environment after an actual failure. Never use uv or `PYTHONPATH=mvp`.
* Every command that changes files runs with an explicit `cd /tmp/a233f`. Capture each command's own exit code.
* Add the log entry for this refresh only by appending at the end of `log.md`, if the merge leaves the file correct without it no extra entry is made beyond the append-only record of this maintenance.

## Critique (single pass)

* Risk: resolving by taking one side loses an entry. Disposition: verify by diff that every line from both sides remains.
* Risk: claiming the merge proves current behaviour. Disposition: the old receipt and browser run are marked historical and no native receipt is claimed.
* Risk: scope creep to the checker or UI. Disposition: stop on any conflict outside the two KB files.
* No conflict with confirmed owner decisions.
