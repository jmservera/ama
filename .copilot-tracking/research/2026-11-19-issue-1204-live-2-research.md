---
title: Research, coordinator contract issue 1204 live pass 2
date: 2026-11-19
task_slug: issue-1204-live-2
---

Disposition: executed (opening). Tier FOCUSED if only `tools/` and docs change.

Scope: first unticked criterion of #1204, criterion 2 (every tick has a next action and bounded closure-review progress; approvals reconciled; one blocked lane is not a global stop). Base: origin/main ec63bfc7c. Prior pass 2026-11-18 left it Unproven and proposed a contained scenario plus a stronger guard.

Opening finding: `tools/check-coordinator-handoff.py` `check_agent_instructions` does not assert the criterion 2 clauses (bounded closure batch of up to five, `closure_review`, `approved_actions` reconcile, `tick_log`, no global stop on a blocked lane), so deleting them would pass the guard.
