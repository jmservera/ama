---
title: PR 538 correction final-candidate plan critique
description: Independent single-pass implementation-readiness assessment, refs 531
ms.date: 2026-10-29
---

## Metadata

* Task ID: 538-review-corrections-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md
* Primary research: .copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md
* Critique execution status: Complete
* Candidate source HEAD observed: 204507d6
* Branch observed: feat/loading-briefing-hax-531, tracking origin/feat/loading-briefing-hax-531
* Execution boundary: exactly one independent assessment of the supplied final
  candidate; no delegated agents, source edits, plan edits or implementation.
  Preserve this original critique unchanged after delivery.

## Inputs and Criterion Boundary

* The supplied user direction requires three corrections: preserve ownership
  when LF precedes a trailing citation; keep titles/common abbreviations from
  fragmenting statements; and recover an initially failed /async-action.js
  before top-level helper-dependent listeners can prevent startup.
* The plan, phase details and primary research C1-C9/W1 were read in full.
  Relevant implementation and regression evidence was inspected directly:
  src/core/src/zava_forward/core/ai_tasks.py,
  src/core/tests/test_ai_statement_sources.py,
  src/api/src/zava_forward/api/web/app.js,
  src/api/src/zava_forward/api/web/async-action.js,
  src/api/src/zava_forward/api/web/index.html,
  src/api/src/zava_forward/api/web/workspace-shell.js,
  src/api/tests/test_workspace_scripts.py,
  src/api/checks/loading_briefing_browser_check.py and
  src/api/checks/workspace_scripts_browser_check.py.
* Repository context was read from the original case study, addendum,
  reference index, owner memory and housing-association primer. The relevant
  src/README.md local-gate guidance was also inspected. These are context,
  not fresh legal, operational or accessibility acceptance evidence.
* Decisions assessed: reuse the existing topic branch; preserve the reported
  completed pull/rebase; use local-only Conventional Commits; retain original
  RPI evidence and one independent post-implementation Review; no push, Azure,
  force-push, closing keywords, publication or replacement of historical
  outcomes. No fresh GitHub lifecycle investigation was necessary.
* Validation criteria assessed: strict mypy and both Ruff commands in core
  and API; worktree-first src/test paths; focused regressions; full units and
  both relevant browsers under nonblocking shared-lock admission; explicitly
  permitted targeted fallback and honest unperformed-check reporting when busy.
* Assessment covers G1-G3, FR1-FR5, non-functional requirements, AC1-AC6,
  P01-T01 through P02-T02, dependencies, change budget, failure contracts and
  regression sufficiency. It assesses readiness, not implemented correctness.
  No new external research or test execution was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1; FR1; C1/C2; P01-T01; AC1/AC2 | Covered | Citation shielding precedes scoped whitespace normalization; LF, CRLF, multiple groups and uncited statements are included. Preserve unresolved labels and unrelated line boundaries. |
| G2; FR2; C1/C2; P01-T01; AC2 | Partial | Medial abbreviation protection is specified, but distinguishing sentence-terminal uses of the same tokens is not operationalized; PC-001. |
| G3; FR3; C3/C6/C8; P01-T02; AC3 | Partial | Awaiting helper readiness before listeners/start is correct. Role-dependent dependency selection while me is null remains unspecified; PC-002. |
| FR4; C6/C8; P01-T02; AC4 | Covered | Cached promises, two retry attempts, concurrency, timeout/evaluation uncertainty and stale-session/route guards are explicitly preserved. |
| FR5; P01-T02; AC4 | Covered | Bootstrap exhaustion and missing readiness require terminal native reload; ordinary service errors retain Try again. Actual-helper browser modes are planned. |
| Non-functional requirements; P01-T03 | Covered | Typed Python, existing lint conventions, no dependency expansion or no-op helper, bounded README change and conditional manifest-pin review. |
| P02-T01; C4/C9; AC3-AC5 | Partial | Targeted/static/full/browser lanes are appropriate; add the specific discriminating fixtures in PC-001 and PC-002 rather than only generic category coverage. |
| P02-T02; AC6; branch and publication limits | Covered | Local commits, authenticated noreply identity, preserved original evidence and one independent Review are explicit. No hosted/full-publication pass is inferred. |
| P01 to P02 dependency; risks and change budget | Covered | Implementation precedes validation; existing harnesses and parameterization can accommodate both corrections without new dependencies or an expanded workstream. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: the overall approach is credible and all three supplied findings
  are represented. Two implementation choices remain underspecified in ways
  that can either transfer evidence to an uncited claim or introduce a
  pre-login dependency regression. Both are direct corrections within the
  confirmed scope; neither requires a new user decision or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Protect medial abbreviations without suppressing their genuine sentence-final boundary

* Related IDs: G1/G2, FR2, AC2, C1/C2, P01-T01.
* Evidence: .copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md:15-21
  instructs protecting recognized abbreviation periods using a marker. The
  plan at .copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md:52-54
  simultaneously requires genuine sentence boundaries and includes St. plus
  unspecified related forms. src/core/src/zava_forward/core/ai_tasks.py:135-161
  attaches all references in each resulting piece to that piece. The existing
  src/core/tests/test_ai_statement_sources.py has no abbreviation fixtures.
* Concern: the details do not define when a recognized token is medial rather
  than sentence-terminal. Unconditionally shielding its periods satisfies
  the Dr. example but defeats the separate requirement to preserve genuine
  boundaries. Merely checking that an ordinary period elsewhere still splits
  does not detect this failure. A next-word-capitalization rule alone is also
  insufficient because Dr. Smith is a required non-boundary.
* Impact: for the proposed negative fixture
  "The address is High St. Repairs are due. [[Second source]]", blanket
  shielding of St. merges the uncited address into the cited repairs
  statement. This recreates misleading citation ownership while apparently
  fixing abbreviation fragmentation. This is a risk of the proposed
  algorithm, not a claim that the unimplemented change already fails.
* Smallest useful change: specify a bounded, contextual rule for protected
  medial uses, distinguish ambiguous terminal uses conservatively, and state
  the exact supported abbreviation set. Add adjacent negative fixtures using
  the same recognized token, not just ordinary sentence punctuation. Keep
  explicit newlines authoritative except the deliberate trailing-citation
  normalization exception. Do not add a general NLP dependency.
* Action owner: planning parent, then P01-T01 implementer.
* Exact resolving evidence: revised P01-T01 describes the boundary rule and
  expected outputs; parameterized regressions in
  src/core/tests/test_ai_statement_sources.py prove that
  "Dr. Smith checked the case. [[First source]]" remains one cited statement,
  that "The address is High St. Repairs are due. [[Second source]]" returns
  two statements with citations [] and ["Second source"] respectively, and
  that a medial St. use such as "St. Mary's needs repairs. [[First source]]"
  remains intact. Include a sentence-terminal case for any additional
  supported dual-use form such as etc., plus explicit newline, LF/CRLF and
  multiple-reference cases. Assert full text, resolved citations and
  unresolved citations, not only statement counts. Record actual focused
  green results during implementation.
* Decision route: direct-apply planner correction. The user already requires
  true sentence boundaries and no invented evidence. No significant or
  divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Define a helper-only pre-session dependency contract

* Related IDs: G3, FR3/FR4, AC3/AC4, C3/C8, P01-T02.
* Evidence: .copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md:26-36
  says to handle me === null and await requireWorkspaceScripts before
  listeners/start, but does not state the bootstrap hash/case arguments or
  which role-specific predicates remain eligible. In
  src/api/src/zava_forward/api/web/app.js:220-233 the existing predicate uses
  me.user.role to choose staff versus contractor files. The loader's current
  post-await if (!me) return is at app.js:241. The existing
  src/api/tests/test_workspace_scripts.py exercises null entry only through
  route(), which returns without calling the loader.
* Concern: null safety alone does not determine the correct dependencies.
  Treating a missing role as "not Contractor" can select staff case scripts
  or Leaflet before authentication. An unauthenticated deep link then risks
  being blocked by files the eventual user does not need, including staff
  files for a contractor case. Conversely, bypassing readiness when null
  remains null permits the original helper dereference failure. The captured
  session identity requirement is sound but does not settle this selection
  contract.
* Impact: a helper-recovery correction can regress sign-in availability or
  role-specific lazy recovery even while the happy-path helper browser
  scenario passes.
* Smallest useful change: explicitly make bootstrap require only the
  session-independent helper while no identity is available, either through
  null-aware predicates that exclude role-specific files or an explicit
  bootstrap selection mode. Select role-dependent files through the existing
  authenticated route afterward. State that unchanged null identity still
  requires the post-load readiness check and that terminal failure cannot
  register helper-dependent listeners or call start().
* Action owner: planning parent, then P01-T02 implementer.
* Exact resolving evidence: revised P01-T02 names the bootstrap selection and
  continuation rules. Extend src/api/tests/test_workspace_scripts.py with
  null-session #/overview and #/case/ZF-1 cases while unrelated globals are
  absent: helper present selects no scripts; helper absent selects only
  /async-action.js; actual readiness permits continuation; exhausted,
  loaded-without-readiness and timed-out helper attempts reject rather than
  resolve via the old null early return. Retain cached attempt counts and
  existing authenticated staff/contractor/stale-session matrices. The
  planned actual-browser scenarios must show that bootstrap terminal states
  expose announced native reload rather than login or service Try again,
  and that successful recovery reaches login and a working helper-dependent
  account action without page errors or document reload.
* Decision route: direct-apply planner correction. This preserves current
  role/session contracts and the confirmed bootstrap requirement; no
  significant or divergent user decision is needed.

## Strengths and Residual Risk

* Scoped citation whitespace normalization is preferable to flattening all
  newlines. Both resolved and unresolved source ownership remain important
  regression assertions.
* The plan recognizes that AsyncAction is a lexical const. Reusing the
  cached loader, avoiding reinjection after uncertain evaluation and testing
  the shipped helper in Chromium are appropriate, rather than installing a
  no-op fallback or relying exclusively on a Node stand-in.
* Initial download failure, recovery, exhaustion and loaded-without-readiness
  are distinct planned browser modes. Existing route/session and briefing
  regressions remain valuable and should not be replaced by the new cases.
* The two-attempt retry budget is additional to the initial HTML request.
  Existing browser expectations distinguish three total failed requests
  from two total requests when the first injection loads without readiness.
* The change budget can hold these additions through parameterized cases;
  no new test file or expanded browser framework is required.
* Nonblocking lock admission and targeted fallback are explicit user choices,
  not missing full-suite evidence to conceal. A busy lock must remain a
  recorded limitation, not an automatic acceptance or a reason to run a
  competing install/full suite.
* Human accessibility, real deployment cold starts and hosted/publication
  gates remain outside this local correction. A local pass cannot establish
  those outcomes.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or external research blocker. Both findings can
  be corrected directly by the planning parent using the supplied source.
* AC1 refers to two exact original reproductions without quoting their
  complete strings in the supplied artifacts. Preserve those original
  examples as implementation fixtures from the parent's supplied feedback;
  the illustrative fixtures above supplement, not replace, them. This is an
  evidence limitation, not an additional withheld finding.

## Limitations

* No implementation, static checks, units, browser execution, installs,
  commits, lock acquisition, Git network operation or remote mutation was
  performed by this critique.
* The assessment does not freshly verify the prior pull/rebase, external
  guideline retrieval, installed tools, axe bytes or manifest hashes;
  those remain claims/pointers in the supplied research until execution.
* Source was inspected only to substantiate the bounded planning concerns.
  This is not a fresh UI/accessibility, security or whole-repository review.
* The observed worktree already contained untracked plan, details, research
  and task-state artifacts. They were not altered or committed. This
  critique is the sole output authored by this assessment.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise P01-T01 with contextual boundary rules
  and discriminating expected-output fixtures; also settle P01-T02's
  helper-only null-session contract. Then finalize the plan and continue
  implementation and the single independent post-implementation Review.
* User response required: no.
* Preserve this original outcome unchanged. Record dispositions in the
  parent's plan/evidence; do not request a second critique pass.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md](.copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md) | Assessed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md](.copilot-tracking/details/2026-10-29/loading-briefing-review-538-phase-details.md) | Assessed implementation and validation details; unchanged. |
| [.copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md](.copilot-tracking/research/2026-10-29/loading-briefing-review-538-research.md) | Supplied primary research; unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-538-plan-critique.md) | Complete original single-pass critique; preserve immutably. |

## Next Steps

The active planning parent should apply PC-001 and PC-002 directly, preserve
this critique, and continue the authorized local-only RPI work. No user action
or additional plan critique is required.
