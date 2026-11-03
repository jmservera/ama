# Research: issue #227 cross-home hazard referral queue

Disposition: executed (reuse of prior #227 evidence plus gap check). Planning Readiness: Ready.

* Per-home safety-lead and hazard-triage screens, a browser check and axe evidence are already on main (#653, #776); see the 2026-11-01 and 2026-11-02 issue-227 research files.
* Both prior reviews routed one follow-up: a cross-home referral queue. The 2026-10-31 closure audit on the issue lists the queue-level view as unmet for criterion 1.
* The existing `summarise`/`summary` contract in `role-screens.js` (resident choice, service issues) fetches each case on the current page of homes and renders a read-only table without a portfolio total. It is reused; no new endpoint, framework or write path.
* Missing: human/AT validation (#155), design-system adoption proof (#150), WCAG acceptance (#151). Not provable here.
* Environment note: `zava_forward` is not importable from this worktree without explicit `PYTHONPATH=src:../core/src:../agents/src`; the safety browser check failed on that import and was not run.
