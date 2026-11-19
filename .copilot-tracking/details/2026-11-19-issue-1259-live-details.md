# Details: issue 1259 live DEMO (2026-11-19)

## Phase 1

* Green: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`.
* Red: detached worktree at `cd687abad^`, overlay the current runner test file and `ranking_blob_fixture.py`, run `UnusableArchivePathTests`, remove the worktree.

## Phase 2

* New note under `docs/reference/research/`, row in `docs/reference/README.md` after the run 2 row, append-only entry in `docs/reference/log.md`.

## Phase 3

* Changes file, review file, state update, markdown link check, commit with trailers.
