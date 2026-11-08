---
title: Issue 1231 changes r8 (api test line wrap)
ms.date: 2026-11-06
---

## Chronology

* Prospective scope committed `8ce843573` at 16:50:19Z before any edit (author and committer `8036360+jmservera@users.noreply.github.com`). Edits and checks followed.
* The Plan file's estimated 16:51Z is later than the commit time; the commit time is authoritative.

## Changes

* `src/api/tests/test_ranking_publication_wiring.py`: line 87 split into a local `unsupported = OSError(number, "hard links unsupported")` plus the unchanged `patch.object(os, "link", side_effect=unsupported)`; line 111 split into `actions = [...]` plus the unchanged `assertEqual(actions, ["ranking_snapshot_published"])`. Values and assertions are identical. 4 insertions, 2 deletions. No other file.

## Checks (outputs `/mnt/ama-gates/restart-1106-1231/r8/`)

* Environment: read-only shared `/tmp/zf79venv`, Ruff 0.17.3 (pin 0.17.1), not isolated or pinned. `PYTHONPATH` bound to this worktree; `import-proof.log` shows `server.py` and `store.py` load from this worktree. Source-bound, not an installed candidate distribution.
* Ruff check across all `src/api`: exit 0. Ruff format --check across `src/api`: 115 files formatted, exit 0.
* `test_ranking_publication_wiring`: 14 tests OK, exit 0.
* Original failure (r7 `0053-project-api.log`, E501 at lines 87 and 111) and the earlier four-file Ruff scope omission are preserved.

## Limits

r7 is invalidated for this new head and was not resumed. No FULL, SQL, browser, image or scanner work. A fresh FULL, independent review, hosted CI and publication remain pending.
