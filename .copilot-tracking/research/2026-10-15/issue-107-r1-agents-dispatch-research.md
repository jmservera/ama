---
title: Issue 107 R1 agents dispatch research
ms.date: 2026-10-15
---

Research disposition: executed. Planning Readiness: Ready.

## Task

Step R1 of the src parity matrix (issue #107, epic #195, #199): rebuild the dispatch half of `assistants.py` in `src/agents` so model calls leave the API process, without breaking the `test_assistants` (50) and `test_assistant_release` (16) contracts.

## Evidence

* ADR 0001 (Agents row, identity table): one `agents` app scaled by the `agent-tasks` queue; identity may call Foundry and the queue, and has no database, blob or Key Vault access; it posts proposals to the API, which validates and stores them.
* ADR 0006 and matrix A1/A2: M2 left `assistants.py`, `ai_registry.py` and `assistant_release.py` in `core` because `core` may not import `agents`; R1 is the deferred split. Row R1: "new code only in `src/`". Matrix line 394: #107 stays open for the dispatch rebuild and the queue-driven worker (#144).
* `src/core/.../assistants.py` (1003 lines). Proposal logic (`capture`, `eligible`, `validate_output`, `Limits`, `SYSTEM`, `runtime_binding`) is pure. The SQL half (`claim`, `renew`, `complete`, `scan`, `review`, release gating) owns leases, fences, allowance and quarantine. `execute()` mixes three things: claim, provider call (thread, slot semaphore, watchdog), and shaping the raw result into a bounded envelope and validated output. The API process calls `store.ai.evidence` in a thread.
* `src/core/.../ai.py` `Ai.evidence` already returns a durable-safe envelope (no raw text on failure, no exception text) and needs no SQL.
* `src/agents` today: `ai_eval` only. Its dependency test allows `agents` and `core` imports, and rejects `sql`/`azure` dependencies. `api` depends on `agents` (allowed until #144).
* Tests: `test_assistants` and `test_assistant_release` run in `src/api/tests` on the server harness with a fake provider assigned to `store.ai`. Baseline run on this branch: 110 tests OK, 46 skipped (MSSQL), 34 s.

## Findings

* The queue transport and the HTTP result post-back need an Azure queue client, a service identity and API authentication for the agents caller. Those belong to #144 and infrastructure and need owner decisions; they are out of scope.
* The dispatch (provider call, slot bound, timeout watchdog, shutdown) and the result shaping can be rebuilt in `agents` as a DB-free worker with ports, and the API can compose it today, so there is one dispatch code path and the future queue consumer reuses it.
* Result shaping must stay shared. If `agents` owned it, `core` would need to import `agents`. It is therefore a pure function in `core` (proposal logic, moved as is from `execute`) that the agents worker calls.

## Owner decisions that block parts of #107 (not implemented)

* Release approvers: `ZF_ASSIST_RELEASE_APPROVERS` is unset; named approvers needed.
* Retention of proposal events, envelopes and quarantine digests.
* Break-glass procedure for release suspension and revocation.
* Authoritative serving attestation and Azure SQL race evidence (CON-009/AC-057) need a deployed environment.
* Queue transport identity, poison queue handling and API caller authentication (#144).

## Planning Readiness

Ready. Scope: seams in `core` (extract pure helpers, injectable provider), new `agents.dispatch` worker with queue and result ports, composition in the API, tests, docs.
