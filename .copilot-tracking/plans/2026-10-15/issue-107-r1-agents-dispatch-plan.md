---
title: Issue 107 R1 agents dispatch plan
ms.date: 2026-10-15
---

Research: [research](../../research/2026-10-15/issue-107-r1-agents-dispatch-research.md). Details: [details](../../details/2026-10-15/issue-107-r1-agents-dispatch-details.md). Critique: [critique](../../plans/2026-10-15/issue-107-r1-agents-dispatch-critique.md).

## Phases

* [x] Phase 1: core seams, behaviour preserving. Extract `build_request` and `shape_result` from `Assistants.execute` as pure functions; add an injectable `provider` port (default `store.ai.evidence`).
* [x] Phase 2: `agents.dispatch` worker: `TaskMessage`, `ResultMessage`, `Provider` port, `AgentWorker` (slot bound, timeout watchdog, shutdown, no DB), `TaskQueue` and `ResultSink` ports with in-memory implementations, `run_once`.
* [x] Phase 3: compose in the API: `Assistants(store, provider=...)` wired to the agents worker provider call; no behaviour change.
* [x] Phase 4: tests in `src/agents/tests` (no SQL, no core store), dependency rule and image identity still pass.
* [x] Phase 5: docs: matrix R1 status, agents README or index, `docs/reference/README.md`, `docs/reference/log.md`.
* [x] Phase 6: validation, changes artifact, one review, commit, push, PR.

## Out of scope (owner decisions or #144)

Approvers, retention, break-glass, attestation, Azure queue transport, API caller authentication, removing in-process SQL leases from the API.
