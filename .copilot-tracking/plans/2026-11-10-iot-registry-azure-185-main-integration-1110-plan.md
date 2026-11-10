<!-- markdownlint-disable-file -->
# Plan: #185 main integration (2026-11-10)

* Phase 1: ordinary `git merge --no-ff` of origin/main `06374dfcac47cf6bcce9e7b91f573e8565ab45e8`; no rebase, reset, amend, force or transplant. Copilot trailer; local identity from `gh api user`.
* Phase 2: parse the merged `src/core/pyproject.toml` with tomllib; confirm adapter, tests and both README intents survive.
* Phase 3: targeted validation in an own isolated venv, true exits captured with `pipefail`, raw logs external.
* Phase 4: one review, then a final local commit of the dated records, `commit-complete` witness and `verify`.

Stop rules: a substantive conflict, a source or config defect or any refused marker stops for Root; no automatic E2.
