---
title: Case journey round seven independent Review
description: Single post-implementation assessment for task 526-round7
ms.date: 2026-10-29
---

## Opening Review State

* Task: 526-round7, seventh correction, PR #529, Refs #526.
* Interpreted goal: Assess outcome preservation, duplicate-dispatch barriers,
  causally fresh resource recovery and retained drafts across all named siblings.
* Scope: Complete uncommitted src/api diff against intake HEAD 815aa615;
  app.js, assistants.js, ops.js, panels.js, test_case_journey.py, both browser
  checks and API README; audit case-workspace.js without source mutation.
* Evidence readiness: Supplied canonical research, plan, details, sole critique,
  changes and state read. Final external validation supplied for inspection.
* Acceptance basis: Current plan acceptance criteria, PC-001 through PC-003
  dispositions and explicit user requirements; not cosmetic preferences.
* First comparison boundary: Complete diff and directly coupled shipped handlers,
  then named regression and final external validation evidence.
* Active read-only boundaries: Only this Review record may be written. No source,
  plan, details, changes, state, remote, Azure or private-data mutation/access.
* Initial blockers: None to bounded Review. Full publication gate and manual
  accessibility/staff acceptance remain separate coordinator-owned gates.
* Initial source diff SHA256:
  14b12fc8b83459e960adc9a8c39ea1e7302edec9439f78ab9c80a0fff4b2a746.
* Guidelines: Current full Web Interface Guidelines fetched on 2026-10-29 from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
  Repository Fluent, plain-language and ASCII conventions take precedence.

## Substantive Comparison State

* Complete supplied source/test/check/README diff read, plus directly coupled
  shipped handlers and the whole case-workspace.js audit boundary.
* Final supplied validation logs/results inspected; browser result/log hashes
  independently match the changes record.
* Bounded, in-memory Node reproductions using shipped JavaScript and the
  repository test DOM confirm two gaps: pending exclusion does not cover
  fieldless case actions or rebuilt raw resident/challenge forms; an old shared
  proposal-queue listing erases a blocked review draft.
* A separate procurement reconstruction probe also demonstrates local pending
  state resets on capacityView construction. This is not a separate finding:
  no ordinary same-view refresh control was established for that probe.
  Causal procurement recovery after an outcome is covered and assessed below.
* Review direction: Complete execution is feasible, but material duplicate
  dispatch and draft-loss findings require Not accepted and later implementation.

## Scope and Evidence

* Review date: 2026-10-29. Exactly one post-implementation Review.
* Intake HEAD: 815aa615cd319aaab6efdfc6e006534cde8471dc.
* Branch: feat/case-journey-ux-526, continuing PR #529 as supplied. No branch,
  commit, PR, thread or remote mutation performed.
* Compared artifacts: Canonical research, plan, phase details, sole critique,
  changes and state listed in the artifact table below.
* Source: Complete git diff HEAD -- src/api, eight changed files; directly
  coupled surrounding code and unchanged case-workspace.js.
* External final evidence root:
  /home/azureuser/.copilot/session-state/266fad4a-d7af-4dcd-8086-dac71170cbfd/files/round7-final.
* Project framing: Original case study, addendum, reference index and owner
  memory read. Memory is context, not correctness evidence.

## Execution Status

* Execution status: Complete.
* This means the bounded independent Review executed completely, not that every
  implementation requirement or publication/acceptance gate passed.
* No nested agent, heavyweight gate, Azure command, private dataset, secret or
  environment-file access. Bounded Node probes ran in memory without adding
  test/source files. Only this record was written.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Outcome preservation, shared barrier and sibling corrections | Reconciled | Exact outcome precedence and post-outcome barriers work; pending exclusion remains incomplete under RV-001. |
| P01-T02 | Four unit methods, extended matrices, two browser helpers and README | Reconciled | No removed methods/helpers; count limits met. Queue draft retention is not protected by the matrix; RV-002. |
| P02-T01 | Final unit, related, static and browser checks | Reconciled | External results match final source hash; automated passes do not resolve the uncovered cases. |
| P02-T02 | Sole Review next, then local retention/commit | Reconciled | Correctly unchecked at intake. This record supplies the sole Review; local retention/commit remains parent-owned. |
| Follow-Up Items | Complete publication gate and human/hosted approvals | Reconciled | Distinct coordinator work, not an implementation acceptance claim. |

## Completed Work Assessment

| Related marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | api preserves status/reasons/outcome. mutationNeedsHistory gives exact committed/uncertain precedence over 409/503 and conservatively blocks transport loss. Ordinary status-bearing refusal remains correctable. Shared refresh returns check-history after uncertain/committed responses and successful writes with failed confirmation reads. Persistent case generations reject pre-outcome reads in both completion orders, including after newer recovery. RV-001 limits pending exclusion. |
| P01-T01 | src/api/src/zava_forward/api/web/assistants.js | Proposal recovery requires a matching ID/revision state-object snapshot captured before the listing; ordinary card reconstruction cannot clear uncertainty. Invocation pending/history state is session-owned across panel replacement and post-outcome case reload. Queue listing does not retain local review fields; RV-002. |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | Draft review retains copyable text/reason and disables review actions without inventing approval. Priority failure no longer repaints away input; explicit refusal re-enables actions. Their deliberate full-workspace reload recovery matches the accepted resource-specific contract. |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | Upload preparation stays inside the form exclusion but outside outcome classification; only POST runs inside shared refresh. File-read failure has zero dispatch and remains retryable; ambiguous upload keeps the file and blocks repetition. |
| P01-T01 | src/api/src/zava_forward/api/web/ops.js | Procurement outcome-aware exclusion and persistent generations protect post-outcome package/order reload. Try again performs reads, never repeats fn. Quality retains its session-owned pending state and uses the corrected shared refresh. |
| P01-T01 | src/api/src/zava_forward/api/web/panels.js | Both raw resident/challenge families preserve input, handle structured uncertain/committed and transport loss, and establish the case generation barrier. Their pending state is still DOM-local; RV-001. |
| P01-T01 | src/api/src/zava_forward/api/web/case-workspace.js | Whole file inspected: projections, navigation, counts and observers; no api/fetch/POST mutation owner. No diff or gratuitous edit. |
| P01-T02 | src/api/tests/test_case_journey.py; src/api/checks/case_journey_browser_check.py; src/api/checks/assistants_browser_check.py; src/api/README.md | Actual shipped-handler/HTTP matrices cover outcome/status combinations, refusal correction, failed/old/fresh reads, retention and dispatch counts. Four added unit methods and one added helper per browser; no removals. README accurately describes intended recovery, but aggregate completion must remain qualified by RV-001/RV-002. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and reason | Evidence and reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01, PC-001 | Persistent case/procurement generations prevent ABA after barrier clearing; proposal snapshots bind recovery to state object and ID/revision | Current details and changes describe both completion orders; final unit matrices execute them | Plan-consistent refinement, not a significant/divergent decision. No new user choice or critique required. |
| P01-T01, PC-002 | File preparation precedes guarded POST under existing form exclusion | Details, upload source and added upload method agree | Applied; no false server-uncertainty barrier for local preparation failure. |
| P01-T02, PC-003 | Concrete ownership across existing matrices and four new unit methods | Current plan/details, AST method comparison and full diff agree | Assignment applied; behavioral omissions remain RV-001/RV-002, not a missing planning decision. |
| P02-T01 | Final raw-form and generation refinements triggered fresh final validation | Changes preserve initial failed fixture runs and earlier browser evidence separately from final logs | Final evidence attributed to unchanged final source, not historical bytes. |

## Critique and Material Revision Assessment

* Original sole critique remains Complete / Revise, with PC-001 High and
  PC-002/PC-003 Medium preserved. Current plan explicitly accepts all three.
* Causal resource-specific recovery and upload preparation changes are directly
  supported by that critique and preserve confirmed user intent.
* No material architecture, authority, dependency or design-system divergence
  found; no unaccepted decision requiring rpi-plan.
* No evidence of dependent work proceeding before its required reconciliation.
  Final validation follows the final source changes. The two defects below
  limit implementation acceptance, not the original critique's preservation.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Assessment |
| --- | --- | --- | --- |
| Exact-head complete publication gate and human/hosted approvals | Explicit no-Azure/no-publication Review boundary; complete gate requires az and cannot be substituted by scoped checks | Coordinator retains evidence, satisfies prerequisites and obtains approval before publication | Open, distinct follow-up; no receipt or publication readiness claimed. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Pending exclusion still permits duplicate case mutations

* Related scope: P01-T01/P01-T02, sibling audit and pending-order assessment.
* Source evidence: src/api/src/zava_forward/api/web/app.js:638-650 uses a
  submitted-field key only when fields exist. With submitted=[], key is null
  and neither the pending check nor registration runs. Fieldless controls such
  as installation advancement at app.js:741 call that path without disabling
  themselves. historyBarrier is established only after an outcome needs checking.
* Sibling evidence: src/api/src/zava_forward/api/web/panels.js:158 and :347
  check only the current button and the post-outcome session barrier. Neither
  raw form registers session-owned pending state. A case GET started/completed
  while the POST is pending passes app.js:621-624 because the generation has
  not changed, then constructs new enabled resident/challenge controls.
  Refresh proposals is an ordinary same-case route to that GET.
* Reproduction: Executed the shipped refresh with two immediate fieldless
  calls while holding its first mutation promise: dispatch count was 2.
  Executed each shipped raw-form factory, held its first fetch, rebuilt the
  same form against the same caseSession as an in-flight case reload does,
  and submitted again: dispatch count was 2 for both resident and challenge.
  Both deferred responses were then delivered as 503/uncertain. No
  authoritative post-outcome read occurred between the two POSTs.
* Test evidence: src/api/tests/test_case_journey.py:1057-1062 tests fieldless
  exclusion only after awaiting the first error; :413-420 retries the same raw
  DOM node, not a form rebuilt during the pending request. Thus the passing
  matrices do not cover either pending bypass.
* Impact: More than one request can already be in flight, and both can commit,
  before the new outcome barrier takes effect. A later correct check-history
  response cannot undo duplicate resident/challenge records or case actions.
  This is a retained gap in the explicitly audited behavior, not a claim that
  the new predicate itself is wrong.
* Destination: Later rpi-implement, within the accepted correction direction.
* Smallest useful next action: Keep action/resource pending identities outside
  replaceable DOM, including fieldless shared-refresh calls. A read initiated
  while the relevant mutation is pending must not reset that exclusion.
  Extend existing matrices to hold POSTs across same-case reload/reconstruction
  and prove exactly one POST, then preserve refused retry and authoritative
  post-outcome recovery.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: An old shared-queue listing erases the blocked review draft

* Related scope: P01-T01/P01-T02, proposal sibling old-read order and retention.
* Source evidence: src/api/src/zava_forward/api/web/assistants.js:225-239 captures
  recovery states but always rebuilds cards and replaces the shared queue.
  assistantProposal at :17-21 creates new reason/editor controls; unlike the
  case panel, the queue captures/restores no review-field draft. On the shared
  queue caseSession is normally null, so case pendingFields is not a fallback.
* Reproduction: Executed shipped assistantQueueView/assistantProposal with the
  repository DOM fixture. Entered a supplied reason, held Reject POST, began a
  queue listing, delivered 503/uncertain, then resolved that pre-outcome listing
  with the same ID/revision. Reject correctly stayed disabled, but the
  still-unconfirmed reason changed from the supplied text to empty before
  any authoritative recovery. The replacement JSON editor likewise comes
  from p.output rather than the person's edited draft.
* Test evidence: src/api/checks/assistants_browser_check.py:247-253 checks old
  listing exclusion but not retained fields; :265 explicitly expects an empty
  queue reason after the later uncertain recovery. The case-panel branch
  expects retention, so a passing browser run masks the queue-specific loss.
* Impact: A person loses their only copy of an unresolved review reason or
  edited proposal while instructed to check history. The old read does not
  establish commitment, refusal or permission to discard that draft.
* Destination: Later rpi-implement.
* Smallest useful next action: Preserve queue draft/recovery fields by proposal
  ID/revision through old, failed and authoritative listings without making
  stale reviews actionable or inventing approval. Update the existing browser
  helper to assert reason and edited JSON remain copyable after the old
  listing, including committed/uncertain and later edits.

## Defects and Routed Findings

| Finding | Severity | Destination | Next owner/action |
| --- | --- | --- | --- |
| RV-001 | High | rpi-implement | Implementation owner adds persistent pending exclusion and extends existing regression ownership. |
| RV-002 | Medium | rpi-implement | Implementation owner retains shared-queue review drafts across asynchronous listings. |

* Severity total: 0 Critical, 1 High, 1 Medium, 0 Low.
* No separate decision or research gap. Later implementation does not require
  this Review to run again; preserve this sole finding set and original outcome.

## Changed Web Guidelines Assessment

Current fetched rules assessed against all four changed behavioral web files.
Native action semantics, existing labels, live/status feedback, focused errors,
copyable inputs, existing focus behavior and ordinary refusal correction remain.
No new CSS, animation, image, layout, locale or framework surface was introduced.
Generic typography/title preferences do not override repository ASCII/plain
language/Fluent choices. Findings use the requested source-location format:

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:642 - RV-001: fieldless pending action has no exclusion; repeated dispatch remains possible.

### src/api/src/zava_forward/api/web/panels.js

src/api/src/zava_forward/api/web/panels.js:158 - RV-001: resident pending exclusion is lost when the form is rebuilt.

src/api/src/zava_forward/api/web/panels.js:347 - RV-001: challenge pending exclusion is lost when the form is rebuilt.

### src/api/src/zava_forward/api/web/assistants.js

src/api/src/zava_forward/api/web/assistants.js:235 - RV-002: asynchronous queue replacement discards unresolved review fields.

### src/api/src/zava_forward/api/web/ops.js

Pass for the changed post-outcome behavior; no additional substantive guideline finding.

## Validation Evidence

All supplied final validation follows the final source changes. This Review
inspected those receipts rather than rerunning heavyweight suites.

| Command/evidence | Status | Result and boundary |
| --- | --- | --- |
| Requested test_case_journey and test_workspace_scripts; units.log | Passed, supplied final evidence inspected | 25 tests, OK. Not an independent rerun. |
| Related accessibility/design/content, procurement and resident suites; related.log | Passed with existing skip, supplied evidence inspected | 67 tests, OK (skipped=1). Constructed rule-store-unavailable logging is retained, not an operational rules-service claim. |
| Owning Ruff at 100 columns; ruff.log | Passed, supplied evidence inspected | All checks passed. |
| Owning format; format.log | Passed, supplied evidence inspected | 51 files already formatted. |
| Owning mypy; mypy.log | Passed, supplied evidence inspected | 99 source files. |
| Five JS parse checks | Supplied pass only | Recorded in changes; no separate parse receipt in final root, not independently rerun. |
| Journey browser; journey/results.json and journey.log | Passed, hashes and counts verified | 259 PASS lines; 42 axe 4.10.3 states; zero violations/page errors; Chromium 156.0.8078.4; actual chrome.tabs.setZoom=2. |
| Assistants browser; assistants/results.json and assistants.log | Passed, hashes and counts verified | 173 checks/PASS lines; 40 axe 4.10.3 states; zero violations/page errors; Chromium 155.0.8059.39. |
| Bounded shipped-JS Node probes during this Review | Defects reproduced | Fieldless/raw-form duplicate pending dispatch and shared-queue draft loss; evidence described in RV-001/RV-002. One queue fixture attempt initially failed because its show stub did not filter undefined nodes; corrected to shipped show semantics before confirming RV-002. |
| AST comparison against HEAD | Passed, independently executed | Exactly four added unit methods and one helper per browser; no removed functions. |
| git diff --check; source hash; case-workspace.js diff | Passed, independently executed | No whitespace errors; unchanged final API diff hash; no case-workspace.js mutation. |
| Manual axe incomplete/contrast, screen reader and staff acceptance | Not performed | 41 journey and 39 assistant incomplete rule items remain; no WCAG or staff acceptance claimed. |
| Complete local publication gate/receipt; hosted and human approval | Not run/deferred | Outside this Review and explicit no-Azure boundary; coordinator-owned prerequisites remain. No receipt fabricated or inferred. |

Verified SHA256 values:

* Final API diff:
  14b12fc8b83459e960adc9a8c39ea1e7302edec9439f78ab9c80a0fff4b2a746.
* Journey results:
  6a30e6f88d2e546fa56dbda3049d46e73a8c5951c47a1aa523dacfff769fb30f.
* Journey log:
  bb070e84c1f1bdb8776beae634de92f14e423303f84ae9162b4ecadb9122568d.
* Assistants results:
  70ce45f7edecd3634bbb84ad0e86b51a837ba95ee7d6877b2055a3829988331a.
* Assistants log:
  695c66e41ae370257945d3a2b0d92a8acf7e8f9b1122177455c43673818c677f.

## Residual Work, Blockers and Remaining Work

* No blocker to execution of this Review.
* RV-001/RV-002 block acceptance of the correction as complete.
* P02-T02 local retention/commit remains with the parent, which must preserve
  this original outcome and keep task/changes/state truthful. No source or
  tracking artifact other than this record was modified by the reviewer.
* Publication gate, exact-head assessment, hosted/human approval and manual
  accessibility/staff evidence remain distinct coordinator follow-ups.
  They are not additional implementation defects or newly activated plan scope.

## Outcome

* Execution status: Complete.
* Outcome: Not accepted.
* Rationale: Outcome propagation and causally fresh post-outcome recovery are
  substantially implemented and tested. However, the named sibling audit still
  permits duplicate pending mutations, and shared-queue recovery loses
  unresolved draft values. Passing automated suites do not cover or negate
  these reproduced cases.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defects | rpi-implement | Parent routes RV-001 and RV-002 for later implementation, without rewriting this Review. |
| Decision gap or invalid assumption | None | No new owner choice required. |
| Material evidence gap | None | Supplied evidence plus bounded reproduction supports the verdict. |
| Non-blocking residual work | Distinct coordinator follow-up | Local retention, complete publication prerequisites, manual and hosted/human gates. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md](.copilot-tracking/research/2026-10-29/case-journey-526-round7-research.md) | Compared research and user direction |
| [.copilot-tracking/plans/2026-10-29/case-journey-526-round7-plan.md](.copilot-tracking/plans/2026-10-29/case-journey-526-round7-plan.md) | Compared current plan |
| [.copilot-tracking/details/2026-10-29/case-journey-526-round7-phase-details.md](.copilot-tracking/details/2026-10-29/case-journey-526-round7-phase-details.md) | Compared current contracts |
| [.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round7-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/case-journey-526-round7-plan-critique.md) | Original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-29/case-journey-526-round7-changes.md](.copilot-tracking/changes/2026-10-29/case-journey-526-round7-changes.md) | Compared implementation/final validation |
| [.copilot-tracking/rpi-sessions/2026-10-29/case-journey-526-round7-state.json](.copilot-tracking/rpi-sessions/2026-10-29/case-journey-526-round7-state.json) | Read-only intake state |
| [.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round7-review.md](.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round7-review.md) | Sole independent Review; Complete / Not accepted |

## Next Steps

The active parent should preserve this Review and route RV-001/RV-002 to later
rpi-implement, reconcile local retention/task state and retain the separate
publication and manual-acceptance gates. Do not run a second Review or infer
publication approval. No user action is required by this reviewer.
