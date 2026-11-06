---
title: "Changes: refresh PR 1224 onto the advanced parent 149"
description: Changes record for the normal local merge of parent 149 into the issue 233 refresh branch
author: Copilot
ms.date: 2026-11-06
ms.topic: reference
---

Written after the Research, Plan, merge and focused checks. Plan: `../plans/2026-11-06-issue-233-parent-refresh-plan.md`.

## Actual change

* Normal `git merge --no-ff` of `c66f2cdd1bd3f841cd61d8487791931e8762a53c` into `fix/atlas-tensions-233-parent-refresh`, producing `3deec25378f8bc1ba055f243efe767356f04acfc` (tree `bd067b27d7a4fe4c8d97854043aad1a48d50606d`). First parent is `fbf40ec2559b2219fa52c6dba9b55a988369600b` (prospective records on top of published `1addf9c3`), second parent is `c66f2cdd`. No rebase, retarget or main merge.
* Git reported no textual conflict, so no manual resolution and no source edit were needed. `docs/reference/README.md` and `docs/reference/log.md` merged automatically: the 2026-11-05 entries and the new 2026-11-06 issue 153 entry all remain in order, and the diff against each parent deleted no earlier line. GitHub's CONFLICTING state was not reproduced locally; its cause is not established.
* Blob equality: checker `5e4e2d51…`, its test `08151f6f…`, `role-screens.js` `7f12536e…` and `test_role_screens_conformance.py` `99d0df0a…` equal the published head. `doc_controls.py`, `test_document_controls.py`, `test_content_standard.py` and `content-standard.md` equal parent `c66f2cdd`.

## Checks run (no service, external caches in `/mnt/ama-gates/restart-1106-233-conflict/`)

* Imports resolved under `/tmp/a233f` (exit 0).
* Checker, role conformance, document-control and content-standard tests: 54 OK, 0 skips (exit 0). A first run exited 1 with 38 tests and 1 import error because `tests/` was not on the path; that log (`unit.log`) is retained and the rerun (`unit2.log`) added the path.
* 17 atlas trace tests OK. Ruff check and format at 100 columns on the checker and its test, and `mypy --strict` on both: exit 0. `git diff --check` exit 0.
* Not run: browser, gate, SQL, full API suite, native receipt. Issue 86 owns the sole full lane. The earlier receipt (sha256 `17f52dd7…`) and 194-PASS Chromium run are historical for this head.
