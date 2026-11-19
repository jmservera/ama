---
title: Issue 189 deployed run-control verifier and live result (2026-11-18)
description: Code and tests that check the deployed hub owner tag and budget alerts, with the read-only live result and a per-criterion table
ms.date: 2026-11-18
---

Refs #189. Synthetic desktop demo, resource group `ama`, cap USD 700. Only read-only `az` calls were made; no resource was created, so nothing needs deleting. No sign-in or credential file was used. Earlier docs-only passes: [first](./issue-189-simulator-run-controls-live-evidence-2026-11-18.md), [second](./simulator-run-controls-live-189-2026-11-18.md), [third](./simulator-run-controls-live-189-r3-2026-11-18.md).

## What changed in code

`synthetic.run_live_check` (new, `src/core`) turns the deployed-state question into a repeatable check over `az iot hub show` and `az consumption budget list` JSON. Six tests in `src/core/tests/test_run_live_check.py` cover the pass case, noreply and placeholder recipients, a contact group, a placeholder owner, a wrong tier, a missing budget, a disabled forecast alert and the CLI exit codes with no address echo.

## Live result (2026-11-18, read-only)

Inputs: [hub.json](./issue-189-live-state-verifier-evidence-2026-11-18/hub.json) (owner name redacted) and [budgets-redacted.json](./issue-189-live-state-verifier-evidence-2026-11-18/budgets-redacted.json) (local parts of addresses redacted). Output: [verifier-output.json](./issue-189-live-state-verifier-evidence-2026-11-18/verifier-output.json); the command exits 3.

| Check | Result |
| --- | --- |
| owner_tag | pass on the unredacted live capture (raw capture not retained); the retained redacted hub.json holds a placeholder owner and fails this check, as does the retained verifier-output.json |
| hub_tier (B1, 1 unit) | pass |
| budget_cap (USD 25 monthly, `budget-iot-hub-redacted`) | pass |
| alert_actual (80 percent) | pass |
| alert_forecast (100 percent) | pass |
| recipient_reachable | FAIL: both enabled notifications use addresses in a noreply domain |

## Per-criterion table

| Criterion | State | Basis |
| --- | --- | --- |
| Cost estimate for N homes before any run | Proven earlier (ticked) | `run_plan` estimate; unchanged |
| Quota headroom against the #140 tier | Proven earlier (ticked) | Live hub B1 matches the verifier's tier check; unchanged |
| Run has an owner | Observed live; raw output not retained | Owner tag passed on the unredacted capture; the retained redacted copy cannot reproduce it. Blank owners refused in `RunMeter` tests |
| Run has a time limit | Proven in code and tests only | `RunMeter` and bounded job replica timeout; no deployed run exists |
| Run has a budget alert | Configuration proven live by code; delivery UNPROVEN | Alerts enabled, but recipients are noreply addresses; firing needs spend at 80 percent of USD 25 |
| Criterion 3 as one live conjunction | Unproven for the demo | Needs a deployed simulator run (production change, not authorised) and a monitored recipient (owner action, not code) |

The owner ticks; this note does not tick criterion 3.
