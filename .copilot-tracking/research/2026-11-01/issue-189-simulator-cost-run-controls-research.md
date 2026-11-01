---
title: Issue 189 research - simulator cost, scale and run controls
ms.date: 2026-11-01
task_id: issue-189
task_slug: simulator-cost-run-controls
---

## Research disposition

`executed` (local repository evidence only; no Azure calls). Planning Readiness: `Ready`.

## Evidence

* Issue 189 acceptance criteria: pre-run cost estimate for declared N homes; quota headroom against the #140 tier; run has owner, time limit and budget alert.
* #140 decision (docs/adrs/0003 decision 6; infra/README.md "IoT Hub (issue 140...)"): B1, exactly one unit, uksouth, USD10/month list price, 400,000 messages/day per unit, 4 KiB metering blocks, `monthlyCostEstimate` default 60, monthly budget in `infra/modules/iothub.bicep` (`budget-<hub>`, 80% actual alerts).
* Declared exercise accounting (src/core/README.md): three paired observations per home per day, so 3N records/day (180,000 for N=60,000).
* Existing code `src/core/src/zava_forward/core/synthetic/sensor_stream.py`: `RunBudget` (owner, cost and alert reference strings, max messages/seconds/rate, B1 headroom check over concrete frames) and `Pacer` (pause, stop, deadline, rate). Gaps: no estimate from N homes alone, no recorded pre-run estimate, no cost figure, no budget alert threshold or cap, no start/stop/scale-down control surface bound to a recorded estimate, no CLI.

## Gaps against acceptance criteria

1. Cost estimate for N recorded before run: missing.
2. Headroom vs hub tier: only per-frame; no N-level check, no unit-count scale option (S1/scale-out rejected by #140).
3. Owner, time limit, budget alert: strings only; no cap or alert threshold, no hard limit on unattended duration.

## Constraints

* Source in `src/core`, tests in `src/core/tests`; no mvp/ or prototype/; pip only; no secrets; no Azure deployment.
* Prices are public list estimates, not the subscription quote (infra/README.md).

## Follow-ups

* Wire the controller into the API publisher (#184) and live budget alert verification (#146): out of scope.
