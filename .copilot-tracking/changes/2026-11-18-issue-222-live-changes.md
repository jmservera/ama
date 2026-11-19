---
title: Issue 222 live changes
ms.date: 2026-11-18
---

Refs #222. Tier FOCUSED; no src change; rpi-checks --all not run. Note: the research note and evidence were written during Research, before this file; no source file was edited.

## Added

* docs/reference/research/cohort-evaluation-live-r2-2026-11-18.md
* docs/reference/research/evaluation/cohort-eval-live-r2-2026-11-18/ (raw output, probe shape)
* index and log entries

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Paired cohorts vs manifest | Proven (synthetic, draft manifest) | unittest-raw.txt, 36 OK |
| Seeded defects detected | Proven (4/4, 3/3) | ranking-defects.txt, ai-biased.txt |
| Counts, errors, review burden, uncertainty reconcile | Proven (fixture) | all outputs |
| Small samples insufficient | Proven (8 blockers) | ranking-baseline.txt |
| Unapproved thresholds block | Proven | activation allowed False x5 |
| OQ-018 owner approval before live use | UNPROVEN: needs named-human approval; synthetic cannot be fairness evidence; DPO/Legal waived for demo | note section |

## Validation

* 36 cohort tests OK. mypy, ruff and web checks not applicable (no src or web change). Live probe read-only; no Azure resource created.
