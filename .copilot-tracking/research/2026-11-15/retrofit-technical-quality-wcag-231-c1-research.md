<!-- markdownlint-disable-file -->

# Task Research: retrofit-technical-quality-wcag-231-c1

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                             |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md |

## Research Brief

* What to research: Diagnose the exact CSS selector regression in src/api/src/zava_forward/api/web/style.css introduced when branch feat/ux-231-retrofit-wcag (HEAD db52dfff4, PR #1767) was rebased onto fe6398197, which caused test_workspace_jump_nav_and_click_activation_focus_target_headings in src/api/tests/test_housing_resident_screen_wcag.py to fail in hosted CI job 132700405590, and verify all sibling WCAG test contracts and focused validation commands.
* Why it matters: 9 of 10 CI checks and 3,569 of 3,570 src-api tests passed on PR #1767; resolving this single rebase CSS selector conflict without regressing #231, #229, #230, or baseline WCAG/design-system suites unblocks PR #1767 cleanly.
* Audience or intended use: Downstream rpi-plan, rpi-implement, and rpi-review phases in Cycle 1 of Issue #231.
* Scope: src/api/src/zava_forward/api/web/style.css, sibling WCAG test suites under src/api/tests/, browser accessibility harnesses under src/api/checks/, prior Cycle 0 RPI artifacts under .copilot-tracking/, and focused local validation commands.
* Non-goals: Pushing to remote, modifying unrelated screens or backend logic, or running destructive git history rewrites.
* Criteria: Exact git diff verification against fe6398197, verification of every CSS regex/substring contract across all WCAG unit and browser tests, WCAG 2.2 focus-appearance/focus-visible compliance per repository UX baseline, and verification of actual test filenames in worktree feat-231-retrofit-wcag.
* Requested outputs: Convergent recommendation for exact CSS selector structure and validation selector list, grounded in codebase and web-guideline evidence.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1: How did style.css diverge between fe6398197 and db52dfff4 around [tabindex="-1"] focus rules? Q2: Which CSS assertions exist across all WCAG tests? Q3: How do prompt path aliases map to actual worktree paths and tests? Q4: Does preserving both :focus and :focus-visible rules satisfy WCAG 2.2, Fluent 2, and web-design-guidelines without visual/click-ring regression? |
| Codebase scope                   | src/api/src/zava_forward/api/web/, src/api/tests/, src/api/checks/, docs/reference/research/ux/, .copilot-tracking/                                                |
| External scope                   | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (required by repository Web Development Guidance)                           |
| Initial internal candidate areas | src/api/src/zava_forward/api/web/style.css, src/api/tests/test_housing_resident_screen_wcag.py, src/api/tests/test_technical_quality_screens_wcag.py, docs/reference/research/ux/wcag-conformance-baseline.md |
| Initial external candidate areas | Vercel Web Interface Guidelines command.md                                                                                                                         |
| Research posture                 | focused                                                                                                                                                            |
| Posture provenance               | default (bounded internal task with named source targets and exact CI failure traceback)                                                                           |
| Explicit limits / deadline       | Non-interactive single-session execution; do not push to remote                                                                                                    |
| Posture-specific completion basis| focused scope and materiality: all named CSS, test, and validation questions verified with exact codebase evidence and contrarian check completed                  |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | .copilot-tracking/                                                                                                                                                 |
| Known constraints / excluded sources | Preserve Fluent 2 design system, WCAG 2.2 AA baseline, plain-language content standard, and Cycle 0 #231 behavior; no .copilot-tracking references in code or commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                                        | Scoped authority or output contract                                         | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | .github/copilot-instructions.md                | applyTo "**" matches all repository files                                   | Enforces UX/WCAG baseline, web-design-guidelines fetch, focused tier, git email/trailer rules | Selected: mandatory repository-wide instructions                                          |
| Instruction         | copilot-tracking.instructions.md               | applyTo ".copilot-tracking/**" matches all RPI artifacts                    | Enforces markdownlint comment, plain-text paths, Pxx/Pxx-Txx/PC-xxx/RV-xxx IDs | Selected: mandatory tracking artifact conventions                                         |
| Skill               | rpi-research                                   | Explicit RPI Phase 1 skill                                                  | Read-only three-wave research artifact and readiness contract               | Selected: active phase skill                                                              |
| Skill               | web-design-guidelines (.github/skills/)        | Required by .github/copilot-instructions.md before web edits and reviews    | Fetches current Vercel Web Interface Guidelines rules                       | Selected: fetched command.md for focus-state and accessibility rule verification          |
| Skill               | redesign-existing-projects (.agents/skills/)   | Referenced by .github/copilot-instructions.md for existing-app web work     | Focus ring and existing-stack targeted fix guidance subordinate to Fluent 2 | Selected: read SKILL.md; subordinate to Fluent 2 and WCAG baseline per repo instructions  |
| Skill               | accessibility (hve-core plugin)                | Semantic match to WCAG focus styling                                        | General WCAG 2.2 reference pack                                             | Skipped: repository local docs/reference/research/ux/wcag-conformance-baseline.md is authoritative |
| Research specialist | hve-core-all:rpi-researcher                    | Registered host subagent for independent research lanes                     | Writes subagent lane markdown under .copilot-tracking/research/subagents/   | Skipped (inline execution): tightly coupled 2-file CSS/test diff takes <=5 direct reads   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                              |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with complete CI traceback, commit SHAs (db52dfff4, fe6398197), and validation criteria supplied | N/A (non-interactive)| Proceed in focused convergence mode; verify worktree/file name aliases directly from git/PR #1767 |
| Direction change | No scope widening beyond style.css focus rules and WCAG test contracts needed                                             | N/A                  | Maintain focused scope                                                                       |
| Convergence      | Single bounded CSS/test reconciliation; no optional follow-up research ambiguity                                          | N/A                  | Converge on verified CSS rule and test coverage once three waves complete                    |

## Scope and Success Criteria

* Scope: Exact rebase diff of src/api/src/zava_forward/api/web/style.css between fe6398197 and db52dfff4, all CSS selector assertions across src/api/tests/, Cycle 0 review follow-up context, and focused validation commands.
* Assumptions: Caller references to feat-231-quality-finance-wcag, styles.css, and test_quality_finance_screen_wcag.py map to PR #1767 worktree feat-231-retrofit-wcag, style.css, and test_technical_quality_screens_wcag.py (plus existing test_finance_*_wcag*.py suites); verify empirically.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (path:line for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one recommendation is selected in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect git show fe6398197 vs current style.css around [tabindex="-1"]:focus and #231 styles; restore/preserve exact [tabindex="-1"]:focus{outline:...} rule so sibling #229 and #231 WCAG tests pass without regressions; record C1 RPI artifacts; run focused validation; commit locally without pushing.
* Inferred research questions: Check whether any other test in src/api/tests/ asserts on [tabindex="-1"]:focus or [tabindex="-1"]:focus-visible or style.css rules, check whether C0 RV-001 interacts with #231 tests, and check how programmatic element.focus() interacts with :focus vs :focus-visible in browsers and Web Interface Guidelines.
* Caller constraints and non-goals: Do not push; leave clean git status --short; use Refs #231 and required Co-authored-by trailer.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                  | Source / checkpoint | Effect on active brief, evidence, or revalidation                            |
|----------------------------------------------------------|------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------|
| narrow                                                   | Fix exact CI failure in src-api job 132700405590 without regressions   | Caller intake       | Constrains implementation target to style.css focus selector compatibility    |
| exclude                                                  | Do not push to remote; leave frozen local commit                       | Caller intake       | Excludes git push and remote PR mutation                                     |

## Research Questions

|  # | Sub-question                                                                                                                | Type (depth / breadth / straightforward) | Priority | Status |
|---:|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|--------|
| Q1 | What exact lines changed in src/api/src/zava_forward/api/web/style.css between fe6398197 and db52dfff4?                     | straightforward                          | H        | answered |
| Q2 | Which unit tests and browser checks inspect style.css around [tabindex="-1"], :focus, :focus-visible, or scroll-margin-top? | breadth                                  | H        | answered |
| Q3 | How do the caller prompt path/file names map to actual PR #1767 files and existing finance/quality WCAG tests?              | straightforward                          | H        | answered |
| Q4 | How do :focus and :focus-visible behave on programmatic heading focus (tabindex="-1") under WCAG 2.2 and web guidelines?    | depth                                    | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json, .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md, .copilot-tracking/reviews/logs/2026-11-15/retrofit-technical-quality-wcag-231-review.md
* Reused (verified) findings: PR #1767 is branch feat/ux-231-retrofit-wcag at HEAD db52dfff4 targeting feat/demo-233-same-home-tensions-0825 (fe6398197); counted baseline guards (aria-invalid = 9, script-built tables = 14, fixed-position rules = 2) remain intact on HEAD.
* Superseded / stale: Cycle 0 assumed merging [tabindex="-1"]:focus and .screen-record h2[tabindex="-1"]:focus-visible into a single comma-separated selector in style.css preserved sibling #229 tests; hosted CI job 132700405590 and local reproduction proved test_housing_resident_screen_wcag.py requires `{` immediately after `[tabindex="-1"]:focus`.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (fix exact CI failure in src-api job 132700405590 without regressions), exclude (do not push to remote)
* Active research posture and completion basis: focused; all named CSS, test, and validation questions verified with exact codebase evidence and contrarian check completed
* Explicit limits or deadline effect: none; complete three-wave cycle executed inline

#### Wave 1: Wider

* Plan and independent lanes: Map PR #1767 worktree, branch, base branch, web asset filenames, and all WCAG test modules referencing style.css or tabindex="-1" across src/api/.
* Worker evidence relationships or inline fallback: inline: tightly coupled 2-file CSS/test investigation completed in <=5 direct calls (Q3 -> C1, C2; Q2 -> C5, C6, C7).
* Reflection: Confirmed PR #1767 maps to worktree /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag on branch feat/ux-231-retrofit-wcag (HEAD db52dfff4) targeting feat/demo-233-same-home-tensions-0825 (fe6398197), web stylesheet is src/api/src/zava_forward/api/web/style.css, and #231 WCAG suite is src/api/tests/test_technical_quality_screens_wcag.py alongside finance suites test_finance_screen_wcag.py, test_finance_grants_screen_wcag.py, and test_finance_screens_wcag_225.py. Prioritized exact git diff and regex boundary inspection for Wave 2.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q1 (exact git diff fe6398197..db52dfff4 on style.css) and Q2 (exact regexes across test_housing_resident_screen_wcag.py, test_technical_quality_screens_wcag.py, test_data_steward_screen_wcag.py, test_accessibility_baseline.py, and test_design_system.py).
* Plan and independent lanes: Inspect git diff fe6398197..db52dfff4, inspect every CSS regex in WCAG and baseline tests, and reproduce the CI failure locally via unittest.
* Worker evidence relationships or inline fallback: inline: direct git diff, view, and unittest reproduction (Q1 -> C3, C4; Q2 -> C5, C6, C7, C8).
* Reflection: Exact root cause proven. Parent commit fe6398197 had standalone `[tabindex="-1"]:focus { outline: ... }` at style.css:374. Rebase commit db52dfff4 combined it into `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible { outline: ... }`. Because test_housing_resident_screen_wcag.py:676 asserts `r'\[tabindex="-1"\]:focus\s*\{\s*outline:'` AND test_technical_quality_screens_wcag.py:306 asserts `r'\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{[^}]*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'`, BOTH selectors require `{` immediately after their own selector with only optional whitespace! Needs contrarian verification of selector-order swap vs separate rules and Web Interface Guidelines compliance in Wave 3.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Test three potential challenges: (1) Could swapping selector order in a single rule satisfy both tests without duplicating the declaration block? (2) Does keeping `[tabindex="-1"]:focus` violate Web Interface Guidelines (`Use :focus-visible over :focus`) or test_accessibility_baseline.py / test_design_system.py? (3) Should Cycle 0 follow-up RV-001 be bundled or kept separate?
* Plan and independent lanes: Evaluate both regexes against swapped single-rule CSS, verify all static CSS invariants in test_technical_quality_screens_wcag.py:302-314, test_accessibility_baseline.py:67-137, and test_design_system.py:32-116, and check W1 focus-state rules.
* Worker evidence relationships or inline fallback: inline: direct regex evaluation against C4, C5, C6, C7, C8, and W1.
* Reflection: Contrarian check disproved single-rule selector swapping: placing `.screen-record h2[tabindex="-1"]:focus-visible` first breaks test_technical_quality_screens_wcag.py:306 (`:focus-visible\s*\{`), while placing `[tabindex="-1"]:focus` first breaks test_housing_resident_screen_wcag.py:676 (`:focus\s*\{`). Two standalone rules preserve 100% identical browser cascade semantics to db52dfff4, satisfy both regexes plus test_data_steward_screen_wcag.py:742, pass `re.findall(r"^\.screen-[^{]*\{[^}]*\}", CSS, flags=re.M)` (no animation/transition), do not alter `position:fixed` count (2), and honour programmatic focus visibility on `tabindex="-1"` jump targets (W1, C8). Adding a standalone `[tabindex="-1"]:focus` regex guard in test_technical_quality_screens_wcag.py directly prevents future rebase regressions while keeping unrelated C0 follow-ups (RV-001 to RV-003) cleanly scoped out per surgical-change discipline.

#### Parent Synthesis and Disposition

| Material / claim                                                                                      | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale                                                                                              | Primary-artifact treatment            |
|-------------------------------------------------------------------------------------------------------|---------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| Split style.css:374 into two standalone rules (`[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible`) | C3, C4, C5, C6, C7, C8, W1      | accepted                                            | Only structure where `{` immediately follows both selectors while preserving identical computed styles and WCAG tokens | Selected Recommendation and Decision  |
| Add regression assertion for standalone `[tabindex="-1"]:focus` rule in test_technical_quality_screens_wcag.py | C5, C6                          | accepted                                            | Directly guards #231 against future rebase selector-merging without modifying sibling #229 tests                      | Selected Recommendation               |
| Swap selector order inside a single comma-separated CSS rule                                          | C5, C6                          | rejected                                            | Fails test_technical_quality_screens_wcag.py:306 because `:focus-visible\s*\{` will not match before `,`              | Rejected Alternative 1                |
| Replace `.screen-record h2[tabindex="-1"]:focus-visible` with `[tabindex="-1"]:focus` alone           | C6, W1                          | rejected                                            | Fails test_technical_quality_screens_wcag.py:306 and drops explicit `:focus-visible` rule from #231 contract          | Rejected Alternative 2                |
| Bundle Cycle 0 follow-ups RV-001, RV-002, RV-003 into Cycle 1 CI fix                                  | C2                              | deferred                                            | Outside caller's explicit Required Fix scope; preserved in prioritized follow-ups                                     | Retained Follow-Up / Potential Next   |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: focused scope saturated; exact git diff, test failure reproduction, all CSS regex contracts, and contrarian alternatives are 100% verified from primary codebase and fetched web-guideline sources.
* Revised brief or revalidation required: none
* Readiness effect: Ready for rpi-plan

## Evidence Log

* Delegation: inline: bounded 2-file CSS rebase conflict and test-contract verification completed directly in <=5 reads per tool-efficiency contract.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | PR #1767 corresponds to branch feat/ux-231-retrofit-wcag at HEAD db52dfff446f306f73c5b6cc632c6f88f4278620 targeting feat/demo-233-same-home-tensions-0825 (fe6398197) in worktree /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag | .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json:1 | bash / read | high | Verified via gh pr view 1767 and git log -n 5 |
| C2 | Cycle 0 review recorded zero production defects on #231 and routed RV-001 (ensure_ascii=False), RV-002 (defect.fixed_by), and RV-003 (prose) as post-review items prior to rebase CI run | .copilot-tracking/reviews/logs/2026-11-15/retrofit-technical-quality-wcag-231-review.md:92 | read | high | Explains C0 history before rebase onto fe6398197 |
| C3 | Parent commit fe6398197 (#229/#1764) defines standalone `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` | src/api/src/zava_forward/api/web/style.css:374 | bash (git show fe6398197) | high | Exact parent baseline line 374 |
| C4 | Rebase commit db52dfff4 merged the rule into `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` | src/api/src/zava_forward/api/web/style.css:374 | read / git diff | high | Inserted `, .screen-record h2[tabindex="-1"]:focus-visible` before `{` |
| C5 | Sibling #229 housing/resident WCAG test asserts `self.assertRegex(css, r'\[tabindex="-1"\]:focus\s*\{\s*outline:')`, which fails on db52dfff4 because `,` precedes `{` | src/api/tests/test_housing_resident_screen_wcag.py:676 | read / bash unittest | high | Reproduced exact CI job 132700405590 failure locally |
| C6 | Issue #231 WCAG test asserts `r'\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{[^}]*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'` and checks `^\.screen-[^{]*\{[^}]*\}` has no animation or transition | src/api/tests/test_technical_quality_screens_wcag.py:306 | read | high | Also requires `{` immediately after `:focus-visible` |
| C7 | Sibling #229 data-steward WCAG test asserts substring `'[tabindex="-1"]:focus'` and `'[tabindex="-1"] { scroll-margin-top: var(--sp-4); }'` in style.css | src/api/tests/test_data_steward_screen_wcag.py:742 | read | high | Compatible with standalone `[tabindex="-1"]:focus` rule |
| C8 | Baseline WCAG and Fluent 2 design-system tests verify `:focus-visible{outline:var(--focus-w) solid var(--focus-ink)` (line 52), no `outline: none|0`, 2 fixed-position rules, and documented tokens/classes; finance WCAG suites live at test_finance_screen_wcag.py, test_finance_grants_screen_wcag.py, and test_finance_screens_wcag_225.py | src/api/tests/test_accessibility_baseline.py:67 | grep / read | high | Also verified src/api/tests/test_design_system.py:32 |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Web Interface Guidelines require visible focus rings, forbid `outline: none` without replacement, prefer `:focus-visible` on interactive controls to avoid click rings, and require `scroll-margin-top` on heading anchors | Vercel Web Interface Guidelines (command.md) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main (fetched 2026-11-15) | high |

### Contradictions / Conflicts

* Focus pseudo-class choice on programmatic jump targets: W1 prefers `:focus-visible` over `:focus` for interactive controls so mouse clicks on buttons do not leave focus rings, whereas sibling #229 (`C3`, `C5`, `C7`) requires `[tabindex="-1"]:focus` on non-interactive programmatic targets (`<main>`, `<h2 tabindex="-1">`, `<section tabindex="-1">`) because pointer-activated jump links call `target.focus()` where browsers suppress `:focus-visible`; resolved by precedence (`C5` repository contract + WCAG 2.4.7 programmatic jump visibility) -> keep standalone `[tabindex="-1"]:focus` rule alongside `.screen-record h2[tabindex="-1"]:focus-visible`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Rebase commit db52dfff4 changed style.css:373 to include `.screen-evidence th` in tabular-nums and merged style.css:374 from standalone `[tabindex="-1"]:focus { ... }` into `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible { ... }`. | C3, C4 | high | Splitting line 374 into two standalone rules restores exact fe6398197 rule syntax while keeping #231's rule. |
| Q2 | test_housing_resident_screen_wcag.py:676 requires `{` immediately after `[tabindex="-1"]:focus`, and test_technical_quality_screens_wcag.py:306 requires `{` immediately after `.screen-record h2[tabindex="-1"]:focus-visible`; test_data_steward_screen_wcag.py:742, test_accessibility_baseline.py:67, and test_design_system.py:32 also pass with two separate rules. | C5, C6, C7, C8 | high | Only two separate rules satisfy all existing regexes simultaneously without editing sibling test suites. |
| Q3 | Prompt references map to PR #1767 worktree /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag, branch feat/ux-231-retrofit-wcag (db52dfff4), base feat/demo-233-same-home-tensions-0825 (fe6398197), stylesheet src/api/src/zava_forward/api/web/style.css, and #231 test src/api/tests/test_technical_quality_screens_wcag.py (plus finance WCAG suites src/api/tests/test_finance_screen_wcag.py, src/api/tests/test_finance_grants_screen_wcag.py, src/api/tests/test_finance_screens_wcag_225.py). | C1, C8 | high | Focused validation will execute test_technical_quality_screens_wcag.py plus all sibling housing/steward/programme/finance/baseline WCAG suites. |
| Q4 | Keeping standalone `[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible` produces identical computed Fluent 2 dual-ring focus styles (`--focus-w`, `--focus-ink`, `--focus-off`, `--focus`) to db52dfff4 and ensures visible focus on both pointer-activated and keyboard-activated in-page jump links. | C3, C4, C8, W1 | high | Zero visual, cascade, or accessibility regression; Planning Readiness is Ready. |

## Key Discoveries

* Both test_housing_resident_screen_wcag.py:676 and test_technical_quality_screens_wcag.py:306 anchor their regexes with `\s*\{` immediately after their respective selector (`[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible`), making any comma-combined single CSS rule fail one of the two tests (C5, C6).
* Splitting src/api/src/zava_forward/api/web/style.css:374 into two standalone consecutive CSS rules preserves 100% identical CSS cascade and token behavior while restoring exact line-for-line compatibility with fe6398197 (C3, C4).
* Adding `self.assertRegex(CSS, r'\[tabindex="-1"\]:focus\s*\{\s*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)')` in src/api/tests/test_technical_quality_screens_wcag.py gives #231's own test suite direct regression protection against future rebase selector merging (C5, C6).

### Configuration Examples

```css
[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }
.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Split src/api/src/zava_forward/api/web/style.css:374 into two standalone rules, restoring fe6398197's exact `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` on line 374 followed by `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` on line 375, and add a focused assertion in src/api/tests/test_technical_quality_screens_wcag.py guarding the standalone `[tabindex="-1"]:focus` rule alongside `.screen-record h2[tabindex="-1"]:focus-visible`.
* Rationale: Preserves identical browser CSS cascade semantics, leaves sibling #229 test files untouched, satisfies every static CSS regex across #229, #231, #150, and #151, and prevents recurrence on future rebases.
* Evidence refs: C3, C4, C5, C6, C7, C8, W1
* Implementation impact: 2 lines in src/api/src/zava_forward/api/web/style.css and 1 assertion in src/api/tests/test_technical_quality_screens_wcag.py, plus Cycle 1 .copilot-tracking/ RPI artifacts.
* Confidence: high: exact CI failure already reproduced locally (C5) and every CSS consumer in src/api/tests/ inspected (C8).

File tree:

```text
src/api/src/zava_forward/api/web/style.css (modified)
src/api/tests/test_technical_quality_screens_wcag.py (modified)
.copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md (new)
.copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md (new)
.copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md (new)
.copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md (new)
.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md (new)
.copilot-tracking/reviews/logs/2026-11-15/retrofit-technical-quality-wcag-231-c1-review.md (new)
.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-c1-state.json (new)
.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json (modified)
```

### Alternative: Swap selector order in a single comma-separated CSS rule

* Approach: Change line 374 to `.screen-record h2[tabindex="-1"]:focus-visible, [tabindex="-1"]:focus { outline: ... }`.
* Trade-offs: Avoids repeating the three focus declarations once, but fails test_technical_quality_screens_wcag.py:306 because its regex requires `\s*\{` immediately after `:focus-visible`.
* Evidence refs: C5, C6
* Rejection rationale: Directly breaks #231's own WCAG test regex (C6) unless test contracts are weakened.

### Alternative: Relax regexes in test_housing_resident_screen_wcag.py or test_technical_quality_screens_wcag.py

* Approach: Edit src/api/tests/test_housing_resident_screen_wcag.py:676 to allow `[^{]*\{` after `[tabindex="-1"]:focus`.
* Trade-offs: Keeps single combined CSS line, but mutates sibling #229's test file unnecessarily and contradicts caller Required Fix item 2 (Restore/preserve the exact `[tabindex="-1"]:focus{outline:...}` rule).
* Evidence refs: C3, C5
* Rejection rationale: Violates caller instructions to restore the CSS rule in src/api/src/zava_forward/api/web/style.css and creates avoidable merge churn on sibling #229's test file.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Caller validation command listed test_quality_finance_screen_wcag.py, which is an alias for #231's src/api/tests/test_technical_quality_screens_wcag.py (plus existing src/api/tests/test_finance_screen_wcag.py, src/api/tests/test_finance_grants_screen_wcag.py, and src/api/tests/test_finance_screens_wcag_225.py in the worktree); the validation phase will run all of those real test modules plus src/api/tests/test_data_steward_screen_wcag.py so zero coverage is missed (C1, C8).
* Follow-up: Prior Cycle 0 follow-ups (RV-001 ensure_ascii=False, RV-002 defect.fixed_by, RV-003 C0 tracking prose, parent-branch #1758 browser-check alignment, and human assistive-technology sign-off under #151/#155) remain distinct open follow-ups outside this surgical CI fix (C2).
* Residual uncertainty: none for the engineering fix; human screen-reader/zoom acceptance remains an external gate (Refs #231).

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Restore standalone `[tabindex="-1"]:focus { ... }` rule on its own line ahead of `.screen-record h2[tabindex="-1"]:focus-visible { ... }` in src/api/src/zava_forward/api/web/style.css | proposed | evidence | Satisfies both #229 and #231 `\s*\{` regex contracts with zero CSS cascade change | C3, C4, C5, C6, C7, W1 | Unblocks src-api CI failure from job 132700405590 |
| Guard standalone `[tabindex="-1"]:focus` rule in src/api/tests/test_technical_quality_screens_wcag.py | proposed | evidence | Prevents future rebases on #231 from re-merging `[tabindex="-1"]:focus` into another selector | C5, C6 | Focused 1-assertion regression guard in #231's existing WCAG test file |
| Map caller alias paths to verified PR #1767 worktree paths (feat-231-retrofit-wcag, src/api/src/zava_forward/api/web/style.css, src/api/tests/test_technical_quality_screens_wcag.py plus finance and steward WCAG suites) | confirmed | evidence | Verified via gh pr view 1767 (db52dfff4) and filesystem inspection | C1, C8 | Runs every relevant WCAG, baseline, lint, mypy, and rename check accurately |
| Keep C0 follow-ups (RV-001, RV-002, RV-003) deferred outside Cycle 1 | deferred | constraint | Preserves surgical scope limited to the exact CI rebase regression requested by caller | C2 | Retained in post-Review prioritized follow-ups |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Human assistive-technology and role-representative sign-off for Issue #231 (#151, #155) | Manual keyboard, NVDA/VoiceOver, and 320px/200%/400% walkthrough execution by human tester | Human reviewer / owner | Required before replacing Refs #231 with closing keyword | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Audit defect.fixed_by vs accepted_by independence across backend and UI (RV-002) | Confirms whether backend store enforces fixer independence alongside submitter independence | User selects PAS 2035 independence follow-up after PR #1767 CI recovery | deferred | C2 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (split combined focus rule at src/api/src/zava_forward/api/web/style.css:374 into two standalone rules and add regression guard in src/api/tests/test_technical_quality_screens_wcag.py).
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, W1
* Preconditions met: Exact CI failure reproduced locally, parent `fe6398197` CSS verified, all sibling regex/token/class invariants checked, and current Web Interface Guidelines fetched.
* Blockers: none
* Smallest action to change readiness: none (already Ready)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Wider, Deeper, and Contrarian completed in order for Cycle 1                                                                   |
| Lane evidence or inline fallback | inline: bounded 2-file CSS/test diff investigated directly without subagent overhead; no material limitation                   |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (C1-C8, W1)                                                                                                              |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | confirmed automatic RPI Agent with automatic continuation to Plan                                                              |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1-C8, W1)                                                                                            |
| Output mode and planning support | convergence; yes, selected recommendation is backed by C3-C8 and W1 with Planning Readiness Ready            |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); three waves complete (passed); pre-transition state write (passed) |
| Continuation result              | automatic continuation to rpi-plan                                                                           |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md                     |
| Notes for planning or re-entry   | Keep source edits surgical to style.css:374 and test_technical_quality_screens_wcag.py:303; map validation commands to actual test module paths |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because the exact single-test CI failure is reproduced locally and every CSS selector consumer in `src/api` has been inspected directly.

## Sources

* W1 - Vercel Web Interface Guidelines (command.md) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-15, main)

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions Risks and Residual Uncertainty, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check
* Missing or limited sections: none
