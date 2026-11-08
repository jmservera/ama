---
title: Critique of the OS-process race plan (#107, C10)
description: Single independent critique executed before source edits, with direct dispositions
ms.date: 2026-11-07
---

Execution: one rubber-duck subagent pass over the research, plan and details, read-only. Verdict: Revise (no user decision needed). This is the only critique for the task.

## Findings and dispositions

1. Blocking, accepted: SQL workers must receive the fixture's effective environment (database `zf_test_assistants`), not the parent's. Children get the explicit `sql_env` dictionary of the fixture; secrets only in the child environment, never argv or files.
2. Blocking, accepted: a fresh invocation after exhaustion is created disabled and never reaches the clamp. The restart case becomes: allowance partially used, a pending proposal, restart under a larger configuration; stored limits stay, the first execute is allowed within the stored allowance and the next is exhausted.
3. Blocking, accepted: a start barrier does not prove contention. Workers also write an `at-claim-<label>` marker and wait for all markers (bounded) immediately before claim, and the parent asserts all markers exist before release; the test does not claim determinism beyond what the existing transaction linearization provides.
4. Non-blocking, accepted: workers are started and reported ready sequentially before the race barrier; child stderr is kept and asserted empty, separating initialization from claim failures.
5. Non-blocking, accepted: the revocation case executes an unaffected control capability first, accounting its one call-log line, before the revocation test proper.

Plan and details are amended prospectively in place by these dispositions; the original critique text above is the record.
