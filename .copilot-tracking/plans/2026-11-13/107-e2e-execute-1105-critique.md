---
title: Issue 107 end-to-end execute probe plan critique
description: Independent rubber-duck critique, executed once; verdict Revise, C1 to C6 applied directly
ms.date: 2026-11-13
---

Executor: rubber-duck subagent (read-only; relayed verbatim in substance by the worker because the subagent could not write files). Verdict: Revise.

* C1 Blocking: verify is not acceptance; `review` needs a later `accept` with the new revision. Add it and assert state and ledger review.
* C2 Blocking: skips can make coverage vacuous. Fail on any skip; executed and accepted sets must equal `REGISTRY`.
* C3 Blocking: join reservation, completion, output and review by meter id, root, attempt and output id; assert tokens and every `report()["by_capability"]` metric, chat separately.
* C4 Blocking: `capture` excludes notes and document summaries, so also seed a permitted captured field (home address) and a valid assistant response carrying distinct sentinels; assert each reaches the request or response before scanning.
* C5 Blocking: table-wide allowlists conceal leaks. Scan ledger partition, audit receipts and envelope fields explicitly; exempt only identified domain-content fields.
* C6 Blocking: chat follows the existing test: `store.ai = inner`, thread id, JSON answer with valid citations; assert returned answer, exact output join and no increase in accepted proposals.

## Disposition

All applied directly to the details file; no user decision needed.
