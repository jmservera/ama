<!-- markdownlint-disable-file -->
# RPI Plan Critique: Map navigation disposal correction

## Metadata

* Task ID: issue-532-pr-539-map-navigation-disposal
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md
* Critique execution status: Complete
* Assessment: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: fix obsolete Expand activation while listView awaits facets; exercise real pointer activation during that wait and retained event activation; reload before every session-expiry iteration; preserve prior evidence and the bounded test budget.
* Research: .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md, including C1-C7 and the recorded W1 retrieval.
* Source evidence read: src/api/src/zava_forward/api/web/app.js, src/api/checks/map_fullscreen_browser_check.py, src/api/tests/test_map_fullscreen.py, src/api/README.md, src/api/pyproject.toml and src/core/pyproject.toml.
* Repository context: original/addendum opening context, knowledge-base index and owner memory; read-only branch/status inspection confirmed feat/map-fullscreen-532 and the supplied new planning artifacts.
* Decisions and dependencies: inert/disabled before collapse; collapse before seq++; slot removal and inert-based expand guard; document reload before Coordinator navigation and fresh instrumentation; existing constructed server, pinned axe and tooling; nonblocking shared-lock admission for heavy checks.
* Acceptance boundary: assess implementation readiness against the supplied requirements, phase details, source lifecycle and test design. Preserve local-only Conventional commits/coauthor, no push, az, force-push, closing keywords or merge. Do not reassess unrelated functionality or broaden the agreed scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C3, P01-T01: obsolete controls during pending navigation | Covered | route() aborts before listView() awaits facets; current dispose leaves the slot connected. Planned inert/disabled state and removal terminate that UI lifetime before destination rendering. |
| C1/C3, P01-T01: retained activation and live-signal disposal | Covered | A guard on slot.inert prevents a retained dispatched click from entering expand even when session disposal does not abort the route signal. Removal alone is not treated as sufficient. |
| P01-T01: existing modal, focus and response cleanup | Covered | Details preserve collapse(false), then seq++, dialog removal, Leaflet removal/nulling and listener/disposer cleanup. Disabling before collapse does not remove its resize path; the sequence invalidation remains afterward. |
| C4, P01-T02: exact pending-facets regression | Covered | Retain original handles/coordinates, hold the real facets request, follow the actual list link, establish aborted old route and pending destination, click before releasing, then exercise retained dispatch. Pending and rendered-destination checks explicitly include modal/body-lock residue. |
| C2/C5, P01-T02: independent expiry iterations | Covered | Reload at each loop's start resets ovState, me and wrapped functions through real startup; Coordinator readiness precedes fresh instrumentation. The synthetic 401 does not invalidate the server cookie. |
| P01-T02: existing browser scenarios | Covered | Existing embedded/expanded expiry assertions, forced collapse-resize draw, late-response checks and separate 640px/32px-font browser remain required, as does page-error collection. |
| C6, P02-T01: strict tools and unit/browser validation | Covered | API/core mypy and both Ruff checks are required. Full units/browser share nonblocking lock admission; explicit current-worktree source/test paths avoid relying on another checkout. Busy-lock fallback names targeted modules and leaves full/browser evidence blocked. |
| P02-T01: regression sensitivity | Covered | The old-app.js served-response negative control is isolated from the worktree and must fail the new pending-navigation regression under admitted lock, without weakening positive assertions. |
| C7: manifest pins | Covered | Planned edits do not intersect the four research-listed pinned inputs; read-only hash verification is required and conditional updates remain limited to changed inputs. |
| Scope, test budget and local closeout | Covered | Four canonical source/documentation targets, at most one browser helper and two source-contract methods, no new dependencies, original evidence retention, one independent Review and local commits are explicit. Publication and hosted/human approval are not inferred. |

## Verdict

* Verdict: Pass
* Rationale: The proposed lifecycle fix addresses both connected obsolete controls and retained callbacks, including disposal with a live route signal. The browser design tests the actual asynchronous exposure window rather than only the eventual destination. Per-iteration reload is the narrow complete reset supported by the current runner and startup behavior. Verification and fallback boundaries are explicit and credible within the caller's locked budget.

## Findings

No actionable PC-xxx findings. Complete severity counts: Critical 0, High 0,
Medium 0, Low 0. No direct planner correction or significant/divergent user
decision is required.

## Strengths and Residual Risk

* The plan preserves collapse-before-sequence-invalidation, which is essential to retain meaningful coverage of collapse-triggered asynchronous redraws.
* Both ordinary pointer interaction and retained synthetic activation are required. Source-string assertions are explicitly supporting evidence, not substitutes for browser behavior.
* The accepted lock-busy branch permits bounded progress, not browser acceptance. Until admitted positive browser and negative-control evidence exists, those acceptance items remain unverified and must be recorded as blocked.
* Real Chromium execution must confirm the pending-state synchronization, retained-handle assertions and full runner progression. The plan does not present these future checks as observed results.
* Local-only validation does not establish publication readiness, hosted approval, human accessibility acceptance or whole-WCAG conformance.

## Questions or Blocking Evidence Gaps

None for plan readiness. Heavy-lock availability and executable results are
implementation-time dependencies already assigned to P02-T01, not reasons to
expand this critique or change the agreed test budget.

## Limitations

* Read-only assessment of supplied planning/research artifacts and relevant supplied source targets; no tests, browser execution, remote inspection or dependency verification performed.
* Research statements about the existing environment, prior pull and pin inventory are supplied evidence, not independently reproduced execution claims.
* This is not a changed-web-file guidelines review, implementation Review or final acceptance assessment. No plan, detail, research, source or historical evidence file was changed.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition, finalize the plan and proceed to P01-T01 within the existing authorization.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md | Assessed task details |
| .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md | Supplied lifecycle and validation evidence |
| .copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md | This single independent critique |

## Next Steps

No user action is required. The active planning parent may finalize disposition
and advance to P01-T01. Critique work stops here; no repeat critique is required.
