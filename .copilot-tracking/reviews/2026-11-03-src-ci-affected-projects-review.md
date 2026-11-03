# Review: src-ci affected projects (2026-11-03)

Self-review plus validation; independent review and hosted CI remain required.

* YAML parses (`yaml.safe_load`), actionlint clean, 13 unit tests pass, ruff and mypy --strict clean on the new tool.
* Risk: workflow triggers only on `pull_request` and `workflow_dispatch`, so push to main runs nothing new; `EVENT_NAME != pull_request` selects all.
* Risk: if a required check is configured for `mssql` or `src-changes`, confirm names after first run.
* Not verified: a live hosted run.
