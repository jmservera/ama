# Research: remaining #531 gap (2026-11-01)

* Research disposition: executed (repository evidence; no Azure or live access).
* Planning Readiness: Ready.
* Evidence: criteria 1-6 delivered by merged #538, #581, #604, #628, #685 (loading shell, per-panel loaders, outcome wording, sources, refresh time, "Unverified" label, HAX note at `docs/reference/research/ux/briefing-hax-design-note.md`, browser/axe check `src/api/checks/loading_briefing_browser_check.py`). Review of #685 routed live verification to the owner.
* Gap: criterion 7 (live verification recorded separately) cannot be proven locally, but the operator-run live entry point `src/api/checks/employee_live_acceptance.py` (observers: chat, map, case in `employee_acceptance_check.py`) has no loading or briefing observer, so a live run could not evidence #531.
* Residual slice: add a read-only `briefing` observer (no click on review controls, no mutation) so the owner's later live run covers Today's briefing: visible, AI or rules label, "Not an instruction", prepared-at time, Sources used, no alert. Criterion 7 stays unmet until the owner records a live run.
* Constraints: src/ only, no new mvp/prototype code, no Azure access, no secrets, existing observer contract (booleans only, admission probe).
