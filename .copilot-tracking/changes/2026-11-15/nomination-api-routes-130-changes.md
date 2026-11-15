<!-- markdownlint-disable-file -->
# RPI Changes: Issue 130 Plain-Language Explanation and Dual-Route API/Workbench Slice

## Metadata

* Task ID: nomination-api-routes-130
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`, `P03-T02`), `P04` (`P04-T01`)
* All remaining active-plan markers: none
* Status basis: All four phases (`P01` through `P04`) executed and verified against `src/core` unit tests (`465` tests across JSON and SQLite stores), `src/api` unit/HTTP/HTML/static-guard/Playwright-keyboard suites (`116` tests), `tools/rename-zava-tests.py` (`25` tests), `ruff format` and `ruff check` (`0` issues), and bare strict `mypy` (`317` files in `src/core` and `294` files in `src/api`, `0` issues).

## Execution Summary

Delivered and verified the complete full-plan implementation (`P01` through `P04`) for the remaining `src/api` and plain-language explanation slice of Issue #130 (`Refs #130`).

## Completed Work

### P01: Core Plain-Language Explanation and Dual-Route Channel Contracts (`P01-T01`, `P01-T02`)

* Added `normalize_route_channel`, `scrub_nomination_restricted_fields`, `nomination_explanation`, `challenge_explanation`, and `filter_explanation_for_viewer` in `src/core/src/zava_forward/core/nomination_route.py`, including deterministic `permitted`, `ai_involved`, `human_decision_owner`, `ai_involvement_explanation`, `sources`, `policy_reasons`, and `uncertainty_note` fields plus `route_mode` and `assisted_channel` preservation in `challenge_trail`.
* Wired dual-route `digital` and `staff_recorded_non_digital` channel normalization, manager-only third-party owner assignment checks on both `_res_nomination_acknowledge` and `_res_challenge_open`, `nomination_permissions`, `confirmed_communicate_representatives`, case-matching `recommendations` lookup, and recursive restricted-vulnerability scrubbing across `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/store.py`, and `src/core/src/zava_forward/core/projection.py`.

### P02: `src/api` Route Boundary and Accessible Keyboard-Operable Workbench Views (`P02-T01`, `P02-T02`)

* Created strictly typed `src/api/src/zava_forward/api/nomination_routes.py` (`nomination_routes_visible`, `build_route_action_payload`, `project_case_nomination_routes`, `render_accessible_nomination_route_html`) and wired `GET /api/cases/<cid>` (including `?view=nomination-routes-html` without adding new `/api/...` route literals) and `POST /api/cases/<cid>/resident` (including structured HTTP `400` `HazardRouted` routing metadata) in `src/api/src/zava_forward/api/server.py`.
* Updated `src/api/src/zava_forward/api/web/panels.js` and `src/api/src/zava_forward/api/web/app.js` to render deterministic plain-language explanations and keyboard-operable dual-route (`digital` and `staff_recorded_non_digital`) acknowledgement, correction, and challenge forms while preserving the `aria-invalid` baseline (`9` sites), table baseline (`14`), plain-language content standard, Epic 149 `"aria-describedby": status.id` error-association invariant, and first-Tab `#nominations summary` focus order.

### P03: Focused Unit, API, Permission, Non-Leakage, and Keyboard/Accessibility Tests (`P03-T01`, `P03-T02`)

* Extended `src/core/tests/test_nomination_route.py` and `src/core/tests/test_resident_decisions.py` to test deterministic plain-language explanations (no-AI, workflow-only rule suggestions, AI model suggestions, `Unknown` uncertainty items, recursive vulnerability-key and prefix scrubbing), dual-route `digital` and `staff_recorded_non_digital` channel validation, manager-only third-party owner assignment, and role redaction across JSON and SQLite stores.
* Extended `src/api/tests/test_nomination_screen.py` and `src/api/tests/test_resident_api.py` and added `src/api/tests/test_nomination_api_routes.py` covering live HTTP JSON and `?view=nomination-routes-html` plain-language explanations, vulnerability non-leakage across authorized and restricted roles, dual-route acknowledgement/challenge/correction submissions, per-role field permissions, structured `HazardRouted` refusal, and headless Playwright Chromium keyboard operability (`Tab`, `Enter`, `Space`, `aria-invalid` focus recovery, and zero horizontal overflow at `1280px` and `320px`).

### P04: Focused Tier Validation and Clean Local Verification (`P04-T01`)

* Executed `ruff format --isolated --line-length 100 --check` (`7` files), `ruff format --check` (`474` files), `ruff check` (`0` errors), targeted `src/core` `unittest` (`465` tests `OK`), targeted `src/api` `unittest` + headless Chromium Playwright + static guards (`116` tests `OK`), `tools/rename-zava-tests.py` (`25` tests `OK`), and bare strict `mypy --cache-dir=/tmp/mypy-130` inside `src/core` (`317` files `OK`) and `src/api` (`294` files `OK`).

## Implementation-Time Plan and Detail Updates

* Local judgment & immediately relevant current-state alignments preserving approved intent:
  * Required explicit `assisted_channel` whenever `channel="staff_recorded_non_digital"` is supplied so assisted non-digital records never omit the assisted medium, and accepted `"permitted_intermediary"` alongside `"trusted_intermediary"` where `allow_intermediary=True`.
  * Included boolean `ai_involved` alongside `permitted`, `human_decision_owner`, `ai_involvement_explanation`, `sources`, `policy_reasons`, and `uncertainty_note`, and enforced manager-only third-party `owner` assignment in `_res_challenge_open` matching `_res_nomination_acknowledge`.
  * Preserved HTTP `400` on `HazardRouted` (`ValueError` subclass asserted by `test_resident_api.py`) while enriching the response body with `dict(e.route, error=str(e))` (`route="independent_hazard_intake"`, `issue="#85"`, `queue_item_created=False`).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff format --isolated --line-length 100 --check` and `ruff format --check` | Modified/added non-excluded files (`7`) and `src/core/` + `src/api/` (`474`) | Passed | `7 files already formatted`; `474 files already formatted` |
| `python3 -m ruff check src/core/ src/api/` | `src/core` and `src/api` | Passed | `All checks passed!` |
| `src/core` targeted unit tests (`test_nomination_route.py`, `test_resident_decisions.py`) | JSON and SQLite stores | Passed | `Ran 465 tests in 63.349s — OK` |
| `src/core` strict `mypy --cache-dir=/tmp/mypy-130` | `src/core` (`317` files) | Passed | `Success: no issues found in 317 source files` |
| `src/api` targeted unit, HTTP, HTML, static guard, and Playwright Chromium keyboard tests | `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_resident_api.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, `test_challenge_non_retaliation_hazard_guard.py` | Passed | `Ran 116 tests in 49.117s — OK` |
| `src/api` strict `mypy --cache-dir=/tmp/mypy-130` | `src/api` (`294` files) | Passed | `Success: no issues found in 294 source files` |
| `python3 tools/rename-zava-tests.py` | Repository naming guard | Passed | `Ran 25 tests in 0.464s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03`, and `P04` and all `Pxx-Txx` tasks marked `[x]`)
* Completed-work evidence and handoff prose: Reconciled across `plan.md` and `changes.md`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining plan items)
* Review readiness: Ready for single post-implementation `rpi-review`

## Blockers

* None

## Remaining Work

* None in declared plan scope (`P01` through `P04` complete)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md, `## Follow-Up Items`
* Resolve human governance open decisions `OD-41` and `OD-42` with Zava North Homes operations and compliance owners, obtain authorized human representative comprehension sign-off, and run hosted PR CI plus independent exact-head review when ready for publication (`Refs #130`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01` through `P04`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`; remaining: none
* Validation coverage: Focused `src/core` + `src/api` unit/HTTP/HTML/Playwright-keyboard/static-guard suites, `ruff check`, `ruff format`, `rename-zava-tests.py`, and strict `mypy` all passed
* Blockers: None
* Current plan and detail updates: Recorded local judgment / current-state alignments above
* Planning and critique state: Ready (`PC-001`..`PC-006` resolved)
* Follow-up items: External human governance (`OD-41`, `OD-42`, representative comprehension, PR CI/review)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
