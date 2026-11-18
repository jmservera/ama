---
title: Cohort and Missing-Data Evaluation, Live Demo Re-run (issue 222)
description: Retained raw evaluation output, read-only live demo probe and per-criterion proven and unproven record for issue 222 on the synthetic desktop demo
ms.date: 2026-11-18
ms.topic: reference
---

Refs #222. Scope: synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). This note supersedes the evidence limits of [the earlier offline note](./cohort-evaluation-demo-2026-11-18.md) by retaining raw output. Synthetic results are not fairness evidence.

## Retained raw output

Folder: [cohort-eval-live-2026-11-18](./evaluation/cohort-eval-live-2026-11-18/), run 2026-11-18 from `src/agents` at the branch base `01de0889e`.

| File | Content |
| --- | --- |
| `unittest-raw.txt` | `test_cohort_ranking_eval`, `test_cohort_ai_eval`, `test_cohort_manifest_draft`: 36 tests OK |
| `ranking-baseline.txt`, `.json` | Deterministic ranking evaluation, no seeded defects: status blocked, activation not allowed |
| `ranking-defects.txt`, `.json` | Seeded defects `history-2-b`, `history-3-b`, `sensor-1-b`, `sensor-4-b`: all four detected as `unjustified_exclusion` |
| `ai-baseline.txt`, `ai-biased.txt`, `ai-unavailable.txt` | AI priority task: faithful, biased (three seeded, three detected) and unavailable modes, all blocked |
| `live-probe-shape.json`, `live_probe.py` | Read-only live probe: structure only, identifiers dropped |

Correction: the earlier note reported seven blockers. The raw output shows eight `insufficient_sample` blockers (every cohort has n=6 or n=42, below the minimum) plus one `unapproved_thresholds` blocker (OQ-018), nine in total for the baseline run.

## Live demo probe (read-only)

* `ca-cutover-test-demo-api` in `ama`: running, revision `ca-cutover-test-demo-api--0000031`. `/healthz` returned 200; unauthenticated `/health` and `/api/ranking` returned 401.
* Signed in with the staff test account through Playwright (credentials read at runtime, not printed): `/api/ranking/policy` 200; `/api/ranking/snapshot` 200 with 443 entries, each holding only an id, rank, reason codes and deciding rule; `/api/ai/priority` 200 with a null recommendation.
* The live snapshot carries no cohort or lawful-analysis attribute, so the cohort evaluation cannot be run against live data without an approved field list. That absence is consistent with the OQ-018 gate and is not a defect.
* A screenshot of the signed-in view was not retained because it showed resident names. Observed; raw output not retained (screenshot only; the shape JSON is retained).
* No Azure resource was created, so there is nothing to delete.

## Per-criterion status

| Criterion | Issue state | Demo status | Evidence |
| --- | --- | --- | --- |
| Paired cohorts evaluated against an approved expected-outcome manifest | ticked | Proven on synthetic fixture | `unittest-raw.txt`; the manifest is a draft, so "approved" rests on the existing ticked review |
| Seeded unjustified exclusion or deprioritisation defects detected | ticked | Proven | `ranking-defects.txt` (4 of 4), `ai-biased.txt` (3 of 3) |
| Per-cohort counts, errors, review burden and uncertainty reconcile | ticked | Proven on fixture | per-cohort rows in the retained outputs and `unittest-raw.txt` |
| Small or missing samples remain insufficient | ticked | Proven | eight `insufficient_sample` blockers |
| Exceeded or unapproved thresholds block activation | ticked | Proven | `unapproved_thresholds` blocker, `activation allowed False` in every mode |
| Cohorts, lawful fields and thresholds owner approved before live use (OQ-018) | unticked | UNPROVEN, deferred | below |

## Why the last criterion stays unticked

OQ-018 needs named-human approval of cohorts, lawful fields, sample sufficiency and thresholds, bound to the manifest digest. DPO and Legal approval are out of scope for the demo (production routes are #1905 and #1906), and the criterion itself states that synthetic results are not fairness evidence. No run on synthetic data can satisfy it. The gate keeps `unapproved_thresholds` in force, which is the intended behaviour. Do not close #222.
