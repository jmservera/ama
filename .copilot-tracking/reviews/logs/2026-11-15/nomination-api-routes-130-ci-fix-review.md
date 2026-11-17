<!-- markdownlint-disable-file -->
# Review: Fix Issue 130 src-api CI Failures from Run 43694720253

## Scope and Evidence

* Task ID: nomination-api-routes-130-ci-fix
* Review date: 2026-11-15
* Review scope: full_task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`)
* Assessed boundary: Resolution of the two `src-api` unit-step CI failures from GitHub Actions run `43694720253` on pull request `#1776` (`feat/ux-130-api-routes`, HEAD `2215209cb`, `Refs #130`), preservation of route/DOM/accessibility/content/manifest invariants, focused-tier local validation, and fresh `web-design-guidelines` review of `src/api/src/zava_forward/api/web/panels.js`
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md (`C1`–`C8`, `W1`), `git diff src/`, fresh fetch of Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), and local test/lint/typecheck/empty-Chromium-cache verification runs

## Opening Review State

* Interpreted review goal: Verify once, from primary code diffs and validation evidence, that both run `43694720253` `src-api` CI failures are fixed without regression, drift, or Web Interface Guidelines violations, and route any remaining work cleanly.
* Review scope: full_task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`)
* Evidence readiness: Ready; research, plan, phase details, single-pass critique (`Pass`), and changes record are reconciled and complete.
* Acceptance basis: Plan functional/non-functional requirements and acceptance criteria, locked test ownership bounds (`0` removals, `1` new test method), `Pass` critique disposition, and Web Interface Guidelines compliance.
* First comparison boundary: Compare `git diff src/` (`panels.js` and `test_nomination_api_routes.py`) against `P01-T01`, `P01-T02`, and `P02-T01` acceptance criteria.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/logs/2026-11-15/nomination-api-routes-130-ci-fix-review.md` during Review; do not mutate plan, details, critique, research, changes, or source files.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across all planned phases (`P01`, `P02`), tasks (`P01-T01`, `P01-T02`, `P02-T01`), `git diff src/`, focused-tier validation logs, and refreshed Vercel Web Interface Guidelines (`command.md`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Guard `c` and restore `formFor`-to-`staff` slice boundary in `affectedChallengePanel` | Reconciled | `panels.js` places `const staff` immediately after `const formFor` and guards `typeof c !== "undefined" && c`; `test_case_journey.py` (`31` tests) passes unchanged. |
| `P01`, `P01-T02` | Align missing-Chromium `PlaywrightError` skip and add skip regression test | Reconciled | `test_nomination_api_routes.py` uses `importlib.util.find_spec("playwright")`, skips on `"Executable doesn't exist"` via `_launch_headless_chromium`, re-raises genuine `PlaywrightError`s, and adds exactly `1` test method (`0` removals). |
| `P02`, `P02-T01` | Execute focused-tier validation suites across `src/api`, `src/core`, and `tools` | Reconciled | All unit, empty-Chromium-cache, a11y/copy static baseline, `ruff`, `mypy`, `scenario-manifest`, and `rename-zava-tests.py` suites passed (`exit 0`). |
| `Follow-Up Items` | Optional `nomination_browser_check.py` interactive axe scan and external push / hosted CI / `OD-41`–`OD-42` human governance | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` completion claims in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/api/src/zava_forward/api/web/panels.js | Reordered `const staff` immediately after `const formFor` and guarded `const caseRecord = typeof c !== "undefined" && c ? c : null;` in `affectedChallengePanel` to prevent Node slice `ReferenceError: c is not defined`. | Clean 8-line diff in `panels.js`; `CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` passes. | Passed (`31` `test_case_journey.py` tests, `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `web-design-guidelines` audit) | Reconciled |
| `P01-T02` | src/api/tests/test_nomination_api_routes.py | Updated `_playwright_available()`, added `_launch_headless_chromium()` catching missing-executable `PlaywrightError` with `self.skipTest("Chromium is installed by the later browser-check step")`, and added `test_keyboard_operability_skips_when_chromium_executable_missing`. | Clean diff in `test_nomination_api_routes.py` honoring locked test bounds (`0` removals, `1` addition). | Passed (`5/5` with local Chromium; `5/5` `OK (skipped=1)` with `PLAYWRIGHT_BROWSERS_PATH=/tmp/empty-playwright-cache-130`; `ruff`; `mypy`) | Reconciled |
| `P02-T01` | .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md | Ran focused-tier unit, browser-skip, static guard, lint, format, type, synthetic-manifest, and naming suites. | Recorded command matrix and exit-`0` outputs. | Passed (`94` `src/api` tests, `19` `src/core` manifest/inventory tests, `25` naming tests, `ruff`, `mypy`) | Reconciled |

### Web Interface Guidelines Audit (`file:line` format)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before review and audited `src/api/src/zava_forward/api/web/panels.js`:

```text
## src/api/src/zava_forward/api/web/panels.js

✓ pass
```

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan or phase-detail scope/requirement changes were needed beyond checking `[x]` completion markers. | None | Markers `[x]` in plan and `complete` statuses in phase details reconciled with changes record. | Ready (`Pass` critique preserved, 0 `PC` findings) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique (`nomination-api-routes-130-ci-fix-plan-critique.md`) returned `Pass` with `0` `PC-xxx` findings; planner preserved `@unittest.skipUnless(_playwright_available(), ...)` on the mock skip test as noted.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent work ran out of order; `P02` ran strictly after `P01-T01` and `P01-T02` completed.
* Justification assessment: Fully supported by primary hosted CI log (`run 43694720253`) and local empty-Chromium-cache reproduction.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Extend `src/api/checks/nomination_browser_check.py` to scan interactive dual-route nomination acknowledgement and correction disclosures with axe-core 4.10.3 | Enhancement beyond the two `src-api` unit-step failures in run `43694720253` | Follow-up engineering task (`#130`) | Open distinct follow-up route |
| Ratify `OD-41` and `OD-42`, obtain human representative comprehension sign-off, push `feat/ux-130-api-routes` (`PR #1776`), and run hosted CI + independent exact-head review | Caller explicitly forbade pushing (`Do NOT push`) and human governance sign-off cannot be fabricated locally | Repository owner and human governance reviewers (`Refs #130`) | Open distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. They are not defects in this task scope.

## Findings

No defects, decision gaps, or evidence gaps were found within the assessed task boundary (`0` `RV-xxx` defect findings).

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No defects or plan/research gaps in assessed CI-fix scope | All planned acceptance criteria satisfied |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Push `feat/ux-130-api-routes` (`PR #1776`) to verify hosted GitHub Actions `src-api` green execution on the new commit, obtain independent exact-head review, and complete human governance ratification (`OD-41`, `OD-42`, representative comprehension sign-off) for `Refs #130`.
* Optional follow-up enhancement to extend `src/api/checks/nomination_browser_check.py` interactive disclosure coverage under axe-core 4.10.3.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/api:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_nomination_api_routes.py src/api/tests/test_content_standard.py src/api/tests/test_accessibility_baseline.py -q` | Targeted `src/api` unit & static guards from repo root | Passed | `Ran 79 tests in 9.137s — OK` |
| `(cd src/api && PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_nomination_api_routes.py tests/test_content_standard.py tests/test_accessibility_baseline.py -q)` | CI-equivalent `src/api` working-directory unit run (with Chromium present) | Passed | `Ran 79 tests in 9.218s — OK` (`skipped=0`) |
| `PYTHONPATH=src/core:src/agents:src/api:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_nomination_api_routes.py src/api/tests/test_content_standard.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_nomination_screen.py src/api/tests/test_epic149_form_error_summary_associations.py -v` | Extended coupled `src/api` suites | Passed | `Ran 94 tests in 9.478s — OK` |
| `(cd src/api && PLAYWRIGHT_BROWSERS_PATH=/tmp/empty-playwright-cache-130 PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_nomination_api_routes.py -v)` | Empty-Chromium-cache hosted CI reproduction | Passed | `Ran 5 tests in 3.933s — OK (skipped=1)` (`'Chromium is installed by the later browser-check step'`) |
| `python3 -m ruff check src/api && (cd src/api && python3 -m ruff format --check .)` | `src/api` lint and formatting | Passed | `All checks passed!`, `210 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/api` static type checking | Passed | `Success: no issues found in 294 source files` |
| `PYTHONPATH=src/core:src/core/src:src/core/tests python3 -m unittest src/core/tests/test_scenario_manifest.py src/core/tests/test_needs_inventory.py -q` | `src/core` synthetic scenario-manifest & needs-inventory | Passed | `Ran 19 tests in 0.080s — OK` |
| `python3 tools/rename-zava-tests.py` | Naming regression check | Passed | `Ran 25 tests in 0.481s — OK` |
| Hosted GitHub Actions CI on new commit | Remote `PR #1776` workflows | Skipped | Caller explicitly instructed `Do NOT push; leave a clean frozen working tree` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Both `src-api` CI failures from GitHub Actions run `43694720253` are resolved cleanly within locked file and test bounds, verified both with live headless Chromium and with an empty `PLAYWRIGHT_BROWSERS_PATH` reproducing the hosted `src-api` unit container, compliant with refreshed Web Interface Guidelines (`✓ pass`), and clean across `unittest`, `ruff`, `mypy`, and `scenario-manifest` checks. Zero production/test/commit references to `.copilot-tracking/` exist.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Owner push + hosted CI verification + independent review + `OD-41`/`OD-42` human governance (`Refs #130`), and optional `nomination_browser_check.py` interactive axe extension |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: 94 `src/api` unit/a11y/copy/browser tests (`OK`), empty-Chromium-cache CI reproduction (`OK (skipped=1)`), `ruff` (`0` issues), `mypy` (`294` files, `0` issues), 19 `src/core` manifest/inventory tests (`OK`), 25 naming tests (`OK`), Web Interface Guidelines (`✓ pass`); hosted CI skipped per no-push constraint
* Blockers: none
