# Details: align #107 candidate onto final main

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-align-plan.md).

1. Poll `gh run view 42361331168` for at most about 10 minutes; then `git fetch origin main` and record the final SHA.
2. Read formatter config (pyproject, CI workflow, tools/rpi-checks.py) for the Ruff format scope; run the configured command on the base file and on the candidate; compare diagnostics for the added block only.
3. `git branch backup/issue-107-4aa717009 4aa717009`; `git rebase origin/main`; confirm patch-id of the test commit and that `git diff` of the test file against the candidate is empty.
4. From `src/api`: ruff check, mypy, release selector (46 tests), with `PYTHONDONTWRITEBYTECODE=1` and the documented test path; report skips.
