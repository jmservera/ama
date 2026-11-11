---
title: Issue 132 keyboard probe E4 validation continuation amendment
description: Additive prospective amendment authorizing diagnostic typing and record-completion selectors for the E4 candidate (issue 132)
ms.date: 2026-11-11
---

## Identity

Native CLI session `3daf20c8-310c-4926-85ce-96019ffd6646`. Worktree `issue-132-keyboard-compat-plan-1111`, branch `test/demo-intake-keyboard-compat-132-1111`, head `f8939a5a438b3fac62c548d2a42c50f36f8a2778`, tree `b2b765c565a82fff758292e688cf084b41c55e35`, base `35eb0e559c7d0660ab87594732675b71be7bee67` (`origin/main` unchanged, fetched), worktree clean at start. This is bounded E4 validation and record completion, not a new source correction. Original C5 and E1 to E4 remain spent; E5 remains. Any source fix needs a separately admitted E5. Prior records are not rewritten.

## Executable blobs to remain unchanged

* `src/api/README.md` `e2bcbbcbbecbc4dbc24b6b9a135eb60ba96c1d5e`
* `src/api/checks/specialist_keyboard_browser_check.py` `0df2dcec1be63db93e8b99bb8d9ff3cb06915917`
* `src/api/tests/test_specialist_keyboard_check.py` `f8633117257b6f51624a538a292529f54021e993`

## Source CI typing contract (read before runtime)

`.github/workflows/src-ci.yml` project job (api): `pip install -e ../core -e ../agents -e ".[dev]"` from `src/api` on Python 3.12, then `mypy` in `src/api` with no `MYPYPATH`; tests then `ruff check . && ruff format --check .`. The earlier E4 run instead used `pip install -e core -e agents -e api` after separately installing pinned dev tools, and then an ad-hoc `MYPYPATH=../agents/src`. That is not the CI command and does not establish a baseline or harmlessness of the two `unused-ignore` errors.

## Disclosure of the earlier typing sequence

Full-project `mypy` ran more than once in the original E4: (1) before any restore, 24 errors in 10 files; (2) after the private installs without `MYPYPATH`, 4 errors in 1 file; (3) with `MYPYPATH=../agents/src`, 2 errors in 1 file. The Changes record said "once"; that wording is inaccurate and is corrected here, additively.

## Admitted selectors (diagnostic only)

1. Record environment origins and versions (private HOME, cache, TMP, venv only; no credentials, `.env` or default data).
2. Create a fresh private venv and restore exactly the CI install for api; no other projects, extras, tools or shared environment.
3. ONE configured `mypy` from `src/api`, no `MYPYPATH`, full stdout and real exit captured to files.
4. If it fails, ONE type-only baseline run on an isolated external checkout of the base commit with the same tool versions, install origins and config; no edits, runtime, browser or SQL. Failure on base does not make a failed check a pass. No third mypy run without Root approval.
5. If typing resolves: one `ruff check` and one `ruff format --check` per CI (`.`) and the seven unit tests once. No new browser; the earlier single browser result stays retained only for the same executable blobs and does not cover axe, assistive technology or human review.
6. Copy the original Author Review section verbatim into the dated reviews file with `f8939a5a` provenance, copied-not-rerun, linked to Changes. It is placement, not a fresh or independent Review.
