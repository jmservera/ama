---
title: "RPI Review: nomination-api-routes-130"
description: "Post-implementation single-pass review for Issue 130 plain-language explanation and dual-route API and workbench slice"
ms.date: 2026-11-15
---

## Scope and Evidence

* Task ID: nomination-api-routes-130
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`)
* Assessed boundary: Remaining `src/api` and `src/core` plain-language explanation and dual-route (`digital` and `staff_recorded_non_digital`) nomination acknowledgement, challenge submission, and nomination correction slice of Issue #130 (`Refs #130`) under the focused validation tier (owner decision D4 / #1294: bounded resident workflow API/UI and core projection slice; no workflow, gate-tool, dependency-manifest, Dockerfile, Bicep, SQL DDL, or auth boundary edits).
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md, .copilot-tracking/reviews/2026-11-14/nomination-challenge-130-2142-review.md, fresh `web-design-guidelines` review (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), focused `src/core` (`465` tests) and `src/api` (`116` tests including headless Playwright Chromium keyboard operability and static WCAG/content baseline suites) test outputs, `tools/rename-zava-tests.py` (`25` tests), `ruff`, and strict `mypy` (`317` files in `src/core`, `294` files in `src/api`).

## Opening Review State

* Interpreted review goal: Verify that both requested acceptance criteria for Issue #130 (`Refs #130`) are completely delivered and locally verified across `src/core` and `src/api` without vulnerability leakage, permission bypass, or accessibility/content baseline regression.
* Review scope: Full plan (`P01` through `P04`).
* Evidence readiness: Complete; research, plan, phase details, single-pass critique, changes record, `web-design-guidelines` audit, and focused validation outputs are reconciled.
* Acceptance basis: User prompt acceptance criteria (AC1 and AC2), plan AC-1 through AC-5, `FR-037`/`FR-041`/`FR-043`/`FR-052`/`AC-065`/`AC-071`/`RULE-005`, resolved critique dispositions `PC-001`..`PC-006`, and `ruff`/`mypy`/`unittest` exit `0`.
* First comparison boundary: `P01` domain explanation, scrubbing, and channel rules (`nomination_route.py`, `resident_decisions.py`, `store.py`, `projection.py`) and `P02` HTTP/HTML/UI boundary (`nomination_routes.py`, `server.py`, `web/panels.js`, `web/app.js`).
* Active read-only boundaries: Single-pass review creates only this review artifact and mutates no source, research, plan, detail, critique, or changes files.
* Initial blockers: None for local engineering delivery; external human governance open decisions `OD-41` and `OD-42` and authorized human representative comprehension sign-off remain distinct follow-up items (`Refs #130`).

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-11-15 single-pass review across full diff (`13` source/test files), artifact reconciliation, refreshed `web-design-guidelines` audit of `src/api/src/zava_forward/api/web/panels.js` and `src/api/src/zava_forward/api/web/app.js`, and complete focused validation execution.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01-T01` | Core Plain-Language Explanation and Dual-Route Channel Contracts (`nomination_route.py`) | Reconciled | Delivers `normalize_route_channel`, `scrub_nomination_restricted_fields`, `nomination_explanation`, `challenge_explanation`, `filter_explanation_for_viewer`, and `challenge_trail` dual-route metadata under strict `mypy`. |
| `P01-T02` | Core Workflow and Projection Wiring (`resident_decisions.py`, `store.py`, `projection.py`) | Reconciled | Integrates dual-route channels, manager-only third-party `owner` assignment, `nomination_permissions`, `confirmed_communicate_representatives`, `self.data["recommendations"]` AI metadata lookup, and recursive vulnerability scrubbing across `Store`, `SqlStore`, and `redact_staff_detail`. |
| `P02-T01` | Typed `src/api` Boundary and `server.py` Delegation (`nomination_routes.py`, `server.py`) | Reconciled | Exposes `nomination_routes_visible`, `build_route_action_payload`, `project_case_nomination_routes`, and `render_accessible_nomination_route_html`, wired into `GET /api/cases/<cid>` (including `?view=nomination-routes-html`) and `POST /api/cases/<cid>/resident` without adding new `/api/...` route literals. |
| `P02-T02` | Accessible Resident Workbench Views and Forms (`web/panels.js`, `web/app.js`) | Reconciled | Renders plain-language explanations and keyboard-operable dual-route acknowledgement, correction, and challenge forms using one shared `_routeForm` `aria-invalid` site (`9` sites, `14` tables, `0` banned words, preserved Epic 149 `"aria-describedby": status.id` and first-Tab `#nominations summary` focus order). |
| `P03-T01` | `src/core` Unit Tests (`test_nomination_route.py`, `test_resident_decisions.py`) | Reconciled | Verifies AC1 and AC2 across pure helpers, `Store`, and `SqlStore` (`465` tests passing). |
| `P03-T02` | `src/api` Screen, HTTP, Permission, Non-Leakage, and Keyboard Tests (`test_nomination_screen.py`, `test_resident_api.py`, `test_nomination_api_routes.py`) | Reconciled | Verifies live HTTP JSON and HTML route fragments, role/field permissions, vulnerability non-leakage, structured `HazardRouted` refusal, and headless Playwright Chromium keyboard operability (`116` tests passing). |
| `P04-T01` | Focused Tier Validation | Reconciled | `ruff format`, `ruff check`, `unittest`, `tools/rename-zava-tests.py`, and bare strict `mypy` in `src/core` and `src/api` all exited `0`. |
| `Follow-Up Items` | External human governance (`OD-41`, `OD-42`, representative comprehension sign-off, PR CI/review) | Reconciled | Kept outside active `P01`..`P04` scope and routed as distinct follow-up work (`Refs #130`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`) | `src/core/src/zava_forward/core/nomination_route.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/projection.py` | Added deterministic plain-language explanation builders, recursive restricted-vulnerability scrubbing, dual-route (`digital` and `staff_recorded_non_digital`) channel normalization, manager-only third-party owner checks, and `nomination_permissions` projection. | Verified in `changes.md` and `src/core` unit tests across JSON and SQLite stores. | `465` `src/core` tests `OK`; strict `mypy` (`317` files `OK`); `ruff` `OK`. | Reconciled |
| `P02` (`P02-T01`, `P02-T02`) | `src/api/src/zava_forward/api/nomination_routes.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js` | Added typed API boundary and accessible HTML fragment renderer, delegated live `server.py` case/resident handlers, and wired Resident-tab plain-language explanations and keyboard-operable dual-route forms. | Verified in `changes.md`, static WCAG/content suites, and `web-design-guidelines` review. | `116` `src/api` tests `OK`; strict `mypy` (`294` files `OK`); `ruff` `OK`. | Reconciled |
| `P03` (`P03-T01`, `P03-T02`) | `src/core/tests/test_nomination_route.py`, `src/core/tests/test_resident_decisions.py`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_nomination_api_routes.py` | Added unit, HTTP, HTML, role/field-permission, vulnerability non-leakage, and headless Chromium keyboard operability tests. | All canonical test targets in the plan lock updated/added (`1` added test file, `0` removals). | `465` `src/core` + `116` `src/api` tests `OK`. | Reconciled |
| `P04` (`P04-T01`) | `src/core/`, `src/api/` | Executed focused-tier formatting, linting, strict typing, unit/browser suites, and clean scratch cleanup. | Verified in `changes.md` `## Validation Record` and clean `git status --short`. | All checks exited `0`. | Reconciled |

## Web Interface Guidelines Audit (`file:line`)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing changed web files (preserving owner-selected Fluent 2, WCAG 2.2 baseline, and sentence-case plain-language content standard per repository instructions):

```text
## src/api/src/zava_forward/api/web/panels.js

✓ pass

## src/api/src/zava_forward/api/web/app.js

✓ pass
```

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01`, `P01-T02`, `P02-T01` | Required explicit `assisted_channel` on `channel="staff_recorded_non_digital"` (and accepted `"permitted_intermediary"` where `allow_intermediary=True`), included boolean `ai_involved` on plain-language explanations, enforced manager-only third-party `owner` assignment on `_res_challenge_open`, and returned structured `dict(e.route, error=str(e))` on HTTP `400` `HazardRouted` refusals. | Triggered by `test_resident_api.py` HTTP `400` `HazardRouted` contract and fail-closed assisted-medium clarity; preserves confirmed user intent without changing scope or architecture. | Recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (ordinary local judgment / immediately relevant current-state alignment; `PC-001`..`PC-006` remain satisfied). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six critique findings (`PC-001` through `PC-006`) in `.copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-plan-critique.md` were resolved in the plan and phase details prior to implementation and verified in the delivered code and tests (including clean removal of temporary `/tmp` scratch directories).
* Material revisions: None required; implementation preserved approved architecture, acceptance criteria, and test ownership lock (`4` updated test files, `1` added test file, `0` removed).
* Dependent-work pause assessment: No unapproved early resumption occurred; phases executed strictly in dependency order (`P01` -> `P02` -> `P03` -> `P04`).
* Justification assessment: Supported by complete unit, HTTP, HTML, static-guard, and Playwright Chromium keyboard evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Human governance open decisions `OD-41` and `OD-42`, authorized human representative comprehension sign-off, and hosted PR CI + independent exact-head review (`Refs #130`) | Requires external human policy owners, resident-representative review, and remote PR publication expressly excluded by caller prompt (`Do NOT push or open a PR`). | Zava North Homes housing operations, safeguarding, and compliance owners plus repository owner when ready to publish PR. | Open as distinct external follow-up (`RV-001`); kept outside active `P01`..`P04` completion claims (`Refs #130`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: External human governance ratification (`OD-41`, `OD-42`), representative comprehension sign-off, and remote PR publication remain open on Issue #130

* Related scope: `Follow-Up Items` (outside local `P01`..`P04` engineering boundary)
* Evidence: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md and .copilot-tracking/reviews/2026-11-14/nomination-challenge-130-2142-review.md
* Impact: Issue #130 must be referenced with `Refs #130` (never a closing keyword) until human governance owners ratify `OD-41` and `OD-42`, authorized human representatives complete comprehension review, and the owner pushes and reviews the stacked PR.
* Destination: `follow-up`
* Smallest useful next action: Keep `Refs #130` on the local commit and route `OD-41`, `OD-42`, representative comprehension review, and PR publication to human governance and owner workflows when parent branch `feat/demo-233-same-home-tensions-0825` is ready.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Housing operations/compliance owners and repository owner (`OD-41`, `OD-42`, representative sign-off, PR publication with `Refs #130`) | External human governance and remote publication outside local unpushed slice |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: External human governance decisions (`OD-41`, `OD-42`), authorized human representative comprehension sign-off, and future remote PR CI/review (`Refs #130`).

## Blockers and Remaining Work

* Blockers: None for the requested local `src/api` and plain-language explanation slice.
* Remaining active work: None (`P01` through `P04` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff format --isolated --line-length 100 --check ...` | `7` modified/added non-legacy-excluded Python files | Passed | `7 files already formatted` |
| `python3 -m ruff format --check src/core/ src/api/` | `src/core` and `src/api` (`474` files) | Passed | `474 files already formatted` |
| `python3 -m ruff check src/core/ src/api/` | `src/core` and `src/api` | Passed | `All checks passed!` |
| `python3 -m unittest tests/test_nomination_route.py tests/test_resident_decisions.py -q` | `src/core` (`Store` and `SqlStore`) | Passed | `Ran 465 tests in 63.349s — OK` |
| `python3 -m mypy --cache-dir=/tmp/mypy-130` (in `src/core`) | `src/core` (`317` source files) | Passed | `Success: no issues found in 317 source files` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest tests/test_nomination_screen.py tests/test_nomination_api_routes.py tests/test_resident_api.py tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_content_standard.py tests/test_role_endpoint_inventory.py tests/test_challenge_non_retaliation_hazard_guard.py -q` | `src/api` HTTP, HTML, permissions, vulnerability non-leakage, static WCAG/content guards, and headless Playwright Chromium keyboard operability | Passed | `Ran 116 tests in 49.117s — OK` |
| `python3 -m mypy --cache-dir=/tmp/mypy-130` (in `src/api`) | `src/api` (`294` source files) | Passed | `Success: no issues found in 294 source files` |
| `python3 tools/rename-zava-tests.py` | Repository naming regression suite | Passed | `Ran 25 tests in 0.464s — OK` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every in-scope requirement (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), acceptance criterion (`AC-1`..`AC-5`), and plan critique disposition (`PC-001`..`PC-006`) is implemented, reconciled across artifacts, and proven locally by passing `src/core` (`465`) and `src/api` (`116` including headless Chromium keyboard operability and static WCAG/content guards) test suites, `ruff`, and strict `mypy` with zero defects. External human governance items (`RV-001`) remain properly bounded under `Refs #130`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up (`RV-001`) | Human governance owners (`OD-41`, `OD-42`, representative comprehension sign-off) and owner PR publication (`Refs #130`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused `src/core` (`465` tests + `317`-file `mypy`), `src/api` (`116` tests including Playwright Chromium keyboard operability + `294`-file `mypy`), `ruff check`, `ruff format`, `rename-zava-tests.py` (`25` tests), and `web-design-guidelines` review all passed
* Blockers: None
