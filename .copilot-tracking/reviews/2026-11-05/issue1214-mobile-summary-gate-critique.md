<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 1214 320px case-summary gate recovery

## Metadata

* Task ID: issue1214-mobile-summary-gate
* Critique date: 2026-11-05
* Plan: .copilot-tracking/plans/2026-11-05/issue1214-mobile-summary-gate-plan.md
* Phase details: .copilot-tracking/details/2026-11-05/issue1214-mobile-summary-gate-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: smallest nav row-gap fix at max-width 600px; unchanged 1600 bound; no hiding, clipping or reordering; no viewport-threshold change; FOCUSED tier.
* Research and evidence considered: .copilot-tracking/research/2026-11-05/issue1214-mobile-summary-gate-research.md; .copilot-tracking/github-issues/issue-1214.md; src/api/src/zava_forward/api/web/style.css (lines 9, 21, 43, 51, 82, 279, 310-317); src/api/checks/case_journey_browser_check.py (1514-1527); src/api/src/zava_forward/api/static_assets.py; src/api/src/zava_forward/api/web/index.html, law.html.
* Decisions, dependencies, and acceptance criteria considered: plan AC1-AC4, FR1-FR2, NFR1-NFR2, P01/P02 tasks, issue criteria 1-5.
* Assessment boundary: static source verification only. No browser was run; geometry figures (527px header, 1676.41 bottom) are taken from the research dump and not re-measured.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|---|---|---|
| C3 nav gap cause | Covered | `style.css:43` `nav{display:flex;gap:1rem}` is the only rule setting nav gap; `:51`, `:82`, `:279` set wrap/order/basis/min-width only, no gap or row-gap. Link height 2.5rem+0 (`:310`) matches 42px claim. |
| Specificity | Covered | `.top nav` (0,1,1) beats `nav` (0,0,1); `#nav a` rules target links not the container. Row-gap-only leaves column gap 1rem (longhand wins over shorthand `gap` by specificity regardless of order). |
| Cascade order | Covered with a wording gap (PC-001) | No later rule overrides; the line 279 rule is `.top nav{flex-wrap:wrap;min-width:0}` with no gap. Placement "near line 310" is after it. Even a rule placed earlier would win on specificity. |
| Arithmetic | Covered | 7 rows give 6 row gaps; (16px - 2px) x 6 = 84px; 1676.41 - 84 = 1592.41, margin 7.59px under the unchanged 1600. Wrapping is unchanged because the column gap is untouched, so the 7-row count holds. |
| Asset cache/versioning | Covered by source, plan task is conditional (PC-004) | `static_assets.py` derives `version` from a SHA-256 of all asset bytes and rewrites HTML `href`/`src` to `?v=`; html is `no-store`. A CSS edit auto-invalidates; no manual bump exists or is needed. |
| 390/1280 | Partial (PC-002, PC-003) | 1280 is outside `max-width:600px` and `.top nav` rules at 1100; unchanged by construction. 390 is affected and has only reflow assertions. |
| Constraints (bound, no hide/clip/reorder, no threshold) | Covered | One CSS declaration at the existing 600px breakpoint (`style.css:115,183,221,317`). |
| AC1-AC4 | Partial | See PC-002, PC-003, PC-005. |

## Verdict

* Verdict: Revise
* Rationale: the technical core is sound and verified against source, but the plan misses the focus-ring interaction a 2px row gap creates at every width up to 600px, leaves 390 evidence to a hook with no pass criterion, and carries a few ambiguities a planner can fix directly. None requires a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: Placement and form of the rule is underspecified

* Related IDs: P01-T01, C6, C7
* Evidence: style.css:43, 51, 82, 279, 310, 317 (existing `@media(max-width:600px)` block at line 317 holds `.card`, `.row`, `.blocked`, `.brand`).
* Concern: details say "adjacent to `#nav a`, near line 310" with a new `@media` block, but do not state that only the `row-gap` longhand is used (a `gap:` shorthand would also change the column gap and could alter wrapping) or that it must follow line 43. The existing line 317 block already is the shell mobile block.
* Impact: a shorthand or a rule before line 43 with equal specificity would silently fail or change wrapping and the 7-row count the 84px saving depends on.
* Smallest useful change: state "append `.top nav{row-gap:.125rem}` to the existing line 317 `max-width:600px` block (or immediately after line 311), `row-gap` only"; note it relies on specificity, not order.
* Action owner: planning parent
* Exact resolving evidence: details P01-T01 names the placement and longhand; changes record shows a single-declaration diff.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Focus-ring overlap between wrapped nav rows is not assessed

* Related IDs: P01-T02, NFR2, issue criterion 3 (keyboard paths)
* Evidence: style.css:21 (`--focus-w:3px`, `--focus-off:2px`), style.css:47 area `:focus-visible{outline:var(--focus-w) solid ...;outline-offset:var(--focus-off);box-shadow:0 0 0 var(--focus-off) ...}`; research C8 says only "focus outline behaviour unchanged".
* Concern: the ring extends about 5px (outline plus offset, plus a 2px shadow) beyond the link box. With a 16px row gap it never touched the adjacent row; with 2px the ring of a focused link overlaps the neighbouring rows' boxes. Link text has 8px padding so text is unlikely to be covered, but the plan asserts unchanged behaviour without evidence, and the existing check has no focused-nav assertion.
* Impact: possible degraded focus visibility, which the issue requires to be preserved (keyboard paths). A 4px gap would avoid some overlap but, per C6, fails the bound, so the fix may need to accept it, but it must be shown acceptable.
* Smallest useful change: in P02-T01 capture a 320 and 390 screenshot with the first, middle and last nav link focused (external, via the same hook) and record that the ring stays fully visible and no text is obscured; if not acceptable, return to the planner rather than widen the gap silently.
* Action owner: planning parent (plan edit), implementer (evidence)
* Exact resolving evidence: recorded screenshots or computed-rect overlap notes in the changes record, and reworded C8 claim.
* Decision route: direct planner correction (a user decision only if the evidence shows the ring is obscured)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: 390 and 1280 evidence has no pass criterion, and the affected range is wider than 390

* Related IDs: AC2, FR2, P02-T01
* Evidence: case_journey_browser_check.py:1514-1527 (reflow asserts at 320/390/1280, bound only at 320); style.css:317 (rule applies to every width <= 600px).
* Concern: AC2 only records geometry. The rule affects all widths 321-600px, not just 390; 1280 is unaffected by construction (the 600px media query does not match, and the 1100px nav rules are untouched), so measuring 1280 is a no-op while 390 has no acceptance threshold. Also the geometry hook is an external extension; the plan does not say it is not committed.
* Impact: "preserve existing 390px behaviour" (issue criterion 3) could be claimed with only a size delta and no judgement.
* Smallest useful change: define pass as: 1280 nav height and summary bottom equal baseline exactly; 390 nav rows and column positions unchanged (same wrapping), only row pitch 58px to 44px, link height 42px, scrollWidth <= innerWidth, existing 390 reflow checks pass; state the hook output stays external and uncommitted.
* Action owner: planning parent
* Exact resolving evidence: AC2 text with those predicates; before/after table in the changes record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Asset-cache task can be closed from source

* Related IDs: details "Cache impact", AC3
* Evidence: src/api/src/zava_forward/api/static_assets.py (content SHA-256 `version`, HTML `?v=` rewrite, html `no-store`, immutable only for matching `v`).
* Concern: the plan leaves "if a manual version bump is required" open, though assets are content-versioned automatically; there is no version constant to bump. Only residual: `asset_cache_browser_check.py` primes a legacy `/style.css`, which a content change does not affect.
* Impact: avoids an implementer adding a spurious bump; low risk.
* Smallest useful change: record "no manual version change; hash changes automatically" and keep `test_static_assets` in AC3 as the evidence.
* Action owner: planning parent
* Exact resolving evidence: details cache line replaced with the conclusion; `test_static_assets` exit 0 recorded.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Thin margin and gate scope are not guarded in acceptance

* Related IDs: AC1, AC3, plan Executive Summary residual risk
* Evidence: arithmetic above gives 1592.41 against 1600 (7.59px); the check at line 1526 is the only bound; issue criterion 5 and plan AC4.
* Concern: success is a computed estimate; the plan does not say what happens if the measured bottom lands in, say, 1595-1600 or if wrapping differs under the pinned Chromium, nor that the fallback (account row packing, about 58px, listed only as a follow-up) would be a scope expansion needing the stop-and-report rule. Also the plan labels "Status: ready after one critique" while criterion 5 forbids `Closes #1214` without hosted/independent evidence; AC4 covers this but the PR keyword rule is not stated.
* Impact: an implementer could be tempted to tweak the gap, padding or bound ad hoc.
* Smallest useful change: add to P02-T01 "if measured bottom > 1600, stop and report; do not alter bound, thresholds or hide content; reassess tier"; state PR uses `Refs #1214` until independent review and hosted checks exist.
* Action owner: planning parent
* Exact resolving evidence: plan contains the stop condition and the Refs wording; measured bottom recorded (expected about 1592.4).
* Decision route: direct planner correction

## Strengths and Residual Risk

* Root cause, specificity, cascade order, 84px arithmetic, unchanged column gap and wrapping, constraint compliance and automatic asset versioning all check out against source.
* Existing check is correctly kept as the regression owner; no trivial CSS-constant test is proposed.
* Residual (accepted by plan): 7.59px margin deterministic only in the pinned Chromium; slightly tighter nav rhythm for widths up to 600px.

## Questions or Blocking Evidence Gaps

* None blocking. The 527px/1676.41 baseline was not re-measured here.

## Limitations

* No browser run; line-numbered claims were verified on the checkout at c6d5a8f3 only. Task did not review the plan's tooling/lock details.

## Recommended Next Action

* Highest-impact finding: PC-002
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-005 as direct edits to the plan and details, then finalize without another critique.
* User response required: no

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-05/issue1214-mobile-summary-gate-plan.md](.copilot-tracking/plans/2026-11-05/issue1214-mobile-summary-gate-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-11-05/issue1214-mobile-summary-gate-phase-details.md](.copilot-tracking/details/2026-11-05/issue1214-mobile-summary-gate-phase-details.md) | Phase details critiqued |
| [.copilot-tracking/research/2026-11-05/issue1214-mobile-summary-gate-research.md](.copilot-tracking/research/2026-11-05/issue1214-mobile-summary-gate-research.md) | Research evidence |

## Next Steps

* Return the verdict to the planning parent; it revises directly. No user action is required and no compaction is advised.
