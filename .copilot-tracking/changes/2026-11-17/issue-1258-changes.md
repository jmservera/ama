---
title: Issue 1258 changes
ms.date: 2026-11-17
---

## Source changes

None. No file under `src/` is modified.

## Evidence

| Command (from `src/core`, `PYTHONPATH=src`) | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -p test_ranking_publication.py -q` | 57 tests OK |
| Temporary mutation `for parent in opened:` to `for parent in []:` in `_confirmed`, same test command | 12 failures (nested order, ancestor sync failure, retry, partial ancestors, non-writable and symlinked parents); source restored, `git status` clean |
| `ruff format --isolated --line-length 100 --check` on `ranking_publication.py` and `test_ranking_publication.py` | 2 files already formatted |
| `mypy` from `src/core` | Success, 327 source files |

Non-applicable: repo-wide core `ruff format --check src tests` reports 52 pre-existing unformatted files untouched by this task; API tests not run (no change); `rpi-checks.py --all` not run (heavy lock, FOCUSED tier).

## Notes

* The default editable install resolves `zava_forward.core` to the main checkout; `PYTHONPATH` to this worktree was needed so the measurement tested this tree.
* Results are mocked syscall-order and fault-injection evidence, not crash or live filesystem acceptance.
