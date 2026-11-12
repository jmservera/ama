---
title: Research, issue 176 five-home demo cohort replay regression
ms.date: 2026-11-12
---

Task: `issue-176-demo-cohort-replay-2236`. Research disposition: executed. Planning Readiness: Ready.
Base: `origin/main` eac1206c6 (fetched 2026-11-12). Synthetic fixtures only; no private `ZF_DATA`, `.env`, register or user dataset was read.

## Remaining acceptance criteria (read from #176 and its history)

* Criterion 1 (byte identity for every generator including the original stock register and sensor data) and criterion 2 (manifests for every output) stay unmet only for the absent original private register generator and untouched historical manifests. The 2026-11-05 owner-visible reconciliation comment and the 2026-11-04 review state that no new non-human code slice was established and that the owner must supply the original inputs or approve a scope amendment. This task does not touch that boundary and ticks nothing.
* Criterion 3 (refresh policy) is ticked and unchanged.
* Delivered and not rerun: #237, #257, #309, #368, #633, #703, #843, #1052, #1137 (replay audit, fictional register, register-backed sensor stream, protected refresh).

## Distinct gap found

The [demo runbook](../../docs/capstone/demo/runbook.md) (2026-11-12, owner-selected five-home target) names five case ids with property type and stage, and says they came from a local replay at seed 20260901 and as-of 2026-10-13. No test or check references any of them (`grep` for `ZF-2025-0355` and the other four finds only the runbook and log). A generator, seed or as-of change could therefore silently stale the demo cohort while every byte-determinism test still passes, because those tests compare a run with itself, not with the published cohort.

Probe evidence (temporary script, deleted): the committed builder with the fictional 6,000-row register (3 localities, 5 forms, 400 each) already used by `test_generated_dataset.py` reproduces all five ids, with the runbook stages (four Quality check, one Funding check) and property types (End terrace, Mid terrace, Bungalow, Mid terrace, Semi-detached), all open and with no hazard record. The ids, stages and types are reproduced with that fictional register; independence from the register is not established, only that a purely synthetic replay matches the published values. Archetype codes (ARC-nn) are not in the seed output and cannot be asserted locally.

## Boundaries

* The runbook states the ids may differ in the private deployed store; the test proves source replay only, not deployment, sensors, simulator control cohort, AI scope or live readiness.
* Scenario recipe hashes: `scenario-manifest.json` pins `src/core/tests/dataset.py` and the workbench recipe; the new test lives in `test_generated_dataset.py`, which is not a pinned source. Verify with `test_scenario_manifest.py`.
* Out of scope: original register, new generators, climate/provider/cloud calls, live simulator changes, criterion ticks.
