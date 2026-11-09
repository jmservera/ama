# Details: issue 144 post-policy validation (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09/issue-144-postpolicy-validation-plan.md`.

## Phase 1: identities

```bash
git status --short; git rev-parse HEAD HEAD^{tree}
git fetch origin main feat/slice-144
git merge-base --is-ancestor <old-remote> HEAD
git merge-tree --write-tree HEAD origin/main
/tmp/c1venv/bin/python -c "import zava_forward.agents as a, zava_forward.core as c; print(list(a.__path__), list(c.__path__))"
```

## Phase 2: unit and integration suite

From `src/agents` with `PYTHONPATH=$PWD/tests:$PWD/../core/tests`:

```bash
python -m unittest test_queue_azure test_worker test_dispatch test_dependency_rule -v
```

Expected: 49 tests OK, no skips. Not used: bare `discover`, which lacks the helper paths.

## Phase 3: contract tests

```bash
python -m unittest test_queue_azure.RequestDateTests -v
```

Covers: every operation (receive, poison POST, ack, release) carries a current RFC 1123 GMT `x-ms-date`; the contract transport refuses a missing or stale date with 403; a receive without the header raises `QueueError`. Tests use the injected transport only, so no credential or network request occurs.

## Phase 4: static checks

From `src/agents`: `ruff check .`, `ruff format --check .`, `mypy` (pinned ruff 0.17.1, mypy 2.4.0).

## Phase 5: records and commit

Write changes and review records and the state file under `.copilot-tracking/`; commit with the repository-local noreply identity and the Copilot trailer; verify `git diff 63d7f8c1 HEAD -- src` is empty and the worktree is clean.
