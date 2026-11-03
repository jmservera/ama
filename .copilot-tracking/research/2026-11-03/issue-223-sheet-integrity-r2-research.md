---
title: Issue 223 research, sheet integrity (round 2)
date: 2026-11-03
---

Research disposition: executed (repo and PR inspection). Planning Readiness: Ready.

Already delivered on main: #428 protocol, #638 gate and scripted panels, #701 reviewer authority, #817 manual worksheet and scoring, #855 class, automation-bias and effort report. #941 (session pooling) merged only into the stacked #218 branch, parent #956 still open, so it is not on main.

Gap found in main: `score_human_session` ignores the sheet `version` and silently ignores answers for proposals outside the scenario. A stale worksheet from an earlier scenario could be scored against a changed one, weakening the "same workflow-only scenario" comparison (criterion 3) and the retained record (criterion 2).

Slice: refuse sheets whose version differs from the current scenario and sheets naming unknown proposals. No gate change, no AI, no security, infrastructure, SQL or deployment change (focused tier).

Acceptance criteria status after this slice: all five remain unmet as closure evidence. No authorised competent human has run the test (1-4 proven for scripted panels only); OQ-017 holders unfilled, thresholds and sample size unapproved (5).
