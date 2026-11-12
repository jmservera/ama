---
title: Issue 132 keyboard probe compatibility research
description: Prospective research for declaring the staff-job-pack-intake screen in the existing specialist keyboard probe (issue 132 follow-up)
ms.date: 2026-11-11
---

## Task

Task `issue-132-keyboard-compat-1111`, slug `issue-132-keyboard-compat`. Research disposition: `executed` (bounded, source reading only). Worktree `/home/azureuser/source/ama-demo-wt/issue-132-keyboard-compat-plan-1111`, branch `test/demo-intake-keyboard-compat-132-1111`, base and head at start `35eb0e559c7d0660ab87594732675b71be7bee67` (equal to `origin/main`), clean. Scope is the existing integration mismatch only; no product, whole-acceptance or perspective re-audit.

## Mismatch (source evidence at base)

* #134 PR1414 (`b23c08e33`) added `src/api/checks/specialist_keyboard_browser_check.py` and `src/api/tests/test_specialist_keyboard_check.py`. `walk_screen` (lines 276-325) walks every screen a role is served and calls `region_failures(screen_id, found)` (lines 148-170).
* `region_failures` fails closed: a screen id in neither `NO_REGION_GAPS` (lines 54-64, five screens) nor `EXPECTED_REGIONS` (lines 43-52, eight screens) returns `screen <id> has no declared region expectation or declared gap`. The existing test already asserts this for `unlisted-screen` (test file line 88).
* #132 PR1425 (`0509ddcef`) registered `staff-job-pack-intake` in `src/api/src/zava_forward/api/web/staff-intake.js:137-141` after PR1414. A static comparison of all 14 `registerRoleScreen({ id: ... })` calls with the two declaration tables shows exactly one undeclared id: `staff-job-pack-intake`.
* Root executed the real helper on base source: `region_failures("staff-job-pack-intake", [])` returned the undeclared-screen failure. This planning pass re-imported the module read-only with the system `python3` and saw the same string. That proves helper rejection only. It does not prove browser reachability, selected-home rendering or a production UI defect; no browser ran.

## Which declaration is correct (derived from source, not guessed)

The probe starts `zava_forward.api.server` on a `ZF_STORE=json` copy of `synthetic_data()` (`design_system_browser_check.main`, lines 250-285; `workbench_browser_check.synthetic_data`, lines 20-56).

* The screen's `load(c)` reads `GET /api/workorders?case=<id>` (`staff-intake.js:141-146`). The server routes this to `s.list_work_orders(u, case)` (`server.py:751-767`), which reads `self._proc()["work_orders"]` (`procurement.py:565-580`).
* `_proc()` defaults to `dict(packages=[], work_orders=[])` (`procurement.py:77-78`). `core/tests/dataset.py`, the base of `synthetic_data()`, contains no `procurement` key and no work orders (only a helper at line 17 that reads one). Nothing in `synthetic_data()` adds any.
* With zero orders, `render` returns the "What this screen does" panel plus `screenPanel("Work orders", p.empty "No work order has been issued for this home.")` (`staff-intake.js:147-158`). Tables are emitted only through `screenTable`, and in this screen only inside `intakeOrder` (recovery table) and `intakeReceipt` (original notes and corrections). `screenTable` is the sole producer of `.table-scroll[role=region] table`. So source predicts zero `.screen-evidence table` elements on the maintained fixture, which `region_inventory` would return as `[]`.
* Therefore the screen belongs in the declared no-table gap class, not in `EXPECTED_REGIONS`. Invented labels such as "If the visit does not happen" would fail every walk because those tables never render without an order.
* This is a source-derived prediction. A later affected-browser run can admit only the narrower observation that no evidence table rendered (`regions == []` for all seven roles). `staff-intake.js:143-145` turns a per-order load error into an alert, not a table, so an empty region list alone cannot prove that no work order exists; the no-order cause stays source-derived (critique finding 2).

## Roles (seven permitted)

`intakeRoles` (`staff-intake.js:4-5`): Retrofit Coordinator, Resident Liaison Officer, Building Safety Liaison, Grants and Evidence Officer, Quality Inspector, Retrofit Programme Manager, Programme Support Officer. `roleScreensView` serves a screen only when `screen.roles.includes(me.user.role)`. `checks/workbench-manifest.json` (`ia-v1`) lists those same seven plus Contractor. Contractor is not in `intakeRoles`, so the menu never offers the screen and `run_browser` records it only through `served[name]`. All seven are staff, resolve through `_actor` in `_work_order_reader`, and are not contractors, so the list call returns `[]` for each. There is no role-specific difference in the expected regions. Role-specific behaviour (managers, quality) only appears when an order and receipt exist, which this fixture does not have.

## Walk steps unaffected by the declaration

The remaining `walk_screen` assertions do not depend on tables: menu reachability, status text `"<role>. Job pack and worker evidence intake. <state>"` and attributes, first `a.item` home, handoff link `.screen-evidence a[href^="#/case/"]`, and `a[data-reset]` (all supplied by `roleScreensView`). The negative controls use `safety-lead` and `technical-queue` on the first role serving both and are unaffected. `report` prints a gap count only, with no total assertion, so six gap screens times the serving roles changes output only.

## Limits kept explicit

* A gap is "not a pass". The populated states (recovery table, receipt tables, forms) are covered by #132's own opt-in `tests/test_staff_intake_browser.py` (Chromium and axe, SQL store). The keyboard probe will not exercise them. Building a work-order fixture here is out of scope.
* `src/api/README.md:4162` says "five screens have no evidence table on the fixture". After the repair the count is six, so that sentence becomes stale. The README is also where root134 adds a short paragraph in another worktree; see the plan for the conditional handling.

## Boundaries and dependencies

* Root134 owns new `connected_home_browser_check.py`, `test_connected_home_check.py` and a short README paragraph; it imports existing helper APIs read-only. No signature change is proposed here: only the data in `NO_REGION_GAPS` changes.
* The shared canonical heavy lock is held by #134's final admission. This research acquires nothing and ran no browser, install, provider call or private-data read.
* Correction authority: original #132 C5 is exhausted; the owner's separate five-cycle extension of 2026-11-10 used E1, E2 and E3; two remain. This work consumes none and authorizes no E4.

## Planning Readiness

`Ready`. Open item for the later run, not for planning: confirm `regions == []` in a real walk.
