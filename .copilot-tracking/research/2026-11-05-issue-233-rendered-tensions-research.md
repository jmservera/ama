# Research: issue 233 rendered tension sequence

Date: 2026-11-05. Issue: #233 (child of #149). Branch: `test/atlas-rendered-tensions-233`. Parent integration target: `test/ux-evidence-149` (local only). Pinned parent and origin/main: `7e0fe64892a1b9a65cc2f580faf2369f3bf009ef`. Research disposition: executed. Planning readiness: Ready.

## Context read

* Repository instructions, `docs/case_study_48_original.md` and addendum framing, `docs/reference/README.md`, `docs/reference/memory.md` (context, not evidence), `docs/reference/research/ux/atlas-screen-trace.md`.
* Pinned worktree sources: `role-screens.js`, `checks/role_screens_browser_check.py`, `checks/role_screens_fixtures.py`, `checks/procurement_screens_browser_check.py`, `checks/design_system_browser_check.py` (owned loopback harness `main`), `core/procurement.py`, `core/tests/dataset.py`.

## Findings

* The trace doc says the rendered behaviour of the two tensions is unassessed. Existing browser checks cover ordinary screens but none asserts the tension sequence: `role_screens_browser_check` story 232 reads panel text but not order, withheld panels or the cross-screen sequence; `procurement_screens_browser_check` asserts a capacity row and reflow but not the precedence order or reference ordering against conflicting headroom.
* A smaller extension of an existing check was rejected: `role_screens_browser_check` already takes 755 lines with per-story scenarios keyed to a single email, and `procurement_screens_browser_check` builds its fixture differently. A new focused module reuses the shared harness (`design_system_browser_check.main`), the shared fixture (`role_screens_fixtures.synthetic_data`) and the Store builder pattern, so no harness is duplicated.
* `pam@example.test` (Retrofit Programme Manager) is installed for `programme-queue`, `resident-choice` and `procurement-packages` (`choiceRoles`, `screenManagers`). No new access is needed.
* The programme connected view renders eight ordered stage links; stage 3 opens `resident-choice` and stage 4 `procurement-packages` with the same `case=`. The screen menu also keeps the selected case. These are the real navigation paths used.
* `.screen-record` panels use `content-visibility: auto`. Off-screen panels and tables read back as empty `innerText`, and full-page screenshots show them blank. Panels and tables must be read while scrolled into view, and per-panel element screenshots are the faithful visual record.
* The shared home ZF-1 carries an open hazard stop, so real work orders cannot be issued for it. A real work order is issuable for ZF-5 (Other Ltd) after the supplied resident fixture, giving a genuine non-zero `in_use` without bypassing a rule. The fixture therefore creates three packages through the real Store: headroom 5, 2/2 and 9, offered 7, 6/3 and 9, so reference order PKG-001..003 differs from headroom, offered and use rankings.
* `/api/packages` returns creation order. The test route reorders only the response order (PKG-002, PKG-003, PKG-001) and leaves values, status and headers semantics unchanged.
* Observation, not a defect claim: the per-package "Draft readiness" panels render in delivered order while the capacity table sorts by id. With the real API (creation order) these agree. Routed as a follow-up.
* Lock: `/tmp/ama-rpi-heavy.lock` was held by native rpi-1214 (PID 1519007) at intake (`flock -n` exit 1). A later non-blocking probe exited 0, and all browser work then ran under `flock -n`.

## Boundaries

C2 engineering only. C4 (connected walkthrough), C5 (WCAG acceptance), #151, #155, the eight-stage EX-HOME-901 walk and the stage 1 source-account feature remain unmet. One shared synthetic case is not the complete connected journey. No human, AT, user, legal, privacy or design approval is claimed.
