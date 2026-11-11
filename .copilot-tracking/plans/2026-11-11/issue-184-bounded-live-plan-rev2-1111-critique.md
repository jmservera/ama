<!-- markdownlint-disable-file -->
# Bounded live demo plan revision 2: author critique (2026-11-11)

Critique of [the rev2 plan](./issue-184-bounded-live-plan-rev2-1111-plan.md) and [research](../../research/2026-11-11/issue-184-bounded-live-plan-rev2-1111-research.md), written by the author after the plan and before the details revision. Execution: one pass by the author in the resumed native session; NO independent agent was used, so this is not independent critique. It is not repeated. It is separate from the original pre-revision `rubber-duck` critique, which is untouched.

| # | Severity | Self-identified gap | Disposition |
| --- | --- | --- | --- |
| 1 | Significant | A tidy "expected exit" table could redefine exit 2 (`RUN_DEADLINE`, `RUN_STOPPED`) as pass | Applied: details record observed source behavior only; no window is declared passing unless the design prerequisite defines it, and failures are never redefined as success |
| 2 | Significant | "13 triggers in 60 minutes" depends on UTC cron alignment; 13 needs both end slots inside the window | Applied: details state the UTC assumption, that 12 or 13 triggers are possible, and that 13 is a maximum, with no manual or replacement executions |
| 3 | Significant | The simulator lists all open cases (`closed = 0`); the one-home restriction depends on the control cohort and was not verified from source | Applied: recorded as an unverified prerequisite, not a claim |
| 4 | Minor | The core meter has a `money-budget-limit` check, which could be read as an enforced currency cap | Applied: stated as source behavior that needs an approved authority and price record, both Unknown; no cap claim |
| 5 | Minor | Illustrative total could be read as a cap | Applied: labelled illustration, with fixed and unpriced classes separate |

No finding conflicted with a confirmed decision; none needed a user decision. Residual: later Review is also the author's, and independent exact-head review remains Root's.
