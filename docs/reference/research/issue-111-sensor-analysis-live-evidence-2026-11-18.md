---
title: Issue 111 sensor analysis live evidence and R1 to R3 disposition
description: Per-criterion record for the unticked R1 to R3 criterion of issue 111 on the synthetic demo
ms.date: 2026-11-18
---

Refs #111. Scope: synthetic demo, desktop only, docs and evidence only. No source change, no Azure change.

## Criteria

| Criterion (issue 111) | Disposition | Evidence |
| --- | --- | --- |
| Outputs are reproducible from retained readings (ticked) | Not re-opened | Local run 2026-11-18 of `src/core` `test_sensor_scenarios` and `test_sensor_analysis`: 33 tests, OK, one expected failure |
| Thresholds are sourced or labelled exercise values (ticked) | Not re-opened | See the status table in the [research plan](iot-sensor-analytics-research-plan.md) |
| Research phases R1 to R3 are complete before a derived measure is used beyond an exercise rule (unticked) | Unproven, cannot be proven on the demo | Below |

## Why the R1 to R3 criterion cannot be proven on the demo

* The gate wording in the [research plan](iot-sensor-analytics-research-plan.md#phases) makes R2 pass only when a competent building-physics reviewer and Asset sign off the method as a candidate, and R3 only when methods meet agreed false-alert and miss limits. Both are named human approvals. A running demo cannot supply them, and the owner decisions of 2026-11-18 do not authorise an agent to stand in for them.
* R1 stays open: the 2026-10-14 source verification records that the official BS 5250, BS EN ISO 13788 and PAS 2035 texts were not read (paywalled or mirrored only).
* R3 bounded evidence exists locally (seeded scenario pack, fixed-truth confusion summary) but the plan states it is exercise-only and does not complete the gate.
* The demo enforces this gate by design: derived measures stay exercise values and review-only.

## Live probes (2026-11-18, resource group ama, read-only)

| Probe | Result |
| --- | --- |
| `GET /healthz` on `ca-cutover-test-demo-api` | 200 |
| `GET /health`, `/api/health`, `/openapi.json` without sign-in | 401 |
| Active revision | `ca-cutover-test-demo-api--0000031` |
| Browser navigation to `/app` (Playwright) | Redirected to the Entra sign-in page ([screenshot](issue-111-demo-entra-gate-2026-11-18.png)) |

A signed-in walk of `/api/cases/{id}/sensors` was not performed: it would show exercise-value output only and could not change the R1 to R3 disposition. No credential was printed or stored, no resource was created, and no cost-bearing action ran.

## Unmet

* R1 official standards texts, R2 reviewer and Asset sign-off, R3 agreed limits. Issue 111 criterion 3 stays unticked.

## Evidence limits

* The test count and the HTTP probe results are observed but not retained as raw output.
