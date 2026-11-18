---
title: Cohort and Missing-Data Evaluation, Third Live Demo Re-run (issue 222)
description: Fresh raw evaluation output and read-only live probe for issue 222 at base 0565b6dc5, with the per-criterion proven and unproven record
ms.date: 2026-11-18
ms.topic: reference
---

Refs #222. Scope: synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). This run repeats [the second live note](./cohort-evaluation-live-r2-2026-11-18.md) at base `0565b6dc5` and retains fresh output in [cohort-eval-live-r3-2026-11-18](./evaluation/cohort-eval-live-r3-2026-11-18/). Synthetic results are not fairness evidence.

## Retained output

| File | Result |
| --- | --- |
| `unittest-raw.txt` | agents `test_cohort_ranking_eval`, `test_cohort_ai_eval`, `test_cohort_manifest_draft`: 36 tests OK; core `test_cohort_eval`: 36 tests OK |
| `ranking-baseline.txt` | status blocked, activation not allowed; insufficient-sample blockers plus one `unapproved_thresholds` |
| `ranking-defects.txt` | seeded `history-2-b`, `history-3-b`, `sensor-1-b`, `sensor-4-b`; all four detected |
| `ai-biased.txt` | seeded `history-3-b`, `sensor-1-b`, `source-2-b`; all three detected; blocked |
| `ai-unavailable.txt` | no-model fallback; blocked on `unapproved_thresholds`, no seeded defects |
| `live-probe-shape.json`, `live_probe.py` | Read-only structure probe of the deployed demo; identifiers dropped, credentials read at runtime and not printed, no screenshot kept because the view shows resident names |

## Live probe

* `ca-cutover-test-demo-api` in `ama`: active revision `ca-cutover-test-demo-api--0000032`.
* Signed in through Playwright with the staff test account: `/api/ranking/policy` 200 (5 rules); `/api/ranking/snapshot` 200 with 443 entries holding only id, rank, reason codes and deciding rule; `/api/ai/priority` 200 with a null recommendation.
* The live snapshot carries no cohort or lawful-analysis attribute, so the cohort evaluation cannot run on live data until an approved field list exists. That matches the OQ-018 gate.
* No Azure resource was created; nothing to delete. Event Hub and the resident app were not needed.

## Per-criterion status

| Criterion | Issue state | Demo status | Evidence |
| --- | --- | --- | --- |
| Paired cohorts evaluated against an expected-outcome manifest | ticked | Proven on synthetic fixture (manifest is a draft) | `unittest-raw.txt`, baseline outputs |
| Seeded unjustified exclusion defects detected | ticked | Proven: 4 of 4 ranking, 3 of 3 AI | `ranking-defects.txt`, `ai-biased.txt` |
| Per-cohort counts, errors, review burden, uncertainty reconcile | ticked | Proven on fixture | per-cohort rows in every output |
| Small or missing samples remain insufficient | ticked | Proven | `ranking-baseline.txt` |
| Exceeded or unapproved thresholds block activation | ticked | Proven: `activation allowed False` in all four runs | all outputs |
| Cohorts, lawful fields and thresholds owner approved before live use (OQ-018) | unticked | UNPROVEN | below |

## Why the last criterion stays unticked

OQ-018 requires named-human owner approval of cohorts, lawful analysis fields, sample sufficiency and thresholds, bound to the manifest digest. The criterion states that synthetic results are not fairness evidence, so no synthetic run can satisfy it, and the demo waives DPO and Legal approval, which removes the route to the approval rather than satisfying it. The blocked record is the correct behaviour and is proven. Do not close #222.
