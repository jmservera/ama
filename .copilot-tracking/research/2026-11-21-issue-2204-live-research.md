# Research: issue 2204 role sign-in and wrong-role denial (2026-11-21)

Research disposition: executed. Planning Readiness: Ready.

## Question

Which of the three unticked criteria of #2204 can be proven on the synthetic demo with recorded evidence, and is there a real defect?

## Findings

* Roles: `DEFAULT_ROLE_MAP` in `src/api/src/zava_forward/api/auth.py` maps eight app roles (Coordinator, Liaison, Safety Liaison, Grants, Quality Inspector, Programme Manager, Support Officer, Contractor); `ZavaForward.ApplicationAdmin` is separate. `workbench.navigation` gives an administrator every option flagged "needs a role with this authority"; `projection.allowed` denies the administrator all data routes. A contractor needs a roster company binding.
* Live: one Entra account (Programme Manager). `az ad app list` still returns insufficient privileges, so no second role can be assigned. Live PM sign-in, 13 nav entries, data 200, simulator control 403 (API and UI), repairs role screen "Screen unavailable".
* Local: real provider and server with synthetic principal headers for every role, administrator, administrator plus staff role and five denial shapes: all as designed.
* Prior notes agree (`entra-signin-live-demo-2026-11-18.md`, `issue-116-live-r2-evidence-2026-11-18.md`, `issue-349-tenant-prerequisites-live-r7-2026-11-21.md`).
* No defect found. Targeted tests pass (108).

## Evidence

* `docs/reference/research/issue-2204-role-signin-wrong-role-denial-live-2026-11-21.md`
* `.copilot-tracking/evidence/2026-11-21/issue-2204-live/`
