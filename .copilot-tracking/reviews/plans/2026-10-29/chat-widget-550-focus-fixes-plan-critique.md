<!-- markdownlint-disable-file -->
# RPI Plan Critique: Chat focus review follow-up

## Metadata

* Task ID: 550-focus-fixes; parent task: 550.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique of this selected
  follow-up, not another critique of the original task.

## Inputs and Criterion Boundary

* Owner requirements: resolve RV-001/RV-002, preserve unobscured external keyboard
  focus, no asynchronous setup/reply focus theft, polite live updates,
  user-action-driven focus, regression tests and updated actual local browser
  evidence. Run the requested unittest, Ruff check/format, mypy, Node syntax and
  local-browser surfaces using the specified runtime/PYTHONPATH. No Azure,
  push or rubric edits; local commit with the requested trailer.
* Candidate inputs: the plan and phase details above;
  .copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md;
  .copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-focus-fixes-state.json.
* Original evidence:
  .copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-review.md and
  .copilot-tracking/changes/2026-10-29/chat-widget-550-changes.md, including the
  original command list and adverse Review. Neither is closure evidence.
* Actual source inspected: shared widget JS/CSS, employee adapter, resident
  assistant chat lifecycle, shared actual-app browser check, affected portions
  of existing employee/resident browser checks and test_chat_panel, Node VM
  test prior art and API validation configuration.
* Repository context: original case study, addendum, reference index and owner
  memory. Fresh canonical Web Interface Guidelines retrieved successfully from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
  Relevant rules require unobscured focus and polite asynchronous updates.
* Boundary: assess research credibility, requirements, dependencies, phases,
  acceptance oracles, test ownership/removals/limits, validation and local
  closeout once. This is not implementation Review, a browser reproduction,
  publication approval or accessibility conformance assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001; research Q1/C1 | Partial | Outside-focus hide(false) is appropriate; launcher exemption has an untested short-height counterexample, PC-001 |
| RV-002; research Q2/C2 | Covered | Remove both asynchronous focusInput calls; preserve explicit submit and synchronous disabling handoff |
| Polite live updates | Partial | Named polite log/status retained, but asynchronous failures still use an implicitly assertive alert, PC-003 |
| Access-loss focus ownership | Partial | Proposed ownership guard is appropriate; no explicit denial regression oracle, PC-004 |
| P01-T01 lifecycle/dependencies | Covered | Hide retains requests/state, dispose unregisters the listener, current-operation fencing remains intact |
| P01-T02 test ownership/removals/limits | Partial | One bounded new Node VM module, subprocess timeout, canonical sources and no removals are explicit; existing employee check needs authorized migration, PC-002 |
| P02-T01 local validation | Partial | Required surfaces and original commands are discoverable; affected employee browser run must be mandatory, PC-002; storage/runtime constraint needs disposition, PC-005 |
| P02-T02 Review/local commit | Covered | One selected-follow-up independent Review, original adverse outcome preserved, closure conditional on evidence, privacy-safe identity and trailer, no push |
| Out-of-scope/residual work | Covered | Original mobile summary baseline, human accessibility/live acceptance and publication gates remain separate |

## Verdict

* Verdict: Revise.
* Rationale: the core two-defect approach is credible, but the stated launcher
  exemption does not guarantee unobscured focus on an existing responsive
  surface. Test migration, asynchronous error announcements and denial coverage
  also need explicit corrections. Resolve the validation-path constraint before
  treating the planned commands as executable. Five Medium findings; no
  Critical, High or Low findings. No additional critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: The launcher exception can retain an entirely obscured focus target

* Related IDs: RV-001, research Q1/Contrarian, P01-T01, P01-T02.
* Evidence:
  .copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md:13-17
  exempts the launcher unconditionally; the focused research says it cannot be
  obscured. src/api/src/zava_forward/api/web/chat-widget.css:1-2 gives launcher
  and popup the same z-index, while :31 moves the popup down to the small bottom
  spacing at max-height:35rem. The factory appends launcher before root in
  src/api/src/zava_forward/api/web/chat-widget.js. The existing browser layout
  sweep uses height 900; the new concrete reproduction uses height 800.
* Concern: at a short desktop viewport such as 1280x500, the wide popup occupies
  the launcher's bottom-right rectangle and is later in paint order. Reverse
  Tab from the heading can focus that launcher without hiding the popup.
  The research premise is therefore unsupported for an existing CSS breakpoint.
* Impact: the proposed fix leaves a concrete RV-001-class keyboard obstruction
  outside the one signed-out 320x800 reproduction.
* Smallest useful change: add the short-height launcher case and plan a bounded
  stacking/layout correction that keeps the focused launcher above/outside the
  popup, or an equivalent dismissal solution that preserves single-click
  toggling. Do not introduce production geometry reads or a modal trap.
  Clarify that external-exit hiding excludes only a demonstrably visible launcher.
* Action owner: planning parent; implementer owns the source/test correction.
* Exact resolving evidence: revised P01 tasks authorize the bounded correction;
  actual-app checks at 1280x500 in both audiences focus the launcher using
  keyboard traversal, verify a visible in-viewport hit point belongs to it,
  preserve focus and prove a single launcher activation toggles correctly.
  Retain the 320x800 Sign in regression and existing layout checks.
* Decision route: direct planner correction; no new user decision or visual
  redesign is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Existing employee acceptance asserts the async focus behavior being removed

* Related IDs: RV-002, P01-T02, P02-T01; test ownership/removals/limits.
* Evidence: src/api/checks/employee_chat_browser_check.py:155-162 opens chat
  using keyboard activation and expects the question to become focused after
  asynchronous setup. The proposed removal leaves the synchronously focused
  heading instead. The plan :36-38 and :77-83 confines browser work to the
  shared check and says preserve every prior assertion; :95-96 makes audience
  checks conditional on being directly affected.
* Concern: this existing employee check is already directly affected and must
  fail under the intended focus behavior unless its obsolete oracle is migrated.
  Literal preservation of that oracle contradicts RV-002.
* Impact: implementation cannot satisfy the plan's test restrictions and retain
  a green, truthful existing employee-browser result simultaneously.
* Smallest useful change: explicitly include the existing employee checker in
  permitted test edits and mandatory validation. Replace only the obsolete
  post-setup input-focus expectation with heading/current-focus preservation,
  then explicitly choose the input before subsequent typing as needed.
  Preserve the test's keyboard entry, six skills, fallback, denial and lifecycle
  coverage. Keep the one-new-unit-module limit; record this as an oracle
  migration, not a removed regression.
* Action owner: planning parent.
* Exact resolving evidence: P01-T02 names ownership of the existing checker and
  the exact migrated expectation; P02-T01 mandates its command. Changes evidence
  records the old/new assertion, rationale and passing updated employee and
  shared actual-app runs.
* Decision route: direct planner correction; owner direction already requires
  removing asynchronous focus theft.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Polite log/status do not make asynchronous failures polite

* Related IDs: polite-live-update requirement, P01-T01, P01-T02.
* Evidence: src/api/src/zava_forward/api/web/chat-widget.js:56 creates the
  shared error with role="alert" and no explicit polite setting; fail() updates
  that node. src/api/src/zava_forward/api/web/chat.js invokes fail() for setup
  and send failures; the resident adapter does likewise for current reply
  failures. Plan :49-50 preserves existing errors and details :35-40 asserts
  updates without specifying an error live-region oracle.
* Concern: role="alert" has implicit assertive live behavior. Keeping the
  existing polite log/status alone does not establish the requested polite
  asynchronous updates on failure.
* Impact: error completion can still interrupt assistive-technology output even
  after keyboard focus theft is fixed.
* Smallest useful change: specify explicit polite semantics for asynchronous
  setup/reply error updates while retaining visible inline text, descriptions
  and user-action validation focus. Define the error announcement assertion,
  including any affected role-based test selectors; do not silently drop error
  coverage.
* Action owner: planning parent.
* Exact resolving evidence: revised P01 details identify the intended live
  semantics; behavioral/actual-app assertions cover setup and current reply
  rejection with polite error semantics, visible retained errors/draft and
  unchanged chosen focus. Record that DOM/browser checks are not a human
  screen-reader acceptance result.
* Decision route: direct planner correction under the owner's polite-update
  requirement, not a request for a new accessibility policy.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The changed access-loss guard lacks an explicit regression contract

* Related IDs: external-focus requirement, P01-T01, P01-T02.
* Evidence: src/api/src/zava_forward/api/web/chat.js:59-63 currently disposes
  the widget and calls app.focus() unconditionally. Details :19-20 proposes
  retaining recovery only for removed popup-owned focus. The new test matrix
  names held generic success/rejection, but not authorization-denial statuses.
  Existing shared-check denials assert disposal only; the employee checker
  :250-277 expects app focus with focus initially inside the popup.
* Concern: generic rejected promises do not exercise deny(), which branches on
  401/403/404. Existing denial assertions cannot detect stealing deliberately
  external or surviving-launcher focus.
* Impact: a tightly coupled focus path specifically changed by this plan could
  regress unnoticed, or be overcorrected so removing a focused popup loses its
  necessary recovery target.
* Smallest useful change: add bounded denial regressions in the owned Node VM
  module/shared browser harness. Cover a current admission/send denial after
  deliberate external focus and visible launcher focus, plus popup-owned focus
  before disposal. Include 403/404 and separately handle the actual 401 session
  transition without changing authentication authority or its existing tests.
* Action owner: planning parent.
* Exact resolving evidence: P01-T02 explicitly identifies deny() outcomes and
  expected targets. Tests prove external/surviving launcher focus is unchanged,
  popup removal recovers focus only when it owned focus, and existing session
  expiry/access denial behavior remains intact.
* Decision route: direct planner correction; no new user decision.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validation locations need an explicit executable-environment disposition

* Related IDs: P01-T02 negative proof, P02-T01 validation.
* Evidence: details :29-30 requires external baseline storage, :48 requires
  /tmp/mv; plan :96 requires output outside the repository. This assessment's
  execution environment prohibits /tmp file operations and requires created
  scratch/evidence files to be repository-relative. The owner's requested
  /tmp/mv runtime is a confirmed requirement, not permission to override an
  execution restriction.
* Concern: the candidate describes those paths as immediately executable without
  acknowledging the conflicting execution constraints.
* Impact: an implementer may either violate the environment restrictions or
  silently substitute tooling/storage and misreport the owner's exact requested
  validation as completed.
* Smallest useful change: explicitly record the location/runtime constraint.
  Use permitted repository-relative ignored evidence storage where authorized;
  preserve historical external-evidence pointers. Establish a permitted,
  existing equivalent runtime only through the appropriate authorization, or
  mark the exact /tmp/mv checks blocked. Do not access prohibited locations,
  install/recreate an environment merely to evade the restriction, or claim
  equivalent commands satisfy an unmet exact-runtime requirement.
* Action owner: planning parent for the constraint/disposition; owner or
  execution-environment authority only if a runtime requirement change is needed.
* Exact resolving evidence: a revised validation section gives permitted paths
  and authorized runtime provenance, or clearly records the blocked commands
  and resulting unmet validation. Actual command/results evidence must match
  whichever disposition is authorized before claiming full local validation.
* Decision route: direct planner correction to disclose and respect the blocker.
  A significant user/environment decision is needed only to change the exact
  runtime requirement or execution authorization; no response is needed merely
  to revise the plan and retain an honest blocked status.

## Strengths and Residual Risk

* The focusin/hide(false) approach retains in-flight work, drafts/history and
  thread state without coupling focus management to cancellation.
* Removing setup/finally focusInput, rather than merely checking visibility,
  correctly protects deliberately chosen internal controls and the launcher.
  Current versus obsolete work is explicitly distinguished.
* Exact signed-out resident reproduction, reverse/forward traversal, current
  controlled promise completion, negative baseline proof, disposal cleanup,
  one bounded new unit module and preserved existing safety assertions are
  substantive test commitments.
* P02 depends on P01. One independent follow-up Review, conditional closure
  evidence, original adverse Review preservation and a local-only privacy-safe
  commit are appropriate. New findings must remain routed honestly rather than
  becoming unreviewed corrections or a second original Review.
* Human accessibility/live-service acceptance, existing unrelated mobile page
  height failure and all publication gates remain outside this task. This
  critique does not accept or close those risks.

## Questions or Blocking Evidence Gaps

* No unresolved product-design choice prevents direct correction of PC-001
  through PC-004.
* PC-005 requires an explicit execution disposition before claiming the exact
  requested validation is available. The parent can revise without asking the
  user; changing confirmed runtime requirements requires the relevant authority.

## Limitations

* Source-based assessment only. No test, browser, /tmp/mv command, Azure
  operation, dependency installation, commit, push or rubric edit was performed.
* The short-height launcher concern is grounded in checked-in stacking, DOM
  order and breakpoint rules; it is not represented as a fresh browser result.
  Implementation must verify it in the actual apps.
* The fetched web guidelines were applied to the supplied focus/live-update
  boundary. This is not an unrelated whole-site style/accessibility audit.
* Worktree inspection found the selected topic branch feat/chat-widget-550 and
  existing untracked follow-up inputs. They were left untouched. Only this
  requested critique artifact is written.

## Recommended Next Action

* Highest-impact finding: PC-001, because the proposed exemption can leave the
  motivating external-focus obstruction unresolved at an existing breakpoint.
* Action owner: planning parent.
* Smallest next action: directly revise the plan/details with the short-height
  launcher oracle and bounded correction, then disposition PC-002 through
  PC-005 in the same revision. Preserve this complete original critique.
* User response required: no for planner corrections; only a subsequent change
  to the exact runtime requirement/authorization would require a decision.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md) | Assessed follow-up candidate |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md) | Assessed implementation/test details |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-focus-fixes-research.md) | Focused research |
| [.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-review.md](.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-review.md) | Preserved original adverse Review |
| [.copilot-tracking/changes/2026-10-29/chat-widget-550-changes.md](.copilot-tracking/changes/2026-10-29/chat-widget-550-changes.md) | Original validation commands/evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-focus-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-focus-fixes-plan-critique.md) | This single independent critique |

## Next Steps

Active planning parent: disposition all five findings directly and finalize the
selected follow-up plan without commissioning another critique. No user action
is required for those corrections. Resolve or explicitly retain the validation
execution blocker before claiming its checks complete. This critique stops here;
it does not invoke implementation, Review or any other stage.
