<!-- markdownlint-disable-file -->

# Task Research: map-navigation-disposal-532

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md |

## Research Brief

Investigate the two supplied PR #539 findings (Refs #532): obsolete map controls
during pending All open cases navigation, and session-expiry browser iteration
isolation. Audience: implementer and independent reviewer. Output mode:
convergence, preparing the explicitly requested Plan/Implement/Review phases.
Success requires obsolete controls to be inert and disconnected before the
destination renders, a pending-facets regression, isolated session-expiry
iterations, and honest local validation evidence.

## Research Parameters

* Focused posture, selected by default for named targets and supplied failures.
* Internal candidates: app.js route/map lifecycle; map fullscreen browser check;
  component test commands; scenario manifest pins; previous correction evidence.
* External candidate: current Web Interface Guidelines, for changed web code only.
* Evidence root: .copilot-tracking/. Research writes only research and required
  lifecycle tracking. Source changes are prohibited until Implement.
* Limits: retain feat/map-fullscreen-532, rebase first, local commits only, no az,
  no push or force-push, no closing keywords. Heavy suites require nonblocking
  /tmp/ama-rpi-heavy.lock admission. No private datasets.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository copilot instructions, all files | Selected: src-only changes, evidence retention, branch/privacy/validation rules |
| Skill | rpi-research | Selected: focused wider/deeper/contrarian cycle |
| Skill | web-design-guidelines | Selected and source fetched 2026-10-29 for scoped web edits/review |
| Specialist | Independent plan critique and code Review | Defer to corresponding phase; inline research is one tightly coupled trace |
| Skill | Visual redesign/public-page design | Skipped: no redesign, styling or public-page work |

## User Participation and Research Decisions

The user explicitly requests all four phases and local-only closeout. No mode
switch or persistent automatic session is inferred. Manual mode with explicit
advance authorization for this bounded round; stop after local commits.
Initial git status was clean; branch matches the open PR; git pull --rebase
completed first and reported already up to date at 310889fa.

## Direction Controls

Preserve earlier artifacts and outcomes. Only correct the named lifecycle and
browser-isolation defects with directly related checks/pins. Do not publish.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How can disposed map controls reopen a body-mounted dialog? | Depth | Answered C1, C3 |
| Q2 | How can the regression hold navigation at the precise disposal boundary? | Depth | Answered C3, C4 |
| Q3 | How should each session-expiry iteration reset state without losing its authenticated server session? | Straightforward | Answered C2, C5 |
| Q4 | What local checks, pin changes and publication restrictions apply? | Straightforward | Answered C6, C7 |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index and owner memory. Previous
map-disposal-reflow-532 state records blocked browser verification and remains
historical, not acceptance for this round. Supplied review findings are hypotheses
to verify against current source.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial reads show mapPanel owns the slot, modal, toggle, route abort listener and
global disposer. The browser check already contains held-request instrumentation
and session-expiry/enlarged-font scenarios. Reflection: investigate lifecycle
ordering and runner setup rather than introduce new infrastructure.

#### Wave 2: Deeper

route() aborts the map route before awaiting listView(); listView() awaits
/api/facets before show() replaces Overview. dispose() clears its global
reference and abort listener without removing the slot. The toggle callback
can therefore append a dialog that no longer has a cleanup owner (C1, C3).
Intercept facets, retain the original toggle and its pointer coordinates,
navigate with the actual list link, and click before releasing facets (C4).
Reflection: test disconnected/inert/disabled controls, stale event dispatch,
absence of modal/scroll lock both while pending and after destination rendering.

The current goto changes only the hash. It cannot reset ovState or restore me
after a synthetic 401. Reload at the top of each iteration, then navigate to
Coordinator before installing fresh instrumentation. The cookie remains valid
because the 401 is intercepted, not a server logout (C2, C5).
Reflection: this preserves meaningful session initialization without bypassing
authentication in the application.

#### Wave 3: Contrarian

Removing only the dialog does not prevent reopening; removing only the slot
leaves retained callbacks callable; a route-signal check alone misses same-route
session expiry. Make the slot inert and toggle disabled at disposal, remove the
slot after collapse, and guard expand using the disposal/inert state. Preserve
collapse-before-sequence-invalidation because collapse can start resize draws;
the previous session-expiry assertions intentionally exercise that path.
Resetting only Overview filters would not fix null me or stacked wrappers.
Document reload is the narrow complete reset. Reflection: no wider cycle needed.

## Evidence Log

* C1: src/api/src/zava_forward/api/web/app.js:1566, dispose collapses the
  modal and destroys Leaflet but retains the connected slot/toggle.
* C2: src/api/checks/map_fullscreen_browser_check.py:88, iteration uses
  fragment-only goto rather than document reload.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-29, requires native controls, keyboard/focus safety and
  interruptible interactions. Repository semantics take precedence over style.
* C3: src/api/src/zava_forward/api/web/app.js:247,282,532,
  route abort precedes the facets await, which precedes screen replacement.
* C4: src/api/checks/map_fullscreen_browser_check.py:155,616,
  route interception already holds real requests; existing expanded list
  navigation covers the destination, but not input while facets is pending.
* C5: src/api/src/zava_forward/api/web/app.js:67,115,1414,1447,
  synthetic 401 sets me null; start() initializes me; hashchange requires me;
  ovState persists within the document.
* C6: src/api/pyproject.toml:56,71; src/core/pyproject.toml:28;
  src/api/README.md:139, mypy/ruff/unit/browser commands and shared heavy lock.
  /tmp/mv already resolves all three editable distributions to this worktree.
* C7: docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:48,
  four pinned files: workbench manifest/check, dataset.py and test_workbench.py.
  None is in this correction's edit set; no pin update necessary.

## Findings, Alternatives and Decision State

Accepted: disconnect/inert the obsolete slot, disable its toggle, guard stale
expand callbacks with the inert state, and reload before each session-expiry
iteration. Reuse existing real-app request interception with no production
exports or private fixtures. Rejected: signal-only guard, dialog-only cleanup,
filter-only reset, and broad route changes (incomplete or unnecessarily broad).

## Open Questions, Risks and Further Research

Heavy lock admission remains unknown until validation. Full browser execution
must reach both expiry modes and enlarged-font coverage, not just the new
navigation check. Local-only work is not publication, live deployment, human
assistive-technology acceptance or whole WCAG conformance.

## Planning Readiness

Ready. Research disposition: executed, complete. One ordered inline
wider/deeper/contrarian cycle completed; questions have direct evidence,
alternatives and residual risk. Parent advances to Plan under the explicit
full-loop user request. No additional discovery or delegation is justified.
