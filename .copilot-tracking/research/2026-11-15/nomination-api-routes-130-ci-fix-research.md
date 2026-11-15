<!-- markdownlint-disable-file -->

# Task Research: nomination-api-routes-130-ci-fix

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic session)                                          |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md  |

## Research Brief

* What to research: Root causes and minimal, regression-safe fixes for the two `src-api` failures in GitHub Actions run `43694720253` (`job 132752737563`) on `PR #1776` (`feat/ux-130-api-routes` targeting `feat/demo-233-same-home-tensions-0825` / `PR #1639`, HEAD `2215209cb`) for Issue #130 (`Refs #130`).
* Why it matters: `src-api` failed `2` out of `3,585` tests on commit `2215209cb` (`1` `FAIL` in `test_case_journey.py` and `1` `ERROR` in `test_nomination_api_routes.py`), blocking green CI on `PR #1776` while all other jobs (`src-core`, `src-agents`, `src-importer`, `src-orchestrator`, `src-namespace`, `src-no-working-data`, `mssql`, `image-paths`) passed.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this continuous automatic RPI execution.
* Scope: `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_nomination_api_routes.py`, and focused verification across `src/api/tests/test_case_journey.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/core/tests/test_scenario_manifest.py`, `src/core/tests/test_needs_inventory.py`, `ruff`, and `mypy`.
* Non-goals: Pushing to `origin`, mutating branch lineage or renaming PR #1776's active head branch `feat/ux-130-api-routes`, overwriting historical RPI artifacts (`nomination-api-routes-130-*`), or weakening any route/DOM/accessibility/content assertion.
* Criteria: Exact reconciliation against the hosted GitHub Actions failure log (`run 43694720253`), zero Node slice `ReferenceError`, clean skip in unit-test containers lacking a Chromium binary while still executing full Playwright keyboard assertions when Chromium is installed and full HTTP/HTML route/DOM assertions unconditionally, and focused-tier validation cleanliness.
* Requested outputs: Converged fix specification ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q4 covering exact run `43694720253` tracebacks vs caller summary, `panels.js` slice boundary in `test_case_journey.py`, Chromium-binary skip conventions in `src/api/tests/`, and downstream static/manifest invariants. |
| Codebase scope                       | `src/api/`, `src/core/tests/`, `.github/workflows/src-ci.yml`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`    |
| External scope                       | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines`) per repository Web Development Guidance |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_case_journey.py`, `src/api/tests/test_nomination_api_routes.py`, `src/api/tests/test_workbench_live_defaults.py`, `src/api/tests/test_browser_asset_urls.py`, `.github/workflows/src-ci.yml`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                   |
| Research posture                     | focused                                                                                                                                    |
| Posture provenance                   | default (bounded CI bugfix with named files, exact SHA `2215209cb`, and retrievable CI run `43694720253` failure logs)                     |
| Explicit limits / deadline           | Focused validation tier; single continuous run ending in clean frozen local commit without push                                             |
| Posture-specific completion basis    | Focused scope and materiality: both CI failures reproduced/inspected from exact hosted logs and mapped to surgical verified fixes           |
| Edits allowed during research?       | no, research-only                                                                                                                          |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                               |
| Known constraints / excluded sources | Never read private datasets; preserve `nomination-api-routes-130-*` historical evidence; preserve WCAG (`9` `aria-invalid`, `14` `table`) and content-standard guards |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                                | Match and provenance                                             | Scoped authority or output contract                                                  | Selected / skipped reason                                                                 |
|---------------------|----------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repo Instructions)| `applyTo: "**"` matches workspace and tracking paths             | Enforces branch reuse for open PRs, focused validation tier, and web-edit checks     | Selected: governs branch preservation (`feat/ux-130-api-routes`), web rules, and commits  |
| Skill               | `web-design-guidelines`                                  | Required by Web Development Guidance before editing `panels.js`  | Fetches current Vercel Web Interface Guidelines (`W1`) for `file:line` review        | Selected: loaded and fetched (`W1`) because `panels.js` is modified                       |
| Skill               | `redesign-existing-projects`                             | Existing-app design improvements                                 | Scoped visual/UX redesign guidance                                                   | Skipped: task is a 2-line JS variable-guard/ordering bugfix with zero UI/visual change    |
| Research specialist | `hve-core-all:rpi-researcher`                            | Registered general RPI research worker                           | Independent subagent lane artifact                                                   | Skipped for inline execution: two tightly coupled tracebacks resolved in <5 direct reads  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                              | Answers / unanswered                   | Resulting decision or selected further research                                          |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive runtime; caller supplied exact worktree, commit SHA `2215209cb`, PR `#1776`, Actions run `43694720253`, and checks | N/A (non-interactive runtime)          | Reconcile prompt shorthand against live Git/PR/Actions metadata and proceed automatically|
| Direction change | Verified live branch name is `feat/ux-130-api-routes` (`PR #1776` targeting `feat/demo-233-same-home-tensions-0825` / `PR #1639`)  | N/A (repository branch-reuse rule)     | Commit on active `PR #1776` branch `feat/ux-130-api-routes` without branch rename        |
| Convergence      | All 4 research questions answered with primary CI log and local reproduction evidence                                              | N/A (non-interactive runtime)          | Converge on two-file fix (`panels.js`, `test_nomination_api_routes.py`) and enter Plan   |

## Scope and Success Criteria

* Scope: Fix the two `src-api` unit-step failures from run `43694720253` in `src/api/src/zava_forward/api/web/panels.js` and `src/api/tests/test_nomination_api_routes.py`, add focused regression coverage for the missing-Chromium skip path, verify all requested test/lint/type/manifest suites, and record dated `2026-11-15` RPI artifacts on `feat/ux-130-api-routes` without pushing.
* Assumptions: Verified rather than trusted—caller prompt's approximate branch/function names (`feat/api-130-nomination-routes`, `renderFundingPanel`, `test_nomination_screen_renders_create_and_step_forms_with_keyboard_reachability`) were checked directly against `gh pr view 1776` and `gh run view 43694720253 --log-failed`.
* Success criteria:
  * Every research question is answered from primary code, GitHub Actions logs, and local test runs (`path:line` and `W1`).
  * Findings, decisions, and readiness cite Evidence Log IDs (`C1`-`C8`, `W1`).
  * Alternatives are evaluated and one recommendation is selected in `convergence` mode.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Diagnose and fix the Node slice `ReferenceError: c is not defined` in `src/api/src/zava_forward/api/web/panels.js` affecting `test_case_journey.py` and the missing-Chromium failure in `src/api/tests/test_nomination_api_routes.py` around line `521`; run requested unit, `ruff`, `mypy`, and `scenario-manifest` checks; commit locally with Copilot trailer without pushing.
* Inferred research questions: Reconcile exact symbol/branch names against run `43694720253`, verify whether `nominationPanel._routeForm` passes `test_case_journey.py` once `c` is guarded/reordered, verify how `src-ci.yml` stages Chromium installation, and verify whether `panels.js` hashes appear in `scenario-manifest.json` or static guards.
* Caller constraints and non-goals: Do not push; leave a clean frozen working tree; preserve route/DOM assertions and existing accessibility/content baselines.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Fix only the two `src-api` failures from run `43694720253` while preserving route/DOM/a11y assertions   | Caller prompt       | Bounds edits to `panels.js` and `test_nomination_api_routes.py` plus RPI artifacts |
| exclude                                                  | Do NOT push to remote; preserve historical `nomination-api-routes-130-*` RPI records as parent evidence | Caller + repo rules | Uses child task slug `nomination-api-routes-130-ci-fix` on `feat/ux-130-api-routes`|

## Research Questions

|  # | Sub-question                                                                                                                               | Type            | Priority | Status   |
|---:|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What were the exact failing test names, line numbers, and branch metadata in GitHub Actions run `43694720253` (`PR #1776`)?                 | straightforward | H        | answered |
| Q2 | Why did `test_case_journey.py` throw `ReferenceError: c is not defined` when slicing `panels.js`, and does `formFor` pass once fixed?      | depth           | H        | answered |
| Q3 | Why did `test_nomination_api_routes.py:521` fail in `src-api` unit tests, and what is the canonical Chromium-availability skip convention? | depth           | H        | answered |
| Q4 | Does editing `panels.js` affect `scenario-manifest.json` hashes, `aria-invalid` counts (`9`), `table` counts (`14`), or banned copy words? | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/nomination-api-routes-130-state.json`, `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-research.md`, `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-plan.md`, `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-changes.md`, `.copilot-tracking/reviews/2026-11-15/nomination-api-routes-130-review.md`.
* Reused (verified) findings: Static WCAG baseline invariants (`9` `aria-invalid` sites, `14` `table` elements in `test_accessibility_baseline.py`), `test_content_standard.py` banned-word rules, and `test_epic149_form_error_summary_associations.py` line-window rules remain active (`C6`).
* Superseded / stale: Local validation in `nomination-api-routes-130` ran `test_nomination_screen.py`, `test_nomination_api_routes.py`, and `test_resident_api.py` on a machine with Chromium already cached, so it did not catch (a) `test_case_journey.py`'s `source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]` slice over `panels.js` or (b) `src-ci.yml` running `unittest discover` before `playwright install --with-deps chromium` (`C1`, `C2`, `C4`, `C5`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to run `43694720253` fixes; exclude remote push and historical RPI overwrite
* Active research posture and completion basis: `focused`; focused scope and materiality over exact CI failure logs and named files
* Explicit limits or deadline effect: Focused validation tier; local commit only

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of Git/worktree state, `gh pr view 1776`, `gh pr view 1639`, `gh run view 43694720253 --log-failed`, `.github/workflows/src-ci.yml`, `panels.js` references across `src/`, `tools/`, and `docs/`, and live `web-design-guidelines` rules (`W1`).
* Worker evidence relationships or inline fallback: Inline (`<5` bounded reads across tightly coupled test/JS files) -> `Q1`/`C1`, `Q3`/`C4`, `Q4`/`C7`, `W1`.
* Reflection: Retrieving the actual run `43694720253` failed log (`C1`) immediately clarified every prompt shorthand: the active `PR #1776` branch at `2215209cb` is `feat/ux-130-api-routes` (targeting `feat/demo-233-same-home-tensions-0825` / `PR #1639`), Failure 1 is `test_case_journey.CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` at `panels.js:821` (`const perms = c.nomination_permissions ...`), and Failure 2 is `test_nomination_api_routes.NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` at `test_nomination_api_routes.py:521` (`BrowserType.launch: Executable doesn't exist`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact JS slice mechanics in `test_case_journey.py:707-792`, `affectedChallengePanel` and `nominationPanel._routeForm` behavior in `panels.js:615-828`, and Chromium skip helpers in `test_workbench_live_defaults.py` and `test_browser_asset_urls.py`.
* Plan and independent lanes: Inline read and local reproduction of `test_case_journey.py` (`C2`, `C3`) and comparison of Playwright/Chromium guards across all `40` `src/api/tests/` matches (`C5`).
* Worker evidence relationships or inline fallback: Inline -> `Q2`/`C2`-`C3`, `Q3`/`C4`-`C5`, `Q4`/`C6`-`C8`.
* Reflection: `test_case_journey.py:709-716` already slices `nominationPanel` (including `nominationPanel._routeForm`) before slicing `"const formFor = " + source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]`; placing `const perms = c.nomination_permissions ...` between `formFor` and `const staff` leaked an unguarded `c` reference into the top-level Node slice (`C2`, `C3`). In `src-ci.yml`, `playwright` Python package is installed by `pip install -e ".[dev]"` before `unittest discover`, while `python -m playwright install --with-deps chromium` runs in a later step, where `test_workbench_live_defaults.py:108-113` and `test_browser_asset_urls.py:58-63` catch `PlaywrightError` on `"Executable doesn't exist"` and call `self.skipTest("Chromium is installed by the later browser-check step")` (`C4`, `C5`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: (1) Check whether fixing `ReferenceError: c is not defined` exposes any deeper incompatibility between `nominationPanel._routeForm` and `test_raw_resident_and_challenge_outcomes_exclude_repeat_posts`; (2) check whether skipping on missing Chromium binary weakens route/DOM coverage or masks real browser launch crashes (such as sandbox/crash errors when Chromium *is* installed); (3) check whether moving/guarding `const perms` in `panels.js` trips `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, or `scenario-manifest.json`.
* Plan and independent lanes: Inline inspection of `_routeForm` state machine (`panels.js:690-750`), `PlaywrightError` discrimination (`"Executable doesn't exist" in str(exc)` vs arbitrary exceptions), static test rules (`C6`), and `scenario-manifest.json` (`C7`).
* Worker evidence relationships or inline fallback: Inline -> supports combined reorder + `typeof c !== "undefined" && c` guard in `panels.js` and narrow `"Executable doesn't exist"` skip in `test_nomination_api_routes.py` (`C3`, `C5`, `C6`, `C7`).
* Reflection: Only skipping when `"Executable doesn't exist" in str(exc)` (and re-raising all other `PlaywrightError`s) ensures real browser crashes still fail loudly when Chromium is present, while `test_accessible_html_route_fragment_labels_channels_and_live_status` continues testing DOM labels/channels/live-regions unconditionally in every `src-api` unit run.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                       | Evidence IDs | Parent disposition | Evidence-based rationale                                                                                                   | Primary-artifact treatment       |
|------------------------------------------------------------------------------------------------------------------------|--------------|--------------------|----------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| Place `const staff` immediately after `const formFor` AND guard `typeof c !== "undefined" && c` in `affectedChallengePanel` | `C2`, `C3`   | accepted           | Restores exact `formFor`..`staff` slice boundary in `test_case_journey.py` AND prevents `ReferenceError` in any slice eval | Selected recommendation (Part 1) |
| Catch `PlaywrightError` with `"Executable doesn't exist" in str(exc)` -> `self.skipTest(...)` + unit test for skip path | `C4`, `C5`   | accepted           | Matches `test_workbench_live_defaults.py` and `test_browser_asset_urls.py` in `src-api` CI while running locally with Chromium | Selected recommendation (Part 2) |
| Gate Playwright test behind opt-in env var `ZF_BROWSER_TESTS=1`                                                        | `C4`, `C5`   | rejected           | Would skip the keyboard test even in local runs where Chromium is installed unless the env var is manually passed           | Rejected alternative             |
| Rename branch `feat/ux-130-api-routes` to `feat/api-130-nomination-routes`                                             | `C8`         | rejected           | `PR #1776` head branch is `feat/ux-130-api-routes` at `2215209cb`; repository instructions require reusing open PR branch   | Recorded Current Decision        |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Both CI failures are completely explained from hosted logs and local code/reproduction with zero remaining ambiguity.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: bounded two-bug CI diagnosis completed directly in fewer than five tightly coupled reads with primary GitHub Actions log verification.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | GitHub Actions run `43694720253` (`src-api` job `132752737563`) ran `3,585` tests with `failures=1, errors=1, skipped=647`: `FAIL` in `test_case_journey.CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` (`ReferenceError: c is not defined` on `const perms = c.nomination_permissions ...`) and `ERROR` in `test_nomination_api_routes.NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` (`BrowserType.launch: Executable doesn't exist`). | `src/api/tests/test_case_journey.py:792`, `src/api/tests/test_nomination_api_routes.py:521` | bash (`gh run view`) / read | high | Primary CI log for HEAD `2215209cb` |
| C2 | `test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` constructs a Node script slicing `"function captureChallengeDrafts" .. "function affectedChallengePanel"` (which includes `nominationPanel._routeForm`) followed by `"const formFor = " + source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]` without defining `c` at top level. | `src/api/tests/test_case_journey.py:709-716` | read / bash | high | Reproduced locally (`Ran 31 tests`, `ReferenceError: c is not defined`) |
| C3 | In `affectedChallengePanel(c, id, refresh)`, `const perms = c.nomination_permissions && typeof c.nomination_permissions === "object" ? c.nomination_permissions : null;` and `const repRefs = ...` were inserted at lines `821-824` between `const formFor = ...` (`803-820`) and `const staff = ...` (`825-827`). | `src/api/src/zava_forward/api/web/panels.js:803-827` | read | high | Placing `const staff` right after `formFor` and guarding `typeof c !== "undefined" && c` fixes both slice shape and defensive scoping |
| C4 | `.github/workflows/src-ci.yml` runs `pip install -e ../core -e ../agents -e ".[dev]"` (installing the Python `playwright` package) and then `python -m unittest discover -s tests -v` before the later `Synthetic design-system browser checks` step runs `python -m playwright install --with-deps chromium`. | `.github/workflows/src-ci.yml:83-112` | read | high | Explains why `_playwright_available()` returned `True` when Chromium binary was absent |
| C5 | Peer `src/api/tests/` tests (`QueueResultSynchronization` in `test_workbench_live_defaults.py` and `BrowserAssetUrls` in `test_browser_asset_urls.py`) catch `PlaywrightError` from `chromium.launch()` when `"Executable doesn't exist" in str(error)` and call `self.skipTest("Chromium is installed by the later browser-check step")`, which cleanly skipped in run `43694720253`. | `src/api/tests/test_workbench_live_defaults.py:104-114`, `src/api/tests/test_browser_asset_urls.py:57-63` | read / grep | high | Canonical repository skip pattern for `src-api` unit discovery |
| C6 | Static guards pin `setAttribute("aria-invalid", "true")` to `9` across `web/*.js`, `h("table", {}, ...)` to `14`, `"before recording this challenge."` in `panels.js`, and `0` banned jargon words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) across `web/*.js`. | `src/api/tests/test_accessibility_baseline.py:86-119`, `src/api/tests/test_content_standard.py:16-95`, `src/api/tests/test_epic149_form_error_summary_associations.py:18-137` | grep / read | high | Reordering `const staff` and adding `typeof c !== "undefined" && c` leaves all counts and copy untouched |
| C7 | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` binds SHA-256 hashes only for `workbench-manifest.json`, `workbench_browser_check.py`, `src/core/tests/dataset.py`, and `src/api/tests/test_workbench.py`—not `panels.js`. | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:45-50` | grep / read | high | `panels.js` edit will not invalidate scenario-manifest recipe SHAs |
| C8 | Worktree `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` is on branch `feat/ux-130-api-routes` at HEAD `2215209cbffde4834c83184d183d83232d8476e7`, which is the active head of open `PR #1776` targeting `feat/demo-233-same-home-tensions-0825` (`PR #1639`). | `.copilot-tracking/rpi-sessions/2026-11-15/nomination-api-routes-130-state.json:1-31` | bash (`git`, `gh pr view`) | high | Reuse active `PR #1776` branch `feat/ux-130-api-routes` per repository Branch Workflow |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Web Interface Guidelines require native labeled controls, `aria-live="polite"` async status updates, inline field error association with focus recovery, `autocomplete="off"` on non-auth inputs, and zero `outline: none` / `transition: all` anti-patterns. | Vercel Web Interface Guidelines (`command.md`) | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | 2026-11-15 | `main` (2026-11-15) | high |

### Contradictions / Conflicts

* Caller prompt shorthand vs live Git/CI identifiers (`feat/api-130-nomination-routes` vs `feat/ux-130-api-routes`; `renderFundingPanel` vs `affectedChallengePanel`; `test_nomination_screen_renders_create_and_step_forms_with_keyboard_reachability` vs `test_workbench_keyboard_operability_for_digital_and_non_digital_routes`): resolved by primary Git/PR/Actions inspection (`C1`, `C2`, `C3`, `C8`) -> apply the fixes at the exact failing locations on active `PR #1776` branch `feat/ux-130-api-routes`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Run `43694720253` on `PR #1776` (`feat/ux-130-api-routes`, HEAD `2215209cb`) had exactly 2 `src-api` unit-step failures: `test_case_journey.CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` and `test_nomination_api_routes.NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes`. | `C1`, `C8` | high | Targets the exact failing functions on `feat/ux-130-api-routes` |
| Q2 | `test_case_journey.py` slices `panels.js` from `const formFor = ` to `const staff`; `const perms = c.nomination_permissions ...` sat inside that slice where `c` is undefined. Moving `const staff` right after `formFor` AND guarding `typeof c !== "undefined" && c` eliminates the `ReferenceError` while preserving `_routeForm` behavior. | `C2`, `C3` | high | Surgical 5-line edit in `panels.js` |
| Q3 | `src-ci.yml` installs the Python `playwright` package before `unittest discover` and installs Chromium only in a later step. Catching `PlaywrightError` when `"Executable doesn't exist" in str(exc)` (plus `importlib.util.find_spec("playwright")` in `_playwright_available()`) matches `test_workbench_live_defaults.py` and `test_browser_asset_urls.py` while keeping HTTP/HTML route/DOM tests unconditional and running Playwright whenever Chromium is present. | `C4`, `C5` | high | Surgical helper + launch guard + unit test in `test_nomination_api_routes.py` |
| Q4 | `panels.js` is not hashed by `scenario-manifest.json`, and reordering/guarding `const perms` leaves `aria-invalid` (`9`), `table` (`14`), Epic 149 error associations, and `test_content_standard.py` untouched (`W1`). | `C6`, `C7`, `W1` | high | Zero collateral impact on manifest or static baselines |

## Key Discoveries

* `test_case_journey.py:709-716` slices two disjoint regions of `panels.js` (`captureChallengeDrafts`..`affectedChallengePanel` and `const formFor = `..`const staff`), so any case-dependent declaration placed between `formFor` and `staff` executes without `c` in scope (`C2`, `C3`).
* In hosted `src-api` CI, `import playwright` succeeds during `unittest discover`, so import-only `@unittest.skipUnless(_playwright_available(), ...)` does not detect an absent Chromium binary; catching `PlaywrightError` on `"Executable doesn't exist"` at `pw.chromium.launch(headless=True)` is the established repository pattern (`C4`, `C5`).
* Active `PR #1776` at HEAD `2215209cb` tracks branch `feat/ux-130-api-routes` targeting `feat/demo-233-same-home-tensions-0825` (`PR #1639`), and prior completed RPI artifacts `nomination-api-routes-130-*` must remain intact as parent lineage (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. In `src/api/src/zava_forward/api/web/panels.js` inside `affectedChallengePanel`, place `const staff = ...` immediately after `const formFor = ...` and guard `c` via `const caseRecord = typeof c !== "undefined" && c ? c : null;` before reading `caseRecord.nomination_permissions`, ensuring both clean `formFor`..`staff` slicing in `test_case_journey.py` and safe evaluation if sliced without `c`.
  2. In `src/api/tests/test_nomination_api_routes.py`, refine `_playwright_available()` using `importlib.util.find_spec("playwright") is not None`, wrap `pw.chromium.launch(headless=True)` in `try ... except PlaywrightError as exc:` calling `self.skipTest("Chromium is installed by the later browser-check step")` when `"Executable doesn't exist" in str(exc)` (re-raising any other `PlaywrightError`), and add a focused unit test verifying that a missing Chromium executable triggers `SkipTest` while keeping all HTTP/HTML route and DOM assertions unconditional.
* Rationale: Directly resolves both hosted `src-api` failures using established repository patterns (`C2`, `C3`, `C5`), keeps full Playwright keyboard coverage active whenever Chromium is installed, preserves every static WCAG/content guard (`C6`, `W1`), and avoids touching `test_case_journey.py` or CI workflows.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `W1`
* Implementation impact: `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_nomination_api_routes.py`, and child `.copilot-tracking/` RPI artifacts (`nomination-api-routes-130-ci-fix`).
* Confidence: `high`: both failures are deterministically explained by hosted tracebacks and local reproduction.

File tree:

```text
src/api/
  src/zava_forward/api/web/
    panels.js                          (modify: reorder staff before perms + typeof c guard)
  tests/
    test_nomination_api_routes.py      (modify: Chromium-missing PlaywrightError skip + unit test)
.copilot-tracking/
  rpi-sessions/2026-11-15/nomination-api-routes-130-ci-fix-state.json
  research/2026-11-15/nomination-api-routes-130-ci-fix-research.md
  plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md
  details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md
  reviews/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan-critique.md
  changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md
  reviews/2026-11-15/nomination-api-routes-130-ci-fix-review.md
```

### Alternative: Gate Playwright test behind opt-in `ZF_BROWSER_TESTS == "1"`

* Approach: Decorate `test_workbench_keyboard_operability_for_digital_and_non_digital_routes` with `@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", ...)`.
* Trade-offs: Simple decorator, but disables keyboard browser execution during default local test runs even when Chromium is installed and is not invoked by `src-ci.yml` unless `src-ci.yml` is also modified.
* Evidence refs: `C4`, `C5`
* Rejection rationale: Catching `PlaywrightError` on `"Executable doesn't exist"` (like `test_workbench_live_defaults.py` and `test_browser_asset_urls.py`) skips cleanly in unit containers without Chromium while running automatically whenever Chromium is installed, without editing `.github/workflows/src-ci.yml`.

### Alternative: Modify `test_case_journey.py` slice delimiter instead of `panels.js`

* Approach: Change `test_case_journey.py:715` `.split("  const staff", 1)[0]` or inject `const c = {};` into `test_case_journey.py`.
* Trade-offs: Would avoid editing `panels.js`, but leaves `panels.js` fragile to slice evaluation and diverges from caller instruction to guard `typeof c !== "undefined" && c` in `panels.js`.
* Evidence refs: `C2`, `C3`
* Rejection rationale: Fixing `panels.js` directly honors caller scope, keeps `test_case_journey.py` as an unchanged regression oracle, and protects both slice boundaries and `typeof c` safety.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: `none`
* Important: External human governance decisions (`OD-41`, `OD-42`), human representative comprehension sign-off, and remote push + hosted CI rerun on `PR #1776` remain post-commit owner actions (`Refs #130`).
* Follow-up: Optional axe-core 4.10.3 interactive scan extension in `src/api/checks/nomination_browser_check.py`.
* Residual uncertainty: `none` for local reproduction and verification.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Reuse active `PR #1776` head branch `feat/ux-130-api-routes` and record child RPI artifacts as `nomination-api-routes-130-ci-fix` | confirmed | constraint | `PR #1776` tracks `feat/ux-130-api-routes` at `2215209cb`; repository rules require reusing open PR branch and preserving parent RPI artifacts | `C8` | Clean additive commit on `feat/ux-130-api-routes` without history rewrite |
| Reorder `const staff` immediately after `formFor` and guard `typeof c !== "undefined" && c` in `affectedChallengePanel` (`panels.js`) | confirmed | evidence | Eliminates Node slice `ReferenceError: c is not defined` in `test_case_journey.py` without changing runtime semantics or static baseline counts | `C2`, `C3`, `C6` | `test_case_journey.py` passes unchanged |
| Skip Playwright launch only when `PlaywrightError` reports `"Executable doesn't exist"` and add a unit test covering that skip branch | confirmed | evidence | Aligns with `test_workbench_live_defaults.py` and `test_browser_asset_urls.py` in `src-api` CI while keeping Chromium runs and HTTP/DOM assertions active | `C4`, `C5` | Passes both with and without Chromium binary installed |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Human ratification of `OD-41` and `OD-42` and representative comprehension sign-off on Issue #130 | Named housing operations, safeguarding, and compliance sign-off | Human governance owners | Keeps PR #1776 linked via `Refs #130` rather than `Closes #130` | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Evaluate adding interactive dual-route axe-core scan steps to `nomination_browser_check.py` | Extends standalone browser check script parity | Separate follow-up selection | deferred | `Q4`; `C6` |

## Planning Readiness

* Status: `Ready`
* Decision state: Converged on surgical fixes in `src/api/src/zava_forward/api/web/panels.js` and `src/api/tests/test_nomination_api_routes.py` under focused-tier validation.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `W1`
* Preconditions met: Both hosted CI failures identified from primary run `43694720253` logs, reproduced/traced locally, and checked against static WCAG/content and manifest invariants.
* Blockers: `none`
* Smallest action to change readiness: `none` (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                       |
| Lane evidence or inline fallback | inline: bounded two-file CI failure investigation executed directly with primary Actions log evidence        |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C8`, `W1`)                                                                                      |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to Plan                                                |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`-`C8`, `W1`)                                                                                      |
| Output mode and planning support | `convergence`; yes — converged recommendation with `Ready` Planning Readiness                                |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (`passed`); Planning Readiness `Ready` (`passed`); pre-transition state write (`passed`) |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md                           |
| Notes for planning or re-entry   | Keep `test_case_journey.py` unchanged as the regression oracle; run `unittest` with `src/core` in `PYTHONPATH` (or from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`) so `tests.test_mvp` resolves cleanly. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because both run `43694720253` failures are completely traced to exact lines with verified repository patterns.

## Sources

* `W1`: Vercel Web Interface Guidelines (`command.md`), `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved 2026-11-15).
* Workspace files and hosted CI logs cited in `C1`–`C8`.

## Self-Check

* Research brief, output mode (`convergence`), scope, non-goals, criteria, and requested outputs recorded: Passed.
* Direction controls, Extension Registry (`4` entries), and Participation record completed: Passed.
* Cycle 1 ordered Wider, Deeper, and Contrarian waves, reflections, parent synthesis dispositions, and re-entry evaluation recorded: Passed.
* All questions `Q1`-`Q4` answered and mapped to `C1`-`C8` and `W1` with gap-free Sources: Passed.
* Selected recommendation and two rejected alternatives documented: Passed.
* Research remained strictly read-only on repository source/test files; untrusted fetched content treated as inert data; zero secrets recorded: Passed.
