<!-- markdownlint-disable-file -->
# RPI Plan Critique: Fix Issue 130 src-api CI Failures from Run 43694720253

## Metadata

* Task ID: nomination-api-routes-130-ci-fix
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Resolve the two hosted `src-api` unit-step failures from GitHub Actions run `43694720253` on Issue `#130` (`PR #1776`, HEAD `2215209cb`, branch `feat/ux-130-api-routes`): (1) eliminate `ReferenceError: c is not defined` when `src/api/tests/test_case_journey.py` slices `affectedChallengePanel` between `const formFor = ` and `const staff` in `src/api/src/zava_forward/api/web/panels.js` using `typeof c !== "undefined" && c` and restoring slice compatibility; (2) align `src/api/tests/test_nomination_api_routes.py:521` with peer `src/api/tests/` missing-Chromium `PlaywrightError` skip handling when Chromium is not yet installed in the `src-api` unit-test step, while keeping HTTP/HTML route and DOM assertions unconditional and executing full Playwright checks whenever Chromium is installed; and (3) run focused validation (`unittest` over `test_case_journey.py`, `test_nomination_api_routes.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `ruff check src/api`, `mypy`, and `test_scenario_manifest.py` plus `test_needs_inventory.py`) and commit locally on `feat/ux-130-api-routes` with the Copilot `Co-authored-by` trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md (`C1` through `C8`, `W1`), .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md, .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md, src/api/src/zava_forward/api/web/panels.js (lines 785-845), src/api/tests/test_case_journey.py (lines 700-800), src/api/tests/test_nomination_api_routes.py (lines 1-110 and 500-632), and src/api/tests/test_workbench_live_defaults.py (lines 1-40 and 95-130).
* Decisions, dependencies, and acceptance criteria considered: Confirmed reuse of active `PR #1776` branch `feat/ux-130-api-routes` (`C8`), preservation of historical `nomination-api-routes-130-*` parent RPI artifacts, locked production/test edit scope (`panels.js` and `test_nomination_api_routes.py` only outside `.copilot-tracking/`, `0` test removals, maximum `1` added unit test), preservation of WCAG and plain-language static baselines (`9` `aria-invalid` attributes, `14` `table` elements, `0` banned copy terms, Epic 149 error-summary associations), focused validation tier applicability, and local-only commit constraint.
* Assessment boundary: Evaluates plan and phase-detail credibility strictly from the supplied artifacts and source/test slices without executing tests, mutating files outside this critique path, or observing post-push hosted CI runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 (`panels.js` slice + `typeof c` guard) | Covered | `P01-T01` moves `const staff` immediately after `const formFor` (`panels.js:803-827`) so `test_case_journey.py:714-715` slices `formFor` cleanly without leaking `perms`/`repRefs`, and guards `typeof c !== "undefined" && c` before reading `nomination_permissions` (`C2`, `C3`). |
| Caller Req 2 (`test_nomination_api_routes.py:521` Chromium skip) | Covered | `P01-T02` catches `PlaywrightError` on `"Executable doesn't exist"` during `pw.chromium.launch(headless=True)` with `self.skipTest("Chromium is installed by the later browser-check step")`, matching `test_workbench_live_defaults.py:108-113` (`C4`, `C5`), re-raising other `PlaywrightError` failures, adding `1` unit test for the skip/re-raise contract, and leaving HTTP/HTML route/DOM tests unconditional. |
| Caller Req 3 (Focused validation + local commit on `feat/ux-130-api-routes`) | Covered | `P02-T01` and Plan Acceptance Criteria cover every caller-requested `unittest`, `ruff`, `mypy`, and `scenario-manifest`/`needs_inventory` check plus coupled `test_nomination_screen.py` and `test_epic149_form_error_summary_associations.py` suites, followed by a local no-push commit on `feat/ux-130-api-routes` with the Copilot `Co-authored-by` trailer (`C6`, `C7`, `C8`). |
| Research `C1`-`C8`, `W1` | Covered | Plan accurately reconciles run `43694720253` tracebacks (`C1`), slice boundaries (`C2`, `C3`), `src-ci.yml` Chromium installation order (`C4`, `C5`), static WCAG/content and `scenario-manifest.json` invariants (`C6`, `C7`, `W1`), and open `PR #1776` branch lineage (`C8`). |
| `P01` / `P01-T01` | Covered | Reordered `staff` has no dependency on `perms` or `repRefs` (`staff` filters `me.staff` only), introduces zero banned words from `test_content_standard.py`, and leaves DOM element/attribute counts unchanged. |
| `P01` / `P01-T02` | Covered | Uses `importlib.util.find_spec("playwright") is not None` in `_playwright_available()`, narrows skip handling strictly to `"Executable doesn't exist" in str(exc)`, preserves live headless-Chromium execution locally, and bounds new tests to `1` (`test_keyboard_operability_skips_when_chromium_executable_missing`). |
| `P02` / `P02-T01` | Covered | Runs `unittest` both from `src/api` (matching `.github/workflows/src-ci.yml`) and from repository root with `src/core` on `PYTHONPATH` so `from tests.test_mvp import DATA` resolves deterministically, alongside `ruff check`, `ruff format --check`, `mypy`, and `src/core` manifest/inventory suites. |

## Verdict

* Verdict: Pass
* Rationale: Every caller requirement and research finding (`C1`-`C8`, `W1`) is traced to exact, minimal, non-breaking changes in `src/api/src/zava_forward/api/web/panels.js` and `src/api/tests/test_nomination_api_routes.py`. In `panels.js:803-827`, `staff` depends only on `me.staff`, so placing `const staff` immediately after `const formFor` restores the exact `source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]` slice expected by `src/api/tests/test_case_journey.py:714-715`, while `const caseRecord = typeof c !== "undefined" && c ? c : null;` eliminates undeclared-identifier `ReferenceError` risk without altering DOM semantics or static WCAG/content baselines. In `src/api/tests/test_nomination_api_routes.py:511-525`, catching `PlaywrightError` only when `"Executable doesn't exist"` appears matches `src/api/tests/test_workbench_live_defaults.py:108-113`, keeps all non-browser HTTP/HTML route and DOM assertions unconditional, runs full Chromium keyboard verification when Chromium is present, and proves the skip/re-raise branch via one focused mock unit test. No actionable `PC-xxx` findings require plan revision.

## Findings

* None (`0` Critical, `0` High, `0` Medium, `0` Low).

## Strengths and Residual Risk

* Exact root-cause alignment without oracle mutation: Fixing `panels.js` directly keeps `src/api/tests/test_case_journey.py` and `.github/workflows/src-ci.yml` untouched as authoritative regression checks (`C2`, `C3`, `C4`).
* Narrow skip discrimination: Re-raising any `PlaywrightError` that does not contain `"Executable doesn't exist"` ensures genuine browser startup or crash failures still fail loudly whenever Chromium is installed (`C5`), while `test_accessible_html_route_fragment_labels_channels_and_live_status` continues verifying accessible route HTML unconditionally in every unit container.
* Non-blocking implementation guardrails to retain during execution: Decorate `test_keyboard_operability_skips_when_chromium_executable_missing` with `@unittest.skipUnless(_playwright_available(), "playwright unavailable")` (or guard `PlaywrightError` import) so collection remains clean even if `playwright` itself is absent; include `src/core` on `PYTHONPATH` if needed when running `src/core/tests/test_scenario_manifest.py` and `src/core/tests/test_needs_inventory.py` from repository root; and configure repository-local `git config --local user.email` from `gh api user` (`{id}+{login}@users.noreply.github.com`) before creating the final post-review local commit with the Copilot `Co-authored-by` trailer.
* Explicitly accepted residual risk: Because the caller forbids pushing to `origin`, hosted GitHub Actions re-verification on `PR #1776` and human governance sign-offs (`OD-41`, `OD-42`, representative comprehension review under `Refs #130`) remain owner-controlled post-commit actions.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is static and read-only over supplied plan, research, and code/test ranges; live test execution, `web-design-guidelines` post-edit audit, and local Git commit verification belong to `rpi-implement` and `rpi-review`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize candidate plan readiness (`Critique Disposition` and `Planning status`) and proceed automatically to `rpi-implement` starting at `P01-T01`.
* User response required: no
