---
title: Map browser shortcuts correction plan critique
description: Independent final-candidate assessment for task 532
ms.date: 2026-10-29
---

## Metadata

* Task ID: 532-map-browser-shortcuts-2026-10-29.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/map-browser-shortcuts-532-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md.
* Critique execution status: Complete.
* Candidate baseline: f4a6bed44ff5891c4edd0455dabcff3ea39492bf.
* Branch: feat/map-fullscreen-532; PR 539 is open against main.
* Assessment: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: ignore Ctrl/Meta/Alt map key events without cancelling
  their defaults, retain Shift-generated plus, and extend the existing map
  browser check. Preserve the locked test ownership, removal prohibition,
  addition budget and source boundaries.
* Primary research:
  .copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md,
  including C1-C7, W1, Q1-Q3 and its disclosed environment substitution.
* Prior defect evidence:
  .copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md,
  particularly RV-001 and the separately owned publication/human-acceptance
  follow-ups.
* Source inspected: the map handler and marker integration in
  src/api/src/zava_forward/api/web/app.js; the complete existing
  src/api/checks/map_fullscreen_browser_check.py; relevant fixture/server
  setup in src/api/checks/design_system_browser_check.py; existing contracts
  in src/api/tests/test_map_fullscreen.py; the map documentation in
  src/api/README.md; and source pins in
  docs/reference/research/retrofit-synthetic-data/scenario-manifest.json.
* Decisions and dependencies assessed: FR1-FR3, NF1-NF2, AC1-AC5, both phases,
  all four tasks, the bounded test-change budget, validation fallback, local
  commit attribution and preservation of original adverse evidence.
* Validation boundary: API units, map browser and pinned axe are implementation
  obligations, subject to the supplied nonblocking heavy-lock policy. The
  disclosed existing substitute venv is not independently validated here.
  No push, az, force push, publication gate or human acceptance is authorized.
* This critique evaluates plan credibility, not implementation acceptance.
  No source/plan/research edits, test executions or delegation were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; C1, C4; RV-001 | Covered | The custom handler currently consumes modified recognized keys; an early modifier return directly addresses the defect, including bubbling marker events. |
| FR2-FR3; AC3 | Covered | Existing consumed-event/control exclusions and the real 80px pan check are retained; trusted Shift plus, equals and minus receive exact zoom-delta assertions. |
| AC1-AC2; Q2 | Covered | Cancelable synthetic events on focused map/marker targets in both modes test cancellation and state/request invariance without invoking native history navigation. |
| NF1-NF2; C5 | Covered | Constructed loopback data, current-worktree source selection and explicit limits on automated accessibility evidence preserve the authorized boundary. |
| Test ownership and change budget | Covered | One existing check owns the matrix; no removals, new test files, helper modules or fixture changes are planned. |
| P01-T01; P02-T01 | Partial | PC-001: the declared dependency puts the requested pre-fix regression run after the source correction. |
| P01-T02; C3 | Covered | Only the directly related map README section changes; browser/map key ownership and check coverage are documented. |
| AC4; P02-T01; Q3 | Covered | Full API/browser checks require the nonblocking heavy lock; contention permits targeted units only with explicit unperformed-check disclosure. Axe violations and incompletes must be inspected. |
| AC5; P02-T02; C7 | Covered | One subsequent independent Review, original adverse evidence, dated local commits and the no-publication boundary are retained. |
| C6 | Covered | None of the three intended edited files is among the manifest's four pinned source paths; no pin change is warranted. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: the proposed behavior and bounded coverage are credible, but the
  task dependency must make the explicitly required pre-fix failure executable
  before the guard is installed. This is a direct planning correction, not a
  product decision or a request for broader testing.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Order the regression proof before the source correction

* Related IDs: P01-T01, P02-T01, AC4.
* Evidence:
  .copilot-tracking/plans/2026-10-29/map-browser-shortcuts-532-plan.md assigns
  both the production guard and browser assertions to P01-T01.
  .copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md
  makes P02-T01 depend on P01, then instructs it to run the extended browser
  check before the source fix. Current
  src/api/src/zava_forward/api/web/app.js:1592-1603 still contains the original
  defective handler, while
  src/api/checks/map_fullscreen_browser_check.py currently has no modifier
  cancellation assertions.
* Concern: following the declared task dependency completes the guard before
  reaching the task that owns the required pre-fix run. The plan does not
  identify a test-only checkpoint or another bounded way to obtain that
  evidence without reversing an already applied correction.
* Impact: implementation can produce passing post-fix checks while missing
  the requested demonstration that the new regression assertions detect the
  original shortcut interception. Ad hoc source rollback to recover that
  evidence creates unnecessary execution risk.
* Smallest useful change: explicitly order P01-T01 as existing-check extension,
  lock-protected pre-fix run, production guard, then post-fix validation.
  Move ownership of the red checkpoint into P01-T01 and leave the remaining
  API/browser/axe validation in P02-T01, preserving the existing test owner,
  helper/call-site budget and no-removal boundary. Carry forward the authorized
  lock-busy fallback rather than running any unlocked full check.
* Action owner: planning parent.
* Exact resolving evidence: the plan and phase details agree that the extended
  check runs against the unchanged defective handler before the guard is
  installed; the implementation changes record subsequently identifies the
  pre-fix modifier-assertion failure and post-fix results with distinct output
  locations, or explicitly records lock contention and the unperformed proof.
  An unrelated harness failure must not be recorded as the regression proof.
* Decision route: direct planner correction. The caller already requires the
  pre-fix proof and specifies the contention policy; no significant or
  divergent user decision is needed.

## Strengths and Residual Risk

* The proposed modifier guard is narrower than suppressing all modified keys:
  Shift plus remains functional, and neither preventDefault nor propagation
  suppression is proposed for protected browser shortcuts.
* The cancellation matrix, map-pane invariance and request-count assertions
  complement the trusted ordinary-key checks without a new test framework.
* Synthetic dispatch proves event cancellation and application behavior, not
  actual operating-system/browser chrome zoom or history behavior. The research
  explicitly acknowledges that limit.
* Human assistive-technology and staff acceptance remain with their existing
  owners. Axe incompletes are inspection evidence, not automatically a pass or
  a newly authorized human-acceptance claim.
* The absent requested venv and substitute environment are disclosed. Lock
  contention can leave browser/axe validation unperformed; that must remain a
  visible limitation rather than be represented as passing validation.
* Publication, hosted approval and full exact-head gate remain outside this
  no-push/no-az correction.

## Questions or Blocking Evidence Gaps

* None requiring a user response. PC-001 is resolved by ordering already
  authorized work, not by expanding scope.

## Limitations

* No unit tests, browser checks, axe runs or environment/tool probes were run.
* The supplied research's external guideline retrieval is attributed evidence;
  this plan-only critique does not claim a fresh UI guideline or accessibility
  conformance review.
* Baseline, worktree status and open PR lifecycle were checked read-only.
  Existing untracked planning/research/state artifacts were not modified.
* This is the complete actionable finding set for the supplied candidate and
  assessment boundary. No second critique is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile the red-before-guard ordering in the plan
  and phase details, then finalize planning and continue within the authorized
  implementation boundary.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/map-browser-shortcuts-532-plan.md](.copilot-tracking/plans/2026-10-29/map-browser-shortcuts-532-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md](.copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md) | Assessed task dependencies and validation sequence |
| [.copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md](.copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md) | Primary supplied research |
| [.copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md](.copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md) | Preserved original adverse Review |

## Next Steps

The active planning parent should apply the direct PC-001 sequencing correction,
preserve this Complete / Revise critique unchanged, and finalize without another
critique. No user action is required. This reviewer stops after this assessment.
