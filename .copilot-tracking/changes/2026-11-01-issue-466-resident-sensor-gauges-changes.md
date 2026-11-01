# Changes: issue 466 evidence slice, 2026-11-01

* Plan: [plan](../plans/2026-11-01-issue-466-resident-sensor-gauges-plan.md)
* Added `docs/reference/log.md` entry "Resident sensor gauges and assistant re-verified on main (Refs #466)".
* Added dated research, plan, changes and review artifacts under `.copilot-tracking/`.
* No source, test, infra, mvp or prototype change. No divergence from plan.
* Validation (pip venv, focused tier): core resident sensors/assistant 15 OK; api resident suites 84 OK (1 skip); ruff check and format clean (core, api); mypy core clean, api only optional `playwright` stub errors.
* Review-thread corrections: research evidence now separates previously accepted engineering checks from browser checks (`checks.resident_sensors_browser_check`, `checks.resident_assistant_browser_check`, no fresh result) and the enabled-advisor versus AI-off expiry paths; plan and review record the unresolved local-gate policy conflict as open publication work.
* CI: the `activation` failure is a GitHub API quota stop in the daily AIC scan restore step, not a code failure; rerun requested.
