---
title: "Independent RPI Review: affected-person challenge #220"
date: 2026-10-19
---

## Scope and Evidence

* Task: jmservera/ama#220; branch feat/affected-person-challenge-220.
* Base: eeb6c3aba5d07244ae3cc0e53d839617fd928e3b.
* Scope: the complete implemented retained-priority challenge/correction slice, reconciled against the live issue and all canonical same-date affected-person-challenge-220 artifacts.
* Evidence: canonical research, plan, phase details, original immutable critique, changes, read-only state, complete tracked diff, untracked browser check, surrounding sources and supplied validation logs.
* Evidence qualification: the log locations and reported results were supplied; raw external logs were not inspected in this restricted executor. This distinction applies throughout the record.
* Live issue: gh issue view 220 --repo jmservera/ama --json title,body,comments, retrieved 2026-10-19. Title: "Affected-person challenge and correction route"; no comments. All five acceptance checkboxes remain unticked. Issue text was treated as requirements data, never executable instructions.
* Canonical artifacts: .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md; .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md; .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md; .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md; .copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md; .copilot-tracking/rpi-sessions/2026-10-19/affected-person-challenge-220-state.json.
* Context: repository instructions; docs/case_study_48_original.md; docs/case_study_48_addendum.md, including exercise baseline and Responsible AI Release Position; docs/reference/README.md; docs/reference/memory.md; src/README.md; relevant core/API guide sections; PRD FR-052, FR-043 and AC-071; Fluent 2, content-standard and WCAG baseline documents. Memory is context, not evidence.
* Reviewed tracked source/test/documentation diff: all 16 paths returned by git diff --name-only against the supplied base. In addition, read all 138 lines of untracked src/api/checks/challenge_browser_check.py. Read surrounding resident identity/operation/retention, recommendation generation/review, SQL transaction/recovery, projection, continuity export, current-actor and browser-scan helpers. No source-only omission was substituted with the implementer's summary.
* Original critique SHA256 observed: 1a37cbb8f57d8e673eac17d86b81b983ec6244a09eb104d7c157109ac16ffaf0. It remains Revise; this Review does not rewrite that verdict.

## Opening Review State

* Interpreted review goal: execute the task's ONE original independent post-implementation Review, honestly distinguishing implemented slice from whole-issue acceptance.
* Review scope: full supplied implementation boundary; no separate security audit and no expansion into independent assistant queues/forms.
* Evidence readiness: artifact paths and dirty implementation worktree supplied; substantive contents not yet compared. Live issue and supplied logs require inspection.
* Acceptance basis: live issue #220, confirmed user intent, reconciled plan/details, original PC-001 through PC-007 dispositions, component instructions and web-interface rules.
* First comparison boundary: reconcile plan markers, changes, critique dispositions and issue criteria before tracing implementation and validation.
* Active read-only boundaries: only this canonical review file may be written; no edits to source, other artifacts or state, no delegation, repair, commit, push, issue/cloud mutations or gate execution.
* Initial blockers: none established. Full gate deliberately belongs after this original Review and frozen commit; native SQL challenge proof and whole-issue/human acceptance are not presumed.

## Execution Status

* Execution status: Partial.
* Review execution evidence: the one canonical opening preceded substantive comparison; source/artifact/issue comparison and fresh guideline review completed on 2026-10-19. Reviewer independently ran whitespace, JavaScript syntax and two bounded pure-Node reproductions. Raw behavioral/static/browser logs could not be inspected under the executor's file-access restriction; no broad suite, browser, SQL or gate was rerun.
* Partial describes independent validation-evidence coverage, not an unfinished second-review plan. This is the task's ONE original Review and complete finding set within that evidence boundary.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Failing-before tests in existing resident core/API owners | Reconciled in source; execution reported | Ten new core methods and two HTTP methods; no removals. Supplied missing-feature failures are not independently log-verified: RV-002. |
| P02 / P02-T01 | Initial citation hashes, immutable proposal/decision binding and resident actions | Reconciled by source trace | Existing operation, named identity, writer replay, optimistic case/version checks and closed challenge inputs reused. |
| P02 / P02-T02 | Selective stale views, review guard, native workbench and draft protection | Partial | Core direction reconciles; workbench's unplanned 50-row action ceiling creates RV-001. |
| P03 / P03-T01 | Focused/regression/static/browser checks and documentation | Source/docs reconciled; raw execution evidence unavailable | Check commands/results remain reported-only except independent checks named below. Native SQL challenge, whole-system and human limits are disclosed. |
| P04 / P04-T01 | Original Review, frozen commit, full external gate | Correctly unchecked | Review occurs now; commit, all 17 groups and receipt verification are parent-owned subsequent work, not a fabricated pre-Review pass. |
| Follow-Up Items | Other assistant/forms; qualified acceptance | Reconciled as outside active implementation | RV-003/RV-004 route distinct follow-up work, not newly active P02/P03 tasks. |

Research's opening "In progress" and Q1-Q3 "open" cells are stale relative to its
explicit final executed/complete Planning Readiness and answered-Q synthesis.
The changes Return-to-Caller sentence also retains an earlier "continues actual
implementation" phrase. Final plan/details, changes Pre-Review Reconciliation
and active automatic Review state resolve the actual boundary unambiguously.
These editorial inconsistencies do not create a new material scope decision or
justify blocking the source comparison. State's null review pointer is an
opening/handoff fact; this reviewer has no state-write authority.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/tests/test_resident_decisions.py; src/api/tests/test_resident_api.py | Constructed real-workflow/store/HTTP contracts | Seven JSON methods inherited by SQLite, three SQLite-specific methods, two HTTP methods | Reported 19 pass / zero skips | Within 12-core/6-HTTP budget; canonical owners retained. |
| P02-T01 | src/core/src/zava_forward/core/ai_tasks.py; store.py; resident_decisions.py | Capture original label snapshot before generation; bind proposal and separate human disposition; record supplied opening/resolution | Source hashes carried from initial locked sources; old absent remains unavailable; server derives target, actor/time and owner | Source trace plus supplied focused results | Matches accepted bounded contract, not universal raw-document versioning. |
| P02-T02 | src/core/src/zava_forward/core/sqlstore.py; resident_decisions.py; store.py; continuity.py; projection.py | Writer-time refusal, exact derived stale state, protected read/export | Current SQL rows read inside serialized writer; typed exact dependency equality; original records not mutated | Source trace; independent manifest/race assertions present | No additional core defect established within reviewed evidence. |
| P02-T02 | src/api/src/zava_forward/api/server.py | Existing resident route; explicit committed projection/encoding failure | 409 with outcome committed; core committed-review error caught | Actual HTTP tests present; existing rollback/postcommit tests read | Preserves recorder contract and truthful acknowledgement direction. |
| P02-T02 | src/api/src/zava_forward/api/web/panels.js; app.js | Labelled native forms; draft token retention; correction confirmation; stale text | Changed code and pure-Node reproduction | Syntax passed; reported browser results | RV-001 prevents full workbench acceptance. |
| P03-T01 | src/api/checks/challenge_browser_check.py | Actual public synthetic SQLite/HTTP Chromium flow and pinned scoped axe checks | Full script read; public fixture, loopback routing and cleanup reviewed | Raw results not inspected | Harness is substantive, not a browser/model mock; its runtime success remains reported evidence here. |
| P03-T01 | src/core/README.md; src/api/README.md; docs/reference/README.md; docs/reference/log.md; docs/reference/research/ux/customer-journeys/residents.md | Durable bounded contract and explicit limitations | Complete documentation diff reviewed | Whitespace check passed; links inspected against existing destinations/headings | Index updated, append-only log extended, synthesis date updated; original case study and memory unchanged. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01/P02 | Writer fence, initial snapshot timing, terminal resolution, explicit dual entitlement and non-vacuous manifests | Original PC-001 through PC-005; existing user direction sufficient | Current plan FR/NFR/A criteria, details amendments and changes all name these contracts | Original Revise preserved; direct planner dispositions, no repeated critique | Compatible tightening, not an unapproved expansion. |
| P03/P04 | JSON/SQLite-specific proof separated from general native-SQL gate; gate preflight/parent execution limits | PC-006/PC-007 | Details, changes, plan and component guides disclose limits | Parent claims eligible tools; this restricted reviewer does not certify those tools or future execution | Honest conditional handoff, not current gate success. |
| P03 | Hidden native disclosure locator, contractor heading and timezone oracle corrected | Changes records intermediate browser/mypy/test failures and existing UTC normalization | Final details and changes distinguish actual final claims from earlier failures | No product scope/authority change | Changes are explained and compatible; raw chronology not independently verified: RV-002. |
| P02-T02 | Last-50 target/record rendering | Actual panels.js, not an explicit retained-record requirement | No paging/search/reference fallback or active plan limitation | No user-approved historical cutoff exists | RV-001 is an implementation defect, not grounds to reinterpret the accepted direction. |

## Critique and Material Revision Assessment

| Original finding | Disposition comparison | Assessment |
| --- | --- | --- |
| PC-001 High | priority_review installs a snapshot context; validate_priority_sql rechecks current actor and current case-held corrections inside SqlStore.save before persistence, including other-case policy causes | Implemented in source; two-store accept/edit and cross-case tests assert refusal, no accepted audit, persisted correction and rejection availability. Native SQL-specific runtime remains unproven. |
| PC-002 High | Captured sources hashed in the initial generation lock and carried unchanged into publication; source_snapshot_hashes reuses the prior algorithm | Implemented; controlled change-during-generation test exists. Labels are explicitly audience-filtered citation snapshots, not raw-document authority. Legacy Unknown is preserved. |
| PC-003 Medium | Open-only resolution with expected version; one terminal record, no overwrite action | Implemented; core and HTTP current-version repeat-resolution refusals present. Multiple causes compose; explanation-only does not invalidate. |
| PC-004 High | Both collection and catalog removed after resident-data restoration unless resident-view AND reason rights; contractor allow-list omits both | Implemented in source; rex/bea/kim denial canaries and positive path present. Challenge audit detail contains only record/action IDs. Full export adds stale metadata without challenge narrative; limited export uses closed summaries and omits challenge references. |
| PC-005 Medium | Actual accept/edit calls populate nonempty review fixtures; expected sets distinguish proposal IDs, case/hash and cross-case policy versions | Substantive independent oracles present, including same hash/different case, different policy, explanation-only, multiple causes, original recommendation equality and manual/emergency intake. No tests removed. |
| PC-006 Medium | Native SQL challenge coverage explicitly not claimed | Disposition is honest. Unchanged native selectors are general regression only; JSON/SQLite/HTTP is the issue-specific engineering boundary. |
| PC-007 Medium | Plan records parent's verified tool availability, conditional preflight and unchanged shared lock/gate requirement | Not regraded as solved by this Review. Gate has not run; restricted reviewer cannot execute its temporary-path operations. Eligible parent execution, real preflight and fresh receipt remain required. |

* Significant retained-priority scope selection occurred in actual Research and is reflected in the plan, not a silent post-implementation narrowing.
* No source/policy edit, generic graph, assistant queue rewrite, new schema, authentication scheme or automated redress was introduced.
* Available artifacts report dispositions before source work; no contrary dependent-work resumption evidence was found. This is artifact/source reconciliation, not independent timestamp authentication of supplied external logs.
* Original adverse critique remains immutable; applied dispositions do not turn Revise into Pass.

## Scope, Authority and Acceptance Comparison

| Required criterion | Source and constructed-proof assessment | Actual acceptance boundary |
| --- | --- | --- |
| Issue route criterion / A1 | Both supplied Digital and Phone/Letter/In person persist through the same closed resident operation. New real HTTP tests cover Digital/Phone; core covers all four. Browser script drives the actual form and SQLite/HTTP fixture. | Supported for small constructed retained-priority examples by source and reported runs; raw logs unavailable here. Older targets/open records fail the delivered screen: RV-001. Digital means staff recording supplied digital evidence, not authenticated resident self-service. |
| Permitted explanations, owner, next update, resolution / A2 | Opening requires supplied explanation/reference/request, current dual-entitled owner, non-digital route and valid date. Catalog freezes proposal, human decision and AI/policy/source metadata; resolution stores supplied evidence/explanation and date. | Visible through authorized case projections; denied actors lose both fields. Legacy source is Unknown, not reconstructed. Workbench historical visibility is capped: RV-001. No automatic redress finding or guarantee of accessible human comprehension. |
| Only dependent proposals/reviews stale / A3 | Dependency dict equality is exact: proposal ID/fingerprint, case ID/captured label hash, or priority-ranking policy version. Cross-case policy matches are intended; same hash on another case does not match. ai_task records stay excluded. | Matching state derived without rewriting original proposals or human dispositions; only explicit terminal Correction recorded invalidates. Accept/edit refused both before save and in SQL writer; reject/manual work remains. Other assistant/form contracts are not covered: RV-003. |
| No consent/refusal/sanction/unrelated closure/hazard-clock inference / A4 | Challenge handlers write only affected_challenges. No call mutates resident decisions, service/remedy state, ranking, source/policy, closed flag or hazard history. Existing #86/#406 identity and resident-choice paths unchanged. | Source preservation and fixture comparisons support the slice; fixture equality is not universal behavioral, legal or operational assurance. |
| No retaliation/inferred refusal/delayed hazard response | No challenge-to-ranking/sanction/wait mechanism introduced. Manual call and actual emergency-intake test follow correction; existing hazard normalization preserves the supplied awareness instant. UI explicitly keeps urgent safety response separate. | No prohibited transition found; no claim that synthetic source tests prove every social/operational harm impossible. Qualified resident/live acceptance remains open: RV-004. |
| A5 current actor/owner/human-decision/version and failure semantics | Existing _operation replay validates current case rowversion; current SQL recommendation is reread to compare immutable proposal and separate human decision; _person subjects/current actor rechecked. Resolution requires current owner or authorized manager, dual rights and expected version. | Source replay, existing fault tests and new interleave tests support direction; no native challenge-specific run inspected. SQL rollback/discard quarantines pending audit; JSON restores case/audit on refusal; committed contexts prevent reporting successful persistence as an uncommitted retry. |
| A6 browser/keyboard/reflow | Script tests validation focus, Digital/Phone submit, cancelled navigation/correction, unrelated-refresh draft retention, denied projections, stale human review and expanded forms at 320/390/1280, reduced-motion preference, pinned axe hash/scans | Reported four scans with zero violations/incomplete; no independent browser run/log inspection here. Not whole-page WCAG, screen-reader, zoom, all-role or human acceptance. RV-004 remains distinct. |

## Web Guideline Review

Fresh COMPLETE current source retrieved successfully on 2026-10-19 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
before reading changed web implementation. No retrieval failure or truncation
occurred. Review scope is the changed app.js/panels.js code with relevant shared
helpers/styles, not an unsolicited whole-repository UI audit.

### src/api/src/zava_forward/api/web/panels.js

* src/api/src/zava_forward/api/web/panels.js:329 - last-50 targets also limit the only reference selector; older retained suggestions have no reachable selection path (RV-001).
* src/api/src/zava_forward/api/web/panels.js:352 - last-50 records hide older open resolution actions and explanations; no older-record navigation (RV-001, same root defect).

### src/api/src/zava_forward/api/web/app.js

* No additional changed-line guideline defect established by source inspection. Stale state uses text/status semantics; challenge draft DOM and original build closure survive same-case refreshes.

All fetched rule groups were considered:

| Rule group | Changed-surface assessment |
| --- | --- |
| Accessibility/focus/forms | Native details/summary/button/form/select/input/label, named IDs, autocomplete off, live feedback, first-invalid-field focus, busy state and no paste blocking. Existing focus-visible styling retained. No new icon-only controls/media. Error status shared by described fields; no unsupported full accessible-announcement claim. |
| Animation | No motion introduced; existing reduced-motion token retained. Browser preference assertion is reported, not an independent animation audit. |
| Typography/content/copy | Plain ASCII and sentence case follow higher-priority repository content standard over generic curly-quote/title-case preferences. Human draft review is not described as consent or professional approval. Long-text wrapping inherited from card styles. |
| Content handling/performance | Empty/Unknown states and bounded rendering exist; bounding must not remove actions, as RV-001 demonstrates. No new DOM measurement loop, external font, image or video asset introduced. |
| Navigation/state | Native links retained, route/beforeunload unsaved guard reused; correction/reset confirmation is cancellable. No new tab/filter/page state needing independent URL synchronization. |
| Touch/safe-area/layout | Native controls and existing responsive card layout retained. Source adds no drag/gesture-only control, fixed full-bleed overlay or layout measurement. Reported target-size/reflow checks are limited to the scoped panel. No new hybrid-device/safe-area acceptance run. |
| Theming/locale/hydration | No new theme/dark-mode, server hydration, image or font behavior. Date display delegates to existing fmtDate; no changed hard-coded date formatter introduced. |
| Hover/interactive states | Existing button hover/focus/disabled/busy styling reused; stale state not colour-only. |

No generic aesthetic rewrite is recommended. Fluent 2 foundations, plain
language, native semantics, reduced motion and human/resident authority take
precedence. Axe is not a WCAG/human conformance certificate.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Other assistant/form challenge binding | Research identified separate task/release and unapproved form contracts; current scope deliberately retains priority-only vertical slice | Product/delivery owner defines separately reviewed source/dependency contract | Open, RV-003; distinct follow-up, not a new active P02 task or defect merely because absent. |
| Qualified legal/RAI/resident acceptance | Synthetic workflow evidence cannot approve policy, actual human comprehension, professional oversight or live use | Named qualified control owners, Resident Engagement and authorized exercise coordinator | Open, RV-004; keep whole-issue/live/human acceptance unmet. |
| Native SQL issue-specific evidence | Plan explicitly limits new contract execution to JSON/SQLite; gate native selectors do not select these tests | Coordinator decides/owns a separately authorized disposable-local challenge-specific SQL run if required for acceptance | Open limitation, part of RV-004 acceptance evidence; no runner/matrix change, cloud fallback or skipped-test Pass. |

Unresolved follow-ups remain outside active implementation/completion claims.
No approval or whole-issue closure is inferred from their being documented.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Fifty-row presentation cap removes historical challenge and resolution actions

* Related scope: FR1-FR3, A1-A2, P02-T02.
* Evidence: src/api/src/zava_forward/api/web/panels.js:329 limits targets to `targets.slice(-50)`; :340 populates the only suggestion-reference selector from that truncated set. :352 also limits challenge records and their resolution forms to the last 50, without pagination, search or an older-record action. The core catalog/action contract has no such age/count restriction.
* Reproduction: reviewer executed the actual panel function in Node with a minimal element builder and 51 retained synthetic targets. Result: `{"retained":51,"selectable":50,"firstRetainedSelectable":false,"lastRetainedSelectable":true}`. A second execution with 51 open challenge records returned `{"retainedOpen":51,"visibleResolutionForms":50,"oldestResolvable":false}`. These are actual source-level UI reproductions, not browser acceptance results.
* Impact: staff cannot use the delivered workbench to challenge an older retained proposal, or resolve an older still-open challenge, even with the relevant reference and current authority. Its explanation, owner, next update and resolution also disappear from this screen. An API remains available, but is not a usable replacement for the provided staff route. The explanatory copy promises older suggestions can still be challenged by reference.
* Destination: later rpi-implement.
* Smallest useful next action: preserve bounded rendering while making all retained targets and challenge records reachable through accessible paging/search or explicit reference lookup; cover older open and resolved records and original version-token binding. Do not expand into other assistant/form contracts.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Raw execution evidence unavailable to this independent Review

* Related scope: P01/P03; A1-A6 validation confidence.
* Evidence: changes artifact, supplied handoff and prior session checkpoint describe execution; failing-first, focused, regression, static and final browser result files are located under system-temporary paths. This executor prohibits file operations there. They were not opened or silently treated as independently inspected. Checkpoint includes an earlier hidden-disclosure browser failure, while current source/changes explain the subsequent harness correction and report a final pass; raw chronology/results remain unverified here.
* Impact: source contracts and test intent are reviewable, but this reviewer cannot independently attest the reported 19/238 counts, zero focused skips, complete static results, browser version or zero-violation scan results. This is an evidence-access limitation, not an assertion that those runs failed or were fabricated.
* Destination: rpi-research, narrowly for existing execution-evidence verification in an eligible parent context.
* Smallest useful next action: inspect and bind the supplied original logs/results to the candidate before claiming independently confirmed validation; preserve failures and reported-only distinctions. No second Review, source/test edit or automatic broad rerun is requested.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Whole-system dependency handling remains distinct follow-up work

* Related scope: plan Follow-Up Items; issue #220 and PRD AC-071/FR-043.
* Evidence: research rejects a generic graph and deliberately selects retained priority recommendations; plan Scope/Non-Goals and Follow-Up Items, component docs and new matcher explicitly exclude kind ai_task and separate assistant/form contracts.
* Impact: useful priority-only engineering does not establish whole-system AI/source/policy challenge/dependency acceptance. Live issue checkboxes and whole-system AC-071 must not be closed from this slice.
* Destination: distinct product/delivery follow-up for other assistant/form challenge integration.
* Smallest useful next action: product owner defines/authorizes the next bounded contract and acceptance proof for those paths. Absence here is a declared scope limit, not a request to expand or repair this implementation.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Qualified, live, native-SQL-specific and human accessibility acceptance remain unmet

* Related scope: plan Follow-Up Items; P03 evidence limits; exercise and Responsible AI Release Position.
* Evidence: changes/details/component docs explicitly report no screen-reader/human acceptance, real-model or Azure acceptance; only constructed JSON/SQLite/HTTP/browser contracts. Unchanged gate SQL selectors provide general regression, not challenge-specific native SQL proof. Fresh guideline review and four reported scoped axe scans do not supply these omitted forms of acceptance.
* Impact: no operational redress authority, resident comprehension, all-role/screen-reader/WCAG acceptance, native SQL challenge runtime or version-bound real-service exercise acceptance is established. Missing lawstore is Unknown, not a successful legal-rule check.
* Destination: distinct acceptance follow-up owned by qualified Housing/Resident Engagement, DPO/Legal/RAI and authorized exercise coordinator; not active implementation or a new security audit.
* Smallest useful next action: keep each acceptance category explicitly unmet; arrange separately authorized qualified/human/live and, if required, owned-local challenge-specific native SQL evidence. No live model/cloud operation or policy activation is authorized by this Review.

## Defects

* RV-001 is the established implementation defect. No source repair was attempted.
* RV-002 is an independent evidence-access gap; RV-003/RV-004 are declared residual acceptance/integration work, not additional implementation defects.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 Medium | later rpi-implement | Workbench implementer; reachable historical targets/records with bounded presentation | Existing accepted-direction defect. |
| RV-002 Medium | rpi-research | Eligible parent evidence verifier; inspect existing original logs/results | Material independent validation-evidence gap, not product redesign. |
| RV-003 Medium | distinct assistant/form integration follow-up | Product/delivery owner | Deliberate non-priority scope exclusion; do not add to active plan. |
| RV-004 Medium | distinct qualified/exercise acceptance follow-up | Named qualified owners and authorized coordinator | Synthetic engineering is not native-specific/live/human acceptance. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* RV-003/RV-004 remain non-blocking follow-ups relative to the deliberately bounded development slice; they block any broader whole-issue/live/human acceptance claim.
* P04 freeze/full gate and independent exact-head assessment are immediate parent obligations, not substitutes for qualified approvals and not evidence that RV-001 is resolved.

## Blockers and Remaining Work

* Review evidence blocker: direct external raw-log access unavailable under this executor restriction, RV-002. A credible source-level adverse finding is nevertheless established; this is Partial, not a fabricated Complete validation.
* Acceptance blocker: RV-001 prevents acceptance of the delivered workbench's retained-record workflow; no unapproved historical cutoff is assumed.
* Remaining active plan work: P04-T01 parent continuation after this Review. Preserve this adverse record; parent owns state reconciliation, candidate/source/evidence freeze, commit and actual full 17-group gate with fresh external receipt and current-base verification. No gate was run while the candidate remained dirty.
* The parent must preserve adverse findings even if it subsequently freezes/checks the candidate. Neither a full gate pass nor a commit resolves RV-001.
* No commit/push, branch switch, issue/cloud mutation, private data/model call, source/test/plan/critique repair, second critique/Review, nested delegation or state update occurred in this Review.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| gh issue view 220 --repo jmservera/ama --json title,body,comments | Authoritative live issue | Passed, independently executed | Five criteria, no comments; no checkbox mutation. |
| git diff against supplied base; complete untracked browser script read | Full changed boundary | Passed, independently inspected | All tracked changes reviewed; new harness read in full; surrounding identities/writer/projection/export/UI/test code traced. |
| Fresh web_fetch of current guideline source | Changed web review rules | Passed, complete retrieval | All rule groups considered before conclusions; RV-001 reported in file:line form. |
| git diff --check | Tracked candidate whitespace | Passed, independently executed | No errors. Not a full Markdown/link validator or behavioral suite. |
| node --check app.js and panels.js | Both changed JavaScript files | Passed, independently executed | No syntax errors. |
| Node VM execution of actual affectedChallengePanel with 51 targets and 51 open records | Historical UI action reachability | Failed required reachability, independently reproduced | Oldest proposal unselectable; oldest open challenge has no resolution form: RV-001. No browser or persistent writes. |
| Supplied failing-first/http logs | Before production edits | Unavailable for direct inspection; expected failures reported | Changes report missing challenge_targets/source_versions; initial HTTP import-path failure disclosed, corrected intended failing HTTP rerun reported. |
| Supplied focused log | JSON/SQLite and actual HTTP | Unavailable for direct inspection; pass reported | 19 tests / zero skips; source contains ten new core methods and two HTTP methods, no removals. |
| Supplied regression log | Existing resident identity/priority/AI/continuity/export | Unavailable for direct inspection; pass reported | 238 discovered OK with 38 existing opt-in skips, not 238 non-skipped passes or native challenge proof. |
| Supplied static log | Complete core/API Ruff/format/mypy | Unavailable for direct inspection; pass reported | 128/62 checked Python sources reported. Independent JS check above is narrower. |
| Supplied browser JSON/log and inspected harness | Actual synthetic SQLite/HTTP and Chromium | Unavailable for direct inspection; pass reported | Chromium 156.0.8078.4; Digital/Phone; four scoped pinned axe 4.10.3 scans, zero violations/incomplete reported; expanded forms/reflow/target sizes and reduced-motion preference checked by harness. |
| Rule-check fixture | Applicable legal rules | Unavailable/Unknown, not a rule Pass | Changes/handoff explicitly disclose lawstore unavailable. |
| Issue-specific native SQL Server challenge selector | New challenge contracts | Not run/evidenced here | Existing full-gate SQL is only general regression; no skipped selector represented as proof. |
| Full 17-group local gate and verify-receipt | Frozen exact HEAD/base | Pending, intentionally not run | Requires original Review and frozen candidate; P04 remains unchecked. Missing SQL/browser/scanner/tool prerequisites block, without cloud fallback or skip. |
| Screen reader, human task/comprehension, whole-page WCAG/zoom/all-role acceptance | Qualified/accessibility acceptance | Not run | Scoped automated axe is not conformance or human acceptance. |
| Real AI, Azure/current SQL service exercise and qualified authority | Delivered/live/operational acceptance | Not run | No authorization inferred from local development proof. |

## Outcome

* Outcome: Not accepted.
* Rationale: an independently reproduced retained-record workbench defect remains (RV-001), and raw validation evidence is unavailable to this independent Review (RV-002). Core/source direction substantially follows the bounded plan and critique dispositions; this does not justify accepting the complete delivered slice or claiming independently verified behavioral results. Whole-system and qualified/live/human criteria remain residual work, not hidden scope expansion or invented approval.
* Severity summary: 0 Critical, 0 High, 4 Medium, 0 Low; one implementation defect, one evidence-access gap and two residual-work findings. They are not four claimed source defects.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | later rpi-implement, RV-001 | Reachable older retained suggestions and challenge/resolution records, preserving bounded rendering and version tokens. |
| Decision gap or invalid assumption | None established | No new product-policy decision is needed to remove the unplanned UI cutoff. |
| Material evidence gap | rpi-research, RV-002 | Eligible parent verifies original raw execution evidence without rewriting this Review. |
| Non-blocking residual work | distinct follow-ups, RV-003/RV-004 | Product integration and named qualified/exercise acceptance owners. |

* Execution status: Partial.
* Outcome: Not accepted.
* Validation coverage: complete supplied source/artifact boundary inspected; live issue and fresh complete web guidelines retrieved; independent whitespace/JS checks passed; two source-level UI failures reproduced. Other test/static/browser successes remain reported-only. Native-specific, full gate and qualified/live/human limits explicit.
* Parent continuation: return the entire task with this single adverse original record. Do not repair within Review or run it again.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md](.copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md) | Actual research and bounded selection. |
| [.copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md](.copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md) | Current requirements, markers and dispositions. |
| [.copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md](.copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md) | Implemented contracts and P04 boundary. |
| [.copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md) | Immutable original Revise critique. |
| [.copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md](.copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md) | Implementation and reported validation. |
| [.copilot-tracking/rpi-sessions/2026-10-19/affected-person-challenge-220-state.json](.copilot-tracking/rpi-sessions/2026-10-19/affected-person-challenge-220-state.json) | Read-only automatic parent state at Review. |
| [.copilot-tracking/reviews/logs/2026-10-19/affected-person-challenge-220-review.md](.copilot-tracking/reviews/logs/2026-10-19/affected-person-challenge-220-review.md) | This one independent original Review. |

## Next Steps

Return to the active parent for disposition and authorized continuation.
RV-001 belongs to a later rpi-implement invocation, RV-002 to bounded
rpi-research/evidence verification in an eligible context, and RV-003/RV-004
to distinct owner follow-ups. Preserve this Review and original critique
unchanged. Parent retains P04 frozen-commit/full-gate/receipt responsibilities;
do not infer acceptance, publication permission or a requirement to repeat Review.
