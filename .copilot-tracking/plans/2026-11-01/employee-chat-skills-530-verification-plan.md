# Plan: employee chat skills local verification (#530)

* Research: [employee-chat-skills-530-verification-research.md](../../research/2026-11-01/employee-chat-skills-530-verification-research.md)
* Tier: focused. No heavy local gate; CI is the evidence.

## Phases

* [x] 1. Prepare isolated pip venv, editable core/agents/api, ruff, mypy, playwright, pyodbc.
* [x] 2. Run unit tests: agents, core chat, full API discover (CI invocation).
* [x] 3. ruff check, ruff format --check, mypy for core, agents, api.
* [x] 4. Run employee chat browser and axe check, the CI browser unit test and the employee acceptance check.
* [x] 5. Run SQL contract tests from `mvp-ci.yml` against a disposable local SQL Server container (loopback, random password, removed afterwards).
* [x] 6. Record evidence: this tracking set and a knowledge-base log entry.
* [x] 7. Publish: topic branch commit, push, PR with `Refs #530` naming the unmet live criterion.

## Critique (single pass, direct dispositions)

* Risk: claiming closure from local checks. Disposition: use `Refs #530`; name live verification as unmet.
* Risk: touching another session's SQL container. Disposition: own container `ama-530-sql` only.
* Risk: source churn. Disposition: no source change; evidence only.
* Verdict: proceed.

## Follow-up (added after Copilot review, original plan preserved)

* Run the complete local gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>`) on the committed candidate and verify the receipt with `--verify-receipt` against current `origin/main` immediately before push and independent exact-head assessment. The focused checks above and hosted CI do not replace it.
