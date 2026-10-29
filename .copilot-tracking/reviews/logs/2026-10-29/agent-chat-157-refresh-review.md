<!-- markdownlint-disable-file -->
# Review: agent-chat-157-refresh

## Scope and Evidence

* Task ID: pr-503-refresh-2026-10-29
* Review date: 2026-10-29
* Scope: local PR #503 rebase refresh, not whole-feature acceptance.
* Base: 5653547507f3056f09a726a18516237728da5e5b.
* Implementation candidate: ca5cb0101040c8176c4f32812be71af02b56670a.
* Artifact set: dated agent-chat-157-refresh research, plan, phase details,
  critique and changes under .copilot-tracking/, all 2026-10-29.

## Opening Review State

Review goal: independently assess preservation of main/topic intent and
truthful local-validation evidence after the explicitly authorized rebase.
P01/P02 implemented and committed; P03 Review active. Read-only source scope;
only this canonical Review record may be written by the independent assessor.
Acceptance basis: current plan, user constraints and disposed critique.
First compare runtime conflict integration, then tests/evidence and follow-ups.
Original feature acceptance, named human approvals, publication receipts and
fresh hosted CI are not established by this local refresh.

## Execution Status

* Execution status: Complete, for this one independent post-implementation
  Review.
* Review execution evidence: independently read the current dated plan,
  details, research, original critique and changes; compared source and tests
  from the captured base to the implementation candidate; inspected the
  original topic and replayed patch differences; performed read-only Git and
  preservation checks on 2026-10-29.
* Implementation execution: P01/P01-T01 and P02/P02-T01 are complete on the
  supplied evidence. This record completes the independent-assessment portion
  of P03/P03-T01. The parent's subsequent evidence commit and local handoff
  remain outstanding; this assessor did not perform them.
* Evidence readiness: sufficient for the bounded local refresh. Current
  changes/details contain evidence-only updates after ca5cb010. Source is
  clean at the assessed candidate; the initially dirty tracking paths and
  pre-existing untracked opening Review were not discarded or moved.
* Authority: only this canonical Review was edited. No implementation repair,
  plan/state/changes edit, delegation, commit, rebase, push, Azure operation,
  test-suite rerun or publication-gate execution was performed.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | Fresh preflight, immutable fetch target and authorized rebase of four commits; five actual conflicts resolved | Reconciled | Captured main is an ancestor of ca5cb010; no unmerged entries. The rebase conflict list covers log, chat_panel, server, chat.js and API test_chat_panel. |
| P01/P01-T01 preservation | Both runtime intents, append-only log/index contributions and original adverse evidence retained | Reconciled | Direct source/patch comparison and byte checks support preservation; details below. No blanket side selection was used for runtime conflicts. |
| Main-owned rubric/manifest acceptance | Empty diff against captured main; frozen-source test included | Reconciled | Independently repeated the exact-boundary Git comparisons; no snapshot exception or edit. |
| P02/P02-T01 | Component static checks, focused unittests, mandatory browser checks, migration regressions and local candidate commit | Reconciled | Supplied command/results tables distinguish initial failures from corrected passes. Focused validation does not establish a complete local gate. |
| P03/P03-T01 | Candidate committed; one independent Review next | Reconciled at this assessment | This original Review is the requested single assessment, not an implementation iteration. Parent must persist its evidence separately without claiming later-head approval. |
| Follow-Up Items | Hosted checks/publication; original RV-001 through RV-005 and human/activation gates | Reconciled | Outside refresh acceptance and not silently completed. Existing destinations and publication blockers remain. |

The plan checklist leaves P03 unchecked and the details/changes correctly
identify it as the next lifecycle phase. The plan's "Ready task after critique:
P01-T01" is a planning-stage handoff statement, not evidence that the later
implementation did not run. Current phase markers, candidate identity and
changes reconciliation provide a credible assessment boundary.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 selected skills | src/api/src/zava_forward/api/server.py; src/core/src/zava_forward/core/chat_panel.py | Preserve main's explicit skill selection through the topic's consumption wrapper | server.py:713-718 passes skill to ask; chat_panel.py:336-385 forwards it to _ask, validates it and applies skill_sources | Existing five-skill/general, invalid-selection, scope and audit tests retained; recorded API pass | Conformant. The wrapper does not lose the selected skill. |
| P01-T01 completion lens | src/core/src/zava_forward/core/chat_panel.py | Recheck current permissions and sources after provider completion without comparing unlike source projections | chat_panel.py:383-385 and 472-481 apply the same selected-skill transformation before comparison | Added test_skill_source_change_during_call_withholds_and_keeps_usage exercises general and every registry skill, checks withheld output and seven-token receipt | Conformant. Main's workflow sources and skill lenses coexist with topic revocation/usage handling. |
| P01-T01 context cap | src/core/src/zava_forward/core/chat_panel.py; src/api/tests/test_chat_panel.py | Include selected-skill system instructions in the combined input cap and preserve fallback metadata | chat_panel.py:437-444 builds final system before measuring; finish at 391-406 preserves skill/context and chat.answer audit; outer finally retains chat.turn | Added test_skill_context_limit_counts_selected_system_and_preserves_audit verifies fallback, skill, case context, no provider call and fallback audit | Conformant. The test deliberately sets a cap that excludes the extra selected-system text; it would expose omission of that text. |
| P01-T01 browser conflict | src/api/src/zava_forward/api/web/chat.js; src/api/tests/test_case_journey.py | Preserve main's draft-version helper together with topic privacy readiness, unsaved tracking, refusal and manual fallback | chat.js:139-143 helper is byte-identical to main; 183-202 snapshots before request and clears only through that helper; 219-231 fails closed until warning readiness | Existing draft-change/whitespace/failure harness preserved; fixture supplies chat/status and waits for readiness; recorded 26-test case-journey pass | Conformant. Newer drafts are not replaced with the topic's older trimmed-string equality behavior. |
| P01-T01 test conflict | src/api/tests/test_chat_panel.py | Retain main employee-skill tests and topic admission/privacy/receipt/browser tests | Main has 18 named methods, topic 19, candidate 28; all topic names remain. Only main's 8,000-character success method is renamed to the bounded fallback test | Recorded API 118 including Chromium, no skips | Conformant. The renamed regression still verifies masked storage/redaction and now asserts zero-call inference fallback, matching the existing topic's 1,000-character allowance. |
| P01-T01 disclaimer | src/api/checks/regulatory_ux_check.py | Narrow the locator after a second muted privacy paragraph was introduced | :299-306 uses #chat-panel > summary + p.muted; asserts exactly one visible element and both original disclaimer clauses | Supplied regulatory JSON reports passed, 19 scans, pinned axe executed | Conformant. The selector targets the actual disclaimer, not both muted paragraphs or an arbitrary first match. |
| P01/P02 admission and legacy route | src/agents/src/zava_forward/agents/chat.py; src/api/src/zava_forward/api/server.py | Retain default-deny admission before/after provider use, safe receipts, legacy cited/refusal routing and status/skills endpoints | ChatModel checks admission around provider_call and preserves validated usage; both routes compose through panel.ask; main logging remains at chat_panel.py:466-470 | Recorded agents 47 and API 118; existing admission, source-change and role/isolation coverage retained | Conformant for integration, not activation authorization or a remedy for original accounting RV-001. |
| P01/P02 documentation | docs/reference/README.md; docs/reference/log.md; src/api/README.md | Preserve main contributions and append topic evidence; distinguish storage from inference limits | Complete main log bytes remain the prefix and complete original topic suffix is present; only the intended chat-DPIA index row changes relative to main | Direct byte/diff inspection; original 2026-10-27 changes, critique and Review compare identical to pre-rebase topic | Conformant. Neither original adverse conclusions nor unrelated main index/log contributions were erased. |

All changed production implementation remains under src component packages.
Tests remain in sibling tests directories and browser tooling in checks;
there is no new legacy implementation, package-contained test or test framework.
The refresh adds only the two directly coupled integration methods described
above. The larger test delta relative to main includes replayed topic tests,
not additional refresh-budget methods.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01/P02 main snapshots and preflight | Require exact captured-main copies and fresh execution checks | PC-001/PC-002; user already selected main copies and authorized rebase | Current acceptance criteria, phase details and changes use the same immutable main SHA | Single critique remains Complete / Revise; compatible corrections recorded, no second critique | Reconciled. Actual checks support the revised constraints. |
| P02 selector/import/browser contract | Resolve commands and source precedence before execution; mandatory browser coverage on actual overlaps | PC-003 and changed web/browser paths | Changes contains directory/command/coverage table, worktree import-origin report and explicit skip/full-gate boundaries | Compatible planning correction; no new user decision | Reconciled. Import-origin evidence is reported implementation evidence, not an import probe rerun by this Review. |
| P01/P02 semantic conflict refinements | Same completion lens, final-system cap, main draft helper and two integration tests | Actual conflicts plus the existing caller requirement to preserve both sides | Changes describes rationale and initial failures; current details retain the original accepted integration scope and two-method budget | No material direction change or fresh critique required | Reconciled. No feature expansion, price/budget authority or human approval invented. |
| P02 post-candidate bookkeeping | Replace in-progress commit statements with ca5cb010 and record preservation/identity checks | Candidate commit completed | Current changes, details and opening Review agree on the source candidate and P03 boundary | Evidence-only updates after implementation | Reconciled. They are considered as current evidence, not silently folded into an exact-head approval. |

The failed initial patch attempt is recorded as having changed no files.
Initial browser navigation and formatting failures are retained, together with
their corrections and subsequent results. This is not a rewritten all-green
execution history.

## Critique and Material Revision Assessment

* PC-001 applied: the unauthorized manifest-hash exception is absent. Main
  rubric/manifest bytes are unchanged and manifest validation is reported
  passing. No contradictory exception was used.
* PC-002 applied: changes records fresh expected-branch/worktree/rebase-state
  and open-draft lifecycle checks, the pre-rebase topic SHA, fetched immutable
  main SHA and actual rebase result. Independent ancestor and unmerged-path
  checks agree. This Review did not repeat remote operations.
* PC-003 applied: concrete focused selectors, ordered source/test paths,
  component tools and browser entry points are recorded. API output independently
  inspected here confirms 118 tests / OK; supplied regulatory output confirms
  19 states with pinned axe executed. Other results are assessed as recorded
  evidence, not rerun or newly certified by the assessor.
* PC-004 remains explicitly partially applied in the plan: focused-only
  execution was retained, while the parent rejected the finding's claimed
  instruction premise about external scratch. The original critique and its
  Revise verdict are preserved. This Review does not resolve or retrospectively
  certify that instruction-premise dispute. No full discovery or locking
  contingency was exercised, so the disputed fallback supplies no acceptance
  evidence. Any later executor must obey its then-current filesystem and
  shared-lock restrictions; neither the plan's probe nor this Review authorizes
  a lockless full API run.
* Dependent-work pause: the supplied changes records critique dispositions
  before implementation. No evidence of a divergent decision or premature
  resumption was found in the assessed boundary.
* Material revisions: none beyond compatible conflict reconciliation and
  evidence bookkeeping. The 8,000-character storage versus 1,000-character
  inference distinction is an intentional pre-existing topic constraint, now
  explicitly reconciled with main's regression rather than silently weakened.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Complete local publication gate and later exact-head checks | Focused tests cannot produce the mandatory full receipt; original Review evidence must first be committed | Active parent attempts complete gate after persisting this original Review and records actual prerequisites/results | Open publication prerequisite, not a new refresh implementation defect or a passed check |
| Coordinator publication and fresh hosted checks | No push is authorized; hosted CI cannot run on the unpushed source candidate | Coordinator/owner retains publication decision after existing blockers and required evidence are satisfied | Open distinct follow-up; old rubric failure is not established fixed |
| Original RV-001 through RV-005 | Expressly excluded from this local rebase refresh | Preserve the original finding owners and routes below | Open, unchanged; no remediation or acceptance credit claimed here |

These items remain outside active refresh implementation/completion claims.
The changes artifact mirrors the plan's follow-ups. In particular, deferring
original RV-001 from refresh work does not remove its existing publication block.

## Bounded Web Guideline Assessment

Refreshed and read the complete current rules on 2026-10-29 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed the changed chatCasePanel hunks and their helper/employee-dialog
context in src/api/src/zava_forward/api/web/chat.js. Repository Fluent 2,
native semantics, plain-language and ASCII requirements take priority over
generic typography, title-case or aesthetic recommendations.

## src/api/src/zava_forward/api/web/chat.js

Pass for the changed integration scope; no new file:line finding.

The changed input has an associated native label, name, autocomplete setting
and described warning; status and conversation updates retain live semantics.
The main version-aware helper and manual-error path remain intact. Disabling
submission before the privacy warning is ready is an intentional fail-closed
boundary, not an instruction to enable an unsafe form to satisfy a generic
form rule. The inherited request state uses textual feedback rather than a new
spinner. No changed media, animations, date formatting, hydration, styling or
navigation surface requires a redesign.

This is not a fresh whole-file/whole-site conformance audit. Automated browser
and axe evidence does not establish named human screen-reader, comprehension,
Fluent adoption or WCAG acceptance.

## Findings

No new refresh-scoped RV-xxx finding is established by this assessment.
Do not renumber or reinterpret the original 2026-10-27 RV-001 through RV-005
as findings introduced or resolved by this refresh.

## Defects

* No newly established implementation defect within the bounded refresh.
* Original RV-001 remains an unresolved Medium implementation/reporting defect:
  the initial current-user denial precedes the receipt try/finally in
  chat_panel.py:340-354. This is preserved original evidence, not a new finding
  or an authorized repair in this Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| Original RV-001 [Medium] | Later rpi-implement | Original reporting owner adds explicit zero-call denied-turn coverage and regression under separate continuation | Existing defect and publication blocker; refresh intentionally does not repair it |
| Original RV-002 [High] | Later authorized rpi-research | Define claim-level/held-out, independently labelled evidence and evaluation prerequisites | Existing semantic/effectiveness evidence gap, not fixed by source lenses or passing focused tests |
| Original RV-003 [High] | Distinct human decision follow-up | Owner/DPO/Legal/access-policy and activation authorities record required decisions | Code or scripted tests cannot approve privacy, access, memory or activation |
| Original RV-004 [Medium] | Distinct accessibility follow-up | Named accessibility participant and owner arrange authorized screen-reader/comprehension exercise | Browser automation cannot establish human acceptance |
| Original RV-005 [Medium] | Distinct parent/#440 follow-up | Stabilization owner completes separate evidence | Whole-parent stabilization is outside bounded refresh |

All routes above are retained from the original Review, whose outcome remains
Not accepted. Later implementation of a routed finding does not require another
Review in this loop.

## Residual Work

* The active parent must persist this original Review and final local handoff
  evidence. That later evidence commit is not the source candidate assessed here.
* The complete local gate has not yet run. Its attempt follows the original
  Review evidence commit; missing prerequisites must remain blockers, not skips
  presented as passes or cloud fallbacks.
* No push, hosted success, feature acceptance, issue closure or activation is
  authorized by this bounded conformant result.

## Blockers and Remaining Work

* No blocker to completing this independent local-refresh assessment.
* Publication remains blocked by the original RV-001 and the absent complete,
  current local-gate evidence/receipt and required publication assessment.
  Any additional prerequisite failure discovered by the later gate is for the
  parent to record, not anticipated as a fabricated result here.
* Fresh hosted checks are unavailable on this unpushed head. Earlier source
  passes and rubric failure/pending observations concern the old hosted head.
* P03's local evidence commit/handoff remains parent-owned. No source repair,
  changed acceptance decision or second Review is performed here.

## Validation Evidence

Recorded implementation results below are assessed as supplied evidence.
This assessor ran only read-only comparison/preservation checks, not the
application suites, browsers, scanners or complete gate.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| git merge-base --is-ancestor 5653547507f3056f09a726a18516237728da5e5b ca5cb0101040c8176c4f32812be71af02b56670a; git ls-files -u | Candidate ancestry/unmerged paths | Passed, independently checked | Captured main ancestor; no unmerged paths |
| git diff --exit-code 56535475 ca5cb010 -- .github/rubric docs/reference/research/retrofit-synthetic-data/scenario-manifest.json | Main-owned snapshots | Passed, independently checked | Empty diff; no rubric/workflow weakening |
| git diff --exit-code 949aafaf ca5cb010 -- original 2026-10-27 changes/critique/Review paths | Original adverse evidence | Passed, independently checked | All three original records byte-preserved |
| Read-only Python/git show assertions and named-method inventory comparison | Log prefix/topic suffix, main helper, both test groups | Passed, independently checked | Complete log contributions and helper retained; no topic methods lost; main long-question method intentionally renamed |
| git diff --check 56535475 ca5cb010; git status --short -- src .github/rubric manifest | Diff integrity/source boundary | Passed, independently checked | No whitespace errors or current dirty source/snapshot paths |
| Core command in changes Validation Command and Coverage Contract | Six focused core modules including scenario manifest | Passed, recorded | 86 tests, no skips |
| Agents command in changes Validation Command and Coverage Contract | Model/eval/provenance/fixture/dependency modules | Passed, recorded | 47 tests, no skips |
| API corrected command with ZF_BROWSER_TESTS=1 in changes | Chat panel/isolation/roles/fixture/case journey/dependency modules | Passed, recorded and output inspected | api-focused.log ends Ran 118 tests / OK; supplied record states no skips and actual Chromium |
| Initial API selectors and initial format checks | Earlier validation attempts | Failed, preserved | Browser used old case-tab location; format failures corrected. They are not represented as final passing attempts |
| /tmp/mv/bin/ruff check .; /tmp/mv/bin/ruff format --check .; /tmp/mv/bin/mypy, each core/agents/api | Full affected-component static checks | Passed, recorded final results | Core 106 formatted/159 typed; agents 20/24; API 56/107 |
| python -m checks.employee_chat_browser_check with ordered PYTHONPATH and pinned axe, as recorded | Employee dialog and controlled late-completion/access/lifecycle states | Passed, supplied record | Six skill choices and nine controlled late successes reported; raw output was not present in the listed session files and was not independently rerun |
| python -m checks.regulatory_ux_check with ordered PYTHONPATH and pinned axe, as recorded | Synthetic regulatory/chat browser states | Passed, supplied JSON inspected | regulatory-chat.json: passed, 19 scans, axe 4.10.3 executed, hash 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb |
| Design-system browser check including delegated workbench checks, as recorded | Existing broader browser contract | Passed, supplied record | Chromium 156.0.8078.4 reported; raw report was not present in the listed session files and was not independently rerun |
| Separate test_case_journey rerun; workflow isolated browser-module Ruff/format | Final fixture-line correction and existing browser tooling | Passed, recorded | 26 tests; browser modules static checks passed |
| node --check src/api/src/zava_forward/api/web/chat.js | JavaScript syntax | Passed, recorded | No syntax errors reported |
| /tmp/mv/bin/python tools/rename-zava-tests.py | Migration regressions | Passed, recorded | 25 tests; deliberate broken.pptx rejection retained |
| Current guideline fetch and bounded changed-web inspection | Web integration | Passed, independently performed | Full source retrieved; no new changed-scope finding; not conformance certification |
| Full API discovery | Broad/heavy suite | Skipped intentionally | Not needed for focused refresh; no shared-lock execution claimed |
| python3 tools/rpi-checks.py --all | Complete local publication gate | Unavailable as evidence at Review time | Parent's later attempt is pending original Review evidence commit; no receipt or pass claimed |
| Fresh hosted CI | Unpushed candidate | Unavailable | No push authorized; old hosted results cannot validate this candidate |
| Named human accessibility, privacy/legal and actual-model acceptance | Original feature/activation gates | Unavailable | Not supplied by these local tests and outside refresh authorization |

The existing /tmp/mv command paths are implementation evidence, not files
created by this assessor. No temporary output or shared lock was created by
this Review. Supplied browser/suite results are not elevated to independently
rerun validation merely because they appear in this table.

## Outcome

* Outcome: Conformant, for the bounded local rebase refresh only.
* Outcome rationale: semantic conflict inspection supports preservation of
  both main and topic intent, selected-skill forwarding and rechecks, full
  selected-system cap, main draft-version handling with privacy readiness,
  both existing test groups and the precise disclaimer assertion. Immutable
  snapshots, ancestry and historical evidence checks agree with the recorded
  execution. Focused validation supports compatibility without claiming a
  full gate, hosted success or original feature acceptance.
* This is not exact-head publication approval. Current evidence-only changes
  and the parent's future Review/state/evidence commit are outside the
  implementation source boundary. Original Complete / Not accepted and
  RV-001 through RV-005 remain unchanged.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| New refresh implementation defect | None | No new defect established; no repair handoff from this Review |
| Decision gap or invalid assumption | None newly established | Preserve current accepted refresh intent and original critique disposition; no new plan decision needed |
| Material evidence gap | Existing RV-002 to later authorized rpi-research | Original evidence owner retains claim-level/independent evaluation work |
| Existing implementation defect | Original RV-001 to later rpi-implement | Original reporting owner; publication block remains |
| Non-blocking refresh residual work | Distinct parent handoff/gate and coordinator hosted-check follow-ups | Persist evidence, attempt required local gate without push, retain existing restrictions |
| Existing external residual work | RV-003, RV-004 and RV-005 distinct owners | Human decisions, named accessibility exercise and #440 stabilization |

* Execution status: Complete, one independent Review.
* Outcome: Conformant for refresh scope, not whole-feature acceptance.
* Validation coverage: independent source/preservation inspection plus
  supplied focused suite/static/browser/migration evidence; no full-suite,
  full-gate, new hosted or human acceptance evidence.
* Blockers: original RV-001, absent required local-gate/publication evidence
  and unavailable fresh hosted checks; original human/activation gates remain.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md](.copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md) | Current refresh plan and critique dispositions |
| [.copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md](.copilot-tracking/details/2026-10-29/agent-chat-157-refresh-phase-details.md) | Current phase details and candidate boundary |
| [.copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md](.copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md) | Focused branch/check research |
| [.copilot-tracking/reviews/plans/2026-10-29/agent-chat-157-refresh-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/agent-chat-157-refresh-plan-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-29/agent-chat-157-refresh-changes.md](.copilot-tracking/changes/2026-10-29/agent-chat-157-refresh-changes.md) | Current commands, failures, passes and limitations |
| [.copilot-tracking/reviews/logs/2026-10-27/agent-chat-157-review.md](.copilot-tracking/reviews/logs/2026-10-27/agent-chat-157-review.md) | Unchanged original Not accepted outcome and RV-001 through RV-005 routes |
| [.copilot-tracking/reviews/logs/2026-10-29/agent-chat-157-refresh-review.md](.copilot-tracking/reviews/logs/2026-10-29/agent-chat-157-refresh-review.md) | This single original independent refresh Review |

## Next Steps

Return this record to the active parent. Persist the original Review and local
handoff evidence, then attempt the required complete local gate under the
applicable filesystem/shared-lock restrictions and record actual results.
Do not push, repair findings, alter original acceptance or perform a second
Review in this loop. Retain the original RV-001 publication blocker and all
existing routes; this bounded conformant outcome grants no later-head,
hosted, human, feature or activation approval.
