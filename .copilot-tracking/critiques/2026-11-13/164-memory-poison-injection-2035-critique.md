---
title: "Plan critique: #164 criterion 3 (single independent critique)"
ms.date: 2026-11-13
task_slug: 164-memory-poison-injection-2035
---

Executed once by the independent `rubber-duck` agent on the final candidate plan. Verdict: Reject (six findings, owner planner, no user decision required). Dispositions are applied directly to the plan details; no second critique is run.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Serving prompt has no memory, so a flag cannot prove integrated resilience | Accepted. Flags are labelled scripted and component-scope; `INTEGRATED_MEMORY` stays "not covered"; enablement stays insufficient |
| 2 | "consent recorded" wording may not trip the action or status guard | Accepted. Run the exact wording first; if the guard misses it, record the miss and either strengthen the guard in core with a failing-first test or keep a failing scenario |
| 3 | Dropping a citation does not drop the foreign claim | Accepted. Assert the reply text excludes the foreign claim, not only the citation list |
| 4 | Gate precedence undefined | Accepted. Precedence: malformed or missing explicit fields or non-zero critical errors or an executed failure gives `fail`; an absent category gives `insufficient`; otherwise `insufficient` (never `pass`) |
| 5 | Prompt-exclusion checks can pass vacuously | Accepted. Such scenarios set `model_called: true` and assert the poison was stored via `isolation_contains` |
| 6 | Regression scope incomplete | Accepted. Update hard-coded probe counts and ids; test subset and empty summaries and `chat_heldout` compatibility |
