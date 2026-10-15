---
title: Issue 197 parity matrix changes
ms.date: 2026-10-15
---

* Added `docs/architecture/mvp-to-src-parity-matrix.md`.
* Edited `docs/reference/README.md` (catalog row, task routing row) and appended an entry to `docs/reference/log.md`.
* Added the RPI artifacts for this task.
* Validation: file-coverage script reported 125 tracked files and none missing; unit suite baseline 703 tests OK (92 skipped); relative links checked.
* Divergence: none from the plan. Open: confirm ADR 0006 alignment, `devtools` package, job placement, PR 287 handling.

## Fix iteration (PR #291 review)

* Merged `origin/main` (ADR 0006 accepted, PR 287 merged); kept both `docs/reference/log.md` entries.
* Edited `docs/architecture/mvp-to-src-parity-matrix.md`: targets follow ADR 0006 exactly, amendments A1 to A5 stated, rows for `assistant_release.py`, `release_support.py` and `test_assistant_release.py`, 450 sandbox files mapped as retire (S1), PR 287 wording and hold action removed, owner answers recorded, counts 128 files and 719 tests (92 skipped).
* Edited the `docs/reference/README.md` catalog row and appended a log entry.
* Validation: coverage script found no missing tracked path; unit suite 719 tests OK (92 skipped).
* Divergence: none. Open: owner decision on A1 to A5.
