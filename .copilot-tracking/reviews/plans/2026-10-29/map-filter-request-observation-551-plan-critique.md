---
title: Map filter request observation final-candidate plan critique
description: One bounded implementation-readiness assessment for issue 551 and PR 553
ms.date: 2026-10-29
---

## Metadata

* Task ID: 551 / map-filter-request-observation-551
* Critique date: 2026-10-29
* Critique execution status: Complete
* Assessment count: exactly one final-candidate critique.
* Plan: .copilot-tracking/plans/2026-10-29/map-filter-request-observation-551-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-filter-request-observation-551-phase-details.md
* Verdict: Revise

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research, the named browser
  source, its imported loopback harness, the application guard, existing
  source-contract tests, API execution guidance and original issue Review.
* Confirmed read-only that PR 553 is open, targets main and uses the current
  feat/map-filters-551 branch. The existing untracked planning inputs were
  preserved; this assessment does not authorize moving or committing them.
* Requirements include all-request observation using check_browser_shortcuts
  prior art, dated RPI evidence, focused tests using /tmp/mv and explicit
  current-source PYTHONPATH, Ruff lint/format, JavaScript syntax, actual local
  browser evidence, a local-only privacy-safe commit and the Copilot trailer.
* Assessed the locked budget: one local listener, two assertions replacing
  the ineffective assertion, no new test file/helper, no application changes.
* No push, az operation, score edit, publication claim, source edit, nested
  delegation or additional critique is authorized by this assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2; all-request observation | Covered | Page request events observe requests that hold_first deliberately continues without appending to held. |
| P01-T01; synchronization | Covered | First activation retains expect_request; the repeated activation is followed by the established two-requestAnimationFrame boundary before count comparison. |
| P01-T01; non-vacuity | Covered | Listener installation precedes the first safety activation, and a separate first-read assertion precedes the saved baseline. The preceding support state has settled. |
| P01-T01; listener lifecycle | Covered | Nested finally removes only the added listener before unrelated area requests; outer unroute and held-response behavior remain unchanged. |
| P01-T01; ownership and budget | Covered | Named existing helper owns the correction; the callback is the permitted local listener, not a new test helper. README-only documentation changes remain bounded. |
| C4/C5; P02-T01 negative control | Covered | Removing the exact already-selected guard causes the second Space activation to call draw and issue another map fetch; only the named duplicate-read assertion is acceptable failure evidence. |
| P02-T01 focused checks | Covered | Six existing unittest modules, explicit source/test PYTHONPATH, requested interpreter, Ruff check/format, node syntax and whitespace checks are specified. |
| P02-T01 actual browser execution prerequisites | Partial | PC-001: the execution recipe omits the documented shared lock and explicit safe browser scratch configuration. |
| P02-T02 evidence and independent Review | Covered | Original failures, deviations and limitations are retained; one bounded independent Review is planned without silently repairing its new findings. |
| P02-T02 local delivery | Covered | GitHub-derived privacy-safe identity, task-owned staging, Conventional Commit and trailer are required; remote and publication operations remain excluded. |

## Verdict

* Verdict: Revise.
* The correction itself is credible and sufficiently bounded. One direct
  planner correction is needed to make the real-browser validation recipe
  safe and executable under the supplied shared-environment constraints.
* Severity counts: Critical 0, High 0, Medium 1, Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Browser execution omits shared-lock and scratch prerequisites

* Related IDs: P02-T01; actual local browser acceptance criterion.
* Evidence: .copilot-tracking/details/2026-10-29/map-filter-request-observation-551-phase-details.md
  specifies the existing loopback browser harness but no lock or browser
  scratch environment. src/api/README.md requires acquisition of the shared
  heavy-check lock nonblocking before execution.
  src/api/checks/map_fullscreen_browser_check.py:616 launches Chromium with
  default scratch handling. The imported harness explicitly places its own
  synthetic server data under the repository's .venv, but does not configure
  Chromium/Playwright scratch. Supplied execution constraints forbid file
  writes under /tmp and require project-relative scratch creation.
* Concern: The proposed output-directory rule controls reports and the
  mutation runner, not all browser scratch writes. The phase also leaves
  the mandatory shared-heavy-check coordination implicit.
* Impact: Browser validation can contend with another user's heavy checks
  or attempt forbidden scratch writes. A successful unittest/static run
  would not resolve either browser-execution prerequisite.
* Smallest useful change: Add the established nonblocking shared-lock
  acquisition and release to the positive and negative browser execution
  recipe. Configure a project-local scratch location for browser processes
  before launch, without changing application or harness source. Preserve
  /tmp/mv as the requested executable location; this finding concerns
  writes, not execution of that existing interpreter. If prerequisites
  cannot be established, record browser validation as blocked rather than
  claim acceptance.
* Action owner: Planning parent, followed by the P02-T01 implementer.
* Exact resolving evidence: Updated P02-T01 details name the existing lock
  acquisition/release mechanism and project-local browser scratch setup.
  Subsequent execution evidence records successful nonblocking acquisition,
  the configured scratch environment for both runs, cleanup/release, and
  either the required positive/targeted-negative results or an honest blocker.
* Decision route: Direct planner correction; no significant or divergent
  user decision and no new critique are required.
* Resolution at critique close: Open; plan sources remain unchanged.

## Strengths and Residual Risk

* The plan correctly distinguishes held-route bookkeeping from all-request
  observation. The existing len(held) invariant cannot detect duplication.
* First-request non-vacuity and unchanged baseline are separate assertions,
  respecting the locked budget and avoiding a false pass from an uninstalled
  or incorrectly filtered listener.
* Two animation frames are relevant to the inspected implementation: the
  click handler calls draw directly, and draw initiates the API read before
  awaiting its response. This is not a general guarantee for future delayed
  or debounced implementations.
* The held original request remains pending while the second activation is
  exercised. Nested listener cleanup leaves the original outer route cleanup
  and newer-area/older-response scenario intact.
* The proposed in-memory mutation is viable without altering the working
  app.js or running source-contract tests against a mutated file. Requiring
  the exact duplicate-read assertion failure rejects unrelated early failures
  as regression-sensitivity evidence.
* The negative runner must actually serve the mutated script to the tested
  page while preserving the external-request block. This is implementation
  work already covered by the required targeted failure, not a missing plan
  decision or additional finding.
* Local-only scope deliberately leaves publication receipts, hosted checks,
  human accessibility acceptance and whole-PR acceptance unestablished.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical research gap.
* PC-001 is a bounded validation-recipe correction, not a product-design
  blocker or permission to add helpers, dependencies or source changes.

## Limitations

* This is a plan critique, not implementation Review or test execution.
  No browser, mutation, unittest, lint or syntax result is claimed here.
* Tool availability, lock availability and actual scratch behavior must be
  established during P02-T01; existing historical results are not fresh
  evidence for this correction.
* Exactly this critique artifact was added. Original research, plan, phase
  details and Review outcomes were not modified.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record PC-001's execution prerequisites and
  disposition in the plan/details, then continue the bounded implementation.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/map-filter-request-observation-551-plan.md](.copilot-tracking/plans/2026-10-29/map-filter-request-observation-551-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/map-filter-request-observation-551-phase-details.md](.copilot-tracking/details/2026-10-29/map-filter-request-observation-551-phase-details.md) | Implementation and validation details |
| [.copilot-tracking/research/2026-10-29/map-filter-request-observation-551-research.md](.copilot-tracking/research/2026-10-29/map-filter-request-observation-551-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/plans/2026-10-29/map-filter-request-observation-551-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/map-filter-request-observation-551-plan-critique.md) | This original critique |

## Next Steps

The active planning parent should resolve PC-001 directly and preserve this
original Revise outcome. No user action or further critique is required.
