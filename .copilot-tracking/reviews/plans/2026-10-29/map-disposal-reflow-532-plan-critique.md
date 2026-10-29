---
title: Map disposal and enlarged-font correction plan critique
description: Single final-candidate credibility assessment for issue 532 and PR 539
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-532-pr-539-map-disposal-reflow
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/map-disposal-reflow-532-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-disposal-reflow-532-phase-details.md
* Critique execution status: Complete
* Assessment count: one final-candidate assessment; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: correct both supplied Copilot findings using sequence
  invalidation after collapse(false) and min(19rem,45%); preserve existing
  behavior; exercise real browser regressions and negative controls; validate
  API/core types, Ruff lint, Ruff formatting and units with explicit
  current-worktree source/test imports; use the requested shared environment
  and nonblocking heavy lock; retain dated evidence and local Conventional
  Commits; do not use az, push or force-push.
* Research: .copilot-tracking/research/2026-10-29/map-disposal-reflow-532-research.md,
  Q1-Q3, C1-C6 and the recorded W1 retrieval.
* Direct evidence: named app.js and style.css targets under
  src/api/src/zava_forward/api/web; src/api/checks/map_fullscreen_browser_check.py;
  src/api/tests/test_map_fullscreen.py; the cited sections of src/api/README.md
  and src/README.md.
* Repository context: original case study, addendum, knowledge-base index and
  owner memory read for scope and standing constraints, not as browser evidence.
* Decisions and dependencies: owner-selected feat/map-fullscreen-532 branch,
  local-only correction, five existing application/documentation files, at most
  two new focused browser helpers, no new unit methods, constructed loopback
  data, existing Chromium and integrity-pinned axe.
* Baseline inspected: 300a1a10. The supplied plan, details, research and session
  state were already untracked. This critique does not move, stage or modify them.
* Boundary: assess implementation credibility once against supplied materials
  and their named evidence. No new external research, fresh guideline audit,
  test execution, environment mutation or remote-state inspection was performed.
  Research's branch/pull history and W1 retrieval remain attributed records,
  not independently repeated operations.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1, C4, P01-T01: disposal correction | Covered | app.js dispose collapses before map removal; draw uses signal and sequence; login disposes without route abort. Requested post-collapse increment addresses the identified boundary. |
| Q2, C2, P01-T01: grid correction | Covered | Desktop expanded track is 19rem; the 600px media query does not cover 640px. Requested cap is bounded and retains the mobile rule. |
| C5, P01-T01: source contracts | Partial | Existing cleanup and layout unit methods are suitable owners. PC-001 specifies the required disposal-local ordering predicate. |
| Q1, Q3, P02-T01: stale-response regression | Partial | Real handlers, controlled 401/success order and live-signal intent are present; latest-request and completion evidence remain underspecified. PC-001. |
| Q2, P02-T01: actual default-font regression | Partial | Root-font assertion and geometry criteria are strong; no supported browser configuration mechanism is selected. PC-002. |
| P02-T01: negative controls | Partial | Pre-fix served-asset overrides are explicitly required. PC-001 and PC-002 require independent controls with defect-specific failures, not generic runner failure. |
| P02-T01: bounded ownership and preservation | Covered | Existing browser file owns at most two helpers; no removals, new fixtures, production hooks, unit methods, casts or suppressions. Existing journeys remain required. |
| P02-T02: static/unit/import gates | Partial | Both packages, explicit worktree source/test PYTHONPATH, strict checks and admission disclosure are required; environment constraints are unresolved. PC-003. |
| P02-T02: evidence, review and local commits | Covered | Dated original evidence, single independent Review, privacy-safe identity and local-only Conventional Commits are planned; no publication or human acceptance claim. |
| C6: lock contention and manifest pins | Covered | Busy admission permits disclosed targeted work, not a fabricated full pass. No planned pinned-input edit is identified; refresh remains conditional. |

## Verdict

* Verdict: Revise
* Rationale: both requested source corrections are credible and appropriately
  bounded. The plan is not yet implementation-ready because its most important
  regression can pass for the wrong reason, its actual browser-font setup is
  unspecified, and its executable validation path conflicts with the current
  session's filesystem restrictions. These are direct planning corrections,
  not reasons to reopen the owner's source decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Pin request ownership and actual continuation completion

* Related IDs: Q1, Q3, C1, C3-C5, P01-T01, P02-T01; disposal acceptance criteria.
* Evidence: research's Risks and Self-check requires the fit request to remain
  latest immediately before release, while P02-T01 also expects collapse-driven
  resize coverage. app.js collapse calls resize; moveend can invoke draw(false),
  and every draw increments seq before awaiting api. The current browser check
  uses network responses and DOM replacement for existing redraw assertions,
  but has no disposed-draw completion observer.
* Concern: the later held draw(true) may already be superseded by a resize draw
  before its successful response is released. Unfixed code would then return
  at my !== seq, yielding a false green. Conversely, requiring sequence equality
  after corrected disposal contradicts the intended invalidation. Waiting for
  requestfinished or a response alone does not prove that the awaited api/draw
  continuation has run. The plan names the desired observations without
  selecting how to obtain them. Ordinary pointer selection of Overview filters
  also cannot be assumed while the modal makes those outside controls inert.
* Impact: a passing browser run could fail to reproduce the supplied stale-fit
  bug, or the new test could hang on an impossible post-disposal precondition.
* Smallest useful change: specify one bounded request/continuation protocol in
  P02-T01. Settle initialization and expansion before capturing requests;
  identify each fit request by its lack of bbox and the exact controlled
  handler invocation; establish that the held success was latest immediately
  before disposal, not after it. Use the embedded case to demonstrate the
  unsuperseded stale-fit defect. For expanded disposal, explicitly control and
  account for collapse-triggered requests and state how the real filter handler
  is invoked without depending on interaction with inert modal background.
  Select a check-only observer of actual draw settlement, followed by a bounded
  task/frame drain, rather than a network-only wait or arbitrary sleep. Capture
  the actual request signal before disposal and prove it remains un-aborted.
  Scope the unit contract to the dispose closure and assert
  collapse(false) < sequence increment < dialog/map removal < map = null;
  a whole-MAP substring ordering check is insufficient.
* Action owner: planning parent; implementation owner executes the specified
  protocol within the existing disposal helper and cleanup unit method.
* Exact resolving evidence: revised details name the capture points, request
  identities, timeout/completion mechanism and expanded-mode request handling.
  Execution later records an original-JS/corrected-CSS negative control failing
  the stale-success assertion after actual continuation settlement, and the
  corrected-JS pass with the same live-signal and nonempty-bounds preconditions.
  Expanded evidence accounts for resize requests and modal/body cleanup. The
  disposal-local unit assertion rejects both missing invalidation and moving
  invalidation before collapse. Neither a superseded request, timeout nor an
  unrelated initial-load error counts as the expected negative-control failure.
* Decision route: directly actionable planner correction. No divergent user
  decision or production test hook is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Select an executable browser-default-font configuration

* Related IDs: Q2, C2-C3, P02-T01; enlarged-font acceptance criteria.
* Evidence: phase details say to launch Chromium configured with
  defaultFontSize=32, but specify no API, preference, protocol call or supported
  command. The existing browser harness only calls chromium.launch and
  browser.new_context with a viewport; it has no font-configuration mechanism.
* Concern: defaultFontSize is a desired setting, not an executable Playwright
  Python recipe. It must not be silently implemented as an unsupported launch
  keyword/ineffective flag or replaced with author CSS. A computed root of
  32px alone cannot distinguish a real browser preference from CSS injection.
* Impact: implementation may block on browser setup or produce a CSS-only
  simulation while claiming the explicitly requested real-default regression.
* Smallest useful change: name a mechanism supported by the installed Chromium
  and Playwright, when it is applied before application layout, and its
  restoration or isolated-browser cleanup. For example, verify an appropriate
  Chromium font-size protocol setting rather than assuming a launch keyword.
  Require both an unstyled-document default-font probe and the real app's
  computed root at 32px, without author font overrides. Retain the selected
  summary, sidebar track, document/dialog/workspace overflow, map width >80px,
  close and exit checks, screenshots and pinned axe in this second helper.
* Action owner: planning parent; implementation owner verifies the selected
  mechanism against the existing local browser.
* Exact resolving evidence: phase details contain the exact supported
  configuration operation and pre-navigation timing. Browser evidence later
  records 32px on the unstyled probe and real root, a 640 CSS-pixel viewport,
  measured geometry and functional close/exit. A corrected-JS/original-CSS
  negative control fails the expected overflow or map-width assertion after
  successful font setup; corrected CSS passes. Existing normal-font cases
  remain unchanged and passing. An unsupported-setting exception is not a
  valid negative control.
* Decision route: directly actionable planner correction. The owner already
  selected a real browser default font; no alternative design decision is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Acknowledge the validation environment restriction

* Related IDs: P02-T02; shared environment, lock and evidence requirements.
* Evidence: plan names /tmp/mv and /tmp/ama-rpi-heavy.lock, and phase details
  permit editable installs into that shared venv. The current execution
  environment expressly prohibits /tmp file operations and requires newly
  created files to be project-relative. Details instead require a new external
  evidence directory. The plan reports no unresolved blockers.
* Concern: the current session cannot execute the proposed /tmp-based
  validation/installation and file-output instructions as written. The user's
  named venv and shared lock must not be silently replaced with a different
  environment or unrelated lock, nor may this restriction be ignored.
* Impact: an apparently ready plan has an execution blocker for mandatory
  validation, even before lock contention or missing dependencies is assessed.
* Smallest useful change: explicitly distinguish authorized validation from
  executable validation in this session. Record the /tmp-backed runs as blocked
  here, retain the exact user-required venv/lock for an execution context that
  permits them, and identify any permitted project-relative evidence location
  without representing it as the specified external run directory. Do not
  install, create alternate coordination, bypass admission, or report these
  suites as passing. Keep the existing busy-lock fallback separate from this
  filesystem-policy blocker.
* Action owner: planning parent for honest blocker/disposition recording;
  authorized execution context for the required runs.
* Exact resolving evidence: revised details and plan status identify the
  restriction and commands not executable here. Subsequent original evidence
  either records the required environment, explicit current-worktree
  source/test PYTHONPATH and package origins, nonblocking shared-lock admission,
  both packages' mypy/Ruff lint/Ruff format/unit exits and browser result in a
  compatible context, or preserves a Blocked/not-run validation outcome.
  No completion claim is inferred from targeted substitutes or local commits.
* Decision route: directly actionable blocker disclosure, not a divergent
  user decision. User confirmation alone does not override the execution
  restriction; no change to the requested validation contract is recommended.

## Strengths and Residual Risk

* The source solution follows the supplied correction exactly. Route abort,
  auth redesign, disposal flags and broad layout changes are correctly excluded.
* Existing source-contract methods and at most two browser helpers are credible
  bounded owners; the findings do not require new files or additional helpers.
* Separate original-JS and original-CSS controls can attribute each regression
  without reverting source files or contaminating existing test journeys.
* Retaining normal-font, mobile, keyboard, manual-list and Coordinator behavior
  is explicit. Automated axe/browser evidence is not WCAG or human acceptance.
* Full-suite contention is already an explicitly disclosed residual risk, not
  permission to claim unrun checks. No cloud, publication or remote-write step
  is needed for this correction.

## Questions or Blocking Evidence Gaps

* No unresolved divergent user choice. PC-001 and PC-002 need precise planner
  mechanisms, not more open-ended research.
* PC-003 blocks executing the named validation environment in this session,
  not this read-only critique or the credibility of the requested source fixes.

## Limitations

* No browser, static checker, unit suite, font-setting experiment, lock probe or
  negative control was executed. This is a plan critique, not implementation
  acceptance. Exact browser mechanism support remains to be demonstrated.
* Only supplied documents and their named source/evidence targets informed the
  substantive assessment. No whole-repository UI or security review is implied.
* Plan, details, research, source and existing evidence remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: specify the deterministic disposal protocol and its
  source-order contract, select the actual browser-font configuration, and
  record the execution-environment blocker before implementation handoff.
* Severity summary: 2 High, 1 Medium; 0 Critical, 0 Low.
* User response required: no.
* Return this complete finding set to the active parent for direct disposition
  and finalization. Do not request another plan critique.
