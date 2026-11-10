---
title: Research - numeric boundary defects in the constructed paired report loader (Refs #216, #208)
description: Prospective reproduction of two Medium findings from the independent assessment of ab365e53
ms.date: 2026-11-10
---

## Execution

* Research disposition: executed (local reproduction plus reading `run_regulatory_gates.py` and `paired_trial.py`). No nested agent.
* Task: bounded correction D1 of the initial report consumer, one debit; historical whole-issue balance UNKNOWN, no reset and no automatic D2 or D3.
* Start: clean head `ab365e53d024e269c9ad4f0b0e33a8361a43e30b`, branch `feat/demo-constructed-paired-report-216-1110`. Source of the findings: `independent-216-paired-report-1110/functional-findings.json` (approve_with_comments, two Medium, read in full). They are not reclassified.

## Prospective reproductions (actual, before any change)

Run from `src/agents` with the owned venv (`/home/azureuser/source/ama-demo-wt/.venv-issue216-1110`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0), `--homes 100`.

| Input | Result on current head |
| --- | --- |
| Cards `elapsed_seconds` 5e-324, chat `elapsed_seconds` 31536000 | exit 0, 21819 bytes of stdout containing `"elapsed_ratio": Infinity` (not interoperable JSON) |
| Cards `elapsed_seconds` minus sign plus 401 digits | exit 1 with a Python `OverflowError: int too large to convert to float` traceback, stdout empty |

## Findings

* F1: `evaluate_paired_trial` divides the chat mean by the cards mean (`paired_trial.py` line 91). The one-year cap bounds sums but not the ratio, so a subnormal positive cards value yields `inf`. `json.dumps` writes `Infinity` by default.
* F2: `valid_observation` calls `isfinite` before checking negativity. A huge negative integer is below the positive-only cap and raises `OverflowError`. Python compares int and float exactly, so `value < 0` is integer-safe.

## Decisions for planning

* Keep the scorer, schema, thresholds, cost and authority unchanged. Add a negative check beside the upper bound. Evaluate the section and serialize it strictly (`allow_nan=False`) before the baseline report is generated or anything is persisted, converting only that `ValueError` into an option-prefixed refusal.
* Default report bytes must not change. Existing `--record` semantics are preserved. The reviewer's `--record` canonical-overwrite observation is out of scope and not guarded.
* Configured mypy covers `src` and `tests`, not `evals/`; script strict typing is supplementary.

## Planning Readiness

Ready.
