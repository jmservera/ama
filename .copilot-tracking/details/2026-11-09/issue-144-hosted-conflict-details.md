# Details: issue 144 hosted conflict reconciliation (Refs #144)

Plan: [plan](../../plans/2026-11-09/issue-144-hosted-conflict-plan.md).

## P2 command

`git merge --no-ff origin/main -m "merge: integrate main d4d6827f into issue 144 queue slice (Refs #144)"` with repository-local author/committer `8036360+jmservera@users.noreply.github.com` and the Copilot trailer.

## P3 and P4 checks

* `git show MERGE:docs/reference/log.md | grep -c` for the 144 headings and main E1 heading.
* `git diff HEAD MERGE -- docs/reference/log.md` must be additions only.
* `git diff 63d7f8c1 MERGE -- src/agents` empty; `git diff HEAD MERGE --stat -- src infra tools .github/workflows` lists exactly the main paired_equity files; no dependency manifest change.
* `git diff HEAD MERGE --name-status -- .copilot-tracking` shows no modified or deleted original records.

## P5 tests (src/agents, venv /tmp/c1venv, `PYTHONPATH=$PWD/tests:$PWD/../core/tests`)

* `python -m unittest test_queue_azure test_worker test_dispatch test_dependency_rule` expected 49 tests.
* `ruff check`, `ruff format --check`, `mypy` on `src/agents` with the pinned tools.
* Negative `x-ms-date` check: only if source differs; source is expected unchanged, so the earlier recorded negative proof stands and is not repeated.
* `src/core`: `python -m unittest test_paired_equity` as the impacted main-changed core module.

## P6 checks

`git diff --check HEAD MERGE` restricted to authored paths; inherited findings counted separately.
