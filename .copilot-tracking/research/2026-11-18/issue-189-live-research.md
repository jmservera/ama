# Research: issue 189 live run controls (2026-11-18)

Status: executed. Scope: unticked criterion "Run has an owner, a time limit and a budget alert", synthetic demo, RG ama, cap USD 700.

Findings: only the run owner, time limit and budget alert criterion is unticked. A first pass exists (docs/reference/research/issue-189-simulator-run-controls-live-evidence-2026-11-18.md). Live: USD 25 IoT budget with 80 percent actual and 100 percent forecast alerts, B1 hub with owner tag, no simulator job, `ZF_SIM_CONTROL_FILE` unset, deployed admin endpoint returns 403 to a staff user. An administrator role grant is a tenant identity change and is not authorised.
Research disposition: executed. Planning Readiness: Ready.
Evidence note: docs/reference/research/simulator-run-controls-live-189-2026-11-18.md
Correction record: the pre-existing state file issue-189-live-state.json was overwritten by mistake at 12:33Z and restored with git checkout before any commit; this run uses issue-189-live-r2-state.json. The research-open witness event referenced the restored path.
