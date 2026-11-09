<!-- markdownlint-disable-file -->
# Details: recovery main reconciliation (#123), 2026-11-09

Plan: [plan](../../plans/2026-11-09/recovery-main-reconcile-123-plan.md).

* Merge: `git merge --no-ff origin/main` with message `merge: reconcile main into discovery assurance integration (#123)`; resolve only understood conflicts, preserving both sides' appended log, index and pack entries.
* Verify append-only: every line of each pre-merge tip's `docs/reference/log.md` appears in order in the merged file (`git diff` of each parent against merge shows no removed lines other than main-only changes).
* Tests (from `src/core`, bytecode off): `python3 -m unittest` on `tests.test_paired_equity` plus coupled comparability/anchor/subject identity modules found by grep; `ruff check`, `ruff format --check`, `mypy` per core config.
* Record exact commands, counts and exits in the changes and review records; no inference from earlier summaries.
