---
title: Issue 121 s3 research
date: 2026-11-04
---

Disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged PRs)

* #919: register, `model_dispatch` gate, task field declarations, rights clock (core, reference-only).
* #1013: read-only `GET /api/data-protection`.
* #281 and #614: chat DPIA record and closure audit; no criterion proven.

## Findings

* `model_dispatch` has no caller outside tests; model calls happen in `core/ai.py` (`Ai.run`, `Ai.look_at`, `Ai.evidence` via `_request`). Raw bytes reach `look_at` with no derivative path.
* Installed editable packages point at another worktree; focused tests need PYTHONPATH to this worktree.
* Existing tests call `look_at` and `run` with constructed text, so default behaviour must not change.

## Remaining unmet

All four issue criteria (DPO, Legal, approved transfer, rights log answered) and all RAI criteria except constructed fixtures. Human or SQL work remains: owner decisions, persisted rights log.

## Chosen slice

Wire the gate into the transport with a fail-closed processing mode (`ZF_DATA_PROCESSING`); no SQL, infra, deployment or auth change. Privacy-control sensitive, so the complete gate is left to the coordinator.
