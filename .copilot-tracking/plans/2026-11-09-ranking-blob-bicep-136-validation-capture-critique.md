# Critique: validation-only capture plan (2026-11-09)

* Executed once, before any check, by an independent read-only rubber-duck agent. Not repeated. Verdict: Revise. Five findings, all compatible with the brief and applied directly (no conflict with a confirmed decision, no user decision needed).

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | Blocking | Commit of records before checks changes HEAD, so "tree still `da8ef003`" cannot hold | Applied: validate that every path outside `.copilot-tracking` is byte-identical to `95fcaf561` and `3de2c2f4c` (`git diff --quiet`), and record the separate validation HEAD and tree |
| C2 | Significant | Checks or editable installs could write into the worktree; `git status` misses ignored files | Applied: `az bicep ... --stdout`, `PYTHONDONTWRITEBYTECODE=1`, `--no-cache`; compare `git status --short --ignored` before and after, record any install-generated metadata |
| C3 | Significant | Ruff 0.17.3 ambient differs from CI pin 0.17.1 | Applied: install `ruff==0.17.1` in the owned venv for the CI-equivalent commands; ambient 0.17.3 run separately labelled; RUF100 baseline retained unsuppressed |
| C4 | Significant | Import provenance excludes Agents; venv was conditional | Applied: all Python checks run in the owned venv created up front with editable installs of this worktree; print Core, Agents and API file paths and fail if any resolves outside this worktree. A single labelled ambient probe records the primary-checkout resolution |
| C5 | Significant | `REQUIRE_AZ_BICEP=1` and skips not recorded | Applied: set it for infra tests, run `-v`, record skipped counts and assess them explicitly |

The plan's phase 2 and 4 and the details' venv and byte-identity rules are superseded by this table where they differ.
