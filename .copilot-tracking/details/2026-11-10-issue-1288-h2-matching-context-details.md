<!-- markdownlint-disable-file -->
# Details: issue 1288 H2 matching-context observation

Readback `date -u` 2026-11-10T00:21Z.

## Step details

* Harness and wrapper live at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/merged-sql-proof-1109/harness_h2_matching_context.py` and `sql-run-h2.sh`; original H0 and H1 files are not touched.
* Wrapper: one invocation under `flock -n /tmp/ama-rpi-heavy.lock`; random loopback port; fresh container labelled `zf.task=1288-h2-sql-disposable`; random SA password never written to logs; own container removed on exit; image id, server version, UTC, head, tree and dirty count recorded; `unittest -v` with the H2 test first, then the existing selectors; exit codes captured.
* Environment: `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, synthetic `ZF_DATA`, `HOME` under the output dir; no Azure, model or network beyond the loopback container.
* Venv: `mktemp -d /tmp/ama-1288-h2-XXXX`, hash-locked `src/api/requirements.txt` then editable core, agents, api. Kept with the raw results until independent assessment.
* Evidence kept externally under `logs-h2-matching-context-1110/` with SHA-256 of each file; durable summaries go into `.copilot-tracking/changes/` and `reviews/`.
* Source identity: product bytes verified equal to `origin/main` (`git diff origin/main HEAD -- src` empty) after the merge.

## Boundaries

* No `release_support.install` on B or C, no release row write, no default `Ai` variant, no guard suppression.
* No push, PR, issue, board, amend, reset or rebase. No shared-doc, source, test or config edit.
