# Changes: issue 184 live simulator stream, run 2

Status: complete. Tier FOCUSED; no source files changed (documentation and evidence only). Refs #184.

## Files

* `docs/reference/research/issue-184-live-simulator-stream-run2-evidence-2026-11-18.md` (new note)
* `docs/reference/research/issue-184-live-simulator-stream-run1-log-2026-11-18.txt`, `...run3-log-2026-11-18.txt` (new, redacted raw job output)
* `docs/reference/README.md` (index), `docs/reference/log.md` (entry, `ms.date`)
* `.copilot-tracking/` research, plan, details, critique, changes, review, r2 state (the existing `issue-184-live-state.json` was not overwritten)

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| All child stories closed or deferred | Unproven: #185 and #189 open, no owner deferral | note, sub-issues API |
| Simulator never connects to, discovers or represents installed real devices | Already ticked; live events all `SYN-` and labelled simulated | run 3 log |
| No device key or connection string in source, logs or telemetry | Already ticked; live output has no key text (0 pattern matches in both logs) | run 3 log |
| Issue summary: live stream into hub, symmetric Hub keys, messages reach Event Hub | Proven for the demo: 9 of 9 sent (204) and read back | run 3 log |

## Live actions and cleanup

Created and deleted: job `job-184r2-probe`, 3 role assignments, 3 devices (hub stats 0). Pre-existing 2026-10-16 Data Receiver untouched; the 2026-10-30 Registry Contributor assignment was found missing before my run (not mine, not restored). Run 1 had a short read window and a delete 401 (adverse, retained). Unretained observations (Azure roles, stats, sub-issue states) are Observed; raw output not retained.

## Validation

No source change, so no unit tests, mypy or ruff applied. Markdown links in new files checked by reading; `git diff` reviewed.
