<!-- markdownlint-disable-file -->
# Bounded live synthetic demo acceptance: critique (2026-11-11, Refs #184 #1288 #108 #440)

Single critique of [the plan](./issue-184-bounded-live-plan-1111-plan.md), [details](../../details/2026-11-11/issue-184-bounded-live-plan-1111-details.md) and [research](../../research/2026-11-11/issue-184-bounded-live-plan-1111-research.md). Executed once by an independent read-only `rubber-duck` agent on the final candidate; not repeated. Verdict as returned: **Revise** (two blocking, four significant, one minor). No finding conflicted with a confirmed decision and none needed a user decision, so all were applied directly. Dispositions are mine, not an independent re-confirmation. Finding 1 was re-verified by me in `assistants.py` and `ai.py`.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Source refuses to send captured sensor readings to a real model, so the live AI chain cannot work unchanged | Applied and verified: plan blocker, research Part C, details gating blocker and approval question (A); the criterion is stated as unreachable by spending approval alone |
| 2 | Blocking | Transport limits not enforced: control may run 3 hours, failed sends may exit 0, schedule ticks after expiry | Applied: independent 60-minute transport expiry, count monitoring, mandatory schedule deletion |
| 3 | Significant | Proactive scanner not restricted to the named case | Applied: isolation proof or stop, as a blocker |
| 4 | Significant | Receiver timing unspecified; reads from latest position | Applied: windows start before designated sends; retained readings designated |
| 5 | Significant | Cost and token bounds overstated; post-expiry ticks; 12,000 chars not proven tokens | Applied: token caveat and post-expiry liability rows in the envelope, marked Unknown |
| 6 | Significant | Approval question not exact | Applied: home, both expiries, receive path, ceiling, liabilities, headroom, alert, OD-51 and approver now named fields |
| 7 | Minor | `SYN-` prefixes device IDs; evidence may expose identifiers | Applied: fixture text corrected; redaction or controlled storage required |

Residual: the arithmetic was confirmed correct by the critic under its assumptions; all currency figures remain list-price estimates, not caps; no execution, Implement or Review marker exists.
