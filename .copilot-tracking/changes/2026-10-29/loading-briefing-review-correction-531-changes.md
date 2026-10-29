<!-- markdownlint-disable-file -->
# RPI Changes: loading-briefing-review-correction-531

## Metadata

* Task ID: 531-review-correction-2026-10-29
* Declared scope: Full plan
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-review-correction-531-plan.md
* Details: .copilot-tracking/details/2026-10-29/loading-briefing-review-correction-531-phase-details.md
* Date: 2026-10-29

## Execution Status

Implementation and requested validation complete; P01/P02/P03-T01 complete.
P03-T02 local candidate commit and parent-owned single Review/final evidence
remain. No source implementation remains before Review.
No source edits preceded the completed dependency and punctuation audit.
Web-design-guidelines loaded and current rules fully retrieved before edits.
Critique executed once, original Revise verdict preserved and disposed in plan.

## Changes and Validation

### P01: Dependency readiness

* Complete audit identified only app/law direct consumers and index/law HTML loaders.
* New whole-law VM exercises absent, null, empty, missing and non-callable methods,
  no premature reads/helper calls, disabled form and callable native reload.
* Regression-first helper run failed: law ReferenceError; app null TypeError.
* law now checks handler/run before use and renders focused native recovery;
  app checks handler/run/feedback before bootstrap and all route work.
* Null helper also requires h()'s native terminal listener path to check the
  object before handler access. Added null to actual startup renderer matrix;
  it first reproduced TypeError, then received the same null guard.
* Browser adds blocked/missing/null/handler-only/run-only law cases, keyboard
  reload, no-read/no-pageerror assertions and restored list/search/details.
  Workspace browser adds run/feedback partial interface cases.

### P02: Punctuation ownership

* Complete run shared by relocation and splitting includes ASCII terminators,
  Unicode ellipsis and existing closing delimiters.
* Expanded existing full-object matrices across terminators/whitespace/closers/
  placement and literal supplied goldens; no existing test removals.
* In-scope counterexample `(Still waiting...). [[First source]]` reproduced
  the same punctuation-only fragment when a closer precedes final punctuation.
  Complete trailing runs therefore permit terminators and supported closers
  to interleave after the first terminator. Added paired/nested closer-plus-dot
  matrix and two literal goldens; no separate parser or fallback.
* Initial test edit had an indentation error, corrected before regression run.
  Literal regression then fails all five before-fix cases; original split and
  Unicode merge outcomes preserved in external logs.
* After fixes: 79 scoped helper/loading/parser/API tests pass in 12.037s.
* JS syntax, diff whitespace and changed test Ruff lint/format pass.
* Manifest integrity: all 11 test_needs_inventory tests pass; no pinned files edited.

### P03: Heavy validation attempt

* Nonblocking admission succeeded; lock held across editable setup and full checks.
* Installed current core/agents/api into /tmp/mv with pip -e.
* Python 3.12.3, mypy 2.4.0, Ruff 0.17.1, Playwright 1.64.0.
* Core mypy (157 files), lint and format (104 files) pass.
* First core discovery failed due same-named test_buildings imported from API:
  shared PYTHONPATH had API test directory before core tests. Fix validation
  environment to put the owning test directory first; not a production defect.
* First API mypy identified unannotated mixed browser fixture metadata.
  Added dict[str, Any] annotation; no suppression or type cast. Rerun required.
* Full/API/browser results still in progress at this point; not claimed passed.
* External logs: /tmp/issue-531-correction-20261029-validation.
* First API discovery passed 1219 tests in 450.871s with 316 explicit skips.
  The external wrapper then exited 2 before browser dispatch because it had
  been edited while running. This attempt is not treated as a full pass.
  Corrected wrapper was syntax-checked, frozen and rerun into a new directory.

### P03: Final stable-source validation

* Source edits complete before this run. Nonblocking admission succeeded again;
  one lock covers editable setup, strict tools, browser and full package suites.
* External evidence: /tmp/issue-531-correction-20261029-validation-final.
* API/core mypy pass (101/157 checked source files); both `ruff check .` and
  `ruff format --check .` pass (53/104 formatted files). Existing repository
  migrated-module exemptions are unchanged.
* Pinned axe 4.10.3 SHA-256 verified by the browser harness; Chromium
  156.0.8078.4 loading/briefing browser check passes. All seven workspace-helper
  scenarios and all five new standalone law-helper failures pass. Each law
  case restores list/search/source/provision actions after keyboard reload.
  Four existing axe states report zero violations; this is not full WCAG,
  screen-reader/voice, staff-user or live-site acceptance.
* Core full discovery passes: 1463 tests, 300.066s, 190 explicit skips.
* Final API discovery passes: 1219 tests, 445.344s, 316 explicit skips.
  Both suites include configured opt-in integration skips; skipped SQL/live/
  browser scenarios are not claimed as executed.
* Rechecked all four scenario-manifest SHA-256 pins directly: unchanged/matching.
* Final scoped 79 tests pass in 11.918s after null-renderer/interleaved-run batch.
* Authenticated gh account resolved and repository-local author/committer
  noreply email configured. No remote write performed.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Regression-first helper | Actual law/bootstrap/renderer scripts | Failed as expected | ReferenceError and null TypeError before guards |
| Regression-first literal parser | Supplied plus Unicode/closer siblings | Failed as expected | Five full-object failures; interleaved closer separately reproduced |
| Scoped units | Helper/loading/parser/API AI tasks | Passed | 79 tests after final source batch |
| Core mypy | src/core, existing strict config | Passed | 157 files |
| API mypy | src/api, existing strict config | Passed | 101 files |
| Core/API Ruff | `ruff check .`; `ruff format --check .` in each project | Passed | 104/53 formatted files; no new exemptions |
| Core full units | `python -m unittest discover -s tests -q` | Passed | 1463 tests, 190 opt-in skips |
| API full units | Same command in API | Passed | 1219 tests, 316 opt-in skips |
| Loading/briefing browser | Existing real-loopback check plus law/helper cases | Passed | Chromium 156.0.8078.4; four axe states, zero violations |
| Scenario metadata | test_needs_inventory and all four SHA-256 pins | Passed | 11 tests; no pinned files edited |
| JS syntax and diff | app.js/law.js; `git diff --check` | Passed | No syntax/whitespace error |
| Complete publication gate | Whole repository/native SQL/images/scanners | Not run | No publication authorized; no full receipt claimed |
| Human/hosted/live acceptance | Staff, screen reader/voice, deployed cold start, PR CI | Not run | Outside local correction; no push |

Final command environment: `PYTHONDONTWRITEBYTECODE=1`; `PYTHONPATH` begins with
this worktree's src/api/src, src/core/src, src/agents/src, then the owning
project's tests before sibling tests to avoid duplicate test-module names.
Tools are /tmp/mv/bin/python, mypy and ruff. Browser:
`python -m checks.loading_briefing_browser_check --axe /tmp/issue-531-correction-20261029-validation-final/axe-4.10.3.min.js --out /tmp/issue-531-correction-20261029-validation-final/browser`.
The final frozen external wrapper exited 0, holding `flock -n` across all
shared-venv mutations, full suites and browser. No queue, cloud or skip fallback.

## Amendments and Divergences

No material divergence. Unicode ellipsis normalization and full workspace
interface readiness were planned sibling corrections, not unrelated expansion.

## Blockers and Remaining Work

No implementation/validation blocker. P03-T02 local commits and the single
parent-owned Review/final evidence remain; original failed attempts retained.

## Pre-Review Reconciliation

* Plan markers/details: P01/P02/P03-T01 complete; P03-T02 lifecycle finalization
  remains explicitly pending, with no pending source change.
* Completed-work and validation evidence: current; no unreported failed check.
* Critique: executed once; original Revise and direct dispositions preserved.
* Scope: seven src/ files plus this dated evidence set; no pinned files changed.
* Review readiness: Ready once candidate implementation/evidence is committed.
* Review boundary: intake bddf4b179dc49147e64c697871899484d16c042f to candidate.
* Follow-up only: human/hosted/live approval and any later publication gates.
