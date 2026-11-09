---
title: Issue 149 parent preparation for child 229, changes
ms.date: 2026-11-07
---

## Changes

* No source edits. Two normal merges: origin/test/ux-evidence-149 dbeab436 (adds #1237 c66f2cdd and #1224) as d99a68a2, then origin/main f0afa8d7 as merge commit cbde9ff9. Ancestry of both verified; no rebase, reset, amend, force or push.
* Conflicts: none. Parent `role-screens.js` blob now equals main (55f503d5); `data_operator_browser_check.py` is still byte-identical to main.
* Main-relative delta (`git diff origin/main...HEAD`, 55 files): 11 non-RPI files, all from child 233 and 153: atlas_tensions_browser_check.py, test_atlas_tensions_checker.py, test_content_standard.py, test_document_controls.py, test_role_screens_conformance.py, doc_controls.py (+8/-2, message text only), src/api/README.md, atlas-screen-trace.md, content-standard.md, docs/reference/README.md and log.md, plus the original 233 and 153 RPI artifacts preserved byte-for-byte.
* Own-scope inherited paths: src/api/checks/atlas_tensions_browser_check.py, src/core/src/zava_forward/core/doc_controls.py and the four test files above.
* Tier: FOCUSED, from original 153 and 233 evidence plus this main-relative diff. doc_controls.py changes only two exception strings; legal-hold and retention predicates, audit events and deletion behaviour are unchanged. Any logic change there would require FULL.

## Light checks (literal)

Run with PYTHONDONTWRITEBYTECODE=1, caches in /tmp, this worktree's src first on PYTHONPATH (doc_controls resolved to this worktree).

* From src/api: unittest test_atlas_tensions_checker test_content_standard test_document_controls test_role_screens_conformance test_exception_register_screen: Ran 69 tests, OK.
* src/api: ruff check . passed; ruff format --check . reported 118 files already formatted; mypy --cache-dir=/tmp/mypy-149 reported no issues in 191 source files (tests included).
* src/core: ruff check . passed; ruff format --check . reported 213 files formatted; mypy --cache-dir=/tmp/mypy-149 reported no issues in 266 source files.
* Skipped by instruction: real browser, axe, SQL, containers, images, scans, `rpi-checks.py` (--changed and --all) and the heavy lock. Not run: full suites. Merge commit d99a68a2 lacks the Co-authored-by trailer and is not amended.
* Not claimed: browser evidence, UX, WCAG, assistive-technology or usability acceptance, resident or legal approval.
