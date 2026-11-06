---
title: Issue 79 details, continuation r15
ms.date: 2026-11-06
---

## Phase 2: tests (before source)

* `src/core/tests/test_ranking_publication.py`
  * garbage, truncated and different-content final file: `publish` raises `PublicationError`, bytes unchanged.
  * deterministic race: wrap real `os.link` so a competing publish with another date completes first; the loser returns `written` False with the winner's date and the retained bytes are the winner's.
  * multi-process race: several processes publish the same snapshot with different dates; exactly one writes, all report the retained date, `verify` is clean, no temp files remain.
  * fsync of file and directory is observed through a counting wrapper around the real `os.fsync`.
* `src/api/tests/test_ranking_publication_wiring.py`
  * corrupt final file: publish returns an error and no `already_published` audit entry exists.
  * unsigned publish: response and audit detail contain the unsigned state.
  * status with `os.listdir` raising `PermissionError`: 200 with a problem entry.

## Phase 3: source

* `ranking_publication.py`: `_check_existing`, temp via `tempfile.mkstemp`, `os.link`, `_fsync_dir`, cleanup in `finally`.
* `store.py`: `publish_ranking_snapshot` adds `policy_signed` to audit detail and response; `ranking_publication_status` catches `OSError` and derives `overdue` from one result.

## Phase 4: documentation and records

* `src/core/README.md`: first-writer-wins and validated existing record, `run_key` and same-window meaning.
* Changes, Review (after checks), state JSON, commit with repository-local privacy-safe identity and the Copilot trailer.
