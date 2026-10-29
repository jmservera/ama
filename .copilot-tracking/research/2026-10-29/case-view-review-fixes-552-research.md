<!-- markdownlint-disable-file -->
---
title: Case view review fixes 552 research
description: Focused evidence for PR 554 summary assertion and packaged journey icons
ms.date: 2026-10-29
---

## Research Brief

* Topic: two Copilot findings on PR #554 / issue #552.
* Purpose and audience: prepare a precise maintainer correction with local evidence.
* Scope: top-level summary term selector, six journey PNGs in the API wheel,
  directly related validation and documentation. No redesign or unrelated fixes.
* Criteria: six top-level terms with unconfirmed funding; all six PNG assets in
  a built wheel; focused API tests, ruff, JavaScript syntax and local browser checks.
* Output mode: convergence, preparing planning.
* Evidence root: `.copilot-tracking/research/2026-10-29/`.

## Research Parameters

* Posture: focused, selected from the named targets and supplied failure evidence.
* Initial questions: does the disclosure explain the selector mismatch, does
  wheel packaging omit the icons, and which local checks exercise both?
* Internal candidates: API browser checks, summary renderer, package manifest,
  Dockerfile, journey tests and existing component instructions.
* External candidates: none required for this bounded internal correction.
* Prior knowledge: user findings are claims to verify against current source.

## Direction Controls

* First absorb rubric bot commit using `git pull --rebase`: completed as clean
  fast-forward to `4220e7aa1c3557997f7149e997834c7b8b2657f9`.
* Preserve branch `feat/case-view-ux-552` and open PR #554.
* Use `/tmp/mv` and supplied source/test PYTHONPATH; no push, az or manual rubric edits.
* User explicitly advances the bounded task through all four phases; retain
  manual mode rather than inventing consent for an ongoing automatic session.

## Extension Registry and Provenance

* Selected: repository guidance and RPI phase skills; their scope is process,
  evidence, local validation and source safety.
* No UI source edits are proposed, so design/restyling skills are not applicable.
* Specialist delegation skipped for research: both findings form one short
  code/package trace; inspect inline. Independent critique and Review remain required.

## User Participation and Research Decisions

The brief is sufficient and interaction is unavailable. Follow explicit user
directions without widening scope.

## Research Cycle Log

Cycle 1, all inline:

1. Wider: inspected API renderer, browser assertion, package manifest,
   Dockerfile and component README. Both named failures fit existing boundaries.
   Reflection: source-tree assets alone cannot validate a wheel-installed container.
2. Deeper: confirmed the outer summary has six `dl > div > dt` children, while
   each blocker contributes three nested `dt` nodes. Ran the actual pre-fix
   browser check: failed exactly at "all six summary values" after login and
   summary geometry passed. Built a pre-fix API wheel: zero journey icons.
   Reflection: both supplied findings are reproduced, not merely plausible.
3. Contrarian: searched other browser selectors and package inclusion paths.
   No other `.case-summary dt` occurrence needs correction. Existing `web/*`
   and vendor globs do not recursively include journey icons (confirmed by the
   built wheel); static serving already resolves nested files below WEB.
   Reject changing markup or Dockerfile: those would obscure the actual cause.
   Reflection: no material counter-evidence; retain both minimal fixes.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `src/api/src/zava_forward/api/web/case-workspace.js:64-80,102-112` | Six summary terms plus nested blocker definition lists. |
| C2 | `src/api/checks/case_journey_browser_check.py:581` | Descendant selector incorrectly counts blocker details. Actual baseline run failed here. |
| C3 | `src/api/pyproject.toml:75-78` | Package data lacks the nested PNG glob. Baseline wheel has zero icons. |
| C4 | `src/api/Dockerfile:14,29` | Container builds then installs wheels, not a source-tree web mount. |
| C5 | `src/api/src/zava_forward/api/server.py:38,240-241` | Static path supports nested existing files within WEB. |
| C6 | `src/api/tests/test_case_journey.py:1266-1278` | Six source icons already checked against exact deck bytes; not a wheel check. |
| C7 | `src/api/checks/design_system_browser_check.py:228-287` | Browser harness owns loopback server and synthetic data; isolates environment and cleans processes. |
| C8 | `.copilot-tracking/rpi-sessions/2026-10-29/case-view-ux-552-state.json` | Prior task completed with original Partial/Residual work Review; preserve it unchanged. |

Baseline commands (repository root unless stated):

```bash
/tmp/mv/bin/python -m pip wheel --no-deps \
  --wheel-dir /tmp/case-552-review-fixes-20261029-wheel-before ./src/api --quiet
cd src/api
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  /tmp/mv/bin/python -m checks.case_journey_browser_check \
  --axe /tmp/ama-526-evidence/axe-4.10.3.min.js \
  --out /tmp/case-552-review-fixes-20261029-browser-before
```

Wheel build exit 0; ZIP inspection found no journey-icons members. Browser exit
1 at C2. Existing local axe bytes pass the check's pinned hash verification.

## Findings Mapped to Questions and Evidence

Both supplied hypotheses accepted as evidence-backed findings C1-C4. Use the
caller-specified selector and package-data glob. C5 rules out a static route
change; C6 preserves source provenance coverage. C7 establishes safe browser
execution; no real data, model or Azure calls are needed.

## Alternatives and Decision State

Selected direct-child selector and explicit nested PNG glob. Reject excluding
popover terms through a broader filter or removing their semantics; exact
structural selection is clearer. Reject Docker COPY/runtime overlays, because
the distribution must contain its own assets. Add a lightweight manifest
regression beside the existing source provenance test, plus inspect actual wheel
members and bytes during validation. No new test framework is needed.

## Open Questions, Risks, and Residual Uncertainty

Playwright, Chromium, pip wheel and pinned local axe are available. Pip builds
with isolated backend requirements; no environment package install is required.
Deployed-container behavior, hosted/publication gates and inherited RV-001 are
not accepted by these focused local checks.

## Planning Readiness

Ready. Research disposition: executed, complete. One three-wave cycle covers
both questions with reproduced failures; another cycle would be redundant.
No research blocker. Self-check: scope, source IDs, alternatives, constraints,
participation, findings and readiness recorded. Parent may advance to Plan
under the user's explicit full-loop direction.
