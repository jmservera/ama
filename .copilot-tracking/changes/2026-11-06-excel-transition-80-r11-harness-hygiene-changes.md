---
title: Issue 80 r11 changes
description: Harness hygiene correction and preservation proof, no deletion
ms.date: 2026-11-06
---

* Plan: [plan](../plans/2026-11-06-excel-transition-80-r11-harness-hygiene-plan.md). Research: [research](../research/2026-11-06-excel-transition-80-r11-harness-hygiene-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r11-harness-hygiene-details.md).

## Chronology (actual)

* Research, plan and details committed as 004c0a005 at 13:46Z, before the first test or harness edit.
* Test file written first; RED run: 4 tests, 4 errors (no `scratch_parent`), log `/mnt/ama-gates/e80-r11-r64-1106/logs/red-a1.log`.
* Harness edit, README note, checks, preservation proof, then this record.

## Changed tracked paths

* `src/api/checks/design_system_browser_check.py`: new `scratch_parent()` (ZF_BROWSER_SCRATCH, absolute and outside the checkout, else the legacy `.venv` as before) and `child_env()` (PATH, HOME, LANG plus PYTHONDONTWRITEBYTECODE and PYTHONPYCACHEPREFIX when set); `main` uses both. Defaults unchanged.
* `src/api/tests/test_browser_harness_scratch.py` (new, 4 tests, no server or browser).
* `src/api/README.md`: short paragraph.
* Schema check, assertions, requests and production `src/{api,core,agents,importer}/src` trees: unchanged; tree hashes equal at 1fa33543 and HEAD for all four.

## Light results (pipefail, bytecode disabled, caches under /mnt/ama-gates/e80-r11-r64-1106/)

* Ten modules together (new one plus the nine r9 modules): rc 0, 124 tests, 0 skips (`logs/ut-a1.log`).
* Ruff check rc 0, format check rc 0, mypy rc 0 over 188 files.
* Imported check and server modules resolve under this worktree. PYTHONPATH of worktree sources was used for these unit modules; the later browser or FULL run must use this candidate's pip-installed distributions in an owned external environment.
* No new ignored paths appeared during r11 (status shows only the original three).

## Preservation (no deletion)

* Archive `/mnt/ama-gates/e80-r11-r64-1106/preservation/snapshot.tar.gz`, sha256 198e5bf5...e7487, 8183 members: whole `.copilot-tracking` snapshot plus the exact generated members, symlinks not followed. Tool note: `tools/tracking_retention.py` is bound to the PR 438 manifest and cannot select these paths, so a small external script (`../preserve.py`) was used under the same policy steps.
* Readback: 8183 expected, 8183 seen, 0 mismatched, 0 extra.
* Restore attempt a1 FAILED mode comparison (stock tar filter strips group write bits); preserved as `restore` and `restore-proof-a1-failed.json`. Attempt a2 with a mode-preserving filter into new `restore-a2`: 8183 of 8183 identical in type, mode, sha256 and link target.
* Protected: tracked index 8720 entries (file hash in `hashes.txt`); no tracking file modified since the snapshot.
* Pending manifest `/mnt/ama-gates/e80-r11-r64-1106/pending-manifest.json`: exact four paths (5, 5, 61 members and the empty `.venv`), status pending, deletion not authorised. All ignored inputs remain present; the worktree is not clean.

## Not done

* No browser rerun, FULL, lock, SQL, install or cleanup. The harness fix is unproven end to end until an admitted browser run shows no new ignored files. Independent review, hosted CI, owner thresholds and every-list exports remain pending.
