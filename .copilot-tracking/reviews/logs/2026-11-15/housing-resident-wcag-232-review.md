<!-- markdownlint-disable-file -->
# Review: Housing Officer and Resident Engagement WCAG 2.2 AA Baseline (#232)

## Scope and Evidence

* Task ID: 2026-11-15-housing-resident-wcag-232
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Automated WCAG 2.2 AA engineering baseline (`#151`) for `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` across `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/panels.js`, coupled selector alignment in `src/api/checks/case_journey_browser_check.py`, and regression suite `src/api/tests/test_housing_resident_wcag_232.py` under Focused-tier validation, preserving `test_accessibility_baseline.py` and `test_content_standard.py`.
* Plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md, `git diff` across `src/api/`, Focused-tier `unittest`/`ruff`/`mypy`/`rename-zava-tests.py` runs, Playwright Chromium + pinned `axe-core 4.10.3` runs (`role_screens_browser_check.py`, `ZF_RESIDENT_BROWSER=1`, `case_journey_browser_check.py --axe`), and refreshed Web Interface Guidelines audit.

## Opening Review State

* Interpreted review goal: Verify once against concrete repository, test, and browser evidence whether the `#232` implementation fulfills all planned requirements (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), acceptance criteria (`AC-1`..`AC-4`, with post-review commit/rebase `AC-5` ready), and critique dispositions (`PC-001`..`PC-004`) without regressing existing accessibility or plain-language baselines, while distinguishing automated engineering checks from human assistive-technology acceptance (`Refs #232`).
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`)
* Evidence readiness: Ready — plan, phase details, single-pass critique, research, changes record, source diff, unit/lint/type results, and Playwright + pinned `axe-core 4.10.3` checks are present and reconciled.
* Acceptance basis: Approved plan requirements (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), acceptance criteria (`AC-1`..`AC-5`), critique dispositions (`PC-001`..`PC-004`), AMA Web Development Guidance, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/research/ux/content-standard.md`.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`–`P03` and `## Follow-Up Items`, excluding out-of-scope specialist screens (`safety-lead`, `hazard-triage`, `procurement`, `contractor`).
* Active read-only boundaries: This stage writes only `.copilot-tracking/reviews/logs/2026-11-15/housing-resident-wcag-232-review.md` (plus RPI Agent session-state transition pointers) and mutates no source, test, plan, detail, critique, research, or changes files.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass comparison on 2026-11-15 across all nine checked plan markers (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`), both implementation-time current-state updates, all four critique dispositions (`PC-001`..`PC-004`), refreshed Web Interface Guidelines findings, Focused-tier unit/lint/format/mypy/migration results, and Playwright + pinned `axe-core 4.10.3` browser runs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `### P01: Staff Route, Live-Status, and Focus Parity (P01-T01, P01-T02)` | Reconciled | `#/role/contact_centre` route + script gating (`split("?")[0]`), shared-host `aria-live="polite"`, `!signal.aborted`-guarded `#workspace-status` lifecycle announcements, preserved `section#screen-evidence` `"aria-label": "Evidence for ${c.id}"`, and single-lookup `a[data-jump]` focus match plan and details. |
| `P02` (`P02-T01`, `P02-T02`) | `### P02: Housing and Resident Case Panel Accessibility (P02-T01, P02-T02)` | Reconciled | Slugified `actForm` IDs with collision disambiguation and `type: "button"`, coupled `#f-raise-a-commitment-supplier` check selector, `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]`, `<th scope="row">`, and plain-language state cues preserving `test_resident_api.py` and `test_case_journey.py` contracts match plan and details. |
| `P03` (`P03-T01`, `P03-T02`) | `### P03: Focused WCAG 2.2 Verification, Web Guidelines Audit, and Validation (P03-T01, P03-T02)` | Reconciled | 8-test strict-typed `src/api/tests/test_housing_resident_wcag_232.py`, refreshed Web Interface Guidelines `file:line` review (`✓ pass`), Focused-tier checks, and Playwright + pinned `axe-core 4.10.3` browser runs match plan and details. |
| `## Follow-Up Items` | `## Follow-Up Items` in plan and changes record | Reconciled | Human assistive-technology/mobile walkthrough (`#151`/`#155`) and full-tier `specialist_keyboard_browser_check.py` `NO_REGION_GAPS` alignment (`#1294`) remain outside active `P01`–`P03` completion claims with named owners. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js` | Normalized `isRoleScreensDestination` with `split("?")[0]` across all role hashes and mapped `#/role/contact_centre` via `Object.hasOwn` to `resident-service-issues` without eagerly loading `panels.js` or `chat.js`. | `app.js` `isRoleScreensDestination`; `role-screens.js` `ROLE_HASH_SCREENS`; `test_housing_resident_wcag_232.py` script-isolation and route-alias tests. | Passed (`test_housing_resident_wcag_232.py`, `role_screens_browser_check.py 232`) | Reconciled; zero gaps. |
| `P01-T02` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `"aria-live": "polite"` on the three shared-host `role="status"` nodes, added `!signal.aborted`-guarded `#workspace-status` announcements across invalid-page, unavailable-screen, chooser (`installed.length` branched), loading, and record-mismatch branches, preserved `section#screen-evidence` `"aria-label": "Evidence for ${c.id}"`, and resolved `a[data-jump]` target once before `.focus()` and `.scrollIntoView({ block: "start" })`. | `role-screens.js` `screenTable`, `roleScreensView`, and `a[data-jump]` listener; `test_housing_resident_wcag_232.py` live-region and jump-nav tests. | Passed (`test_housing_resident_wcag_232.py`, `role_screens_browser_check.py 232` and `232s` with `0` axe 4.10.3 violations and `0` incomplete items) | Reconciled; zero gaps. |
| `P02-T01` | `src/api/src/zava_forward/api/web/panels.js`, `src/api/checks/case_journey_browser_check.py` | Slugified `actForm` field `id` and `<label for>` attributes (`f-${formSlug}-${slug(name)}` with duplicate disambiguation), set `type: "button"` on manual submit button, and aligned coupled `#f-raise-a-commitment-supplier` selector in `case_journey_browser_check.py`. | `panels.js` `actForm`; `case_journey_browser_check.py`; `test_housing_resident_wcag_232.py` `test_panels_act_form_and_resident_panel_wcag_semantics`. | Passed (`test_housing_resident_wcag_232.py`, `test_case_journey.py`, `case_journey_browser_check.py --axe`) | Reconciled; zero gaps. |
| `P02-T02` | `src/api/src/zava_forward/api/web/panels.js` | Wrapped `Resident decisions by measure` in `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]`, promoted measure names to `<th scope="row">`, and added plain-language textual state cues (`Confirmed`, `Waiting for resident`, `Action needed`, `Unknown`) across contractor readiness, measure rows, update commitments, and service/remedy items while preserving `test_resident_api.py` contiguous `"Response: <status>. Owner: <name>."` / `"Remedy: <status>. Owner: <name>."` substrings. | `panels.js` `residentPanel`; `test_housing_resident_wcag_232.py` Resident-panel VM assertions. | Passed (`test_housing_resident_wcag_232.py`, `ZF_RESIDENT_BROWSER=1 test_resident_api.py`, `test_accessibility_baseline.py`, `test_content_standard.py`) | Reconciled; zero gaps. |
| `P03-T01` | `src/api/tests/test_housing_resident_wcag_232.py` | Authored 8-test strict-typed WCAG 2.2 AA regression module covering static guards, Node VM routing/isolation, default-deny and prototype-key rejection, `aria-live` and `#workspace-status` lifecycle, landmarks/headings/jump focus/`section#screen-evidence` naming, `.table-scroll` and `<th scope="row">`, `ensure_ascii=False` Unicode fidelity, `panels.js` semantics/state cues, and Python RBAC/safeguarding redaction without mutating `sys.modules`. | `src/api/tests/test_housing_resident_wcag_232.py`. | Passed (`unittest` 51 focused / 115 coupled tests, `ruff check`, `ruff format --check`, `mypy` across 292 files) | Reconciled; zero gaps. |
| `P03-T02` | `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md`, `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md` | Refreshed Web Interface Guidelines (`✓ pass` on `app.js`, `role-screens.js`, `panels.js`), executed Focused-tier, coupled unit, and Playwright + pinned `axe-core 4.10.3` checks, and reconciled tracking artifacts. | Changes record `## Validation Record` and `## Pre-Review Reconciliation`. | Passed (`unittest`, `ruff`, `mypy`, `rename-zava-tests.py`, Playwright/axe) | Reconciled; zero gaps. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T02` (`role-screens.js`) | Preserved `"aria-label": "Evidence for ${c.id}"` alongside `id: "screen-evidence"` and `<h2 id="screen-evidence-heading" tabindex="-1">` on the selected-home section. | `checks/role_screens_browser_check.py 232` caught that earlier commit `321a22960` had swapped `aria-label` for `aria-labelledby`, breaking `get_by_role("region", name="Evidence for ZF-1", exact=True)`; no new user decision required because preserving region naming fulfills approved intent. | Updated `role-screens.js`, added regression assertion in `test_housing_resident_wcag_232.py`, and reconciled `housing-resident-wcag-232-phase-details.md` and `housing-resident-wcag-232-changes.md`. | Not needed (immediately relevant current-state update preserving `PC-002` and approved scope). | Reconciled and justified. |
| `P02-T01` (`src/api/checks/case_journey_browser_check.py`) | Updated coupled selector from `[id="f-Raise a commitment-supplier"]` to `#f-raise-a-commitment-supplier` in non-gate browser check script run by hosted CI `src-ci.yml`. | Inspecting `.github/workflows/src-ci.yml` and executing `case_journey_browser_check.py --axe` confirmed direct coupling to `P02-T01` `actForm` ID slugification; Focused tier preserved under `#1294` because selector alignment changes no permissions, dependencies, security controls, or gate semantics. | Updated `case_journey_browser_check.py`, `housing-resident-wcag-232-plan.md`, `housing-resident-wcag-232-phase-details.md`, and `housing-resident-wcag-232-changes.md`. | Not needed (immediately relevant coupled test-selector alignment preserving `PC-004` and approved scope). | Reconciled and justified. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four findings from `.copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md` (`PC-001` High contiguous `Response`/`Remedy` `Owner` contract + `ZF_RESIDENT_BROWSER` validation, `PC-002` High shared-host/`#232` `aria-live` boundary + `installed.length` chooser + `!signal.aborted` guard, `PC-003` Medium caller-mandated commit subject + post-review rebase onto `origin/feat/demo-233-same-home-tensions-0825`, and `PC-004` Low `split("?")[0]` route normalization + local `panels.js` helper scoping) were applied directly in the plan and verified in implementation and tests.
* Material revisions: None — neither implementation-time update altered requirements, architecture, acceptance criteria, dependency order, or validation tier.
* Dependent-work pause assessment: No pause required; tasks executed in plan order `P01` -> `P02` -> `P03` with single-pass critique preserved unchanged.
* Justification assessment: Fully supported by unit, Node VM, static-guard, linter, strict `mypy`, and Playwright + pinned `axe-core 4.10.3` evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Human assistive-technology (NVDA, JAWS, VoiceOver) and 360px mobile walkthrough across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing `#232` | Automated DOM, Node VM, and Playwright/axe checks verify the `#151` engineering baseline, whereas AMA UX governance (`#151`, `#155`, `wcag-conformance-baseline.md`) requires human AT verification before accessibility acceptance and issue closure (`Refs #232`). | Human accessibility reviewer — execute scripted keyboard + screen-reader walkthrough and record acceptance evidence on `#232`. | Open distinct follow-up (`RV-001` -> `follow-up`). |
| Reconcile parent-branch `resident-service-issues` (`Routes to ask` region) declaration in `src/api/checks/specialist_keyboard_browser_check.py` | Parent commit `#86` added `redressRoutePanel` (`Routes to ask`) to `resident-service-issues` while `NO_REGION_GAPS` in `specialist_keyboard_browser_check.py` still listed `resident-service-issues`; modifying a gate check script falls under full-tier governance (`#1294`) outside this Focused-tier PR. | Harness maintainer — update `NO_REGION_GAPS` in a dedicated full-tier gate-tool PR. | Open distinct follow-up (`RV-002` -> `follow-up`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Human assistive-technology and mobile acceptance walkthrough remains required before closing Issue #232

* Related scope: Plan `## Follow-Up Items` (`#232` closure boundary under `#151` and `#155`)
* Evidence: `docs/reference/research/ux/wcag-conformance-baseline.md`; `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` (`## Validation Record`, `## Follow-Up Items`)
* Impact: Automated Node VM, static-guard, and Playwright + pinned `axe-core 4.10.3` checks verify engineering WCAG 2.2 AA semantics, keyboard reachability, focus restoration, `320px` reflow, and non-colour textual state cues, but AMA Web Development Guidance specifies that engineering checks alone do not establish full accessibility acceptance; this delivery therefore uses `Refs #232` rather than `Closes #232`.
* Destination: `follow-up`
* Smallest useful next action: Run a human NVDA/JAWS/VoiceOver and 360px mobile walkthrough across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` and attach the evidence to `#232`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Parent-branch `specialist_keyboard_browser_check.py` `NO_REGION_GAPS` still lists `resident-service-issues` after `#86` added `Routes to ask`

* Related scope: Plan `## Follow-Up Items` (out-of-scope full-tier gate harness synchronization)
* Evidence: `src/api/checks/specialist_keyboard_browser_check.py`; `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` (`## Follow-Up Items`)
* Impact: Does not affect `role_screens_browser_check.py 232`/`232s`, `case_journey_browser_check.py --axe`, or `src-ci.yml`, and keyboard Tab reachability across `Routes to ask` passed in Playwright, but keeping `specialist_keyboard_browser_check.py` aligned in a dedicated full-tier PR avoids stale `NO_REGION_GAPS` expectations on future full-gate runs.
* Destination: `follow-up`
* Smallest useful next action: Open a dedicated full-tier gate-tool PR updating `NO_REGION_GAPS` for `resident-service-issues` in `src/api/checks/specialist_keyboard_browser_check.py` with a verified external `rpi-checks.py --all` receipt.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (`RV-001` and `RV-002` are non-blocking residual follow-up items) | None (`rpi-implement`, `rpi-plan`, and `rpi-research` not required) | Human accessibility reviewer (`RV-001`) and harness maintainer (`RV-002`) | Zero implementation defects, decision gaps, or material research gaps within the approved Focused-tier `#232` scope. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` (`follow-up`, human accessibility reviewer): Execute human NVDA/JAWS/VoiceOver and 360px mobile walkthroughs on `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing `#232`.
* `RV-002` (`follow-up`, harness maintainer): Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier PR under `#1294`.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None in RPI implementation/review scope (caller-requested local Git commit and clean rebase onto `origin/feat/demo-233-same-home-tensions-0825` execute immediately after RPI Review transitions session state to `Follow-up`).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests/test_housing_resident_wcag_232.py tests/test_accessibility_baseline.py tests/test_content_standard.py -v` | `src/api` (`#232` WCAG + baseline + plain-language copy) | Passed | `Ran 51 tests in 0.460s - OK` |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest` across 10 coupled WCAG, role-screen, case-journey, and resident modules | `src/api` coupled regression surface | Passed | `Ran 115 tests in 2.681s - OK` |
| `ZF_RESIDENT_BROWSER=1 PYTHONPATH=../core/tests:../agents/tests python -m unittest tests/test_resident_api.py -q` | `src/api` Resident tab live Chromium workflow | Passed | `Ran 21 tests in 5.839s - OK` |
| `ZF_AXE_JS=<axe-4.10.3.min.js> python checks/role_screens_browser_check.py` (`parent`, `232`, `232s`) | `role-screens.js` specialist screens + pinned `axe-core 4.10.3` | Passed | `0` axe violations and `0` incomplete items across queue + selected home on `232` and `232s`, `320px`/`390px`/`1280px` reflow, keyboard Tab table-region reachability, reduced motion, and zero POSTs |
| `ZF_AXE_JS=<axe-4.10.3.min.js> python checks/case_journey_browser_check.py --axe` | `panels.js` + `case_journey_browser_check.py` | Passed | `#f-raise-a-commitment-supplier` field-clear assertion, Resident tab mutations/dirty-draft retention, `320px` Resident reflow, and `axe no serious/critical` scans across every case tab passed (untouched Overview `.case-summary` `1637.4px` vs `1600px` local Chromium 156 font-height check noted as pre-existing outside `#232`) |
| `ruff check . && ruff format --check . && mypy` | `src/api` (`src`, `tests`, `checks`) | Passed | `All checks passed!`, `208 files already formatted`, `Success: no issues found in 292 source files` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression | Passed | `Ran 25 tests in 0.538s - OK` |
| Refreshed `web-design-guidelines` review (`command.md`) | `app.js`, `role-screens.js`, `panels.js` | Passed | `✓ pass` across all three changed web files |

## Outcome

* Outcome: Residual work
* Outcome rationale: Every planned engineering task (`P01`–`P03`), acceptance criterion (`AC-1`..`AC-4`), and critique disposition (`PC-001`..`PC-004`) passed static, Node VM, Python RBAC/redaction, strict typing, plain-language copy, Web Interface Guidelines, and Playwright + pinned `axe-core 4.10.3` validation with zero implementation defects, decision gaps, or research gaps. Outcome is recorded as `Residual work` rather than claiming complete accessibility conformance because human assistive-technology/mobile acceptance (`RV-001`, `#151`/`#155`, hence `Refs #232`) and out-of-scope full-tier `specialist_keyboard_browser_check.py` alignment (`RV-002`, `#1294`) remain open distinct follow-up items.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | `follow-up` (`RV-001`, `RV-002`) | Human accessibility reviewer (`RV-001` NVDA/JAWS/VoiceOver + 360px walkthrough on `#232`); harness maintainer (`RV-002` dedicated full-tier `specialist_keyboard_browser_check.py` PR) |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: Focused unit/baseline/copy (51 tests), coupled suites (115 tests), `ZF_RESIDENT_BROWSER=1` (21 tests), Playwright + pinned `axe-core 4.10.3` (`role_screens_browser_check.py` `parent`/`232`/`232s` and `case_journey_browser_check.py --axe`), `ruff check`, `ruff format --check`, `mypy` (292 files), `rename-zava-tests.py` (25 tests), and refreshed `web-design-guidelines` audit all passed.
* Blockers: None
