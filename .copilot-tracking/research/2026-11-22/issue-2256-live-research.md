# Research: issue 2256

Disposition: executed. Planning Readiness: Ready.

Cause: `handoff_ageing` (src/core/src/zava_forward/core/workflows.py) raises on a timezone-less `offered_at`; `unaccepted_handoffs` swallows it and drops the case. Live seed offers have `offered_at` 2026-10-13T09:00. Live probe: `/api/handoffs` 4 rows, `/api/handoffs/unaccepted` 0 rows.

Evidence: docs/reference/research/issue-2256-handoff-waiting-2026-11-22.md
