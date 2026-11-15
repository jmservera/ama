<!-- markdownlint-disable-file -->
# Review: Issue 231 Cycle 1 Rebase CSS Focus Rule Recovery (PR 1767)

## Scope and Evidence

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231-c1
* Review date: 2026-11-15
* Review scope: full task (P01, P01-T01, P01-T02, P02, P02-T01, P02-T02)
* Assessed boundary: Cycle 1 surgical recovery of the rebase-merged programmatic focus rule in src/api/src/zava_forward/api/web/style.css against parent commit fe6398197 and HEAD db52dfff4, standalone regression guard in src/api/tests/test_technical_quality_screens_wcag.py (`0` removals, `1` assertion addition), focused WCAG/baseline/static/type/rename/Web-Interface-Guidelines validation, pre-review git noreply author identity and worktree hygiene, critique dispositions (`PC-001` through `PC-003`), and deferred follow-up boundaries. Excludes manual human assistive-technology and zoom walkthroughs tracked externally under #151 and #155.
* Plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md, git diff against fe6398197 and db52dfff4 on src/api/src/zava_forward/api/web/style.css and src/api/tests/test_technical_quality_screens_wcag.py, refreshed Vercel Web Interface Guidelines (https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md), and docs/reference/research/ux/wcag-conformance-baseline.md.

## Opening Review State

* Interpreted review goal: Independently verify once whether Cycle 1 implementation restores standalone `[tabindex="-1"]:focus` parity with parent fe6398197 while preserving Issue #231's `.screen-record h2[tabindex="-1"]:focus-visible` rule, locks regression coverage in Issue #231's WCAG suite, satisfies all focused validation and repository hygiene rules, and reconciles all RPI planning and critique artifacts cleanly.
* Review scope: full task (P01 and P02)
* Evidence readiness: Ready; plan, phase details, single-pass critique, changes record, research record, and workspace diffs are present and current.
* Acceptance basis: Caller Required Fix items 1 through 5, Functional and Non-Functional Requirements and Acceptance Criteria in .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md, resolved critique dispositions (`PC-001`, `PC-002`, `PC-003`), and repository UX/WCAG and engineering instructions in .github/copilot-instructions.md.
* First comparison boundary: Reconcile plan checklist markers, phase details, critique dispositions, and changes-record completion evidence against actual `git diff` in src/api/src/zava_forward/api/web/style.css and src/api/tests/test_technical_quality_screens_wcag.py.
* Active read-only boundaries: Write only .copilot-tracking/reviews/logs/2026-11-15/retrofit-technical-quality-wcag-231-c1-review.md during review; do not mutate source, test, plan, phase-details, critique, research, or changes files.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only comparison on 2026-11-15 across all Cycle 1 planning, critique, research, and changes artifacts, verified `git diff fe6398197` and `git diff db52dfff4` on src/api/src/zava_forward/api/web/style.css and src/api/tests/test_technical_quality_screens_wcag.py, verified passing validation evidence (`109` WCAG/baseline unit tests, ruff lint/format, mypy, rename-zava-tests.py, refreshed Web Interface Guidelines check), and verified local git noreply configuration and worktree status.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| P01, P01-T01 | Split merged programmatic focus rule in workbench stylesheet | Reconciled | `[x]` in plan, `Complete` in phase details, exact two-rule split verified against fe6398197 and db52dfff4 |
| P01, P01-T02 | Add standalone programmatic focus regex guard in Issue 231 WCAG tests | Reconciled | `[x]` in plan, `Complete` in phase details, `1` assertion addition (`0` removals) verified in TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants |
| P02, P02-T01 | Run focused WCAG unit tests, static analysis, test-rename check, and Web Interface Guidelines review | Reconciled | `[x]` in plan, `Complete` in phase details, all 10 unittest modules, ruff, mypy, rename-zava-tests.py, and Web Interface Guidelines review recorded as Passed |
| P02, P02-T02 | Configure repository-local git noreply identity and verify pre-review worktree hygiene | Reconciled | `[x]` in plan, `Complete` in phase details, `8036360+jmservera@users.noreply.github.com` configured and worktree inventory verified including parent state JSON |
| Follow-Up Items | Canonical plan Follow-Up Items mirrored in changes record | Reconciled | All three deferred items (Cycle 0 RV-001/RV-003, Cycle 0 RV-002, external AT sign-off #151/#155) remain outside active P01-P02 claims |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| P01-T01 | src/api/src/zava_forward/api/web/style.css | Split merged `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible` rule into two consecutive standalone Fluent 2 dual-ring focus rules (`--focus-w`, `--focus-ink`, `--focus-off`, `--focus`) | `git diff fe6398197 -- src/api/src/zava_forward/api/web/style.css` confirms byte-for-byte restoration of `[tabindex="-1"]:focus` while keeping `.screen-evidence th` tabular-nums and `.screen-record h2[tabindex="-1"]:focus-visible` | Passed (`109` WCAG/baseline unit tests and Web Interface Guidelines check) | Reconciled |
| P01-T02 | src/api/tests/test_technical_quality_screens_wcag.py | Added standalone `[tabindex="-1"]:focus\s*\{\s*outline:` regex guard in TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants (`0` removals, `1` addition) | `git diff -- src/api/tests/test_technical_quality_screens_wcag.py` confirms single focused assertion with zero `.copilot-tracking/` citations | Passed (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`, `rename-zava-tests.py`) | Reconciled |
| P02-T01 | .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md | Executed all 10 focused WCAG/baseline unittest modules, ruff check, ruff format check, strict mypy, rename-zava-tests.py, and refreshed Web Interface Guidelines review | Zero-exit outputs recorded for every tool (`109` unit tests in `3.507s`, `207` files formatted, `30` mypy files clean, `25` rename tests in `0.580s`, `0` Web Interface Guidelines violations) | Passed | Reconciled |
| P02-T02 | .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md | Configured repository-local GitHub noreply email (`8036360+jmservera@users.noreply.github.com`) and audited pre-review worktree and diff hygiene | `git config --local --get user.email` verified; zero `.copilot-tracking/` matches in `src/`; parent state JSON included in staging inventory for RPI parent closeout | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time updates to the plan or phase details were required after pre-implementation critique resolution | None | Plan, phase details, and changes record remained aligned throughout P01 and P02 execution | Ready (`PC-001`, `PC-002`, `PC-003` resolved before implementation) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three critique findings from .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md (`PC-001` decoupling P02-T02 pre-commit hygiene from post-review parent atomic commit and including parent state JSON, `PC-002` correcting `test_rebase_preserves_housing_resident_helpers_alongside_steward_screen` and `TechnicalAndQualityWcagTests` symbol names, and `PC-003` adding refreshed `web-design-guidelines` review to P02-T01) were resolved directly in .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md and .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md prior to implementation.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent work bypassed prerequisites or required a user-decision pause.
* Justification assessment: Supported by primary commit, stylesheet, test, and validation evidence (`C1` through `C8`, `W1`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Cycle 0 RV-001 and RV-003 (`ensure_ascii=False` in `json.dumps(tree)` inside src/api/tests/test_technical_quality_screens_wcag.py and historical Cycle 0 prose cleanup) | Unrelated to the `[tabindex="-1"]:focus` CSS rebase selector conflict that failed CI job 132700405590 | User-selectable follow-up child RPI task after Cycle 1 closeout | Open distinct follow-up route (non-defect for Cycle 1) |
| Cycle 0 RV-002 (extend `qualityAcceptanceGap(r)` in src/api/src/zava_forward/api/web/app.js to check `defect.fixed_by` alongside `submitted_by`) | Unrelated PAS 2035 helper enhancement outside surgical CSS CI fix boundary | User-selectable follow-up child RPI task after Cycle 1 closeout | Open distinct follow-up route (non-defect for Cycle 1) |
| External human assistive-technology and role-representative validation (#151, #155) | Requires human NVDA/VoiceOver and 320px/200%/400% manual walkthrough outside automated CLI session | Human accessibility reviewer / issue owner before replacing `Refs #231` with a closing keyword | Open distinct external follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

* None. Zero implementation defects, decision gaps, or material evidence gaps were identified within the assessed Cycle 1 boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No defect, plan gap, or research gap requires re-entry for Cycle 1 | Conformant implementation |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Prior Cycle 0 deferred items (`RV-001`/`RV-003` test serializer `ensure_ascii=False` and prose cleanup; `RV-002` `defect.fixed_by` check in `qualityAcceptanceGap`) and external human assistive-technology sign-off (`#151`, `#155`) remain distinct follow-up work outside Cycle 1 scope.
* Immediately upon returning this review record to the confirmed automatic RPI Agent parent and persisting `Follow-up` / `completed` task state, the RPI parent executes the caller-requested atomic local commit (`Refs #231` plus Copilot `Co-authored-by` trailer, no push, leaving `git status --short` empty).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None in active plan scope (`P01` and `P02` complete); RPI parent performs the post-review atomic local git commit before presenting post-Review follow-up choices.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_technical_quality_screens_wcag.py src/api/tests/test_housing_resident_screen_wcag.py src/api/tests/test_data_steward_screen_wcag.py src/api/tests/test_programme_screen_wcag.py src/api/tests/test_finance_screen_wcag.py src/api/tests/test_finance_grants_screen_wcag.py src/api/tests/test_finance_screens_wcag_225.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py src/api/tests/test_design_system.py` | Issue #231, sibling #229/#230/finance, WCAG baseline, content standard, and Fluent 2 design system suites | Passed | Ran 109 tests in 3.507s; OK (exit code 0), including previously failing `test_workspace_jump_nav_and_click_activation_focus_target_headings` and new standalone `[tabindex="-1"]:focus` guard |
| `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && MYPYPATH=../core/src:src python3 -m mypy src tests/test_technical_quality_screens_wcag.py tests/test_housing_resident_screen_wcag.py)` | `src/api` lint, format, and strict static typing | Passed | Ruff all checks passed; 207 files already formatted; mypy found 0 issues in 30 source files |
| `python3 tools/rename-zava-tests.py` | Repository `zava`-prefixed test module enforcement | Passed | Ran 25 tests in 0.580s; OK (exit code 0) |
| Web Interface Guidelines refresh and review (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) | src/api/src/zava_forward/api/web/style.css | Passed | `pass` (`0` violations across accessibility, focus states, scroll-margin-top, motion, and typography rules) |
| Manual NVDA/Firefox and VoiceOver/Safari screen-reader and zoom walkthrough (#151, #155) | Live browser assistive-technology acceptance | Unavailable | Requires human assistive-technology operator; tracked as external follow-up while commit uses `Refs #231` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every Cycle 1 requirement, acceptance criterion, critique disposition (`PC-001` through `PC-003`), and repository engineering/UX gate is satisfied with verified primary evidence. Splitting the rebase-merged CSS selector in src/api/src/zava_forward/api/web/style.css into standalone `[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible` rules resolves the exact hosted CI `src-api` job `132700405590` failure without regressing any Issue #231, sibling #229/#230/finance, WCAG baseline, content-standard, or Fluent 2 design-system invariant, and the new assertion in src/api/tests/test_technical_quality_screens_wcag.py directly guards against recurrence.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Retain ranked Cycle 0 follow-ups (RV-001/RV-003, RV-002) and external human AT sign-off (#151, #155) at the RPI Agent post-Review checkpoint after atomic local commit closeout |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: 109 WCAG/baseline unit tests passed, ruff check/format passed (207 files), mypy passed (30 files), rename-zava-tests.py passed (25 tests), refreshed Web Interface Guidelines check passed (0 violations); manual human AT walkthrough unavailable in CLI and tracked externally under #151/#155
* Blockers: None
