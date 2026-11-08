---
title: Issue 1231 details (ranking archive concurrent-writer metadata)
ms.date: 2026-11-06
---

## Mechanism

`publish` keeps validation, `makedirs`, the exists pre-check and the returned shape. For a missing target it creates a unique staging file in the same directory with `os.open(..., O_WRONLY|O_CREAT|O_EXCL)` named `.<final-name>.<random hex>.tmp` (ignored by `verify`, which lists only `ranking-*.json`), writes the exact canonical text as UTF-8 (same bytes as before), then calls `os.link(stage, final)`.

* Link succeeds: this caller is the single publisher; return `written=True` with its own `published_on`.
* `FileExistsError`: another writer finished first; read that record and return `written=False` with its actual `published_on`.
* Any other `OSError` (including a filesystem without hard links) propagates unchanged, so the runner reports `publish_failed`; no fallback and no overwrite.
* A `finally` removes only the staging file this call created (it created it exclusively). Foreign temporary files, including a legacy `<final>.tmp`, are never touched. A missing stage at cleanup is the only tolerated condition.

## Regression plan (tests first, RED on the unchanged helper)

In `test_ranking_publication.py` (real files in a temporary directory, no I/O result faked; a gate wrapper only waits before the real `os.link` or, on the old helper, `os.replace`):

* Same snapshot, A `2026-11-05` and B `2026-11-06` as threads, both held at the publication step, A released then B: exactly one record, A published with written True, retained bytes carry A's date, B returns `written=False` and A's date, no exception, archive verifies, no stage left.
* Existing finished record versus delayed contender: B passes the pre-check and is held; A publishes completely; B released: bytes and date unchanged, B returns A's date with `written=False` (new coverage; not an original probe claim).
* Ownership-safe cleanup: foreign `ranking-...json.tmp`, a dotted foreign `.tmp` and an unrelated file survive both a successful publish and a publish whose link step really fails (a wrapper raises `PermissionError` in place of the link; the stage is removed, no record is created, the error propagates).
* Sequential: bytes equal the canonical text, the filename is unchanged, the second caller is idempotent with the original date.
* Separate processes: N spawned processes (spawn context, barrier-aligned start, distinct dates) publish one snapshot; exactly one `written=True`, every returned date equals the retained bytes' date, one record, verify clean. Qualification: the OS schedules the interleaving, so this checks the invariant under real process concurrency but is not a forced interleaving; local POSIX filesystem only.
* Narrowed guard `test_module_has_no_clock_and_no_delete`: still forbids `datetime`, `import time`, `os.remove`, `rmtree`; allows exactly one `os.unlink(` call on the owned staging path.

In `test_ranking_publication_runner.py`: the issue reproduction through `runner.run("publish", ...)` with the real helper and the existing `signed_registry()` and `open_cases()` fixtures: A `published`/Nov 5, B `already_published`, written False, Nov 5, retained bytes Nov 5, verify clean.

## Checks (light, external outputs)

From `src/core`, `PYTHONPATH=<child>/src/core/src:<child>/src/core/tests`, `PYTHONDONTWRITEBYTECODE=1`, `/tmp/zf79venv/bin/python` read-only; print `__file__` and SHA-256 of the helper and both test modules to prove the child sources. Run `-m unittest` for the two modules, `ruff check --no-cache`, `ruff format --check --no-cache`, `mypy --cache-dir /tmp/...` limited to the touched files. Every command writes to a unique path under `/tmp/1231-ranking-archive-r1-1106/`; a retry gets a new path. Not run: gate, SQL, browser, Docker, install, lock, cloud, push, cleanup.

## Qualifications to repeat in every later record

* Hard-link support is now required on the archive directory; no production archive mount is defined in the repository. Unsupported mounts fail loudly, never overwrite. Owner/deployment decision needed before an SMB-style mount is used.
* The unlink-scan guard was narrowed deliberately; independent assessor should confirm.
* One original interleaving was confirmed; overwrite of a finished record is reasoned and is only demonstrated by this task's new regression against the old helper.
* Windows, network filesystems, production likelihood unmeasured.
