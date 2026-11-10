<!-- markdownlint-disable-file -->
# Changes: issue 189 C1 correction (2026-11-09)

Head before: `522adc3946f754a86f48747bd00fb0911434e469`; base `df8e858b2150198e5e22c73d224a0d3592c73daa`. Plan: [plan](../../plans/2026-11-09/simulator-control-189-c1-plan.md). Critique: [critique](../../plans/2026-11-09/simulator-control-189-c1-critique.md) (one run, Revise, all five findings applied). Cycle C1 of five TOTAL; four remain.

The original changes, review, plan, details, critique and state artifacts are frozen and unchanged. This file supersedes only their validation wording for the selected-suite error (F3) and the "view-only administrator can start/stop by design" caveat in the original handoff (F1), which is withdrawn.

## F1 (High) corrected

* `server.py`: the simulator POST hook now runs after the existing `view_only` refusal, so the server denial applies first with its standard message.
* `simulator_admin.py`: `handle` refuses every non-GET for a truthy `view_only` (`VIEW_ONLY`, 403, same wording as the server gate) before any file, lock or audit access. GET status stays available and reports `read_only` and `writable: false` for a view-only administrator.
* `workbench.py`: the simulator entry is "needs a role with this authority" for a view-only administrator, "available" otherwise.
* No new permission, capability, allowlist, schema, role or owner approval. Valid authority stays administrator plus an existing staff role.
* Tests: `test_entra_authoritative` assertion returned to its base form (all destinations need a role for an administrator alone); `test_simulator_admin` module and HTTP tests deny start and stop for a view-only administrator with a valid revision, CSRF and trusted principal and assert file bytes, lock sidecar and audit entries unchanged; a test patches the module handler and proves the server gate denies before it is called; success paths use administrator plus staff; lookalike paths give 404 for administrator plus staff and 403 for administrator alone; non-administrator matrices unchanged. With the three source files stashed these tests fail (9 failures, 3 errors), confirming they encode the corrected contract.

## F2 (Medium) corrected

* `web/simulator-control.js`: a confirmed Stop form with the loaded revision for every parsed writable control (permitted, expired, invalid window, already stopped); Start whenever not permitted; a view-only message when `read_only`.
* `checks/simulator_control_browser_check.py` (real Chromium, pinned axe 4.10.3 sha256 `880970c0...8a68bb`): unavailable, rejected start, permitted, stop, expired enabled, invalid window, already stopped (twice), stale, failed write (patched `OSError`), manual not-writable, view-only administrator. Each stop asserts the cohort, owner and expiry are kept and Stop stays available; stale and failed writes leave the file bytes unchanged. 0 axe violations in every state. On the previous screen the check fails ("permitted stop", Stop stays available).

## F3 (Medium) kept unresolved

The label "unrelated" is withdrawn. The original error (`ConsumptionApi.test_assistant_completion_preserves_capacity_quarantine_and_terminal_release`, subtest `model='other-model', capacity=False, revoked=True`, 2103 ran, 365 skipped, 1 error) is an **unresolved selected-suite error**; its traceback was lost to the `grep` producer and cannot be recovered without a full rerun, which is excluded. Bounded reproduction (exact commands in the research artifact, raw output files `/tmp/c1/*.txt`, not committed):

| Reproducer | Tree | Result |
| --- | --- | --- |
| single test | head `.venv` | exit 0, 1 OK (9.4 s) |
| `test_accessibility_baseline`, `test_ai_boundary`, `test_ai_call_site_inventory`, then single test | head | exit 0, 25 OK |
| `discover -p "test_a[a-i]*.py"` | head | exit 0, 110 OK (76 s) |
| single test | base worktree, fresh venv | exit 0, 1 OK |
| `discover -p "test_a[a-i]*.py"` | base worktree, fresh venv | exit 0, 110 OK (99 s) |

Not reproduced at head or base; cause not established; no baseline-failure, flake or waiver claim. The full suite was not rerun. A later, owner-selected full-suite run with raw capture would be the only way to settle it.

## Docs

`src/api/README.md`: view-only administrators read status only; Stop is offered for every readable writable control.

## Validation (targeted demo tier)

* 315 tests OK: `test_accessibility_baseline`, `test_auth`, `test_buildings`, `test_case_journey`, `test_content_standard`, `test_employee_acceptance_check`, `test_employee_identity_check`, `test_entra_authoritative`, `test_exception_register_screen`, `test_programme_screen`, `test_role_screens`, `test_simulator_admin`, `test_workbench`, `test_workbench_live_defaults`, `test_workspace_scripts`, `test_live_control`, `test_live_simulator`, `test_design_system` (every module that references navigation, view-only, workbench or the administrator role, plus live control and design system).
* `ruff format --check`, `ruff check` and `mypy` clean on the touched Python files; `node --check` on the screen.
* Web rules: full skill read and public source fetched this session (HTTP 200, 8055 bytes, sha256 `d246b026...e0234`) by the Parent; changed-UI rules applied with the Fluent 2, plain-language, WCAG and ASCII overrides. The original independent reviewer lacked fetch tools, so no fresh complete independent web or assistive-technology review is claimed.
* Not run: full gate, `rpi-checks`, full suite, cloud, private `ZF_DATA`, global install, SMB flock proof, control API mount, budget alert reference (AC3), live cohort acceptance. No push, PR, issue, board or merge.
* Integration: `origin/main` is `ad679b96b`; no `src/api` path changed since the base, so no refresh was made. Final host integration waits for #1292 on main, with no unmerged #1292 copy.
