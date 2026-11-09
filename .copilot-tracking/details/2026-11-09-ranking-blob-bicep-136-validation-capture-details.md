# Details: validation-only capture (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-validation-capture-plan.md`. Refs #136, Refs #1258.

* External log directory (kept): `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/logs-136-validation-capture/run-rhvN6X/`. One `NN-name.log` per command containing the command, cwd, start time, combined stdout and stderr, and `EXIT=<code>`; `exits.tsv` holds the producer exits; `SHA256SUMS` is written after the last check; an `identities.log` holds git, tool and import-path identities.
* Runner: a small shell loop in the bash tool; the logs are produced by the commands themselves with `2>&1`. Nothing is written into the repository tree during checks (`PYTHONDONTWRITEBYTECODE=1`, `RUFF_NO_CACHE=true`, `--no-cache`), so the byte-identity check `git status --short` empty remains meaningful.
* Owned venv: `run-rhvN6X/venv`, created only after the API run fails on a missing or wrong distribution, with `pip install -e src/core -e src/agents -e src/api` from THIS worktree; install output is logged. The venv stays external.
* Pass criteria: exits 0 and the expected counts (100, 25, 45, 35). Any difference is reported as recorded.
* Source qualification: `git diff --stat 95fcaf561a9f046671d2cdf1bac8a6619f703610 HEAD -- . ':!.copilot-tracking'` must be empty, and `git rev-parse HEAD^{tree}` must equal `da8ef003...` before and after the checks.
* Lost records stay lost: the removed raw logs and the invalid ambient primary-import API failure from the integration lane are disclosed as lost, not reproduced; a fresh ambient probe is a new, separately labelled observation.
