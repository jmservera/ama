---
title: Issue 164 F2 correction1 prospective critique
description: One independent prospective critique of the correction1 plan, run before implementation, with dispositions
ms.date: 2026-11-08
---

Execution: Complete (one pass, rubber-duck agent, read-only, 2026-11-08, after the correction1 research, plan and details and before any source edit). Verdict: proceed with changes. No second critique runs in this task. The original critique (`challenges/2026-11-08/issue-164-f2-memory-probe-scope-critique.md`) is unchanged; its claim of constructor and partial-execution test coverage was not met by the b2f diff (constructor failure and no-probe only) and is preserved as history.

## Findings and dispositions

* CR1-001 (Blocking): `Run.ask` swallows turn exceptions, so a missing receipt can coexist with earlier valid receipts and still give declared-false coverage. Accepted. Research of the golden data shows every turn, including expected errors, yields exactly one `chat.turn` receipt (24 scenarios, zero mismatches). `run_scenario` will record `turns_asked`; evidence is complete only when `execution_complete` is true and receipts equal turns asked. Expected refusals or assertion failures keep their receipts and stay complete; `chat.turn.unstored` entries are not receipts and make the scenario incomplete (conservative).
* CR1-002 (Blocking): a true receipt must not take precedence over incomplete evidence. Accepted. Incomplete or missing evidence gives `unknown` first; true declarations are counted separately and only a complete report with a true receipt reports `deviation`.
* CR1-003 (Blocking): `gate_results` forwarded an existing `serving_path_coverage` from an older report. Accepted. The gate row uses the summary statement only when the scope carries the new completeness fields; otherwise unknown. Tested with a stale scope.
* CR1-004 (Non-blocking): the static open item still asserts non-consumption. Accepted; reworded as a receipt declaration pointing to `summary.memory_scope`. The `bindings` policy salt "no panel memory" is left unchanged so bindings do not move.

## Residual

No conflict with a confirmed decision and nothing needing user input.
