---
title: Issue 79 changes, slice 4 (local publication runner)
ms.date: 2026-11-05
---

## Changes

* New `src/core/src/zava_forward/core/ranking_publication_runner.py`: `run` and `main` for schedule, publish and verify over the existing `ranking_publication` and `ranking` helpers.
* New `src/core/tests/test_ranking_publication_runner.py`: 17 synthetic-fixture tests, including a persisted `Store` round trip.
* `src/core/pyproject.toml`: the two new modules join the existing mypy `disallow_untyped_calls = false` group.
* `src/core/README.md`: runner paragraph. `docs/reference/log.md`: 2026-11-05 entry.
* Not changed: `ranking_publication.py`, `ranking.py`, `ranking-v1.json` (still draft, owner `to be named`), `store.py`, Store schema, workflow and gate families, API and web routes.

## Divergence and amendment

* Plan listed no stale or future source handling. The single Review found that a stale or future-dated case file published as current. Amended in the candidate before freeze: a future as_of is refused (`source_future`); an older as_of publishes with a visible `source_not_current` warning (JSON and stderr), because requirements set no age tolerance. Verify still checks the publication date, not data age (routed follow-up).

## Validation (focused, local, synthetic only)

Environment: `/tmp/zf79venv`, pip editable installs of this worktree's `src/core`, `src/agents`, `src/api`.

| Command (from `src/core` unless stated) | Result |
| --- | --- |
| `python -m unittest discover -s tests -p 'test_ranking_publication*.py' -q` | 30 tests OK (after the amendment) |
| `python -m ruff check .` and `ruff format --check` on the two new files | pass |
| `python -m mypy` (strict, tests included) | no issues in 268 source files |
| `python -m unittest discover -s tests -q` (full core suite, before the stale-source amendment) | 2356 tests OK, 226 skipped |
| From `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_ranking_p*.py' -q` | 25 tests OK |

## FULL tier status

FULL gate pending, not run. `/tmp/ama-rpi-heavy.lock` is held by the actual holder, pid 1148896 (`python3 tools/rpi-checks.py --all --jobs 2 --lock-timeout 0` for #188, observed with `fuser`). No duplicate, waiting or queued gate was started, and no focused result is presented as FULL. This candidate is not publishable evidence until a passing external receipt covers the clean actual head and current `origin/main`.

## Criteria after this slice

* Criterion 3 (named owner signs first rule order): unmet, human decision; draft policy unchanged.
* Criterion 4 (scheduled and retained): a local invocation exists; no scheduler is deployed, the schedule is proposed only, the retention period is not set (Legal). Unmet. Use `Refs #79`.
