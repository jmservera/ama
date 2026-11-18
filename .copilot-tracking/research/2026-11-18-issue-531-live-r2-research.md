# Research: issue #531 live verification, second pass (2026-11-18)

Disposition: executed. Planning Readiness: Ready.

Scope: the one unticked criterion (live verification on the employee site). Demo, desktop only, live Azure authorised (rg ama).
Prior evidence on main: docs/reference/research/issue-531-live-demo-evidence-2026-11-18.md (#1978). It left gaps: live build two files behind main, no real cold start, no recorded review through the UI, no AI-written briefing.
Plan: re-check deployed parity, attempt a real cold start only if replicas are already zero (no scale change), run the UI review reject live once, re-observe shell/live region/reduced motion/wording, record per-criterion table.
Evidence: docs/reference/research/issue-531-live-r2-2026-11-18/. Focused tier, no src change.

Findings: replica polling for 10 minutes (14:03 to 14:13Z) showed 1 to 2 replicas throughout because other work shares the app; scale-to-zero never occurred, so a real cold start could not be observed without changing scale (not allowed). Deployed revision 0000031 still serves app.js and style.css that differ from main; workspace-shell.js and async-action.js match. Review reject through the UI succeeded live (POST /api/ai/review/{id}/reject 200, state Rejected, outcome text "not an approval"). No AI briefing (release admission denied).
