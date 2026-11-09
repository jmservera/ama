---
title: Issue 1231 changes r2 (owner-approved hard-link contract verification)
ms.date: 2026-11-06
---

## Chronology

* Prospective r2 research, plan, details committed first: `a5bf43d4d` (2026-11-06T07:57:43Z), before any edit or run.
* Then two characterization tests were added and run against the unchanged helper (50 tests, exit 0; `pre-fix-run1.log`). They did not fail first: the helper already propagates a hard-link-unsupported `OSError` and the runner already refuses. No source gap was found, so product source is unchanged (helper SHA-256 `4d222878a5031fbe04b69f7d2c063d2486daac6505483167eeefa94160544c2b`, same as R1 final).

## Files changed

* `src/core/tests/test_ranking_publication.py`: `test_filesystem_without_hard_links_refuses_and_publishes_nothing` (`os.link` wrapped to raise `OSError(EPERM)`; the error propagates; no record; foreign files byte-identical; later real publish succeeds).
* `src/core/tests/test_ranking_publication_runner.py`: `test_filesystem_without_hard_links_is_a_refusal_and_writes_no_record` (runner returns `publish_failed`, no `written`, empty archive, later publish succeeds); added `errno` and `os` imports.
* New r2 records: research, plan, details, changes, review, state. R1 records and external R1 outputs are untouched. README, owner memory, case study, index and log untouched.

## Evidence (light; raw outputs under `/mnt/ama-gates/1231-r2-light-1106-0757/`)

* Imports: `import-proof.txt` and `import-proof-final.txt` show the helper and both test modules load from this worktree via `PYTHONPATH=<child>/src/core/src:<child>/src/core/tests`, using the read-only `/tmp/zf79venv/bin/python` 3.12.3.
* Core archive and runner tests: three full runs of 50 tests OK (`core-run1` to `core-run3`), final run OK (`core-final`); no skips. API wiring `test_ranking_publication_wiring` 12 tests OK (`api-wiring`).
* First failures retained: `ruff-check.log` (exit 1, I001 import order in the runner test) and `ruff-format.log` (exit 1, one blank-line reformat). Fixed with Ruff, rechecked: `ruff-check-2`, `ruff-format-2`, `mypy-2` all exit 0 (mypy also exit 0 in `mypy.log` before the fix).
* Tools: ruff 0.17.3 and mypy 2.4.1 in the shared venv versus project pins 0.17.1 and 2.4.0. Not an isolated package, not FULL.

## Limits

The errno injection is the only simulated element; no real hard-link-unsupported mount was tested. Windows, network filesystems and production unmeasured. No deployment or mount change, retention, legal or policy decision was made. Not run: FULL, changed gate, SQL, browser, containers, installs, heavy lock, cloud, push. #144 untouched.
