<!-- markdownlint-disable-file -->
# Review: Rebase Housing and Resident WCAG (#232) onto Programme Coordinator WCAG (#230)

## Scope and Evidence

* Task ID: 2026-11-15-housing-resident-wcag-232-c1
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Cycle 1 rebase of `feat/ux-232-resident-wcag` (`e2528cc63`, `af9fcb891` from `184b828e1`, `cffec920a`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, including merged `PR #1784` for Issue #230), three-way overlap resolution in `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`, `#230` + `#232` coexistence verification in `src/api/tests/test_housing_resident_wcag_232.py`, Focused + coupled WCAG/lint/type/migration/Web Interface Guidelines validation, and RPI tracking artifact hygiene preserving Cycle 0 critique/review immutability.
* Plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md, .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md, .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md (verified unmodified), .copilot-tracking/reviews/logs/2026-11-15/housing-resident-wcag-232-review.md (verified unmodified), `git diff origin/feat/demo-233-same-home-tensions-0825...HEAD`, and direct Focused + coupled validation outputs.

## Opening Review State

* Interpreted review goal: Assess whether the Cycle 1 rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) preserves 100% of `#230` and `#232` accessibility, route, state-cue, and plain-language invariants, satisfies `FR-1`..`FR-4`, `NFR-1`, `NFR-2`, `AC-1`..`AC-4`, and `PC-001`, and keeps Cycle 0 historical verdicts untouched.
* Review scope: full task (`P01`, `P02`)
* Evidence readiness: Ready — plan markers, phase-detail statuses, critique disposition (`PC-001`), Cycle 1 changes record, Cycle 0 changes addendum, git ancestry (`af9fcb891` <- `e2528cc63` <- `6510b6fbc` <- `a1d0be5f6`), and validation outputs are reconciled.
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`, `NFR-2`, `AC-1`..`AC-4`, `PC-001`, AMA Web Development Guidance, and AMA Branch and Pull Request Workflow.
* First comparison boundary: `git diff origin/feat/demo-233-same-home-tensions-0825...HEAD -- src/api/` compared against `#230` (`6510b6fbc`) and `#232` (`e2528cc63`, `af9fcb891`) invariants.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/housing-resident-wcag-232-c1-review.md` and does not modify source, tests, plan, details, critique, research, or changes records.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-15 across all Cycle 1 plan, detail, critique, changes, research, git-ancestry, diff, and validation artifacts.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Rebase onto `origin/feat/demo-233-same-home-tensions-0825` and `#230` + `#232` Conflict Resolution | Reconciled | `[x]` in plan, `Complete` in phase details, ancestry `6510b6fbc` -> `e2528cc63` -> `af9fcb891` verified. |
| `P02`, `P02-T01` | Post-Rebase `#230` + `#232` Coexistence Tests, Focused Validation, and Web Guidelines Audit | Reconciled | `[x]` in plan, `Complete` in phase details, `PC-001` Node VM exports and coexistence assertions implemented and passing. |
| `P02-T02` | Cycle 1 Tracking Artifacts and Cycle 0 Post-Rebase Addendum Reconciliation | Reconciled | `[x]` in plan, `Complete` in phase details, Cycle 1 artifacts and Cycle 0 `changes` addendum reconciled while Cycle 0 critique/review remain untouched. |
| `## Follow-Up Items` | Full-tier `specialist_keyboard_browser_check.py` alignment (`#1294`) and human AT/mobile walkthroughs (`#151`, `#155`) | Reconciled | Mirrored between plan and changes record outside active `P01`/`P02` completion claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js` | Rebased `#232` onto `6510b6fbc` (`#230`) with local privacy-safe noreply email; union-merged `isRoleScreensDestination` with `split("?")[0]` across `#/screens` and all 9 `#/role/*` routes in `app.js` and preserved all 9 `ROLE_HASH_SCREENS` aliases plus all `#230` (`programme-shared-queue`, `programme-funnel`, `programme-queue`) and `#232` (`resident-choice`, `resident-service-issues`, `#workspace-status`, `section#screen-evidence`, `data-state-cue="scope"`, two-line `document.getElementById` jump listener) hunks in `role-screens.js`. | `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exited `0`; `0` conflict markers; clean diff against `6510b6fbc`. | Passed (`64` Focused + `65` coupled WCAG tests) | Reconciled |
| `P02`, `P02-T01` | `src/api/tests/test_housing_resident_wcag_232.py` | Exported lexical `ROLE_HASH_SCREENS` and `programmeOverviewSections` in the Node VM harness and extended `verifyRouter()` + `test_contact_centre_housing_and_resident_routes_and_script_isolation` to lock `#230` + `#232` coexistence across routes, `roleScreens`, `ROLE_HASH_SCREENS`, and `programmeOverviewSections`. | `HousingResidentWcag232Tests` (`8` methods) and `ProgrammeCoordinatorWcag230Tests` (`5` methods) pass together alongside counted baselines (`14` tables, `9` `aria-invalid`, `0` bare `th`). | Passed (`64` Focused tests, `65` coupled tests, `ruff`, `mypy`, `rename-zava-tests.py`, `web-design-guidelines`) | Reconciled |
| `P02-T02` | `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`, `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md`, `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md` | Recorded Cycle 1 changes evidence and appended Cycle 1 post-rebase addendum to Cycle 0 `changes` log without mutating Cycle 0 critique or review records. | Reconciled plan/detail markers and diff review; parent RPI Agent performs the single post-review atomic Conventional Commit (`Refs #232` + Copilot trailer) without `git push`. | Passed (Markdown and git status check) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `## Dependencies` (`P02-T01`) | Noted that `/home/azureuser/source/ama/.venv` is an empty directory in this workspace while `/usr/bin/python3`, `/home/azureuser/.local/bin/ruff`, and `/home/azureuser/.local/bin/mypy` on `PATH` run the exact caller selector sets. | `ls -la /home/azureuser/source/ama/.venv` and `which python3 ruff mypy`; no user decision needed (ordinary local runner resolution). | Updated `## Dependencies` in `housing-resident-wcag-232-c1-plan.md` and recorded exact commands/counts in `housing-resident-wcag-232-c1-changes.md`. | Not needed (`Ready`, `PC-001` preserved) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` (`[Low]`) in `.copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-c1-plan-critique.md` was applied directly before implementation (`test_contact_centre_housing_and_resident_routes_and_script_isolation` naming, `"programme-queue"` registered screen ID vs `"programme-shared-queue"` / `"programme-funnel"` jump-target section IDs, and explicit Node VM export of lexical `ROLE_HASH_SCREENS` and `programmeOverviewSections`) and verified in `src/api/tests/test_housing_resident_wcag_232.py`.
* Material revisions: None required during implementation; all work stayed strictly within approved `P01` and `P02` scope.
* Dependent-work pause assessment: `P01-T01` completed and verified commit ancestry before `P02-T01` and `P02-T02` executed; no premature continuation occurred.
* Justification assessment: Supported by direct workspace git-ancestry, merge-diff, and automated validation evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` (`#1294`) | Modifying gate/harness expectations belongs in a dedicated full-tier gate-tool PR with an external `rpi-checks.py --all` receipt rather than a Focused-tier rebase. | Harness maintainer — open dedicated full-tier gate-tool PR. | Open distinct follow-up (`RV-002`) |
| Execute human assistive-technology (`NVDA`, `JAWS`, `VoiceOver`) and `360px` mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` (`#151`, `#155`) | Automated tests establish `#151` engineering readiness (`Refs #232`) only; human AT acceptance cannot be claimed by automated checks per `wcag-conformance-baseline.md`. | Human accessibility reviewer — run AT and mobile walkthroughs before closing `#232`. | Open distinct follow-up (`RV-001`) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Human assistive-technology and 360px mobile walkthroughs remain required before closing Issue #232

* Related scope: `## Follow-Up Items` (`Refs #232`, `#151`, `#155`)
* Evidence: `docs/reference/research/ux/wcag-conformance-baseline.md`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md` (`## Non-Goals`, `## Follow-Up Items`)
* Impact: Automated Node VM, static, type, plain-language, and Playwright/axe checks verify the `#151` engineering baseline across the rebased `#230` + `#232` branch, so commits and `PR #1786` must continue using `Refs #232` rather than `Closes #232` until human screen-reader (`NVDA`, `JAWS`, `VoiceOver`) and mobile walkthroughs complete.
* Destination: `follow-up`
* Smallest useful next action: Human accessibility reviewer executes the `#151` / `#155` assistive-technology and `360px` mobile walkthroughs on `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: `specialist_keyboard_browser_check.py` `NO_REGION_GAPS` declaration for `resident-service-issues` remains deferred to a full-tier gate-tool PR

* Related scope: `## Follow-Up Items` (`#1294`)
* Evidence: `src/api/checks/specialist_keyboard_browser_check.py`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md` (`## Follow-Up Items`)
* Impact: Does not affect Focused-tier checks or hosted `src-ci.yml`, but updating `NO_REGION_GAPS` in a dedicated full-tier PR keeps `specialist_keyboard_browser_check.py` synchronized for future full-gate runs.
* Destination: `follow-up`
* Smallest useful next action: Open a dedicated full-tier gate-tool PR updating `NO_REGION_GAPS` for `resident-service-issues` in `src/api/checks/specialist_keyboard_browser_check.py` with a verified external `rpi-checks.py --all` receipt.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (`RV-001` and `RV-002` are non-blocking residual follow-up items) | None (`rpi-implement`, `rpi-plan`, and `rpi-research` not required) | Human accessibility reviewer (`RV-001`) and harness maintainer (`RV-002`) | Zero implementation defects, decision gaps, or material evidence gaps within the Cycle 1 rebase and Focused verification scope. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` (`follow-up`, human accessibility reviewer): Complete human `NVDA`/`JAWS`/`VoiceOver` and `360px` mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing `#232`.
* `RV-002` (`follow-up`, harness maintainer): Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR under `#1294`.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None inside RPI `Implement` or `Review`; parent RPI Agent transitions `housing-resident-wcag-232-c1-state.json` to `Follow-up`, creates the single clean frozen Conventional Commit (`Refs #232` + Copilot trailer) without running `git push`, and re-verifies clean `git status --short` and validation on the frozen `HEAD`.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest tests/test_housing_resident_wcag_232.py tests/test_programme_coordinator_wcag_230.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_procurement_contractor_screen_wcag.py -v` | `src/api` (`#232` + `#230` + WCAG baseline + plain-language copy + `#229`) | Passed | `Ran 64 tests in 5.577s - OK` |
| `PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest tests/test_asset_exec_screen_wcag.py tests/test_technical_quality_screens_wcag.py tests/test_programme_screen_wcag.py tests/test_housing_resident_screen_wcag.py tests/test_data_steward_screen_wcag.py tests/test_role_screens.py tests/test_role_screens_conformance.py -q` | `src/api` coupled specialist WCAG & conformance suites | Passed | `Ran 65 tests in 3.745s - OK` |
| `ruff check src/zava_forward/api tests/test_housing_resident_wcag_232.py checks/case_journey_browser_check.py && ruff format --check src/zava_forward/api tests/test_housing_resident_wcag_232.py checks/case_journey_browser_check.py` | `src/api` lint and formatting | Passed | `All checks passed!`, `27 files already formatted` |
| `mypy` (in `src/api`) | `src/api` (`src`, `tests`, `checks`) | Passed | `Success: no issues found in 294 source files` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression | Passed | `Ran 25 tests in 1.063s - OK` |
| Refreshed `web-design-guidelines` review (`command.md`) | `app.js`, `role-screens.js`, `panels.js` | Passed | `✓ pass` across all three changed web files in `file:line` format |

## Outcome

* Outcome: Residual work
* Outcome rationale: Rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), `#230` + `#232` conflict union in `app.js` and `role-screens.js`, coexistence assertions in `test_housing_resident_wcag_232.py`, Focused + coupled validation (`64` + `65` + `25` tests, `ruff`, strict `mypy` across `294` files, refreshed `web-design-guidelines`), and Cycle 1 RPI tracking reconciliation all succeeded with zero defects, decision gaps, or material evidence gaps. Outcome is recorded as `Residual work` solely to keep open the non-blocking human assistive-technology walkthrough (`RV-001`, `#151`/`#155`, `Refs #232`) and full-tier `specialist_keyboard_browser_check.py` alignment (`RV-002`, `#1294`) without overclaiming human accessibility acceptance.

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
* Validation coverage: Focused 5-module `unittest` (`64` tests), coupled specialist WCAG suites (`65` tests), `ruff check`, `ruff format --check`, strict `mypy` (`294` files), `rename-zava-tests.py` (`25` tests), and refreshed `web-design-guidelines` review all passed.
* Blockers: None
