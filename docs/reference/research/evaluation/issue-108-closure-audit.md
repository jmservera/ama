---
title: Issue 108 closure audit against main (2026-11-17)
description: Per-criterion evidence audit of the AI evaluation harness issue against main eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4; offline evidence only
ms.date: 2026-11-17
ms.topic: reference
---

Scope: issue #108, audited against `origin/main` eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Offline accounting only. This page is not actual-model, held-out, human or regional evidence, and it ticks nothing. Delivery is cited as `Refs #108`; the issue stays open.

## Measured on main

* The held-out evaluation split freeze, five-assistant coverage, subgroup accounting and calibration work merged in #1771 sits on the parent branch of #1641, not on main (commit `08c36e4dc` is not an ancestor of main). Treat it as not on main until the parent integrates.
* `ai_eval` task coverage on main exercises six retained paths (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`) with a scripted provider. It reports seven tasks as not evaluated by this harness: `stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`, `chat-case-conversation` and `aftercare-concern-pack`.
* The evidence gate records calibration as not applicable, benefit as not permitted, and actual-model and human effectiveness as not evaluated.
* `candidate_comparison` on main enforces one lever per candidate (`model`, `routing`, `caching` or `prompt`) on the same cases against a recorded baseline. No routing or caching option has been measured.
* Targeted tests on main before this change: `test_ai_eval` 20, `test_candidate_comparison` 19, `test_heldout_freeze` 13 and `test_heldout_batch` 40, all passing.

## Criteria matrix

| Criterion | State on main | Evidence |
| --- | --- | --- |
| Critical misses fail the run | Supported offline | `ai_eval` critical-miss gate and `TaskCoverageTests` |
| Model, prompt version, latency and reviewer outcomes reported | Supported offline | per-run records in the `ai_eval` report |
| Model names, versions and quotas confirmed in region | Open | 2026-11-10 metadata pass; quota limit and unit unknown |
| Benefit not claimed without calibrated results | Supported | evidence gate `benefit_claim` |
| Freeze versions and independently labelled held-out split | Open | `heldout_freeze` checks a manifest; no real manifest or independent labels |
| Cover five assistants and legacy families | Not on main | five assistants and two further families reported not evaluated; the issue body tick needs reconciliation with the 2026-11-17 closure correction |
| Critical errors, usable coverage, subgroups, calibration | Partly on main | critical misses and calibration not applicable are recorded; subgroup accounting is not on main |
| Human participants block seeded critical proposals | Open | no authorised participants |
| Effort and cost comparison against alternatives | Open | no finance validation or effort data |
| Hashes, split, denominators, serving version, usage | Open | scripted runs only |
| Actual-call authorization and serving attestation | Open | no authorization |
| Scripted dry runs not treated as actual evaluation | Supported | evidence gate wording |
| Real AI, SQL and Azure proof (CON-009, AC-057) | Open | not exercised here |
| Cost per accepted proposal; failed cheaper candidate | Supported offline | `candidate_comparison` |
| One routing or caching lever at a time, same cases | Gate on main, nothing evaluated | `LEVERS` and `test_candidate_comparison` |
| Tokens per proposal and spread | Supported offline | `candidate_comparison` |

## Unproved

Actual-model results, an independently labelled held-out set, approved thresholds, human participation, effort and cost comparison, regional model and quota confirmation and serving attestation remain unproved. No new call, spend or approval is inferred.
