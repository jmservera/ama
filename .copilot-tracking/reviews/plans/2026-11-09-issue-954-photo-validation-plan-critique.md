# Plan critique: issue 954 photo flag browser validation (2026-11-09)

Execution: one critique pass by an independent read-only rubber-duck agent over the final-candidate research, plan and details, before implementation. Never repeated for this task.

## Verdict

Issues: 3 blocking, 2 non-blocking. All are compatible with the owner clarification and were applied directly to the details record before the planning commit; none required a user decision.

## Findings and dispositions

* B1 false refresh could pass vacuously (flag already false). Applied: assert the refresh `/api/me` response was processed and the true, false, true flag sequence was served before counting requests.
* B2 import binding not proven and unit commands lacked the worktree path. Applied: worktree `PYTHONPATH` on every command; the checker asserts that `zava_forward.api`, `zava_forward.core`, `test_mvp` and `test_auth` resolve inside this worktree.
* B3 recovery precondition conflicted with the committed plan (HEAD no longer the base). Applied: verify the planning commit's parent is `ef28d4da4` and its non-tracking source tree equals the base.
* N1 console assertion exceeded the owner definition. Applied: record every event unfiltered; fail only on page errors and console error/warning events other than the expected native photo diagnostic; native diagnostics are classified separately.
* N2 receipt lost on early failure. Applied: per-status receipt written from `finally`.
