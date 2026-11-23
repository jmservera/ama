# Research: issue 2202 hardening proof angle (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Earlier workers (live, demosmoke, deployproof, finalproof, gates-recheck) left "Revisions Running and Healthy; hardening enforced with rollback noted (agents app difference explained)" partly proven by hand: the finalproof note says the resident app carries no hardening variable and no agents difference was explained. No tool in the repo checks `ZF_CONTAINER_HARDENING` on the deployed estate; `tools/demo_preflight.py` checks revisions, health, jobs and counts only.

New angle: add a read-only hardening check to `tools/demo_preflight.py` with unit tests, and run it live.

Live read-only evidence (az, 2026-11-23): see docs/reference/research/issue-2202-live2-2026-11-23/az-state.txt. API 0000058 (created 19:20 UTC), resident 0000028, agents 0000003, simulator and receiver jobs all show `enforced`. The resident app now carries the variable (earlier note outdated). Agents app: internal ingress, min replicas 0, runningState ScaledToZero (Healthy), which explains its difference from API: it is idle, not unhardened. All apps run in Single revision mode, so no previous revision is retained for rollback.

Owner-only skipped: none needed. Not provable for demo: rollback exercise (no drills authorised).
