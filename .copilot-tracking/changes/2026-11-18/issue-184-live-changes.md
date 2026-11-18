# Issue 184 live changes (2026-11-18)

Tier: FOCUSED. Docs and evidence only; no `src/` change; no Azure resource created, so nothing to delete. No `rpi-checks.py --all`.

Files: `docs/reference/research/issue-184-live-simulator-stream-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index paragraph), `docs/reference/log.md` (entry).

Adverse/process note: the first `plan-done` witness call (seq 3) was refused because the critique path in state did not resolve; the path was corrected and the retry (seq 4) succeeded. The refusal is preserved in the witness log.

## Per-criterion table (#184)

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | UNPROVEN | #185 and #189 open; no owner deferral; #189 live owner and time limit not demonstrable (control env var unset on the demo API, enabling it is a deployment change excluded by the owner decision) |
| Simulator never connects to, discovers or represents installed real devices | Already ticked, not re-proven | Live runs used `SYN-` demo identities |
| No device key or connection string in source, logs or telemetry | Already ticked, supported | #185 live note: no key text in job output |

Supporting live fact: demo hub budget `budget-iot-cutover-test-rzsrg` USD 25 monthly, two enabled notifications (80 percent actual, 100 percent forecast).

Validation: relative links checked below; `git diff` is docs only.

Witness qualification (seq 5): implement-start reported the docs were already dirty because the evidence note was drafted during research and plan; edits predate that witness. Preserved as is.
