# Issue 76 hazard clock and owner changes (2026-11-14)

Plan: [.copilot-tracking/plans/2026-11-14-issue-76-hazard-clock-owner-plan.md](../plans/2026-11-14-issue-76-hazard-clock-owner-plan.md)

* `src/core/src/zava_forward/core/taskqueues.py`: hazard clocks gain `kind`, `accountable_owner` (named owner, else `ESCALATION_OWNER`) and `clock_text`.
* `src/api/src/zava_forward/api/web/app.js`: `workSummary` shows the clock text and an accountable owner on queue rows, role screens and case-card views, with a client-side fallback owner.
* `src/api/tests/test_workbench_hazard_clock_owner.py`: five tests covering the core payload and the real JS render.

No divergence from plan. Validation (focused tier): core `test_taskqueues` (22 ok); API targeted tests (46 ok, including accessibility baseline and role screens); mypy and ruff check/format clean in `src/core` and `src/api` with /tmp caches. The full API discover run was stopped for time; `tools/rpi-checks.py --all` not run by instruction. Local import needed PYTHONPATH to the worktree `src` dirs because the installed distributions point at another checkout.

## Cycle 1 follow-up changes

* `src/core/src/zava_forward/core/workflows.py` and `src/api/src/zava_forward/api/web/app.js`: `Safeguarding` is now a recordable hazard category, so the Safeguarding clock is reachable.
* `src/core/tests/test_hazard_referral.py`: one test for recording a safeguarding concern.
* Findings 2 and 3: no change; the referenced function, module and title do not exist at this HEAD.
* Validation: core `test_hazard_referral` and `test_taskqueues` (69 ok, 1 skipped); API targeted workbench, hazard, safety and workflow tests ok; mypy, ruff check and ruff format clean in `src/core`; ruff/mypy in `src/api` not re-run after change beyond the earlier run. The full unittest discover runs exceed practical time and were stopped; PYTHONPATH pointed at the worktree `src` dirs.

## Cycle 2 changes (independent review of 81f4b81af)

* Paths named in the review (`taskqueues.py`, `projection.py`, `ai_tasks.py` under `rules/`) live under `src/core/src/zava_forward/core/`; the `external_service_due_at` field is not in the dataset, so the real `response_due_at` and `resident_update_due_at` deadlines drive the check (the generic field is also honoured when it parses).
* `taskqueues.py`: new `hazard_clock`, `accountable_owner` and `safe_category`. Released items with an open or overdue external deadline keep a clock; blank or `Unknown` owners fall back to `ESCALATION_OWNER`; `reason_ok=False` renders the clock kind as `Safety`, never `Safeguarding`.
* `workflows.py` `hazard_view`: every hazard carries `clock_text` and `accountable_owner`. `projection.py` redacts a safeguarding category and clock text to `Safety review` for roles without reason visibility. `ai_tasks.py` and `store.py` use the same redaction and owner fallback.
* `app.js` `safetyPanel` and `role-screens.js` (`safety-lead`, `hazard-triage`): show the clock and accountable owner per item, including released items.
* Tests: new core test for released-with-open-deadline, fallback owner and redaction; an existing test updated because released items with an open deadline now keep a clock.
* Validation (focused): core `test_rule_engine`, `test_taskqueues`, `test_hazard_referral` (100 ok); API `test_workbench_hazard_clock_owner`, `test_hazard_api`, `test_role_screens`, content standard, design system, accessibility baseline, dependency rule (71 ok); ruff and mypy clean in both. The named `test_rules_engine`, `test_hazard_clocks` and `test_hazard_clocks_api` modules do not exist; the nearest existing modules ran. No `unittest discover`; branch is `feat/ux-76-hazard-clock-owner-1338`.

## Cycle 3 changes (rebase onto a1bfc1748 and independent review of e1fc765fd)

* Rebased onto `origin/feat/demo-233-same-home-tensions-0825`. One conflict in `role-screens.js`: upstream's `hazardClock` (service response clock) and `hazardEscalationState` were kept; this issue's clock helper is renamed `hazardSafetyClock`. The restart table shows the service response clock, the safety clock, the accountable owner and the response time; the queue summary keeps 13 columns. Upstream's `hazardEscalationState`, `data-safety-focus-key` and `aria-label` code is unchanged.
* `test_safety_panel_ux.py`: the legacy-row fact list now has 6 terms (the added `Safety clock` and `Accountable owner`) and asserts both labels; the truthfulness assertions are unchanged.
* Review findings: `hazard_view` and `store.detail` use the store `as_of`; `store.py` reads `owner` with `.get`; `hazard_clock` only prints a due time that parses; `projection.py` also redacts `Safeguarding` in hazard history snapshots and `legacy_record`; `role-screens.js` guards an unreadable `response_due_at` with `Number.isNaN`.
* Not applicable: the request named `formatStatutoryDeadlineCell`, `statutory_clock_evidence`, `Investigation due`, `Make-safe due`, `Safeguarding & escalation` and `tests.test_hazard_clock_owner*`; none exist in this repository or in the review file, so nothing was invented. No statutory calculation is added.
* Validation: core `test_taskqueues`, `test_hazard_referral`, ruff and mypy clean; API `test_workbench_hazard_clock_owner`, `test_safety_panel_ux`, `test_safety_screen_wcag_keyboard`, `test_safety_screens`, content standard, design system, accessibility baseline, dependency rule (85 ok), ruff and mypy clean. No `unittest discover`.
