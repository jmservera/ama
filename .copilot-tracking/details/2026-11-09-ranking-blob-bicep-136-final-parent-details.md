# Details: final-parent integration and validation (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-final-parent-plan.md`. Refs #136, Refs #1258.

* External log directory (kept, never auto-removed): `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/logs-136-final-parent/run-XXXXXX/` created with `mktemp -d`. Each command writes `NN-name.log` with command, cwd, start time, combined output and `EXIT=<code>`; `exits.tsv`, `SHA256SUMS`, `run.sh` and `run-stdout.txt` are kept beside it. The owned venv lives inside it and is not evidence.
* Merge: `git merge --no-ff 9b1e2567c2d0a2173b562103cd27508f75181526 -m "merge: integrate frozen #1258 SQL-main parent (Refs #136, Refs #1258)"`, then record `git rev-parse HEAD HEAD^{tree}`, `git diff --stat HEAD^1 HEAD` (what the parent brings) and `git diff --stat HEAD^2 HEAD -- . ':!.copilot-tracking'` (what #136 adds over the parent).
* Overlap classes expected: parent-only (SQL store, priority order, docs research), #136-only (Bicep storage/containerapps/guard, main.bicep, infra README, params, `test_bicep_policy.py`, API settings), shared (`store.py`, `server.py`, READMEs). Shared files are inspected by diff after the merge, not assumed.
* Pass criteria: every selected exit 0, no unexpected skips in the targeted selectors, and counts recorded as measured against the stated baselines. Differences are reported, never adjusted.
* Inherited adverse expectation: isolated ruff on `src/api/tests/test_ranking_publication_wiring.py` exits 1 (10 errors) as in the parent. If it passes, report that as a difference from the parent.
* Tool identities recorded: ruff pinned 0.17.1 inside the venv and ambient version, azure-cli, bicep, Python, pip freeze for the editable installs, `git status --short` and `git status --ignored --short`.
* Preserved and untouched: the earlier records, the coordinator proof file and `run-rhvN6X`. Lost raw integration-lane logs are not claimed to exist.
