---
title: Assistant Task Data Contract Enforcement (Issue 121, 2026-11-23)
description: Enforcement of the declared per-task data contract on the five assistant tasks before any provider text is built, with a per-criterion table for issue 121
author: AMA programme
ms.date: 2026-11-23
ms.topic: reference
---

## Scope and result

Synthetic demo, desktop only; owner decisions of 2026-11-18 apply. No Azure resource was created or changed, and the demo apps were not redeployed (production change is out of scope), so the new behaviour is proven offline. No legal interpretation is made and DPO or Legal approval is not claimed.

Gap closed: the [issue 2311 note](./issue-2311-task-contracts-2026-11-23.md) recorded that the five assistant tasks declared a contract but their request builder did not enforce it. `assistants.build_request` now calls `task_contracts.enforce` with `case_id` and the canonical evidence as `source_snapshot`. A refusal is handled on every runtime path:

* Permit path: `_permit_block` returns `data-contract`, the attempt is refused with the manual-route reason and no provider call is made.
* Claimed execution: the task completes with outcome `data-contract-refused` and a manual-review message.
* Agents worker (`dispatch.py`): a failure result with the same outcome and no provider call.

The refusal message names the kind of content, never the value.

A false positive found and fixed: the telephone pattern matched digit runs inside hexadecimal digests in canonical snapshots (for example `c0512699516aa...`). The pattern now requires a non-word character before and after the number.

## Evidence

* New tests: `test_task_contracts` (refusal before a prompt, no echo, over-length, clean evidence with a digest still builds) and `test_dispatch` (refusal with no provider call, no value in the result). Both fail on the base code and pass with the change.
* Core modules touching assistants, prompts or contracts: 805 tests, OK (185 skipped, as on base). API modules touching assistants: see the changes record.
* `mypy` in `src/core` shows the same 3 baseline errors as the base; `src/agents` clean; `ruff` clean.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Map staff/tenant identities and review records separately from fixtures | Proven | Live register `subject_populations` (2026-11-22 note); unchanged |
| Cover inputs through retained copies | Proven | Live `whole_system_coverage` (2026-11-22 note); unchanged |
| Every task declares purpose, fields, types, lengths, prohibited content, necessity | Proven offline for all 13 tasks, and now enforced for the five assistant tasks | `task_contracts`, the new tests; chat and concern-pack prompt builders are still not routed through `enforce` (follow-up); live enforcement unproven until deployment |
| DPO/Legal and owners approve purpose, transfer, retention, legal hold, erasure, representative authority, provider copies | Unproven | Production-only, deferred to #1906; not needed for the demo |
| Upload/store permission does not approve model dispatch | Proven | Live read-doc hold (2026-11-22 note); `enforce` ignores `user_permission` |
| Synthetic residents do not remove staff scope; UK hosting is not UK inference | Proven | Ticked; register wording |
| Retention, erasure, audit, restore explicit and owned | Explicit proven; owners unproven | Live statement and retention values; owners are production-only (#1906 to #1908) |
| Constructed fixtures remain the development path | Proven | Ticked |

## Limits

* The regexes catch identifiers only, not free-text special-category data.
* The 40000-character `source_snapshot` limit is above the 12000-character assistant input limit, so it does not change existing behaviour.
