---
title: "RPI Plan Critique: Compact case view"
description: Independent final-candidate assessment for issue 552
ms.date: 2026-10-29
---

## Metadata

* Task ID: 552
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: existing presentation/web icons; six compact labelled steps; one-line blocker summary with complete keyboard/touch disclosure; attached tabs outside inner scrolling; Fluent 2, WCAG and content preservation; desktop and narrow browser evidence.
* Research: .copilot-tracking/research/2026-10-29/case-view-ux-552-research.md, including Q1-Q4 and C1-C6/W1.
* Implementation evidence inspected to resolve concrete doubts: src/api/src/zava_forward/api/web/case-workspace.js; src/api/src/zava_forward/api/web/app.js, caseView and its enhancement fallback; src/api/src/zava_forward/api/web/style.css, case layout rules; src/api/tests/test_case_journey.py; src/api/checks/design_system_browser_check.py; PNG MIME support in src/api/src/zava_forward/api/server.py.
* Applicable context: both case studies, knowledge-base index and owner memory, sector primer, and docs/reference/research/ux/design-system.md, wcag-conformance-baseline.md and content-standard.md.
* Assessed decisions and dependencies: exact slide-four PNG reuse, native auto popovers, mounted manually activated tabs, isolated constructed-data loopback harness, current-worktree source selection for the installed interpreter, P01-T01 through P02-T02, and acceptance criteria 1-6.
* Locked boundary: production edits confined to the named web source files/assets; existing journey test ownership; one new browser check; at most three new unittest methods plus the existing blocker expectation update; six PNG additions; directly related README and dated RPI evidence. No removals or additional test/framework/dependency proposals.
* This assessment evaluates planning credibility, not implemented behaviour or completion of issue acceptance. No application, unittest, Node or browser checks were run. No Azure, az, push, rubric edits or further agents were used. Only this critique is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Icons; AC1; Q1/C4; P01-T01 | Covered | Six explicit deck media mappings, byte provenance, decorative alternatives, dimensions and rendered image loading. PNG serving is already supported. |
| Compact labelled steps; AC2; C1/C2; P01-T01/T02 | Covered | Same-fixture baseline comparison, measurable height ceilings, full step labels and non-colour state words. |
| Complete blocker disclosure; AC3; Q2/W1; P01-T02/P02-T01 | Partial | Native buttons, safe rendering, unique targets, keyboard/touch dismissal and complete content are specified; long-content reachability is not an explicit assertion. PC-001. |
| Attached tabs; AC4; Q3/C5; P01-T02 | Covered | Wrapping tabs precede bounded panels; manual activation, URL/back, mounted panels and retained inputs are preserved. Stationary-tab scrolling is measured. |
| Listed fallback sections; functional requirements; P01-T02/P02-T01 | Partial | Unbounded fallback is promised but enhancement-disabled/failure browser evidence is absent. PC-002. |
| Fluent/WCAG/content; AC5; C3; P02-T01/T02 | Covered with findings | Focus, target sizes, reduced motion, native semantics, existing regression modules and fresh guidelines review are planned. PC-001/002 address changed-surface reachability; full conformance is explicitly not claimed. |
| Desktop/narrow evidence; AC6; P02-T01 | Covered | 1280/390/320 CSS px, JSON, screenshots, no overflow and JavaScript-error checks. |
| Isolation and validation dependencies; Q4/C5/C6 | Covered | Existing harness constructs data, selects local source roots, sanitizes server environment and owns process cleanup. Candidate additionally requires external-traffic blocking. |
| Scope, ownership, budget and governance | Covered | Source-only UI change; no backend authority, safety, consent, framework or dependency change. Both findings fit the already allocated browser file. |
| Independent Review and local commit; P02-T02 | Covered | Preserve original critique/Review, privacy-safe identity and trailer, no push; full publication and human/live gates remain explicitly unperformed. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 2; Low 0.
* Rationale: The implementation direction is credible and respects confirmed owner choices. Two bounded verification omissions could allow inaccessible hidden content or a broken manual fallback to pass the stated checks. These are direct planning corrections, not reasons to reopen icon, framework, popover or tab decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Prove full long-popover content is reachable, not merely present

* Related IDs: AC3, AC5, Q2, P01-T02, P02-T01.
* Evidence: The phase details require full every-blocker reason/owner/action and a long/multiple-blocker fixture. P02-T01 lists full-details assertions, keyboard activation, dismissal and page overflow, but does not require the last content item to be reachable within the open popover. The plan constrains collapsed step heights, not disclosure geometry. The supplied WCAG baseline includes text resize and reflow; the content standard requires reason, owner and next action together.
* Concern: Text-content assertions and document-width checks can pass while a top-layer disclosure clips a later blocker or its next action. Native popover activation/dismissal alone does not establish suitable wrapping and overflow handling for lengthy content on a narrow or short viewport.
* Impact: The compact summary could conceal the only complete explanation from keyboard or touch users even though the planned presence checks pass. This is a validation gap, not an observed implementation defect.
* Smallest useful change: Specify viewport-constrained wrapping and a reachable scrolling path when needed. Extend the single allocated browser check to open a multi-blocker disclosure at 320px and a short viewport, verify access to the final reason/owner/action using keyboard and touch, and repeat affected content checks with enlarged text. Keep collapsed height ceilings at the declared default text size; enlarged text must remain readable rather than satisfy a fixed-height clipping rule. Include explicit missing-owner/action fallbacks from the research.
* Action owner: Planning parent, then implementer under P01-T02/P02-T01.
* Exact resolving evidence: Revised details name these assertions and fixture cases. The existing planned browser JSON records viewport/text scale, actual disclosure overflow/reachability, final-blocker visibility after scrolling, and keyboard/touch results; linked screenshots show the open disclosure. No extra file or unittest method is required.
* Decision route: Direct planner correction. The owner already requires complete keyboard/touch disclosure and preserved accessibility; no significant or divergent owner decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Exercise the fallback after relocating tabs and bounding panels

* Related IDs: Functional requirement for usable listed fallback sections, AC4, AC5, P01-T02, P02-T01.
* Evidence: P01-T02 explicitly promises that unenhanced listed panels stay unbounded. P02-T01 only enumerates enhanced tab/scroll checks. In src/api/src/zava_forward/api/web/app.js, caseView constructs all panels before enhancement, catches enhancement errors, unhides panels and removes tab-related attributes. The candidate relocates the tablist into that workspace and introduces bounded scrolling, adding layout state beyond the existing fallback cleanup.
* Concern: Normal-path tests cannot prove that new enhancement-specific classes, scroll bounds or inserted tab controls are absent or cleaned up when enhancement is unavailable or fails. The existing catch restores specific attributes, not arbitrary future layout state.
* Impact: A regression in the explicitly preserved manual path could leave listed sections constrained, hidden or paired with unusable tab controls while every enhanced-path assertion passes. This is a missing negative-path check, not a claim that the current fallback is broken.
* Smallest useful change: Require enhancement-only scrolling/layout state and successful fallback cleanup. Add two scenarios inside the already allocated browser check: make the workspace script unavailable, and inject a controlled enhancement exception after layout mutation. Use the real app and constructed data, not a replacement page. Assert all expected sections are visible/listed, panels have no imposed inner-scroll bound, tab UI is absent or operable, persistent safety remains reachable, and representative ordinary controls remain usable.
* Action owner: Planning parent, then implementer under P01-T02/P02-T01.
* Exact resolving evidence: Revised phase details explicitly include both failure scenarios. The planned browser JSON records panel visibility/computed scrolling constraints and manual-control checks for each scenario, plus expected fallback messaging. Record the deliberately injected exception separately from unexpected JavaScript errors so the existing no-error assertion is not silently weakened.
* Decision route: Direct planner correction within the locked source/test budget. No significant or divergent owner decision.

## Strengths and Residual Risk

* Exact existing presentation assets avoid icon invention and runtime dependencies.
* Status-rule preservation, safe text construction, disclosure controls outside links, explicit owner/action content and persistent safety are appropriately retained.
* Tests execute shipped JavaScript; real-browser geometry is not replaced with source-string assertions.
* The plan distinguishes native Fluent foundations from completed library adoption and local engineering evidence from WCAG, assistive-technology, user or live acceptance.
* Chromium-only popover compatibility and wider cross-browser/AT acceptance remain explicitly recorded residual limitations. This critique does not expand the task into those wider acceptance exercises.
* Publication remains outside this local-only task. A later publication would require the repository's complete, current gate; this verdict does not waive it.

## Questions or Blocking Evidence Gaps

* No significant owner decision or decision-critical research gap. Both findings can be resolved directly without altering locked ownership or additions.

## Limitations

* This is a source-grounded plan assessment, not fresh rendered UI review. The guideline retrieval and PPTX mapping are supplied research evidence, not independently re-fetched/re-extracted here.
* No private datasets, operational services or full publication prerequisites were inspected.
* Existing untracked planning/research/state artifacts were left untouched. Implementation checks and success evidence remain pending.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the disclosure-reachability and fallback scenarios to the existing tasks, record direct dispositions for PC-001/PC-002, then finalize for implementation.
* User response required: No.
* Preserve this original outcome; do not schedule another plan critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md](.copilot-tracking/plans/2026-10-29/case-view-ux-552-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md](.copilot-tracking/details/2026-10-29/case-view-ux-552-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-29/case-view-ux-552-research.md](.copilot-tracking/research/2026-10-29/case-view-ux-552-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/case-view-ux-552-plan-critique.md) | Complete original critique |

## Next Steps

The active planning parent should directly disposition both findings, revise the
existing tasks within their locked budget, and finalize without another critique.
No user action is required.
