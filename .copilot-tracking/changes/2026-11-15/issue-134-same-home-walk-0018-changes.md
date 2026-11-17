<!-- markdownlint-disable-file -->
# RPI Changes: Issue #134 Profile Journey Contract and Connected Same-Home Journey Acceptance

## Metadata

* Task ID: issue-134-same-home-walk-0018
* Related plan: .copilot-tracking/plans/2026-11-15/issue-134-same-home-walk-0018-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-134-same-home-walk-0018-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`), `P02` (`P02-T01`, `P02-T02`, `P02-T03`), `P03` (`P03-T01`), `P04` (`P04-T01`)
* All remaining active-plan markers: none
* Status basis: Every planned task in `P01`-`P04` has been implemented and verified under the Focused validation tier with zero failures, lint/type/format clean across `src/core` and `src/api`, and UX traceability/link guards passing.

## Execution Summary

Completed connected same-home profile journey contract validators and projection bundling in `src/core/src/zava_forward/core/profile_journey_contract.py`, surfaced plain-language `Current owner` and `Next action` continuity on selected-home staff specialist views in `src/api/src/zava_forward/api/web/role-screens.js` (leaving contractor views redacted), strengthened `src/core/tests/test_profile_journey_contract.py` with multi-stage Store walkthrough and negative invariant tests, added full-stack HTTP + live `ResidentPreview` (`GET /resident/view`) + Node `role-screens.js` acceptance tests in `src/api/tests/test_same_home_profile_journey_acceptance.py`, and published `docs/reference/research/ux/profile-journey-contract.md` with knowledge-base index and log updates while keeping `accepted = False` and all human/resident/AT boundaries `not-established`.

## Completed Work

### Core Connected Same-Home Profile Journey Contract (`P01`, `P01-T01`)

* Updated `src/core/src/zava_forward/core/profile_journey_contract.py` while preserving `ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")`, `NON_TEXT`, `validate(record)`, and `gaps(root)` backward compatibility.
* Added `SIX_STAFF_PROFILES`, `REASON_STAFF_PROFILES`, `REDACTED_STAFF_PROFILES`, `BANNED_INTERNAL_TERMS`, `BOUNDARIES` (all `not-established`), `SAME_HOME_NOTICE`, `CONTRACTOR_FORBIDDEN_KEYS`, `check_shared_facts`, `check_vulnerability_redaction`, `check_handover_dependencies`, `check_next_action_continuity`, `project_same_home_bundle`, and `validate_same_home_walk` (`accepted = False`, `status = "complete_in_shape"` when zero blockers remain).

### Specialist Role-Screen Continuity and Core/API Connected Journey Acceptance Suites (`P02`, `P02-T01`, `P02-T02`, `P02-T03`)

* Updated `src/api/src/zava_forward/api/web/role-screens.js` inside `section.screen-evidence` to render `<p data-same-home-next-action="${c.id}">Current owner: ... Next action: ...</p>` whenever `c.work?.next_action` is present on staff projections, omitting internal `work` continuity on contractor views.
* Expanded `src/core/tests/test_profile_journey_contract.py` (`ConnectedSameHomeContractTests`) with a multi-stage Store + `resident_preview.resident_view` walkthrough on `ZF-1` alongside sibling `ZF-2` (safeguarding stop/restart, EPC conflict/reconciliation, technical sign-offs, resident scope/decision, pending-to-accepted handoff with `taskqueues.HELD` redaction, work order + staff-mediated job pack + acknowledged worker receipt, quality return/fix/reinspect/handover, finance match/disposition/payment) and negative mutation tests for every invariant group.
* Created `src/api/tests/test_same_home_profile_journey_acceptance.py` (`SameHomeApiAndResidentPortalWalkTests` and `RoleScreensSameHomeWalkAndRedactionTests`, the single planned new test file, zero skips) exercising authenticated HTTP endpoints across all six staff profiles, `Programme Support Officer`, assigned and unassigned `Contractor` (`404` on unassigned `/api/cases/ZF-1`, `[]` on unassigned `/api/workorders`, `403` on staff-only `/job-pack`), live loopback `ResidentPreview` (`GET /resident/view` for `ZF-1` and sibling `ZF-2`), and Node `vm` execution of `role-screens.js` + `app.js` `workSummary` against live loopback HTTP responses across `programme-queue`, `technical-queue`, `resident-choice`, `procurement-packages`, `quality-queue`, `finance-invoices`, `safety-lead`, and `contractor-job-pack`.

### Canonical UX Profile Journey Contract Reference and Knowledge Base Index (`P03`, `P03-T01`)

* Authored `docs/reference/research/ux/profile-journey-contract.md` following AMA Markdown style (YAML frontmatter without `# H1`, `*` unordered lists, plain ASCII punctuation, zero em dashes, valid PRD/BRD requirement IDs, runnable test module references, and explicit `not-established` human/resident/AT boundaries).
* Indexed `profile-journey-contract.md` in `docs/reference/README.md` and appended a dated `[2026-11-15] create` entry to `docs/reference/log.md`.

### Focused Validation and Web Interface Guidelines Verification (`P04`, `P04-T01`)

* Verified `src/core` and `src/api` with `ruff check .`, `ruff format --check .`, `mypy`, and all targeted unit, traceability, link, manifest, and needs-inventory suites without modifying `role_screens_browser_check.py`.
* Refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and reviewed `src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass`.

## Implementation-Time Plan and Detail Updates

* Local judgment refinements (preserved approved intent without changing scope or plan markers):
  * Accepted BOTH `job_pack.SUBMITTED` and `job_pack.ACKNOWLEDGED` non-acceptance statuses in `check_handover_dependencies` because `job_pack.worker_receipt(...)` initializes in `SUBMITTED` before `job_pack.acknowledge_receipt(...)` records `ACKNOWLEDGED`, while still blocking `accepted = True` or downstream quality bypass.
  * Used `store.audit_entries()` (falling back to `store.data.get("audit", [])`) in `project_same_home_bundle` to match `Store`'s public audit accessor.
  * Added `contractor_private_markers` alongside `private_markers` in `check_vulnerability_redaction` / `validate_same_home_walk` so staff-visible resident contact fields (such as `resident.phone`) are verified absent from contractor, job-pack, work-order, and resident-preview payloads while adjustment-specific substrings remain forbidden on non-reason staff projections as well.
  * Asserted HTTP `404` (rather than `403`) when an unassigned contractor requests `/api/cases/ZF-1`, matching server non-enumeration behavior.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` & `ruff format --check .` | `src/core` (264 files) | Passed | All checks passed; 264 files formatted |
| `mypy` | `src/core` (317 files) | Passed | `Success: no issues found in 317 source files` |
| Targeted `src/core` unit, manifest, needs & link suites | `test_profile_journey_contract`, `test_perspective_walkthroughs`, `test_journey_acceptance`, `test_journey_trace`, `test_journey_store`, `test_resident_preview`, `test_scenario_manifest`, `test_needs_inventory`, `test_atlas_screen_trace`, `test_live_doc_links` | Passed | 105 tests (`103 + 2`), `OK` (`0` failures, `0` skips) |
| `ruff check .` & `ruff format --check .` | `src/api` (202 files) | Passed | All checks passed; 202 files formatted |
| `mypy` | `src/api` (286 files) | Passed | `Success: no issues found in 286 source files` |
| Targeted `src/api` acceptance, screen, copy & traceability suites | `test_same_home_profile_journey_acceptance`, `test_resident_preview_api`, `test_role_screens`, `test_role_screens_conformance`, `test_role_screens_connected_journey`, `test_role_screens_same_home_identity`, `test_role_screens_stage_map_focus`, `test_role_screens_tensions_same_home`, `test_connected_home_check`, `test_content_standard`, `test_epic149_ux_journey_requirement_traceability`, `test_ux_design_traceability`, `test_screen_design_traceability` | Passed | 123 tests in 9.302s, `OK` (`0` failures, `0` skips) |
| `web-design-guidelines` live rules review | `src/api/src/zava_forward/api/web/role-screens.js` | Passed | Refreshed `vercel-labs/web-interface-guidelines` `command.md`; `src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass` |
| `scenario-manifest.json` recipe SHA check | `role_screens_browser_check.py` untouched | Passed | `role_screens_browser_check.py` unmodified; `test_scenario_manifest.py` and `test_needs_inventory.py` passed |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P02-T03`, `P03`, `P03-T01`, `P04`, `P04-T01` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled across `plan.md` and `changes.md`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan items)
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None in active plan (`P01`-`P04` complete). Post-`rpi-review` local commit on `feat/ux-134-same-home-walk-0018` will capture code, tests, docs, and `.copilot-tracking/` artifacts together without pushing.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-134-same-home-walk-0018-plan.md, `## Follow-Up Items`
* Live user walkthroughs across the 11 perspectives (`#155`, OQ-004, OQ-005, OQ-011) and assistive-technology conformance verification (`#151`) remain open human-gated acceptance items before `#134` (`AC-034` through `AC-043`) can be closed.
* Optional browser-harness extension: extend `src/api/checks/role_screens_browser_check.py` (updating `scenario-manifest.json`'s recipe SHA) if Chromium-level assertions on `data-same-home-next-action` are desired alongside the existing Node `vm` and live HTTP suites.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`, `P03`, `P04` all complete)
* Validation coverage: Focused tier passed (`mypy`, `ruff check`, `ruff format --check`, 105 `src/core` tests, 123 `src/api` tests, `web-design-guidelines` pass)
* Blockers: None
* Current plan and detail updates: All `P01`-`P04` markers checked; 4 minor local judgment refinements documented
* Planning and critique state: Complete (`PC-001` through `PC-006` resolved)
* Follow-up items: Live perspective walkthroughs (`#155`), AT conformance runs (`#151`), optional Chromium check assertion on `data-same-home-next-action`
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`RPI Agent`, confirmed automatic mode)
