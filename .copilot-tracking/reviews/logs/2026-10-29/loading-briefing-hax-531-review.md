---
title: Loading and HAX briefing review
description: Original single post-implementation Review for issue 531
ms.date: 2026-10-29
---

## Scope and Evidence

* Task: #531, loading-briefing-hax-531.
* Scope: full P01-P03 implementation against issue requirements and accepted plan.
* Assessed baseline: local parent anchor
  6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c, current staged/unstaged candidate.
* Plan: .copilot-tracking/plans/2026-10-28/loading-briefing-hax-531-plan.md
* Details: .copilot-tracking/details/2026-10-28/loading-briefing-hax-531-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/loading-briefing-hax-531-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-28/loading-briefing-hax-531-changes.md
* Research: .copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md

## Opening Review State

* Goal: independently compare implemented loading/action/briefing behavior,
  retained authority/manual paths, accepted critique and actual evidence once.
* Readiness: P01-P03 markers/details/changes reconciled; full API discovery
  passed 1178 tests with 316 environment-dependent skips; required browser
  checks, new loading/axe and additional assistant/design checks passed.
* Acceptance basis: explicit #531 request, latest comment, plan acceptance and
  PC-001/PC-002/PC-003 dispositions. HAX/Fluent are pattern references only.
* First boundary: full source diff and new source files, relevant existing
  helpers, owned synthetic evidence and declared publication limitations.
* Read-only: source, plan, details, research, critique and changes are frozen.
  Only this canonical Review record may be written during assessment.
* Initial blockers: no-az prevents complete publication gate; refreshed parent
  PR #529 ancestry differs from the original local anchor. Neither is waived.
  No deployed, SQL Server, human assistive-technology or usability acceptance.
* Web guidelines: source freshly retrieved immediately before Review on
  2026-10-29; repository ASCII/sentence case/Fluent requirements take precedence.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent post-implementation assessment on
  2026-10-29, covering P01-P03, the complete tracked diff against the supplied
  anchor and the four explicitly named untracked source/test/check files.
* This is the original Review, not a critique or a repeated assessment. No
  source correction, commit, push, remote mutation or agent dispatch occurred.
* Implementation execution and acceptance are separate: completed phase markers
  describe performed work, not satisfaction of every acceptance criterion.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Static shell, shared action lifecycle, direct listeners, appointment/quality promises, map regional feedback | Reconciled | Scope and implementation inventory match. Action-specific live feedback has RV-002. |
| P02 / P02-T01 | Final-output statement references, preparation time, mode choice, conditional reviews, local dismissal | Reconciled with defects | Normal-path behavior matches; immutable template attribution and briefing draft retention have RV-001 and RV-003. |
| P03 / P03-T01 | Existing and new unit/browser checks, axe/reflow, regression migrations, component/KB documentation | Reconciled | Reported checks cover the agreed local synthetic boundary, not the defects' additional scenarios or publication acceptance. |
| Critique dispositions | PC-001/002/003 accepted before implementation | Reconciled | No second critique, unaccepted scope expansion or requirement deletion found. PC-002's invariant remains incomplete under concurrent edits. |
| Follow-Up Items | Human/deployed checks remain outside local acceptance | Reconciled | Open, explicitly unperformed; distinct owner follow-up RV-004. |
| Handoff/publication | Local commit permitted; complete gate and refreshed parent ancestry blocked | Reconciled | Publication is not claimed. This Review assesses only the original local-anchor candidate. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/index.html; src/api/src/zava_forward/api/web/workspace-shell.js | Static HTML feedback, independent 4s/15s watchdog and reload; remove startup when session/login is usable | Full new shell and index inspected; existing script-recovery implementation retained | Owned held/failed-script and service-retry browser evidence reported passed | Meets delivered-HTML boundary; not ingress or deployed cold-start acceptance |
| P01-T01 | src/api/src/zava_forward/api/web/async-action.js; src/api/src/zava_forward/api/web/app.js | Immediate text, delayed spinner, pending-control deduplication, owned disabled-state cleanup and errors | Entire new helper and changed central/direct integrations inspected | Actual-helper controlled-clock unit and real draft/appointment/law/map browser evidence reported passed | Lifecycle is broadly implemented; form announcement topology needs RV-002 |
| P01-T01 | src/api/src/zava_forward/api/web/ops.js; src/api/src/zava_forward/api/web/timecapture.js; src/api/src/zava_forward/api/web/law.js; src/api/src/zava_forward/api/web/law.html; src/api/src/zava_forward/api/web/style.css | Return mutation/redraw promises, adapt standalone law actions, regional map state, reduced motion and non-colour feedback | Changed callbacks, script order and applicable styling inspected | Required recovery and additional design/assistant checks reported passed | No dropped promise found in the changed adapters; no automatic write retry or framework migration |
| P02-T01 | src/core/src/zava_forward/core/ai_tasks.py; src/core/src/zava_forward/core/store.py | Preserve declared references, filtered output and UTC generation time; add rules fragments | Finish/analyse/statement extraction, cache and briefing generation inspected | Added AI-task tests and existing continuity suites reported passed | Normal/filter/quarantine/cache paths addressed; concurrent rules-fallback snapshot mismatch reproduced, RV-001 |
| P02-T01 | src/api/src/zava_forward/api/web/app.js | AI/rules label, declared-source case links, ranking/time explanation, hide/show, plain mode and conditional review | Changed aiBox/aiNotes plus draft-retention dependencies inspected | Required briefing/journey and new loading evidence reported passed | Draft-only authority and server source checks retained; new refresh discards unsaved review fields, RV-003 |
| P03-T01 | src/api/tests/test_loading_feedback.py; src/api/tests/test_ai_tasks.py; src/api/tests/test_case_journey.py; src/api/checks/loading_briefing_browser_check.py; src/api/checks/employee_briefing_browser_check.py; src/api/checks/case_journey_browser_check.py; src/api/checks/workbench_browser_check.py | New timing/lifecycle/provenance checks; migrate existing reveal/submit/mode assertions without deleting checks | Both new files explicitly read in full; changed existing assertions compared | Supplied focused/full/API/browser results assessed below | Tests are meaningful but do not cover the three reported defects |
| P03-T01 | src/api/README.md; docs/reference/README.md; docs/reference/log.md; docs/reference/research/ux/design-system.md | Describe native patterns, boundaries and commands; update KB index and append-only log | Complete documentation diff inspected | Link destinations and diff reviewed; git diff --check passed during Review | Related documentation reconciled; broad behavior claims remain subject to RV-001/002/003 |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 integration inventory | Include law, appointment mutation, map background reads and additional quality/overview returned promises | PC-001 and implementation source trace; preserves the already confirmed all-employee-action direction | Plan functional requirements, details inventory and changes P01/amendments agree | Compatible correction accepted before implementation; no new decision required | Justified, within scope |
| P02 final-output metadata | Whole-bullet filtering, quarantine attribution, scoped source IDs and stable timezone-bearing preparation time | PC-002 and actual source/publication/cache behavior | Plan requirements, P02 details and changes describe the invariant | Compatible correction accepted; no authority or framework change | Direction justified; RV-001 identifies a remaining implementation defect, not an unaccepted plan decision |
| P03 regression migrations | Separate reveal/submit in journey tests; update mode/status selectors in workbench tests | PC-003 and preserved failing old-selector runs | Test ownership/budget, details and changes reconcile all affected existing tests | Compatible correction; no tests removed | Justified; delayed dispatch, later edits, cancel/reopen and external resident payload assertions retained |
| P03 startup/visual corrections | Remove completed startup placeholder, avoid loading pseudo-content changing button names, suppress empty warning glyph | Preserved browser failures and bounded visual QA | Changes record identifies failures/corrections and final reruns; current code agrees | Implementation corrections, not a new material direction | Historical corrected failures are not current defects |
| Research/design note | Requested UX agent returned questions; parent supplied an evidence-labelled HAX note instead | Recorded participation result; no user research claimed | Research, changes and API guide state the limitation consistently | No replacement delegation or framework adoption; accepted native direction unchanged | Justified delivery-method divergence, not validated staff research |
| Handoff | Clarify phase completion versus Review/publication; preserve refreshed-parent divergence | Local test completion and supplied fresh remote inspection | Plan, details and changes agree | No rebase/merge/rewrite authorized or performed | Local-only assessment is credible; no fresh-parent acceptance inferred |

## Critique and Material Revision Assessment

* Original critique outcome remains Revise: 0 Critical, 1 High, 2 Medium, 0 Low.
  PC-001/002/003 each have a compatible accepted disposition in the plan.
* PC-001: expanded inventory and actual appointment/law/map checks were
  implemented within the permitted addition budget. RV-002 concerns semantics
  of the shared feedback, not absence of those adapters.
* PC-002: normal, unresolved, dropped-bullet, zero-case, cache timestamp and
  quarantine paths have direct tests. However, the rules-fragment enrichment
  reads mutable cases after generation rather than the published snapshot.
  RV-001 is the remaining defect against this accepted invariant.
* PC-003: existing journey browser and Node tests now reveal, fill and submit
  separately, preserving delayed immutable dispatch and later-value safeguards.
  The new check also exercises cancel/reopen and external resident draft text.
* No significant implementation decision was found that contradicts confirmed
  intent or requires retrospective authorization. No dependent-work resumption
  before the recorded critique dispositions was evidenced.
* Descriptive implementation-time updates are reconciled. The current checked
  markers can stand as execution history; they must not be used as acceptance
  while the material findings below remain.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Human screen-reader and voice-control checks | Synthetic DOM/axe/keyboard evidence is not assistive-technology acceptance | Accessibility owner tests representative startup, form feedback, sources and review choices with actual AT | Open; RV-004, distinct follow-up, not a newly added phase task |
| Staff usability | No employee study or validated staff research supplied | Product/research owner observes staff using the changed flows | Open; RV-004, distinct follow-up |
| Deployed employee cold start | Local delivered-HTML/script/API fixtures cannot establish host ingress or deployed behavior | Deployment/operations owner verifies the authorized employee site | Open; RV-004, distinct follow-up |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Rules statement metadata can describe different output from the published draft

* Related scope: P02-T01; PC-002 final-output invariant.
* Evidence: src/core/src/zava_forward/core/store.py:744-760 captures live case
  objects and prepares the template before the model/fallback call.
  src/core/src/zava_forward/core/store.py:767-775 subsequently rebuilds statement
  text and references from those same mutable objects. The new browser renders
  statements at src/api/src/zava_forward/api/web/app.js:448-451 rather than the
  published text. _case returns the stored object at
  src/core/src/zava_forward/core/store.py:1027-1032; existing case-return logic
  updates it in place at src/core/src/zava_forward/core/workflows.py:129.
* Independent reproduction: Python executed the actual AST-extracted
  Store.briefing method with one constructed case and stubbed collaborators,
  simulating an in-place case update during a completed rules fallback. The
  returned text and flat citations remained "survey booked, 3 days"; the new
  statement and its references said "design in progress, 1 days". Assertions
  proved the statement was not in the published text and references differed.
  This isolates snapshot behavior; it is not a real threaded-store/SQL test.
* Impact: a normal slow-AI fallback concurrent with employee case work can show
  a different draft and source attribution from the saved shown_output and
  review payload. Metadata can retain verified=True despite never validating
  its new references. The retained server freshness check still protects
  review authority, but does not repair this misleading display.
* Destination: rpi-implement.
* Smallest useful next action: capture the rules statement fragments and their
  references from the same immutable snapshot as the template, before releasing
  the lock; enrich only the matching final template result. Add a deterministic
  delayed-fallback/concurrent-case-change regression comparing published text,
  statement text, references and saved review output. Preserve quarantine rules.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Action-specific progress is placed inside its own busy subtree

* Related scope: P01-T01 polite action announcements; P02 briefing loading.
* Evidence: src/api/src/zava_forward/api/web/async-action.js:13 appends a form's
  role=status node inside that form, then :47-49 marks the form aria-busy=true.
  On success :56-65 removes the status before clearing busy. Similarly,
  src/api/src/zava_forward/api/web/app.js:462-463 marks the whole briefing busy
  before updating its descendant live status.
* Impact: aria-busy allows AT to defer changes within the busy container.
  The required action-specific working message can therefore be withheld
  throughout the wait and removed before it becomes announceable. Generic
  "Loading workspace data" outside the form is not the promised action text,
  and does not exist in the standalone law viewer's get helper. Attribute
  presence and zero axe violations do not establish this announcement behavior.
  This is a source-level semantic defect; no empirical screen-reader failure
  or general accessibility-conformance result is claimed.
* Destination: rpi-implement.
* Smallest useful next action: keep the action/briefing progress announcer
  outside the busy subtree, or scope busy to the separate updated controls/
  content. Retain the disabled/deduplication behavior and immediate text.
  Add a structural regression for form submissions and briefing refresh;
  actual AT confirmation remains the separate RV-004 follow-up.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: The new Refresh briefing action silently discards unsaved review edits

* Related scope: P02-T01 draft retention and correction; P03 regression coverage.
* Evidence: src/api/src/zava_forward/api/web/app.js:454 adds Refresh briefing
  beside aiNotes. Its load path calls paint at :467, whose :440 replacement
  destroys the existing editor/reason; the error path also replaces content
  at :471. There is no dirty-value check, preservation or confirmation in this
  path. Existing input bookkeeping at :936-938 applies only with caseSession,
  which is absent in the briefing queue.
* Independent reproduction: Node executed the actual aiNotes/aiBox source
  with a minimal in-memory DOM and an identical synthetic briefing response.
  After choosing Edit this draft and entering a replacement and reason,
  Refresh briefing detached both field nodes; the new editor reverted to
  "Original synthetic briefing" and the new reason became empty. Assertions
  confirmed two reads and loss of both values without a confirmation guard.
  This is isolated DOM logic, not browser, navigation or AT acceptance.
* Impact: an ordinary newly provided action loses employee correction work,
  contrary to the accepted draft-retention requirement. This finding concerns
  the new refresh path; the underlying case-only bookkeeping and older mode
  reload weakness are inherited context, not a separate legacy audit finding.
* Destination: rpi-implement.
* Smallest useful next action: protect briefing-local unsaved editor/reason
  values before refresh replaces them, with explicit discard confirmation or
  retained copyable values bound to the old evidence. Do not silently attach
  edits to a different record; prevent refresh from replacing a pending review.
  Add success/failure refresh regressions alongside existing cancel/reopen tests.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Human and deployed acceptance remains distinct follow-up work

* Related scope: plan Follow-Up Items; changes remaining work.
* Evidence: the canonical plan, details and changes explicitly leave
  screen-reader, voice-control, staff usability and deployed employee cold-start
  verification unperformed. SQL Server acceptance is also unperformed and
  cannot be inferred from environment-dependent unit skips.
* Impact: local engineering evidence does not establish those acceptance
  claims. This is acknowledged residual work, not a new implementation defect,
  a research blocker to this local Review, or permission to expand P01-P03.
* Destination: distinct follow-up owners.
* Smallest useful next action: accessibility owner performs actual AT checks;
  product/research owner performs staff usability; deployment/operations owner
  verifies authorized deployed cold start; SQL/data-store owner validates the
  SQL Server environment when authorized. Preserve each unperformed status
  until its own evidence exists.

## Defects

* RV-001: published rules output and new statement metadata can diverge;
  rpi-implement.
* RV-002: action-specific live feedback can be deferred by its busy ancestor;
  rpi-implement.
* RV-003: new briefing refresh destroys unsaved correction/reason values;
  rpi-implement.
* No Critical finding, authority bypass, unaccepted framework migration or
  material decision gap was identified in the supplied boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Core/briefing implementer freezes output-aligned rules metadata and adds a race regression | Defect within the accepted PC-002 direction |
| RV-002 | rpi-implement | Native UI implementer separates announcers from busy subtrees | Defect within the accepted polite-progress direction |
| RV-003 | rpi-implement | Briefing UI implementer guards refresh and preserves correctly bound local edits | Defect within accepted draft retention |
| RV-004 | Distinct follow-up | Accessibility; product/research; deployment/operations; SQL/data-store owners, as individually scoped above | Explicitly deferred human/live/environment acceptance |

Later implementation of routed defects does not require this original Review
to run again. Preserve its findings and outcome; record subsequent corrections
in later implementation evidence. A materially different reconciled publication
candidate still needs its own exact-candidate assessment under repository gates.

## Web Interface Guidelines Assessment

Fresh source retrieved successfully on 2026-10-29:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed changed web behavior and applicable surrounding semantics, with the
entire two new scripts read. These grouped results are source review plus the
supplied bounded synthetic evidence, not a fresh browser or AT review.

### src/api/src/zava_forward/api/web/async-action.js

* src/api/src/zava_forward/api/web/async-action.js:13 - RV-002: form progress
  status is inside the subtree marked busy at :49.
* src/api/src/zava_forward/api/web/async-action.js:8-22 - pass: polite atomic
  status, text accompanies decorative spinner, delay is 200ms.
* src/api/src/zava_forward/api/web/async-action.js:34-69 - pass: deduplicates
  control promises, disables pending control, retains handler-owned disabled
  changes, surfaces uncaught errors with recovery text.

### src/api/src/zava_forward/api/web/workspace-shell.js

* src/api/src/zava_forward/api/web/workspace-shell.js:8-22 - pass: bounded
  timers, explicit wait/retry/support copy, native reload control; no new
  gesture-only interaction or automatic write retry.

### src/api/src/zava_forward/api/web/app.js

* src/api/src/zava_forward/api/web/app.js:440 - RV-003: replacing briefing
  content discards local review input without warning.
* src/api/src/zava_forward/api/web/app.js:462 - RV-002: briefing progress live
  status is inside its own busy region.
* src/api/src/zava_forward/api/web/app.js:336-406 - pass: labelled uncontrolled
  textareas, meaningful names/autocomplete, explicit choices, required reason
  error linked and focused, conditional fields and native button semantics.
* src/api/src/zava_forward/api/web/app.js:431-451 - pass: source case whitelist,
  encoded native navigation links, Intl preparation time/counts, explicit
  unresolved/absent-source messages; RV-001 qualifies server data alignment.
* src/api/src/zava_forward/api/web/app.js:426-429 - pass: reversible local
  hide/show, no audit deletion or approval implied.

### src/api/src/zava_forward/api/web/index.html

* src/api/src/zava_forward/api/web/index.html:12-18 - pass: delivered-HTML
  static status, labelled retry, noscript guidance, watchdog before dependencies.
* src/api/src/zava_forward/api/web/index.html:11 - pass: retained skip link;
  startup placeholder is removed rather than leaving a second completed h1.
* src/api/src/zava_forward/api/web/index.html:20,24 - legacy: image dimensions
  are not HTML attributes; existing CSS reserves logo/avatar sizes. Unchanged,
  not introduced by this increment and not a new RV finding.

### src/api/src/zava_forward/api/web/style.css

* src/api/src/zava_forward/api/web/style.css:27-37 - pass: overflow wrapping,
  minimum widths, readable large fields, transform-only progress animation,
  reduced-motion static variant and text/non-colour progress.
* src/api/src/zava_forward/api/web/style.css:45,48,238-245 - pass: retained
  hover/visible-focus and native disabled/error styling; no transition:all or
  removed focus outline introduced.

### src/api/src/zava_forward/api/web/ops.js

* src/api/src/zava_forward/api/web/ops.js:87,116,321 - pass: initial checklist
  text and returned quality/appointment promises; actual appointment submit
  scenario is retained. Shared form announcements remain subject to RV-002.

### src/api/src/zava_forward/api/web/timecapture.js

* src/api/src/zava_forward/api/web/timecapture.js:15-29 - pass: native actions
  await mutation and redraw so the shared lifecycle covers the whole action.
  No new approval, data-entry, styling or navigation authority.

### src/api/src/zava_forward/api/web/law.js

* src/api/src/zava_forward/api/web/law.js:22,42,62,69-71 - pass: direct native
  actions adapted, returned requests observed, failure gives explicit recovery;
  form-specific announcements remain subject to RV-002.

### src/api/src/zava_forward/api/web/law.html

* src/api/src/zava_forward/api/web/law.html:22-27 - pass: initial polite source
  status and shared helper loaded before standalone script.
* src/api/src/zava_forward/api/web/law.html:18 - legacy: search input lacks a
  meaningful name; labelled and autocomplete=off already existed. Not a new
  field or an expanded form audit.

### Applicable-rule coverage and exclusions

* Accessibility, keyboard/semantic controls, labels, focus, async status and
  form validation were assessed above. No new icon-only unnamed controls,
  paste blocking, autofocus, zoom prohibition or clickable div/span introduced.
* Animation, reduced motion, non-colour states, long/empty content, native
  uncontrolled inputs, locale formatting and actionable copy were assessed.
  The spinner is task-progress motion, not decorative autoplay media.
* Images/CDN/fonts/media, large-list virtualization, layout-read batching,
  gestures/drag, modal scrolling, notched full-bleed layout, dark theme and
  hydration introduce no new applicable mechanism in this increment. Existing
  generic touch/highlight, image and unrelated list conventions are not
  represented as newly fixed or accepted.
* Case navigation retains real anchors. Citation disclosures and local
  dismissal are transient local controls, not new routes or destructive record
  actions. RV-003 is the material unsaved-state exception.
* Repository plain ASCII, sentence case and owner-selected Fluent tokens
  override generic curly typography, ellipsis and Title Case preferences.
  No React migration or claim of complete Fluent adoption is supported.

## Residual Work

* RV-004 preserves individually owned human/live/SQL checks, outside active
  phase completion. No source fix or research synthesis can substitute for them.
* Publication coordination is an already declared handoff blocker, not another
  newly discovered implementation defect or a decision forced into P01-P03.

## Blockers and Remaining Work

* Publication: full tools/rpi-checks.py --all requires az, prohibited by the
  user. No complete receipt exists; no partial receipt, cloud fallback,
  protection change, push or PR is authorized by the local passes. Local commit
  handoff is allowed by the supplied direction, but was not performed here.
* Lineage: supplied fresh inspection reports origin/main
  9bfed51863b05a25e9939d82504c576524688e14 and OPEN PR #529 parent
  73e365e618d8cf701a12434e4cd0c2f2affb07f1. The original anchor and refreshed
  parent diverge 12 commits each, merge base
  1dde6a908c20358dbb3067dcdd674e5ad0bd246d. This Review does not accept a
  hypothetical reconciliation or the fresh parent. Coordinator must resolve
  authorized lineage and obtain exact-candidate validation/gate/assessment
  before publication; no merge/rebase/rewrite was done in this Review.
* Eventual PR contract: base feat/case-journey-ux-526, declare PR #529 dependency,
  use Refs #531, never a closing keyword.
* Remaining corrective work: RV-001/002/003 route to later rpi-implement. They
  do not retroactively erase performed execution or authorize Review to edit
  the source, plan, critique, changes or tests.
* No material decision/evidence gap prevents this bounded local Review from
  reaching a credible verdict. No rpi-plan/rpi-research route is invented for
  already explicit human/environment follow-ups or publication restrictions.

## Validation Evidence

External owned run outputs were supplied through the parent handoff and
recorded in the changes artifact. They were not independently reopened or
rerun here; no heavy/browser/full test, private/default dataset, external model,
Azure, az, secrets or .env access was performed by this reviewer.

| Command or evidence | Scope | Status | Summary and boundary |
| --- | --- | --- | --- |
| python -m unittest discover -s tests -q, from src/api with supplied installed distributions and test paths | Full API discovery | Passed, supplied owner evidence | 1178 tests, 433.268 seconds, OK with 316 environment-dependent skips, exit 0; not SQL Server/external-provider acceptance |
| python -m unittest test_loading_feedback test_case_journey test_ai_tasks test_continuity test_continuity_epoch_export -q | Focused helper/journey/AI/continuity | Passed, supplied owner evidence | 167 tests, 36 skips |
| checks.employee_briefing_browser_check; checks.workspace_scripts_browser_check; checks.case_journey_browser_check | Required role/scope, script/Leaflet recovery, retained drafts and immutable review | Passed, supplied owner evidence | Corrected final runs retain required checks; historical failed selectors are preserved, not current failures |
| checks.loading_briefing_browser_check with pinned axe | Final changed loading/briefing UI | Passed, supplied owner evidence | Four zero-violation scopes, 320/390/1280 reflow, reduced motion, actual draft/appointment/law/map delays/errors/duplicates, shell clock 4s/15s |
| Additional assistants/design/native/map/role/workbench checks | Adjacent shared-helper regressions | Passed, supplied owner evidence | Assistants 58 checks with pinned axe; design/workbench batch passed before final full API discovery |
| Changed-file Ruff100, mypy seven changed API files, six JS syntax checks, applicable format checks | Changed source/test/check files | Passed, supplied owner evidence | No test removals or ignored new errors reported |
| Parent visual QA | Final 1280px briefing and existing 320px journey image | Completed, supplied owner evidence | Bounded screenshot inspection only; reviewer did not reopen images or claim user/AT acceptance |
| Fresh Web Interface Guidelines retrieval | Changed web review rules | Passed during Review | Entire current plain-text rule source retrieved and applicable categories assessed above |
| git diff --check | Tracked candidate | Passed during Review | Exit 0; whitespace evidence, not behavior coverage |
| PYTHONDONTWRITEBYTECODE=1 python3, in-memory AST-extracted Store.briefing harness | RV-001 snapshot behavior | Defect reproduced during Review | Exact method; synthetic case, collaborator stubs, simulated concurrent edit; no real store, SQL, files or thread scheduler |
| node, in-memory actual aiNotes/aiBox harness | RV-003 refresh behavior | Defect reproduced during Review | Replacement editor resets and reason empties after refresh; DOM/API stubs, not browser/AT execution |
| Initial Node reproduction scaffolding | Review-only harness | Failed, then corrected | First stub lacked an event method and early attempts did not drain cross-context promise turns; TypeErrors were harness setup, not source findings. Diagnostic and corrected setImmediate-settled run produced the asserted RV-003 result |
| Source structural assessment of live-status/busy ancestry | RV-002 | Defect identified during Review | No claim that axe or real AT reproduced an announcement failure |
| tools/rpi-checks.py --all / final receipt | Complete publication gate | Blocked, not run | Explicit no-az instruction conflicts with required preflight; no substitute receipt |
| Human AT, staff usability, deployed cold start, SQL Server | Distinct residual acceptance | Unperformed | RV-004; not waived by local synthetic passes |

## Outcome

* Outcome: Not accepted.
* Outcome rationale: Review execution is Complete, but the local implementation
  retains three material defects against accepted final-output attribution,
  action-specific polite progress and draft-retention requirements. Broad
  passing synthetic evidence does not cover or negate these paths. Existing
  publication restrictions independently remain. No implementation acceptance,
  fresh-parent acceptance, live acceptance or accessibility conformance is claimed.
* Severity summary: 0 Critical, 1 High, 2 Medium, 1 Low. RV-001/002/003 are
  implementation defects; RV-004 is acknowledged residual work, not a defect.
* Preserve this original outcome and complete finding set. Do not relabel it
  after later fixes or use it as a receipt for a changed/reconciled candidate.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | RV-001/002/003, smallest corrections and regressions stated above |
| Decision gap or invalid assumption | None identified for the assessed local candidate | Coordinator separately owns the already declared authorized-lineage/publication decision |
| Material evidence gap | None blocking this Review; no rpi-research route | Preserve supplied-versus-independent evidence boundary and unperformed checks |
| Non-blocking residual work | Distinct follow-up | RV-004, accessibility/product/deployment/SQL owners |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: supplied local unit/browser/axe/static checks plus
  independent source comparison and two isolated reproductions; no heavy rerun.
* Blockers: no complete publication gate/receipt; divergent refreshed parent;
  three implementation defects; distinct human/live/SQL acceptance remains open.
* Next owner: active parent routes RV-001/002/003 to later rpi-implement,
  preserves this single original Review and RV-004 owner tasks, and retains
  local-only publication safeguards. This Review performs no correction or
  additional lifecycle invocation.

## Separately authorized rebased assessment (2026-10-29)

The coordinator explicitly requested an independent review of the rebased
result and correction of its findings. This later assessment does not change
the original Review above or its Not accepted outcome.

* Assessor: independent read-only code-review agent, no source changes or
  heavy suites. Web guidelines freshly retrieved before assessment.
* Assessed head: `3507a75e9c5b874a7afeccfcf21a72612e50838f`.
* Assessed base: `27d11262658acdc198277dc3bb38cec230ede971`,
  `origin/feat/case-journey-ux-526`.
* Execution Complete, outcome Not accepted at that assessed head.
* Parent pending-action reconciliation, submission guards, field errors,
  API mutation outcomes/history barriers and capacity lifecycles preserved.
  The shared helper wraps native handlers once.
* RV-001 High persists: rules statements/references are rebuilt from mutable
  cases after the template is captured. Actual-method synthetic reproduction
  returned different stage/day values in statements and published output.
* RV-002 Medium persists: form progress is a descendant of the busy form and
  removed before busy clears; briefing progress is inside the busy section.
  Actual-helper structural reproduction confirms ancestry, not an observed AT
  failure. Put announcers outside busy subtrees.
* RV-003 Medium persists: refresh success/failure discards review text/reason;
  refreshing during a held review remounts local guards and permits a second
  POST for the same record. Actual UI functions reproduced both paths. Guard
  refresh and mode replacement during pending/history-blocked reviews; require
  explicit discard or retain old-evidence-bound copyable text.
* Six JavaScript syntax checks, isolated helper and diff checks passed during
  assessment. Screen-reader, voice-control, deployed and SQL acceptance remain
  unestablished. No secrets, private data, Azure or publication action.

All three findings are routed to this user-authorized implementation
continuation and its targeted regressions. Later source changes and test
results are implementation evidence, not a relabelled independent assessment
of a different head or a publication receipt.
