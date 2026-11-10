---
title: Issue 136 public simulation lane deployment binding review
description: Single author-inline post-implementation review with routed findings
ms.date: 2026-11-10
---

## Execution

One review executed after `implement-done`, by the implementing session (no nested agent), so it is not independent. It assesses the dirty snapshot on base `d52f20a5198de7269f39daf794911545aee01ced` against the [plan](../plans/2026-11-10-issue-136-simulation-binding-1110-plan.md) and [changes](../changes/2026-11-10-issue-136-simulation-binding-1110-changes.md). It is not repeated; the coordinator's exact-head independent review follows. Review findings become later work and do not reopen this task.

## Scope check

Source paths changed: `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`, `infra/README.md`, `infra/tests/test_bicep_policy.py`, new `infra/tests/test_public_simulation_startup.py`. No `ai.py`, `simulation_lane.py`, API, UI, Dockerfile, workflow or parameter-set change. Conformant.

## Assessment

* Default off: compiled-template diff against the `d52f20a5` base shows OFF differs only by the added parameter, guards, a `null` command, a conditional `maxReplicas` expression and unused variables. Rendered OFF equals the base contract (no command, no `ZF_SIM_*`, max 4).
* Boundaries: five named guards refuse production, non-demo, unauthenticated or bearer-only, no applications, placeholder image and more than one replica; the enabled valid case is accepted with and without `enableApiAi`.
* Accounting: the template fixes `ZF_STORE=mssql`; tests assert it and the unchanged `AI_*` env. Source trace (`begin_call`, `fence_send`, release and hold checks) places allowance and attempts in the working store, not the simulation store.
* Execution: the rendered recipe ran in the real API image at UID 10001 under read-only, no capabilities and no-new-privileges with no entrypoint override; fresh, reuse, partial and corrupt scenarios pass.

## Findings and routing

* F1 (low, not blocking) The recipe imports `simulation_lane` before its `try`, so an image lacking the module would stop the container instead of starting the API with the lane unavailable. The guard requires a real image built from this source, and a changed recipe was not made after `implement-done` to keep the reviewed snapshot identical. Route: later small follow-up under the owning #136 allowance if the coordinator wants it.
* F2 (information) ACA behaviour of `command`, the writable `/state` layer and replica replacement is established only by the local Docker equivalent; no Azure deployment or what-if was run. Route: needs an owner deployment decision outside this task.
* F3 (information) Operator-provisioned durable allowance and release in Azure SQL remain the only live-call control; the template cannot enforce them. Route: unchanged, outside this template.
* F4 (information) The API regression used worktree `PYTHONPATH` because editable installs point at another checkout; one pre-existing ruff RUF100 finding exists in `test_bicep_policy.py`. Route: owning environment and lint ownership, not repaired here.

## Outcome

No blocking finding. Review outcome: `findings routed to later work (F1 low)`. Human, hosted CI and independent exact-head review remain required and are not claimed. All five whole-#136 criteria stay unticked.
