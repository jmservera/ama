---
title: Queue dispatch protocol checkpoint 440 research
description: Research for the fourteenth #440 checkpoint on the proposed #144 background-dispatch safeguards
ms.date: 2026-11-06
---

## Identity

Task `queue-dispatch-protocol-checkpoint-440`, a new bounded documentation-only preimplementation checkpoint under the existing OPEN #440. Refs #144 (OPEN), #107, #118, #122. Worktree `docs-parent123-history-checkpoint`, new branch `docs/queue-dispatch-protocol-checkpoint-440`, start `119828353ccc1d678c1a4e9c1c67b621b0d263a0`, ignored-clean. After a fresh `git fetch` (exit 0): governance `feat/discovery-assurance-integration-123` `119828353ccc...`, main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Candidate (read-only, not changed) `/home/azureuser/source/ama-wt/issue-144-queue-recovery` HEAD `4c878d664853074e9dec49e57d5c89c4cc9bf3a2`, tree `978986c9374f6b1019136d121a4ee1f21be7941c`; its merge base with main is main itself.

Research disposition: executed as bounded direct reads of git objects and documents. The skill body was not re-read in this cycle. No subagent was used.

## Pin discrepancy

The brief says `feat/infra-hosting-integration-136` points to main. `git ls-remote origin 'refs/heads/feat/infra*'` returned nothing and `gh api .../branches/feat/infra-hosting-integration-136` returned HTTP 404 "Branch not found" on 2026-11-06. So that branch was not observed on the remote by this author. The brief's statement is supplied, not observed. Candidate `src` vs main differs by 12 files, +1241/-18 (the whole queue transport slice), so parent 136 would equal main only if it carries none of that slice.

## Main versus candidate (static symbol counts, `git grep` on each commit under `src`)

* Main `bb3a3b03`: no `WORKER_ROLE`, `_worker_complete`, `build_serve`, `publish_pending` or `ZF_ASSIST_QUEUE`. It has the ledger (`Consumption.reserve`, `dispatch_check`, `complete`, `liability-unknown`) and `claim`/`complete`.
* Candidate: all of the above exist, plus the single AgentsWorker completion route and the default-off flag (`ZF_ASSIST_QUEUE`, server.py lines 79-88).
* Both: `ai.py` raises `DispatchHeld("financial-meter-unavailable")` when `consumption is None` (line 96-97).

So the queue worker, its role and its single route are unmerged candidate code, not main behavior. The checkpoint must not label them main.

## Source checks of the r8 draft (candidate commit, read-only)

* Ledger transactions: `Assistants.transaction()` (assistants.py 445-465) opens a NEW connection with `BEGIN IMMEDIATE` on every call. `Consumption.reserve` (ai_consumption.py 478) and `Consumption.complete` (653) each open their own `port.transaction()`. The r8 plan names an additive `db` parameter for `reserve` only. `complete` has the same shape and would need it too for the planned settlement inside the completion transaction. Neither is re-entrant, so the "one transaction" claim is unproven and the fallback order (reserve first, then compare-and-set) leaves a window.
* Ledger stop: an uncompleted reservation older than 40 s blocks later reservations (lines 541, 625). `complete` records `liability-unknown` when usage is `None`, the model differs, or settlement is at or after 40 s from the reservation (line 673). So the plan's `complete(meter_id, None, None, "provider-unavailable")` for an unknown outcome always holds liability, and a real settlement after 40 s also holds.
* Retry on unknown: `Assistants.complete` (line 1025) returns a `timeout` or `provider-unavailable` task to `pending` while attempts remain, and line 1052 leaves `active_until` set for those outcomes. `claim` (882) re-claims any expired lease with a new fence. The plan's claim guard (`permitted|dispatching|unknown`) does not say how the existing pending-retry at line 1025 or the attempt `outcome` column (overwritten with the envelope outcome, line 1050) is reconciled with the new states.
* No ledger-clearing route: `git grep` for `clear|reconcile|resolve` functions in `src/core` on main finds only unrelated modules (`exception_queue.clear_outage` is a different component). The budget-wide liability-unknown clearing authority is unspecified.
* Worker side (candidate `dispatch.py`): releases the message on any exception and acks only after the post. API (`server.py` 349-368, route at 1146) accepts the service caller on one route; `auth.service_caller` requires proxy flag and exact worker oid and appid (auth.py 183-194).

## Documents (read 2026-11-06 at governance `119828353`)

| Document | Version and status | Blob |
| --- | --- | --- |
| BRD | 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD | 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0001 | Proposed (queue/worker estate; `agents` app and `agent-tasks` queue) | `d42fa5c4615f4107cee83e07555dba6985c1f53e` |
| ADR 0002 | Proposed (2026-10-24) | `cbe21530043ff15432cc6dce1086d080f5eb15b4` |
| ADR 0003 | Accepted with owner amendment (2026-10-15) | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | Accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Checked IDs: PRD FR-061 (AI consumption economics, joins BRD FR-052/AC-102/AC-103/OD-51) and NFR-017 (bounds and metering, joins BRD NFR-012/AC-100/AC-101/OD-51), verified by PRD AC-107/AC-108 and AC-109/AC-110. PRD AC-109 is the closest criterion (loop or fan-out, reached limit, unknown price, expired authority: dispatch stops with a recorded outcome, no further provider call, workflow-only path). PRD NFR-017 says a missing price or unknown liability degrades to the workflow-only path with an owned alert and requires human approval for live budgets, owners and price sources (BRD OD-51). BRD AC-100..AC-103 and OD-51 exist in the BRD; PRD AC-100..103 are not these.

Candidate mapping corrections: the candidate cites "ADR 0002 decision 6" and "ADR 0002 Five-Assistant Exercise Runtime" as anchors. ADR 0002 is Proposed, and its decision 6 is the Dockerfile and CI item (line 1085), not a dispatch decision. The Five-Assistant section (line 142) says the queue/agent/orchestrator estate "remains proposed" in ADR 0001. ADR 0003 decision 6 is IoT Hub ingestion, unrelated. ADR 0003 decision 1 (accepted) says "No new service, queue, store or network path is added" for the journey capabilities. That is a tension with a background queue that this checkpoint records and does not resolve; the queue estate has only Proposed ADR support (ADR 0001) and the owner decision in this brief is code and design authority, not final ADR acceptance.

## Owner decisions in force (brief, supplied)

Retain duplicate-dispatch and revocation safeguards for the demo; "Include background processing and recovery; design and implement its safeguards first". Code and design authority only. Not a live grant, deployment, provider call, financial-policy waiver, price approval, production budget, operational enablement or final ADR acceptance.

## r8 record qualifications (supplied by the coordinator, kept)

The r8 skill body was not loaded; creation order was Research, Details, Plan, state, log, commit; three originals have no YAML frontmatter; "no network" is not literal (gh metadata); no live Azure, Graph, provider, SQL or browser. Raw log `/tmp/rpi-144-demo-dispatch-design-r8-20261106.log` was not inspected by this author. The r8 diff is 5 files, 238 additions, research/plan/details/state and log only (coordinator-supplied; this author did not re-diff that single commit).

## Open design gaps found (not code defects; no test exists for them)

1. Transaction composition: `reserve` and `complete` each own a connection; atomic permit issue and settlement are unproven on SQLite and SQL Server.
2. Time bounds: lease (default 60 s, allowed 10-120 s), provider timeout (default 20 s, allowed 1-40 s; assistants.py 266 and 285-286), the 40 s ledger window and the permit deadline are four clocks. A configured timeout of 40 s equals the ledger window, so a legitimate late settlement could already be held; the plan binds none of them to concrete values.
3. Attempt state: how `permitted`/`dispatching`/`unknown` coexist with the envelope outcome written into the same column and with the line-1025 pending-retry.
4. Lost permit response: classified `unknown` though no call occurred; it still holds the budget (fail closed) with no clearing authority.
5. Revocation: three distinct windows (before permit, permit to dispatch, after dispatch); a remote permit cannot recall an in-flight call.
6. Late or wrong-fence result: settle the real earlier call using the stored meter id, but do not accept the result; the interplay with the 40 s hold is unspecified.
7. Authority: a second exact worker route is role-code authority not yet approved; the liability-unknown operator path has no named approver.

## Boundaries

No live unsafe call and no newly reproduced production bug is claimed. Existing High findings 1 and 2 (financial-meter-unavailable on the composed worker; redelivery re-inference) stay OPEN. No SQL, browser, container, model, provider or lock work. Nothing in the candidate is changed.

## Planning readiness

Ready for a documentation checkpoint plan. Not ready for #144 implementation until the resume conditions in the plan are met.
