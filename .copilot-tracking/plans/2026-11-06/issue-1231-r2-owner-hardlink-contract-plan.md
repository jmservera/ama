---
title: Issue 1231 plan r2 (owner-approved hard-link contract verification)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Committed with the research and details before any implementation, test or documentation edit or new probe. R1 files are untouched.

## Phases

1. [ ] Commit these prospective records.
2. [ ] Verify by reading and by a fresh focused run that helper and tests meet the contract; add, if absent, a regression for an actual unsupported-hard-link errno through helper and runner (stage removed, no record, foreign files kept, runner `publish_failed`). Run it against the unchanged source first and keep the raw result under a new unique path.
3. [ ] Change product source only if that regression exposes a real gap; otherwise tests-only or records-only.
4. [ ] Focused checks (core archive/runner tests, API wiring test, Ruff, format, mypy on edited files) with import-source proof.
5. [ ] Write changes, then run a separate author Review, then state, commit, freeze.

## Boundaries

No push, PR, retarget, gh write, cloud, FULL, SQL, browser, container, install, heavy lock, cleanup. FULL, independent feature review and publication stay pending.
