---
title: Regulatory UX optional browser dependency plan critique
description: Bounded final-candidate import-boundary assessment for Refs 215
ms.date: 2026-10-16
---

## Metadata

* Task ID: Refs #215; existing PR #354.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-ux-optional-browser-215-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/regulatory-ux-optional-browser-215-phase-details.md
* Critique execution status: Complete.

## Inputs and Criterion Boundary

* Reviewed the supplied plan, phase details and research, plus
  src/api/checks/regulatory_ux_check.py,
  src/api/tests/test_regulatory_ux_check.py, src/api/pyproject.toml and
  .github/workflows/src-ci.yml.
* Assessed only whether lazy Playwright imports preserve pure discovery,
  browser execution and type safety. No broader discovery, implementation,
  test execution, dependency installation, data/environment reads or delegation.
* Caller requirements retained: full API suites without and with Playwright
  in the requested /tmp/v215c environment, Ruff/mypy, real CI browser harness,
  main merge first (already committed per caller), related documentation,
  append-only log, and normal commit/push on the existing branch.
  This critique neither executes those steps nor independently verifies
  their completion.
* Existing untracked planning inputs were left unchanged. The only write is
  this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C4; P01-T01: pure discovery and axe rejection | Covered | Deferred annotations already exist; TYPE_CHECKING-only Page avoids runtime loading. Moving runtime imports after hash verification preserves the bad-axe test. |
| C4; P01-T01: runtime browser imports | Partial | Helpers are addressed, but run itself also calls expect extensively; see PC-001. |
| C3, C6; P02-T01: typing and dependency boundary | Covered | Keep real Page typing, dev-only Playwright, strict mypy covering checks, and no suppression or runtime dependency addition. |
| C5; P02-T01: actual browser coverage | Covered | src-ci.yml installs Chromium and runs both harnesses; the plan retains these and requires local execution with pinned axe and synthetic fixtures. |
| P01-T01, P02-T01: regression evidence | Covered | Fresh import-blocking subprocess plus complete API suites before/after dependency installation cover distinct import and execution boundaries without skipping pure tests. |
| P03-T01: delivery constraints | Covered within boundary | Documentation, append-only log and same-branch publication are retained; their content and completion are not assessed here. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* The approach is credible, but its runtime import instructions need one
  explicit correction before implementation. No architectural or user
  decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Explicitly import expect inside run as well as its helpers

* Related IDs: C4, C5, P01-T01, P02-T01.
* Evidence: The P01 details say to import expect within helpers and
  sync_playwright inside run. However,
  src/api/checks/regulatory_ux_check.py:197-362 contains many direct
  expect calls in run, beginning with the breach-risk assertion.
* Concern: The instructions do not explicitly cover the runner's own expect
  dependency. Local imports in open_home, keyboard_activate and keyboard_walk
  cannot bind expect in run. This is an ambiguity in the plan, not an observed
  implementation failure.
* Impact: Following the narrower reading removes the global binding and
  breaks real browser execution with NameError even though discovery and the
  three pure tests pass. Strict mypy should also detect the undefined name.
* Smallest useful change: In P01-T01, explicitly require
  `from playwright.sync_api import expect, sync_playwright` inside run,
  after axe verification and before fixture startup, alongside local expect
  imports in each helper that uses it. Keep Page under TYPE_CHECKING.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 names both runner imports and
  helper imports. Implementation evidence then records passing strict mypy
  and the actual regulatory Chromium harness, in addition to both full API
  unit environments and the import-blocking regression already required.
* Decision route: Direct planner correction; no significant or divergent
  user decision.

## Strengths and Residual Risk

* Existing postponed annotations make TYPE_CHECKING-only Page appropriate
  without weakening browser types or adding Playwright to runtime dependencies.
* Import failure remains explicit when browser execution is requested;
  no broad catch, skip, fallback or CI removal is proposed.
* The subprocess regression checks import isolation even in a developer
  environment containing Playwright. It does not replace real browser evidence.
* This is plan credibility assessment only, not proof of runtime success or
  accessibility conformance. Existing human acceptance exclusions remain intact.

## Questions or Blocking Evidence Gaps

* None requiring user input or additional research.

## Limitations

* No tests, Ruff, mypy or browsers were run. Main integration and PR lifecycle
  are accepted as caller context rather than independently audited.
* No production, legacy, data or environment files were examined or changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Clarify P01-T01's runner-local expect import, then
  finalize the plan without another critique and proceed through existing gates.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/regulatory-ux-optional-browser-215-plan.md](.copilot-tracking/plans/2026-10-16/regulatory-ux-optional-browser-215-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/regulatory-ux-optional-browser-215-phase-details.md](.copilot-tracking/details/2026-10-16/regulatory-ux-optional-browser-215-phase-details.md) | P01 correction target |
| [.copilot-tracking/research/2026-10-16/regulatory-ux-optional-browser-215-research.md](.copilot-tracking/research/2026-10-16/regulatory-ux-optional-browser-215-research.md) | Supplied bounded research |
| [.copilot-tracking/plans/2026-10-16/regulatory-ux-optional-browser-215-critique.md](.copilot-tracking/plans/2026-10-16/regulatory-ux-optional-browser-215-critique.md) | Complete finding set |

## Next Steps

Planning parent: resolve PC-001 directly and finalize without another critique.
No user action is required. This bounded critique stops here.
