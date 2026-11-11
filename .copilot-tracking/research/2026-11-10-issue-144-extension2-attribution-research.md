---
title: Issue 144 extension 2 result-attribution research
description: Research for binding permitted result attribution to the server-stored reservation root
ms.date: 2026-11-10
task_id: issue-144-extension2-attribution
---

## Scope

E2 of the new finite five-correction grant (E1 used, three left after this cycle). One tightly coupled Medium finding from the independent E1 review (`independent-144-main-port-e1-1110/functional-findings.json`, `assistants.py` 1553-1563). No B scope, no new issue, no consent, provider, spend or live decision. Refs #144 only.

## Disposition

Research executed. Planning Readiness: Ready.

## Base

* Prior candidate `59fd510bd` (E1) merged with origin/main `83c28132ceb7c8609569c4c4fe9f1f9bca1ded58` by an ordinary merge, no conflicts, no rewrite: HEAD `7bb8fc2b3222fb42892910d26cf232fcd2f21fe5`, tree `b0c2ca0a8b0a1ad0bc9ec3e5e2330e53fb337d1a`. The source diff against main stays the five E1 files.

## Actual contract

* `shape_result` copies `meter_id`, `meter_root`, `configuration`, `prompt_hash` from the caller result when they are 64-hex strings. The caller therefore controls them.
* `Assistants.complete` publishes output attribution (`consumption.publish_output(envelope["meter_root"], ...)`) only when `envelope["meter_root"]` is present and the state is not `pending`. `review` records financial review only when `task["envelope"]["meter_root"]` is present.
* `issue_permit` reserves with root `reference(tid)` and returns `meter_id` only. The `permitted` marker stores `meter_id`, owner and fence, not the root.
* `complete_result` with a marker checks owner, fence and `meter_id in (None, marker.meter_id)`, settles the marker meter, then forwards the caller envelope unchanged to `complete`.
* The reservation record (`reserved`) holds `id` and `root`, so the server-side root is recoverable from the marker's `meter_id`.

## Reproduction (real store, owned local fixture, not made-up values)

Scratch harness `144-extension2-attribution-1110/repro/repro_attribution.py` subclasses the existing `ConsumptionApi` fixture, issues a real permit and posts a valid output through `complete_result`. Log `logs/02-repro.out`, exit 0:

* Root omitted: `completed True`, state `ready`, outputs `[]`. The valid proposal has no output attribution, so review accounting is skipped despite a settled permit.
* Root `aaaa...` (conflicting): `completed True`, state `ready`, output attributed to `aaaa...`, not the reserved root.

An import error on the first attempt is kept in `logs/01-repro-import-error.*`.

## Callers

No production caller of `complete_result` exists yet (E1 review, confirmed by search). The only callers are tests.

## Design

* With a `permitted` marker, derive the root from the reservation named by `marker["meter_id"]`. Copy the envelope; set `meter_id` and `meter_root` from the server. Reject a caller `meter_root` that differs, as with `meter_id`, with a `result-rejected` event and `False`, before any settlement.
* Fail closed if the reservation record is not found: reject, no settlement.
* Without a marker, behavior is unchanged (not in the finding).
* Preserved: first completion wins, failed and no-output semantics, refund, closed lease, fence, authority.

## Environment and checks

* Own venv `144-main-port-extension1-1110/venv` (editable core, agents, api in this worktree), ruff 0.17.1, mypy 2.4.0.
* Heavy lock `/tmp/ama-rpi-heavy.lock` was free at the probe (non-queued `flock -n`). Disposable SQL is only run if the existing project fixture and tool prerequisites are already available; otherwise reported blocked.
