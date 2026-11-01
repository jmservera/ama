---
title: Issue 189 plan - simulator cost, scale and run controls
ms.date: 2026-11-01
task_id: issue-189
---

## Scope

Add `src/core/src/zava_forward/core/synthetic/run_plan.py` plus `src/core/tests/test_run_plan.py` and a short README section. Reuse `RunBudget` and `Pacer`; no transport, no Azure.

## Phases

* [x] Phase 1: `estimate(homes, records_per_home_day, days, message_bytes, units)` returning messages, 4 KiB units/day, quota headroom against 400,000 x units, prorated hub cost (USD10/unit/month list price) and verdict; refuse if over quota or reserved headroom (AC 2).
* [x] Phase 2: `RunPlan` requiring owner, time limit (max 3600 s, matching `RunBudget`), budget cap and alert threshold fraction plus alert reference; `record(path)` writes the estimate as JSON with SHA-256 before a run (AC 1, AC 3).
* [x] Phase 3: `RunController` with `start` (requires a recorded estimate matching the plan hash), `stop`, `scale_down(factor)` (cuts rate and homes, never up) and a hard deadline via `Pacer`; start refuses a second run (no unattended run).
* [x] Phase 4: CLI `python -m zava_forward.core.synthetic.run_plan estimate ...`; tests; README; lint, format, mypy.

## Decisions

* Units fixed at 1 (B1); more units rejected per #140.
* Money figures are planning list prices, labelled as such.
* Critique (single pass, self-run): scope tight; no connection to live publisher; verdict compatible, no conflicts with decisions.

## Correction cycle, PR 707

Plan amended with the two fixes above; no divergence.

## Correction cycle 2026-11-01 (PR 707 review threads)

Two valid Copilot threads on iot_stream.py fixed: eligibility rechecked after admit_send before send_message, and skipped frames no longer advance the replay clock. Regression added; ruff and touched-file mypy clean; tests.test_iot_stream 33 OK.
