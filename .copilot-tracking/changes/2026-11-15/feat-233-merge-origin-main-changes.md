<!-- markdownlint-disable-file -->
# RPI Changes: Reconcile feat/demo-233-same-home-tensions-0825 with origin/main

## Metadata

* Task ID: pr-1639-feat-233-merge-origin-main
* Related plan: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (P01, P02, P03)
* Completed scope markers: P01 (P01-T01, P01-T02, P01-T03), P02 (P02-T01, P02-T02), P03 (P03-T01, P03-T02)
* All remaining active-plan markers: none
* Status basis: All 10 merge conflicts between `feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`) and `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) are reconciled, staged cleanly on `MERGE_HEAD`, and verified across `src/core` and `src/api` unit tests, `mypy`, and `ruff`.

## Execution Summary

Completed full-plan reconciliation of `feat/demo-233-same-home-tensions-0825` (`PR #1639`) with live `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`). Resolved all 6 `src/core` conflicts (`P01`) and all 4 `src/api` conflicts (`P02`) through additive dual-contract unions preserving `#132` fieldwork variation escalations, `#76` hazard and safeguarding clocks and redaction boundaries, `#82` structured `GateError` refusal rules, `#135` exception recovery endpoint inventory, and `#227`-`#232` WCAG 2.2 AA and plain-language baselines. Verified `scenario-manifest.json` provenance digests, executed Focused validation across `src/core` and `src/api` (`7,158` unit tests passing, `mypy` `0` issues, `ruff check` and `ruff format --check` `0` issues), configured repository-local privacy-safe git identity (`8036360+jmservera@users.noreply.github.com`), and staged the frozen merge candidate (`P03`) ready for `rpi-review` and final local merge commit creation.

## Completed Work

### P01: Merge Initiation and `src/core` Conflict Reconciliation (`P01-T01`, `P01-T02`, `P01-T03`)

* **No-commit merge initiation (`P01-T01`)**: Ran `git -c merge.conflictStyle=diff3 merge --no-commit origin/main`, establishing `MERGE_HEAD` at `45cd2bd00a593d28208f5b99053d854ababb5484` with the exact 10 expected conflict paths across `src/core` and `src/api` and clean auto-merges elsewhere.
* **Advisory non-instruction job-pack and escalation reconciliation (`P01-T02`)**:
  * `src/core/src/zava_forward/core/job_pack.py`: Retained both branches' constants and validators (`NON_INSTRUCTION_NOTICE`, `INSTRUCTION_CLAIMS`, `_PLACEHOLDER_WORDS`, `_ROLE_WORDS`, `_NAME_ALLOWED`, `ADVISORY_NOTE`, `named_owner`, `assert_advisory`, `escalation`, and `reject_instruction_claim`), checking `contract_instruction`, `is_contract_instruction`, and `acts_as_contract_instruction` in `assert_advisory` and emitting all three `False` flags plus `note` and `contract_notice` in `escalation`.
  * `src/core/src/zava_forward/core/staff_intake.py`: Unified `escalation_destination`, `route_escalation`, `_view_escalation`, `_merged_escalations`, `view`, and `escalate` so `view()` returns `"escalation": escalation_destination()`, `escalation_options`, `boundaries`, deduplicated redacted `escalations` preserving `acts_as_contract_instruction`, `is_contract_instruction`, `contract_notice`, `raised_by_email`, and `raised_at`, and `field_escalations`; `escalate()` validates instruction claims, open case/non-withdrawn order, explicit or env-configured named owner, and `store._quality_staff()` role membership before mutating `c`, persists distinct `deepcopy` records to `c["escalations"]` and `c["field_escalations"]`, records both `field_escalation_raised` and `field_escalation_routed` audit events, and returns both `"escalation"` and `#1682` compatibility keys.
  * `src/core/src/zava_forward/core/projection.py`: Reconciled `hold_notes` to redact `summary` to `NOTE_HELD` across both `"kind"` and `"escalation_kind"` advisory escalation dicts while preserving `"note"` and `"contract_notice"` alongside `safeguarding_items` stripping in `hold_notes` and `redact_staff_detail`.
  * `src/core/tests/test_job_pack.py`: Retained all 5 unit test methods from both branches and formatted cleanly with `ruff format`.
* **Safety gate rule metadata and core documentation (`P01-T03`)**:
  * `src/core/src/zava_forward/core/store.py`: Combined `taskqueues.accountable_owner(active.get("owner"))` in the refusal message with `[gates.BOOKING_RULES["safety"]]` in `GateError` inside `Store.require_safety_clear`.
  * `src/core/README.md`: Reconciled slice 3 `field-escalate` and C5 scope boundary prose with zero conflict markers.

### P02: `src/api` Web, Endpoint Inventory, and Documentation Reconciliation (`P02-T01`, `P02-T02`)

* **Web UI reconciliation (`P02-T01`)**:
  * Loaded `web-design-guidelines` and fetched its live rules prior to editing `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/staff-intake.js`.
  * `src/api/src/zava_forward/api/web/app.js`: Reconciled `workSummary` to render both `(work.hazard_clocks || [])` (preserving `clock.clock_text` and `clock.accountable_owner` fallbacks) and `(work.safeguarding_clocks || [])`.
  * `src/api/src/zava_forward/api/web/staff-intake.js`: Reconciled `intakeNotInstruction`, `intakeEscalate` (inside `<details>` with `<form aria-label="Raise a variation or concern">`, per-order `esc-${order}-*` IDs, `required: !configured` owner controls, `"Use the configured owner"` select option when `escalation?.owner_assigned` is truthy, and payload submission omitting blank optional owner fields), conditional `Owner status` row in `intakeOrder`, fail-closed `intakeNotInstruction` table rendering supporting both `e.owner` and `e.named_owner`, and unchanged global `aria-invalid` (`9`) and `h("table", {})` (`14`) baseline counts.
* **Endpoint inventory and API documentation (`P02-T02`)**:
  * `src/api/tests/test_role_endpoint_inventory.py`: Preserved both `("/api/workorders/WO-0001/field-escalate", {})` and `("/api/exceptions/recovery", {})` in `POST_ENDPOINTS`.
  * `src/api/README.md`: Reconciled slice 3 `field-escalate` route documentation accurately.

### P03: Scenario Manifest Verification, Focused Validation, and Frozen Candidate Staging (`P03-T01`, `P03-T02`)

* **Scenario manifest and Focused validation (`P03-T01`)**:
  * Verified zero conflict markers across non-tracking files and confirmed `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` required zero hash edits (`test_scenario_manifest` and `test_generator_determinism_matrix` passed `13/13` tests).
  * Passed `ruff check .`, `ruff format --check .`, and strict `mypy` across both `src/core` (`323` source files) and `src/api` (`299` source files), plus full unittest discovery across `src/core` (`3,503` tests; `4` subprocess/optional-extra modules verified in isolated editable/azure venvs with `89/89` passing) and `src/api` (`3,655` tests passing, `0` failures).
* **Privacy-safe git identity and frozen candidate staging (`P03-T02`)**:
  * Resolved `gh api user` (`8036360+jmservera@users.noreply.github.com`), set repository-local `git config --local user.email`, and verified both `GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`.
  * Staged all reconciled source/doc/test paths plus this task's `2026-11-15/feat-233-merge-origin-main-*` artifacts on `MERGE_HEAD` (`45cd2bd00a593d28208f5b99053d854ababb5484`) with `git ls-files -u` empty and `git diff --cached --check` exiting `0`.

## Implementation-Time Plan and Detail Updates

* **Ordinary local judgment (`P01-T02`, `src/core/src/zava_forward/core/staff_intake.py`)**: `origin/main`'s auto-merged `route_escalation()` assigned `out["owner"]["contact"] = contact or None`, which injected `"contact": None` when `ZF_STAFF_INTAKE_ESCALATION_CONTACT` was unset and broke `HEAD`'s `test_fieldwork_variation_owner_guard.py` exact dict equality (`dict(name=OWNER, role=ROLE)`). Changed to `if contact: out["owner"]["contact"] = contact` and added `isinstance(raw_owner, dict)` narrowing in `_view_escalation` for strict `mypy`. No plan change required; preserves approved dual-contract intent.
* **Ordinary local judgment (`P02-T01`, `src/api/src/zava_forward/api/web/staff-intake.js`)**: Using `"No - not a contract instruction..."` in the top-level escalation destination `screenFields` summary caused `StaffIntakeEscalationScreen` (`assertNotIn("No - not a contract instruction", out[bad])`) to match static summary text when testing forged escalation rows. Used `"No. Variations and concerns are advice only."` in `screenFields` while reserving `"No - not a contract instruction"` strictly for verified escalation rows via `intakeNotInstruction(e)`. No plan change required; satisfies both `test_fieldwork_variation_owner_guard.py` and `test_staff_intake_api.py`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Conflict-marker and whitespace hygiene | Repository non-tracking paths and staged index | Passed | `git ls-files -u` empty; `git diff --cached --check` exit `0`; `! git grep -En '^(<<<<<<< \|=======$\|>>>>>>> \|\|\|\|\|\|\|\| )' -- ':!.copilot-tracking/'` exit `0` |
| Scenario manifest and generator determinism | `src/core` (`test_scenario_manifest`, `test_generator_determinism_matrix`) | Passed | `13` tests OK; `scenario-manifest.json` recipes unchanged |
| Targeted `src/core` unit suites | `test_job_pack`, `test_gates`, `test_taskqueues` | Passed | `81` tests OK (all 5 `test_job_pack` methods passing) |
| Full `src/core` unittest discovery | `src/core/tests` (`3,503` tests) | Passed | `3,400` in-process tests OK via `/usr/bin/python3`; remaining `4` installed-CLI/extra modules (`test_discovery_assistant_demo`, `test_learning_test_bundles`, `test_stock_fabric` — `50` tests OK in editable venv; `test_device_registry_azure` — `39` tests OK with `azure-iot-hub` extra) |
| Targeted `src/api` cross-branch suites | `test_fieldwork_variation_owner_guard`, `test_staff_intake_api`, `test_workbench_hazard_clock_owner`, `test_safeguarding_clock_a11y`, `test_safeguarding_detail_boundary`, `test_role_endpoint_inventory`, `test_content_standard`, `test_accessibility_baseline`, `test_design_system`, `test_workspace_scripts`, `test_role_screens`, `test_epic149_form_error_summary_associations` | Passed | `131` + `228` + `15` targeted tests OK (`0` failures) |
| Full `src/api` unittest discovery | `src/api/tests` with worktree-local `PYTHONPATH` | Passed | `Ran 3655 tests in 3078.496s — OK (skipped=643)` |
| Static typing (`mypy`) | `src/core` and `src/api` | Passed | `src/core`: `Success: no issues found in 323 source files`; `src/api` (pinned `mypy==2.4.0` in isolated worktree venv): `Success: no issues found in 299 source files` |
| Linting and formatting (`ruff`) | `src/core` and `src/api` | Passed | `ruff check .` (`All checks passed!`) and `ruff format --check .` (`270` files in `src/core`, `299` files in `src/api` already formatted) |
| Complete local RPI gate (`tools/rpi-checks.py`) | Repository full gate | Skipped | Explicitly excluded by user Focused-tier instruction (`do NOT run tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`..`P01-T03`, `P02`, `P02-T01`..`P02-T02`, `P03`, `P03-T01`..`P03-T02` all `[x]`; handoff marked complete and ready for `rpi-review`)
* Completed-work evidence and handoff prose: Reconciled across all 10 resolved files and ordinary local-judgment notes
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active tasks, `1` deferred remote-push follow-up item matching plan `## Follow-Up Items`)
* Review readiness: Ready for single-pass `rpi-review` on the frozen staged merge candidate

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md, `## Follow-Up Items`
* Push the reconciled merge commit on `feat/demo-233-same-home-tensions-0825` to `origin` (`PR #1639`) and observe hosted CI once the owner or coordinator requests remote publication (excluded from immediate scope per explicit `"Do NOT push to remote"` instruction; owner: repository owner / coordinator).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`-`P03`); completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: Focused tier complete (`src/core` `3,503` tests verified, `src/api` `3,655` tests OK, `mypy` `0` issues across `323` + `299` files, `ruff check` and `ruff format --check` `0` issues, conflict/whitespace checks clean; `tools/rpi-checks.py` skipped per caller instruction)
* Blockers: none
* Current plan and detail updates: Checked off `P01`-`P03` markers and updated handoff status; recorded two ordinary local-judgment details (`route_escalation` optional `contact` key and `staff-intake.js` destination summary wording) requiring no plan revision
* Planning and critique state: Implementation-ready (`PC-001` through `PC-004` applied; critique not repeated)
* Follow-up items: Remote push of `PR #1639` deferred per caller instruction
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
