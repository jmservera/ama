---
title: Issue 80 r12 review, harness test isolation and README correction
description: Separate later author Review after actual focused checks; not independent acceptance
ms.date: 2026-11-06
---

* Review execution: executed once after the final focused checks and the implementation commit c1a4b577e. Boundary: the r12 test and README diff over 02ca61914 and the r12 records. Author review, not independent.
* Outcome: no findings in the assessed boundary.

## Evidence

* The isolated test patches `harness.ROOT` to an owned temporary directory, so `scratch_parent()` cannot create `.venv` in the real checkout. The checkout `.venv` inode and mtime were unchanged across the run.
* Four harness tests, Ruff, format and mypy exited 0. Production `src/*/src` and `src/api/checks` bytes match 5fa44964.
* README now matches `scratch_parent()` and `child_env()` behaviour (default legacy scratch; absolute external override; unsafe values refused; bytecode controls passed when set).
* Web guidelines: no web source file (HTML, CSS, JS) changed in r12, so no web-interface-guidelines review applies; the guidelines were not refetched.
* Chronology: r11 Research/Plan/Details were concurrent (13:46:25.833-.834) and are qualified here; r12 Research, Plan, Details were serial and committed before edits.

## Not covered

* The unit change is not browser evidence; the harness fix is still unproven by a real run. No FULL, WCAG, owner thresholds, every-list export or independent review. Ignored inputs remain, worktree not clean. The external current-head preservation proof is built after this commit and is observed only in the external handoff. No deletion is authorised.
