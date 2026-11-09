---
title: "Plan, issue 133 assisted aftercare source integration, Stage A (2026-11-09)"
ms.date: 2026-11-09
---
Written 2026-11-09 (UTC, committed 22:32Z as aebfe6f40), before any source edit. Research: [research](../research/2026-11-09/assisted-aftercare-133-stagea-research.md). Details: [details](../details/2026-11-09/assisted-aftercare-133-stagea-details.md). State: `.copilot-tracking/rpi-sessions/2026-11-09/assisted-aftercare-133-stagea-state.json`.

## Objective

A synthetic, existing-staff-assisted household or representative concern intake with a durable receipt, an owner, investigation and remedy display, and a joined synthetic baseline, outcome and unresolved-concern view, built as dedicated modules around the delivered `AftercareRegister`. Refs #133 only.

## Admission and ownership

* Allowed: `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/src/zava_forward/api/web/aftercare.js` (unwired), `src/api/tests/test_aftercare_screen.py`, a short README paragraph, a log entry and the tracking artefacts.
* Not touched: `server.py`, `role-screens.js`, `index.html`, `store.py`, `sqlstore.py`, endpoint inventory, common browser fixtures, `aftercare.py`, importer files.

## Phases

* [ ] Phase 1: `aftercare_intake.py` service: existing-staff role checks (`controls.RESIDENT_ROLES` to record, `RESIDENT_VIEW_ROLES` to view and act, `workflows.MANAGER_ROLES` to assign an owner and record closure), assisted intake validation (core `intake_errors`, channel, next-update date, request id, home in the stated synthetic set, personal-detail refusal), durable receipt, idempotent replay, owner actions bound to the owner role with Unknown refused, closure and sensor context pass-through, atomic persistence through a two-method state-store protocol with a file implementation, restore refusal, and `handle(method, path, user, body)` returning `(status, payload)`.
* [ ] Phase 2: joined synthetic view inside the same module: per home baseline, early and late observed means from `sensor_scenarios.retrofit_comparison`, Unknown where insufficient, concerns, unresolved and closures; totals with denominators delegated to core `evaluator_view`; fixed Unknowns for synthetic values, evaluator role and outcome-data position.
* [ ] Phase 3: `test_aftercare_intake.py` (core, strict mypy and ruff clean) covering the cases listed in the details.
* [ ] Phase 4: `aftercare.js` dedicated screens (intake form, receipt, concern display, evaluator view) using native controls, error summary, `role=status`, captions and no colour-only state, plus a node test with stubs. Load the redesign and web-design-guidelines skills and fetch the current guidelines source first.
* [ ] Phase 5: README paragraph, log entry, changes, review, handoff.

## Validation (focused tier, planned before execution)

* Fresh scratch venv `/tmp/issue133-1109/venv` with this worktree's core installed; no `PYTHONPATH`.
* `unittest` for `tests.test_aftercare`, `tests.test_aftercare_intake`, `tests.test_retrofit_scenarios_production_consumers`; `ruff check` and `mypy` on the new and test files.
* `node` screen test via `python -m unittest` in `src/api/tests/test_aftercare_screen.py` (needs only node and stdlib).
* `git diff --check` and Markdown link review.
* No SQL, served-process, browser or axe check runs in Stage A; they are listed UNEXECUTED in the handoff. No shared heavy resource is requested.
* Classification: Stage A is focused tier (no SQL, deployment, permission, dependency, workflow or gate change; the new role tuples reuse existing constants). The hook continuation adds API role checks over household-related records and persistence, so it should be treated as the full tier unless the coordinator classifies it otherwise; doubt takes the full tier.

## Correction budget

Five total productive correction cycles for the issue; none spent at planning.

## Critique (one pass)

Executed once on 2026-11-09 before commit aebfe6f40. Verdict: Revise; seven findings applied directly to the details, none needed a user decision. See [critique](assisted-aftercare-133-stagea-critique.md). The plan phases are unchanged; the details carry the corrections. Implementation begins after the plan commit.
