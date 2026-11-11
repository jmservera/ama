---
title: Issue 144 extension 2 result-attribution review
description: Authored post-implementation review of the attribution binding (E2)
ms.date: 2026-11-10
task_id: issue-144-extension2-attribution
---

## Review execution

Executed once by the implementing agent as an authored review (no sub-agents authorized). Boundary: the working-tree diff (`assistants.py`, `test_ai_consumption_api.py`) on merge commit `7bb8fc2b3222fb42892910d26cf232fcd2f21fe5` plus the RPI records. Not independent; the independent reviewer must assess the final exact head.

## Outcome

Conformant for the declared scope at the DEMO targeted tier. The Medium finding (result attribution not bound to the permitted root) is closed in source and tests; no material finding is open inside this batch.

## Requirement checks

* Root omitted on a valid permitted result: output attribution published on the reserved root, task envelope carries the root and meter id, accept review records review accounting (test 1, real store).
* Conflicting caller `meter_root` or `meter_id`: `result-rejected`, no settlement, no output record, task still leased; a correct retry completes once (test 2).
* Failed or unavailable result without a root: meter settled, no output published; semantics unchanged (test 3).
* Missing reservation fails closed to rejection; no broad catch, no fallback.
* RED on frozen source: 2 causal failures (log 07). The E1 clock fix, fence, consent, captured-readings and authority paths are untouched; existing selectors pass (api 511, core 59, agents 15).

## Findings routed to later work

* Without a permit marker, `complete_result` still forwards caller attribution (out of this finding). Route: later decision with the worker port.
* Real MSSQL selectors unobserved (no ready task-labelled disposable fixture tool for this task; new tests are not MSSQL-parameterized).
* Production caller of `complete_result` still absent (B).

## Limits

No consent, provider, spend, live or deployment decision. No whole-issue 144 or publication approval. Cycle accounting: E2 of the new five used, three left; original spent history and the unknown minimum preserved.
