---
title: Issue 1231 changes (ranking archive concurrent-writer metadata)
ms.date: 2026-11-06
---

## Chronology

* Research, plan, details and issue record committed first: `748526484e76dd8d0c2751bbc6c6be146aeeda63` (2026-11-06T04:41:59Z), before any source or test edit.
* Tests written, then run against the unchanged helper (RED), then the helper changed (GREEN). Raw outputs are external under `/tmp/1231-ranking-archive-r1-1106/` and are not committed.

## Files changed

* `src/core/src/zava_forward/core/ranking_publication.py`: `publish` stages the record in a unique exclusively created same-directory file `.<name>.<random>.tmp` (ignored by `verify`), writes the same canonical UTF-8 bytes and publishes with `os.link` (no overwrite). `FileExistsError` returns the finished record with `written=False` and its original date. Other `OSError` propagates (runner reports `publish_failed`). Only the stage this call created is removed. Docstring updated; helper `_existing` shares the read path.
* `src/core/tests/test_ranking_publication.py`: `CommitGate`/`gated` helper (waits before the real `os.link`/`os.replace`, no faked I/O result), new `ConcurrentWriterTests` (same snapshot, two dates; finished record versus delayed contender; ownership-safe cleanup; real failed link; sequential bytes and name; four spawned processes) and the narrowed no-clock/no-delete scan (forbids `os.remove`, `rmtree`; exactly one `os.unlink(` on the owned stage).
* `src/core/tests/test_ranking_publication_runner.py`: `ConcurrentPublishTests`, the issue reproduction through `runner.run("publish")` with the existing fixtures.
* `src/core/README.md`: concurrent-writer and hard-link qualification; "never overwrites or deletes a record".
* New records: research, plan, details, changes, review, state, `github-issues/issue-1231.md`.

## Evidence (light, external)

* Source proof: `PYTHONPATH=<child>/src/core/src:<child>/src/core/tests` with read-only `/tmp/zf79venv/bin/python`; `import-proof-pre.txt` and `import-proof-final.txt` show the three modules load from this worktree. Pre-change helper SHA-256 `83304551...eed76ad`; final helper `4d222878a5031fbe04b69f7d2c063d2486daac6505483167eeefa94160544c2b`, helper test `ab90c263...b51693`, runner test `9199cd95...c138cc`.
* RED (`red1.log`, exit 1): 48 tests, failures 4, errors 2 against the unchanged helper. First failures retained: `'2026-10-11' != '2026-10-10'` (loser-wins metadata), real `FileNotFoundError` from the shared stage, the delayed-contender and failed-link/cleanup cases, the runner reproduction (error), and the no-delete scan. Separate-process and sequential cases passed on the old helper (the process test does not force an interleaving).
* GREEN (`green5.log`, exit 0): 48 tests OK; five further reruns all OK. API wiring `test_ranking_publication_wiring` 12 tests OK (`api-wiring.log`, exit 0). Ruff check exit 0, Ruff format check exit 0, mypy exit 0 on the three Python files (`*5.*`). Earlier `green1`-`green4`, `ruff-*1/3/4` and `mypy1` outputs are retained, including the Ruff line-length and format failures fixed along the way.

## Divergences and qualifications

* Hard-link support is a new requirement on the archive directory. No production archive mount is defined in the repository. A folder without hard links refuses to publish and overwrites nothing. An owner or deployment decision is needed before an SMB-style mount (for example Azure Files) is used.
* The old no-delete source scan was narrowed deliberately (owned stage only). Assessor to confirm.
* The finished-record test failed on the old helper because the delayed contender raised `FileNotFoundError` (its shared stage was already consumed), not because it overwrote the record. Overwrite of a finished record therefore remains unproven by any run here; the original probe did not claim it either. This coverage is new, not an original probe claim. The old helper also consumed a foreign legacy `<name>.tmp` file (cleanup test RED).
* Not run: FULL, changed gate, SQL, browser, containers, installs, heavy lock, cloud, push. No Windows, network filesystem, scale or production measurement.
