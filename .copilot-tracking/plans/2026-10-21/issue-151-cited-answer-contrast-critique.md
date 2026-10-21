<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-151-cited-answer-contrast

## Metadata

* Task ID: issue-151-cited-answer-contrast
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: reproduce and fix the hosted cited-answer axe color-contrast failure at root cause; no axe, rule, coverage or transitional-state masking; preserve Fluent 2, native semantics, keyboard, focus, reduced motion; a focused regression that fails without the fix plus the existing regulatory browser check; no conformance claim; src only; exactly four requirements files from a3257c71 and nothing else; no push, PR or merge.
* Research and evidence considered: .copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md, checked against src/api/src/zava_forward/api/web/style.css (lines 21, 23, 33, 34, 191, 192), src/api/src/zava_forward/api/web/chat.js (lines 47, 58, 212, 227, 237), src/api/checks/regulatory_ux_check.py (scan at 62, cited-answer scan at 309), src/api/tests/test_regulatory_ux_check.py, .github/workflows/src-ci.yml (lines 92 to 104) and git object a3257c71.
* Decisions, dependencies, and acceptance criteria considered: plan FR-1, FR-2, NFR-1 to NFR-3, AC-1 to AC-4, P01 to P03 ordering.
* Assessment boundary: static review of the supplied artifacts and code. No browser run, so the 26 percent blend arithmetic and the reproduction (C7, uncommitted probe) are taken from research, not re-observed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Root cause (C1 to C3, C7) | Covered | style.css:191 transitions background-color only; style.css:192 sets the disabled colour and text. The blend arithmetic is internally consistent. |
| Axe unchanged (NFR-1, FR-2) | Covered | scan() unchanged; new state reuses it. |
| P01-T01 unit regression | Partial | Narrow regex guard (PC-002). |
| P01-T02 mid-fade browser state | Partial | Vacuous once fixed; fractions and side effects unspecified (PC-001, PC-003). |
| P02-T01 CSS edit | Covered | Single rule split; tokens and reduced motion untouched. |
| P03-T01 four requirements files | Covered | a3257c71 exists locally, is not an ancestor of HEAD, and its diff touches only the four requirements files under src plus tracking files; checkout by path is safe. |
| P03-T02 README and validation | Partial | Validation commands not pinned to CI (PC-005); gate status unstated (PC-006). |
| Research follow-up on .alt hover | Concern | Claim contradicts the cascade (PC-004). |
| Same-mechanism siblings | Partial | Only the submit button is scanned (PC-003). |

## Verdict

* Verdict: Revise
* Rationale: The root cause and CSS fix are credible and directly evidenced. The regression design is weaker than claimed: the browser state proves nothing after the fix, the unit guard is easy to bypass, and one research claim is contradicted by the stylesheet. All findings are planner-owned corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Mid-fade browser state is vacuous after the fix and 20 percent may not fail before it

* Related IDs: FR-2, AC-1, AC-2, P01-T02
* Evidence: regulatory_ux_check.py:309; style.css:191; research C7 (reproduced only at 35 percent progress, with easing: #6497a0).
* Concern: After the fix no background-color animation exists, so "pause animations at 20, 50, 80 percent" pauses nothing relevant and the scan trivially passes; nothing asserts the helper actually froze a transition on the unfixed CSS. A 20 percent blend is about 4.9:1 and is unlikely to fail, and the plan does not say which fractions must fail. Pausing at a fraction of duration is also eased, so the colour differs from the nominal blend.
* Impact: The state can pass for the wrong reason, or become a silent no-op if the helper's selector or toggle misses; AC-1 cannot be shown to be sound.
* Smallest useful change: Have the helper record, per fraction, the `getAnimations()` entries and the computed background, and assert in the helper that on the fixed CSS no animation targets background-color and the computed background equals the brand colour immediately after the enable. Also assert on the unfixed run that at least one background-color animation was paused. Require AC-1 to name the fractions that must fail (50 and 80), and keep 20 only if shown to fail or drop it.
* Action owner: planning parent
* Exact resolving evidence: revised P01-T02 and AC-1 text with these assertions; recorded red run (color-contrast on the target at the named fractions) and green run in the changes record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Unit regression via regex is bypassable and may false-pass

* Related IDs: FR-1, P01-T01
* Evidence: style.css:191 is the only transition rule; the test file currently imports only `run` and `target_sizes`.
* Concern: "Simple regex on rule blocks" with selector lists containing `button` would miss `transition: all`, `transition-property`, a later rule, `.btn` alone, or a `color` transition added back; it also does not state how the CSS path is resolved from the test.
* Impact: The guard does not protect the stated cause (any non-instant fade of background without the text).
* Smallest useful change: Specify the asserted properties (no `background-color`, `all` or `background` in any transition or transition-property of a rule whose selectors include `button` or `.btn`), resolve the path from the package location, and add a negative-control assertion that the parser finds the border-color rule so an empty parse fails.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 text with the property list and non-empty-match assertion; test fails on the original line 191.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Helper side effects and sibling coverage unspecified

* Related IDs: FR-2, P01-T02, research C4
* Evidence: chat.js:227 and :237 (input.focus() after re-enable); chat.js:212 (aria-disabled removal uses the same fade path); regulatory_ux_check.py:309 to 330 (later states rely on focus and DOM state).
* Concern: Toggling `disabled` on a focused button drops focus in Chromium, and the plan does not say focus is restored or that later keyboard states (doubt.focus, keyboard_walk) are unaffected. Ask, refresh and the aria-disabled doubt button share the mechanism but only the submit button is exercised, so coverage of the class is claimed (research Key Discoveries) but not tested.
* Impact: Possible order-dependent regressions in later states, and an overclaim of coverage.
* Smallest useful change: State that the helper restores focus and original disabled state, cancels the paused animations, and runs where a focus-neutral position follows. Either add the doubt button (aria-disabled toggle) to the helper or state the scan covers the submit button only.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 boundaries updated; full `regulatory_ux_check.py --axe` passes with later states unchanged.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: .alt hover follow-up and "alt swaps to dark background" claim contradict the cascade

* Related IDs: research Open Questions, plan Follow-Up Items
* Evidence: style.css:33 `button:hover,.btn:hover{background:var(--brand-d)}` and :34 `button.alt,.btn.alt{background:var(--surface);color:var(--brand)}` have equal specificity and :34 is later, so .alt keeps the surface background on hover.
* Concern: The recorded follow-up states a hover state that the stylesheet does not appear to produce; it was not observed. The plan carries it as a known defect.
* Impact: Misleading follow-up in the changes record and later #151 audit.
* Smallest useful change: Verify the computed hover background of an .alt button in the browser, then correct or drop the follow-up and the research note.
* Action owner: planning parent
* Exact resolving evidence: computed-style observation recorded, plan Follow-Up Items revised accordingly.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validation does not mirror CI and depends on /tmp artifacts

* Related IDs: NFR-3, AC-2, AC-4, Implementation Context Record
* Evidence: .github/workflows/src-ci.yml:92 to 104 (isolated ruff select E,F,I,B,UP line-length 100 on checks/regulatory_ux_check.py; check run with axe-4.10.3 from RUNNER_TEMP); plan uses /tmp/ama-221-pr419-venv and /tmp/ama-220-axe.min.js.
* Concern: "repo ruff/mypy settings" is not pinned to the CI commands; the axe version and SHA of the local file are not stated against the 4.10.3 pin; the environment is outside the worktree and not reproducible from the record.
* Impact: Local green may not equal the hosted job that failed.
* Smallest useful change: List the exact ruff, format, mypy and unit commands from src-ci.yml, record the axe version and SHA-256 matched, and state the environment is an acknowledged unrecorded local prerequisite.
* Action owner: planning parent
* Exact resolving evidence: AC-2 and the changes record list the exact commands, axe version and results.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Local RPI gate and commit sequencing not stated

* Related IDs: AC-4, P01, P02, Non-Goals
* Evidence: repository instructions (complete local gate before publication); caller forbids push, PR, merge.
* Concern: Non-Goals exclude "checks or gates beyond focused ones" without saying the full `tools/rpi-checks.py --all` gate and external receipt are deferred to publication, and the red-then-green evidence has no commit plan (a red commit would break history; the check must stay unpublished).
* Impact: Reader may think the gate is waived; red evidence could be lost or committed broken.
* Smallest useful change: State the gate is not run here because there is no publication, that red output is captured to the changes record before the fix, and that commits are made only after green.
* Action owner: planning parent
* Exact resolving evidence: plan text clarifying deferral and commit sequencing.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Root cause is evidenced from code and consistent with the hosted colour; the fix is minimal and keeps tokens, reduced motion, border-color transition, focus and semantics.
* Axe tags, rules and selector unchanged; no masking or retry.
* The requirements reuse is bounded and verifiable.
* Residual risk (to be accepted): hosted timing is inferred, not re-observed.

## Questions or Blocking Evidence Gaps

* None decision-critical; no user decision needed.

## Limitations

* No browser execution; reproduction numbers rely on research C6 and C7.
* The 20 percent threshold and the .alt hover claim were assessed by reasoning, not observation.

## Related Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md](.copilot-tracking/plans/2026-10-21/issue-151-cited-answer-contrast-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md](.copilot-tracking/details/2026-10-21/issue-151-cited-answer-contrast-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md](.copilot-tracking/research/2026-10-21/issue-151-cited-answer-contrast-research.md) | Research |

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: revise P01-T02 and AC-1 so the browser state asserts a real paused background animation pre-fix and none post-fix, then apply PC-002 to PC-006 directly and finalize without another critique.
* User response required: no

## Next Steps

Returned to the planning parent: revise directly, then proceed to implementation. No user action required.
