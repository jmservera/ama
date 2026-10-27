<!-- markdownlint-disable-file -->
# Review: Per-user agent chat and memory

## Scope and Evidence

* Task ID: 157
* Review date: 2026-10-27
* Review scope: independent engineering delivery across P01-P03, not live activation.
* Assessed boundary: baseline 0ded682bab690d24eb59b78e704be82d337bf6cd plus src diff SHA-256 2e616b6c2242ffbe37022a78409948e34c5ea7c8d6fef48050ba8623d1d43cf7.
* Research: .copilot-tracking/research/2026-10-27/agent-chat-157-research.md
* Plan: .copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/agent-chat-157-changes.md
* Evaluation: .copilot-tracking/changes/2026-10-27/agent-chat-157-eval.json

## Opening Review State

* Interpreted review goal: independently assess whether bounded changes meet the approved engineering plan without manufacturing whole-issue or human acceptance.
* Review scope: dispatch/admission, prompt/current-source isolation, receipt accounting, warning/UI, legacy-route parity, development reporting and evidence reconciliation.
* Evidence readiness: reconciled P01-P03, original critique and dispositions, final 80-test API/browser pass, 109-test agents discovery, static gates and migration tests. Supplemental full core/API suites remain pending, not passed.
* Acceptance basis: current plan acceptance criteria, #157/#162/#159/#164/#163 evidence matrix and explicit owner local-only constraints.
* First comparison boundary: complete src diff versus plan and tests; current human/semantic residuals are not new implementation defects.
* Active read-only boundaries: no source/plan/details/changes/research/critique mutation. Only this canonical Review record may be updated.
* Initial blockers: DPO/Legal/access-policy/retention/provider approvals; human accessibility and independently labelled/serving-model evidence; known grounding failure; #440 stabilization and actual approved role budgets. These block activation/closure, not independently reviewable offline engineering.

## Execution Status

* Execution status: Complete
* Review execution evidence: one independent comparison of the current plan, details, original critique, changes, research, generated evaluation and all 17 tracked changed source/documentation/test files against baseline 0ded682bab690d24eb59b78e704be82d337bf6cd.
* Source diff SHA-256 independently checked twice: 2e616b6c2242ffbe37022a78409948e34c5ea7c8d6fef48050ba8623d1d43cf7. This identifies the assessed uncommitted source delta, not an accepted commit or later publication head.
* No subagents, fixes, plan changes, repeated Review, model calls, cloud operations, private-data inspection or heavy gate. Only this record was written. Review execution is complete even though one engineering acceptance gap and external residuals remain.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Runtime: shared cited routes, admission, usage, prompt bounds and completion checks | Reconciled for the present default-denied API boundary | Adapter checks admission twice; source/current-role changes suppress the answer; usage survives the tested completion failures. No conversational release is registered or approved. |
| P02 / P02-T01 warning | Warning and evaluation; scoped web review | Reconciled | Server-owned warning, disabled entry, described input, native controls, refusal/manual route and unsent-input guard match the bounded plan. |
| P02 / P02-T01 reporting | Per-turn/scenario/runtime-answer consumption | Partial | Generated report contains 59 consumption entries for 61 scenario turns. Two pre-dispatch permission denials disappear from the consumption list, RV-001. |
| P03 / P03-T01 | Validation, acceptance matrix, documentation and Review preparation | Reconciled within stated validation limits | Targeted/static/browser evidence is reported; broad core/API discoveries are pending. A completed preparation task does not establish this Review's acceptance or exact-head gates. |
| Follow-Up Items | Human decisions, semantic failure and stabilization | Reconciled as external residuals | Explicitly outside active implementation and whole-issue closure. Routes appear below. |

The changes header still says implementation is in progress, while its later
P03 and Handoff sections and current plan/details say preparation is complete.
The later, explicit frozen-boundary handoff supplies an unambiguous reviewable
candidate; the stale introductory wording is not evidence that validation or
acceptance occurred. Completion claims for P02 reporting require RV-001's
qualification.

## Completed Work Assessment

| Marker | Files | Completion evidence | Assessment |
| --- | --- | --- | --- |
| P01-T01 | src/agents/src/zava_forward/agents/chat.py; src/agents/tests/test_chat_model.py | Missing/denied admission prevents provider invocation; completion denial discards text and retains validated usage; bool/negative/inconsistent token counts become Unknown; fixed failure outcomes do not copy provider errors | Present-path contract supported. No shared last-usage state or retry added. |
| P01-T01 | src/core/src/zava_forward/core/chat_panel.py; src/core/src/zava_forward/core/chat_isolation.py | Complete serialized source map rather than generic 2,000-character block truncation; final system/prompt ceiling; bounded user-only history; no assistant-history or retained-memory prompting | Engineering character bounds are not tokenizer, per-role budget or semantic grounding guarantees. Source values retain the pre-existing projection/value limits. |
| P01-T01 | src/core/src/zava_forward/core/chat_panel.py; src/api/tests/test_chat_panel.py | Current user/thread/case re-read after callback; changed projected sources or role withhold; removed role/case/thread reject; finally records incurred usage for those tested post-call paths | Supported for normal-process accounting, not crash-safe or transactional exactly-once billing. RV-001 concerns earlier zero-call rejection, not these incurred-call cases. |
| P01-T01 | src/api/src/zava_forward/api/server.py; src/api/tests/test_chat_isolation.py; src/api/tests/test_role_endpoint_inventory.py | Both HTTP turn routes call the panel; legacy reply/label/model/withheld keys retained; unapproved actual adapter denied on both routes; regulatory and proposal paths remain distinct | Deliberate removal of legacy uncited replies and HTTP memory prompting is documented, not a regression to restore. Direct core memory assembly remains tested separately. |
| P02-T01 | src/api/src/zava_forward/api/web/chat.js; src/api/tests/test_chat_panel.py | Canonical warning/status route, accessible description, fetch-failure lockout, refusal/manual status, keyboard/focus/live-log/390px tests and unsent-input retention | Bounded browser behavior supported; no named screen-reader or full reflow/conformance claim. |
| P02-T01 | src/agents/src/zava_forward/agents/chat_eval.py; src/agents/tests/test_chat_eval.py | Ledger-derived consumption, distinct scripted/actual calls, Unknown usage/cost and runtime-answer denominator | Aggregate arithmetic is correct; per-turn completeness is not, RV-001. New test checks reported entries but does not require an entry for every scenario turn. |
| P03-T01 | docs/adrs/0004-per-user-agent-chat-and-memory.md; docs/reference/research/chat-memory-dpia.md; docs/reference/README.md; docs/reference/log.md; component READMEs | Stale no-implementation statement corrected without changing ADR direction; warning/route/receipt/current privacy boundaries documented; index and append-only log updated | No approval or deployment inferred. Original case study and memory remain unchanged. Documentation links inspected. |

Twelve added test methods across existing files are within the locked maximum
of twenty. No test method was removed. Moving the legacy memory assertion to
direct isolated assembly preserves that lifecycle check while intentionally
removing HTTP memory activation; it is not equivalent to a live memory test.

## Issue-by-Issue Acceptance Assessment

The complete changes-record matrix was assessed against the changed code,
existing boundary and generated development evidence. No GitHub checkbox or
issue state was changed in this Review.

| Issue / criteria group | Engineering assessment | Remaining acceptance boundary |
| --- | --- | --- |
| #157 accepted direction and child acceptance | ADR 0004 preserves staged Option C; bounded hardening is not first implementation | Direction does not close children or parent. |
| #157 stabilization, memory/control and consumption | No controlled-record tool or new agent/store; neither HTTP turn prompts retained memory; context caps and normal-process receipts added | #440 and actual finite role call/token/budget/expiry authority remain open; RV-001 limits per-turn report completeness. |
| #162 server owner key, endpoint denial and field projection | Server derives caller; status inventory and legacy parity added; existing cross-user/canary tests retained | No new owner selector or cross-user retrieval path found. |
| #162 prompt isolation, revocation and injection | Current projected sources and post-call checks; assistant answers excluded; decoded answer checked for tool syntax; no executor added | Lexical/scripted checks do not establish semantic or actual-model injection resistance. |
| #162 administrator/break-glass | Existing audited metadata-only default denial unchanged | OD-46 remains a human policy decision; no content-access authority granted. |
| #159 optional panel, citations and abstention | Current-source citations, labels, refusals and legacy routing supported | Citation existence is not entailment. Known unsupported-claim acceptance remains, RV-002. |
| #159 follow-up permissions and proposals | Per-turn and completion checks; role-history regression; existing independent proposal-review path unchanged | No consent, approval, contact or record-write authority added. |
| #159 failure/manual route and tokenomics | Admission/provider/input-limit fallbacks and warning failure behavior supported | Runtime acceptance is not human acceptance; real usage/prices/role budgets remain unavailable. |
| #159 keyboard, screen reader and announcements | Actual Chromium evidence supplied; native controls, focus and live-log structure inspected | Named human screen-reader/announcement/comprehension exercise remains open, RV-004. |
| #164 golden multi-turn/source/refusal coverage and comparator | Existing shared harness retained; 24 development scenarios, 61 turns; expected-answer comparator remains distinct from runtime answers | No independently labelled held-out set, measured human review effort or observed benefit. |
| #164 poisoning, stale/conflicting/unsupported/revoked evidence | Scripted attacks and source/access changes exercised; original failure explicitly retained | Two critical checks fail in one known scenario. Memory-free HTTP paths do not prove all-input or serving-model behavior. |
| #164 task/version/threshold/reviewer/enablement | Updated development bindings and fail/disabled report; conversational task remains unregistered and default denied | Actual serving/control versions, thresholds, named qualified reviewer and release approvals absent. |
| #164 human seeded-error exercises, payload/provider limits and tokenomics | Zero actual calls; 33 scripted calls and 19 runtime-accepted answers; tokens/cost Unknown | No human or spend approval inferred; RV-001 is a reporting gap independent of those approval blockers. |
| #163 data map and diagnostics/performance exclusion | Current HTTP prompt differs from direct memory assembly; receipt metadata excludes question/answer/source/memory/provider-error text | Linkable user/thread metadata still needs retention/use/rights decisions; target SQL/uksouth architecture is not observed processing evidence. |
| #163 lawful basis, notice, DPIA, retention and provider region/handling | Draft expressly preserves unknowns and lack of current provider terms | DPO/Legal decisions remain absent, RV-003; no retention number or transfer position invented. |
| #163 locate/delete and warning/redaction | Existing content lifecycle tests retained; warning now beside described staff input and fail closed on retrieval failure | Ledger/backups/provider erasure and other free-text surfaces are not fully assessed; masking and warning do not establish comprehension or lawful processing. |

All five issues remain Refs, not Closes. Existing checked criteria are not
reclassified as live or whole-issue acceptance.

## Implementation-Time Plan and Detail Update Assessment

| Area | Update, reason and evidence | Decision/reconciliation assessment |
| --- | --- | --- |
| P01-T01 admission and receipts | PC-001/002 triggered completion-time admission and exceptional-turn accounting changes | Compatible engineering correction, no new human authority needed. Tests cover revoked admission and incurred calls after role/case/thread rejection. Earlier permission-denial accounting remains incomplete, RV-001. |
| P01-T01 legacy route and memory | Route convergence deliberately removes HTTP memory prompting; direct memory assembly remains testable | Matches staged memory gate and stated no-activation intent; current plan/details/changes and API/DPIA documentation agree. No DPO rejection or permanent Option B decision inferred. |
| P01-T01 history and decoded output | Prior-role questions dropped when thread owner role differs; decoded tool-like output checked in addition to raw JSON | Tightening the existing isolation boundary, not a new task/authority. Historical assistant answers remain excluded. Not a semantic-entailment claim. |
| P02-T01 reporting | Random thread IDs removed only from exported report; current development bindings and economics added | Compatible deterministic reporting update; 18 expected/case-card answer turns and 19 runtime answers correctly distinguished. Missing two zero-call entries is not reconciled by those aggregate totals. |
| P02-T01 browser | Unsent question retained and existing form navigation guard reused after failed request | Compatible failure-path completion; final supplied Chromium run includes it. No framework/style overhaul or added approval scope. |
| P03-T01 validation/publication | Dependency restoration after missing-import failures; targeted rather than optional heavy gate; one-pass Review and material-defect publication boundary clarified | Original failures and limited passes are recorded. No second critique/Review or exact-head acceptance is implied. |

These updates preserve confirmed local-only intent. No material expansion into
live activation, spending, new agents or human decisions was found. New
engineering completion claims nevertheless remain subject to RV-001.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with one High and three Medium findings. Its original verdict is not rewritten.
* PC-001 applied for the present admission boundary: adapter denies missing admission, checks before dispatch and again after completion, and preserves usage on denial. The current unregistered conversational task cannot select an approved release. The boolean/reason callback does not capture or compare a selected release identity; no release-replacement assurance is established. Before any future registration/activation, a release-bearing path must supply that binding and corresponding replacement/continuity evidence. This is not a request to register the task or a demonstrated bypass of the current default-denied routes.
* PC-002 substantially applied for invoked calls and tested post-call failures: metadata is retained independently of answer persistence and read from the ledger. The broader zero-call/per-turn reporting acceptance is incomplete for initial current-user denial, RV-001.
* PC-003's original finding and rejected disposition are preserved. The parent's disposition treats the asserted earlier environment prohibition as unsupported. This Review does not retroactively change that historical instruction assessment or execute the recorded external-path commands.
* PC-004 partially applied as recorded: original outcome and assessed boundary remain immutable; new material defects block publication and route to later implementation. Human/semantic residuals alone would permit only a Refs-only draft PR. No repeated Review is authorized.
* Planning/critique readiness: no new divergent user decision was inferred and no fresh critique was performed. Changes and details document the compatible implementation-time refinements. RV-001 is an implementation/reporting gap, not grounds to invent a new plan or approval.
* Dependent-work pause: supplied artifacts show the critique dispositions incorporated into the current direction; no evidence of an unaccepted live or authority-expanding revision was found.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Human owner/DPO/Legal decisions | Cannot be supplied by local code or scripted tests | Owner/DPO/Legal to record OD-45/46/48/49 and actual provider/privacy/access/role-budget decisions | Open, distinct human follow-up, RV-003; not an engineering defect. |
| Named accessibility exercise | DOM and keyboard tests cannot demonstrate screen-reader announcements or comprehension | Named accessibility participant and owner to arrange authorized exercise | Open, distinct human follow-up, RV-004. |
| Known semantic grounding failure | Explicit existing development failure, not introduced by this delta | Later rpi-research to define independently labelled claim-level evidence and authorized evaluation prerequisites | Open material evidence gap, RV-002; no paid or human exercise authorized by this route. |
| #440 stabilization | Bounded integration is not the recurring whole-programme checkpoint | Parent/#440 owner to complete its separate evidence | Open, distinct stabilization follow-up, RV-005. |

Follow-ups remain outside P01-P03 completion and are not silently promoted into
new active tasks. Missing human decisions alone are not new engineering
defects.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Two pre-dispatch rejected turns are absent from per-turn consumption evidence

* Class: new bounded implementation/reporting defect.
* Related scope: P01-T01 zero-call accounting; P02-T01 per-turn reporting; PC-002.
* Evidence: src/core/src/zava_forward/core/chat_panel.py:300 calls current_user before receipt creation and the try/finally. A ChatForbidden at that point emits no chat.turn receipt. src/agents/src/zava_forward/agents/chat_eval.py:268-274 exports only new ledger receipts, with no explicit per-turn entry when that receipt is absent.
* Reproduced from the frozen generated JSON using a read-only standard-library count: 61 scenario turns, 59 consumption entries. Scenario permission-role-and-staff-revoked-mid-thread has three turns but only one consumption entry. Golden turns 2 and 3 explicitly expect ChatForbidden and model_called=false; both disappear from its consumption evidence.
* Impact: the required per-turn outcome/calls/usage accounting is incomplete precisely for two permission-denied turns. The new reporting test iterates existing receipts without asserting turn coverage, so reported test passes do not detect this. The 33 scripted calls, zero actual calls and 19 runtime answers are not numerically understated by these zero-call omissions. This is not an incurred-call loss, content leak, billing guarantee failure or new human-approval requirement.
* Destination: later rpi-implement, within the accepted reporting direction.
* Smallest useful next action: represent every scenario turn explicitly, including authenticated-but-currently-denied zero-call attempts, without restoring access or copying content. Distinguish an evaluator-derived pre-dispatch denial entry from an actual ledger receipt. Add a regression asserting full turn coverage, turn identity/outcome, and zero calls for those two rejections while preserving incurred-call accounting and the known semantic failure.
* Publication implication: blocks publication of this candidate under the caller's material engineering-defect rule. Do not repair it during Review or convert this original outcome into later-head acceptance.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Existing semantic grounding and independent effectiveness evidence remain insufficient

* Class: pre-existing material evidence gap, not a new implementation regression.
* Related scope: #159/#164; plan semantic Follow-Up Item.
* Evidence: agent-chat-157-eval.json preserves two critical failed checks in grounding-unsupported-claim-with-valid-citation: a permitted citation accompanies unsupported "Funding is secured." The report remains fail/disabled; labels, actual serving-model evaluation, human seeded-error exercises, reviewer and thresholds are unavailable.
* Impact: valid citation IDs and runtime acceptance cannot establish entailment, safe effectiveness, a saving, benefit or activation. The nineteenth runtime answer is the known unsupported claim, not an extra beneficial/comparator answer.
* Destination: later rpi-research for the evidence design and labelled grounding investigation; qualified owner controls any actual evaluation authorization.
* Smallest useful next action: preserve the failing development case, define independently labelled claim/source checks and held-out/serving-version protocol, and obtain prerequisite payload/provider/budget/reviewer approvals before any human or real-model exercise.
* Publication implication: alone permits only a clearly qualified Refs-only draft PR, not enablement or issue closure. RV-001 independently blocks this candidate's publication.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Human privacy, access, memory and activation decisions remain unrecorded

* Class: accepted external residual, not an engineering defect or invented approval.
* Related scope: #157/#162/#163/#164; OD-45/46/48/49.
* Evidence: ADR 0004, DPIA draft, current plan and issue matrix retain unknown lawful basis/notice/DPIA/retention/provider-region handling, break-glass policy, memory decision, thresholds/reviewer and finite role call/token/budget/expiry authority. ai_registry has no conversational entry; server admission defaults to denial.
* Impact: no live processing/model dispatch, spend authorization, memory activation, monitoring use, release acceptance or whole-issue closure follows from the hardening. Linkable receipt metadata still needs rights/retention decisions.
* Destination: distinct owner/DPO/Legal/access-policy and activation follow-up, not rpi-implement.
* Smallest useful next action: named humans record dated decisions and evidence. Any future activation work must separately establish selected release/version binding, continuity and actual serving/provider/budget contracts; current boolean admission tests do not establish release replacement safety.
* Publication implication: alone permits only Refs-only draft publication with explicit blockers; no activation or closure.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Named screen-reader and comprehension acceptance remains open

* Class: accepted external accessibility residual.
* Related scope: #159/#163; named accessibility Follow-Up Item.
* Evidence: changed chat.js uses native form/details controls, described warning and live status/log; supplied final 80-test API run includes real Chromium keyboard/focus/refusal/fetch-failure/390px and unsent-question checks. No named reader exercise, spoken announcement/comprehension result or complete zoom/reflow assessment is supplied.
* Impact: browser/DOM evidence cannot close the screen-reader criterion or justify accessibility conformance.
* Destination: distinct accessibility/human-validation follow-up.
* Smallest useful next action: owner arranges the named, authorized screen-reader exercise with warning/refusal/failure and ordinary-workflow paths.
* Publication implication: retain the limitation in a future eligible draft; no accessibility acceptance inferred.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Whole-parent stabilization remains separate

* Class: accepted programme residual.
* Related scope: #157/#440; stabilization Follow-Up Item.
* Evidence: changes matrix explicitly identifies local bounded integration, not the complete recurring stabilization checkpoint; broader core/API discoveries are still reported pending.
* Impact: targeted engineering evidence cannot establish whole-parent acceptance, deployment health or #440 completion.
* Destination: distinct #440/parent stabilization follow-up.
* Smallest useful next action: parent owner retains and completes the separate stabilization evidence without relabelling local passes or this Review.
* Publication implication: no parent closure. Later validation/artifact updates are not a second Review or exact-head acceptance.

## Defects

* RV-001: one Medium new reporting-completeness defect, routed to later rpi-implement and blocking publication.
* No new Critical/High implementation defect established. RV-002/003 are High residual/evidence risks; RV-004/005 are Medium residuals. The development evaluator's two critical checks are known failures in one scenario, not two new Review defects.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Later implementation adds explicit zero-call denied-turn coverage and regression | In-scope reporting defect; no plan or human policy change needed. |
| RV-002 | rpi-research | Define claim-level/held-out evidence under explicit evaluation approvals | Material existing evidence gap, not a new regression. |
| RV-003 | Distinct human decision follow-up | Owner/DPO/Legal/access and activation authorities | Agents cannot supply these decisions. |
| RV-004 | Distinct accessibility follow-up | Named human participant and owner | Browser evidence does not replace human acceptance. |
| RV-005 | Distinct #440 stabilization follow-up | Parent/stabilization owner | Outside this bounded implementation scope. |

Later implementation does not require another Review. Preserve this original
outcome and the assessed source boundary; record any later disposition as
unreviewed implementation/validation evidence, not independent exact-head
acceptance.

## Residual Work

* RV-002 through RV-005 remain distinct from the engineering defect and from each other.
* Future conversational registration/release selection is not part of this candidate. No request to enable or weaken the present default denial is made.
* Broad core/API suite results and hosted/publication gates are separate evidence; no result is inferred.

## Blockers and Remaining Work

* Publication blocker introduced by this Review: RV-001 remains unresolved. Do not push/open this candidate's PR merely because runtime and static checks passed.
* Activation/whole-issue blockers: known semantic failure; named human privacy/access/memory/threshold/provider/budget decisions; independently labelled serving-model/human evidence; named screen-reader exercise; #440 stabilization.
* Remaining active engineering gap: per-turn reporting coverage. P01/P03's tested work is not invalidated wholesale, but P02's per-turn completion and blanket P01-P03 engineering-complete claim are qualified.
* No human decision is guessed and no GitHub closure/checkbox action is authorized.

## Validation Evidence

| Check | Status / provenance | Scope and limitation |
| --- | --- | --- |
| git status, branch, baseline diff and src diff SHA-256 | Independently inspected | Correct supplied branch, 17 changed tracked files, expected frozen source delta; not a clean/committed exact-head gate. |
| Standard-library inspection of generated JSON and golden expectations | Independently inspected | Confirms 24 scenarios/61 turns, 59 consumption entries, 33 scripted calls, 19 runtime answers, two missing zero-call denied turns and known failure. No evaluator rerun or model call. |
| Final API: ZF_BROWSER_TESTS=1 PYTHONPATH=tests:../core/tests:../agents/tests /tmp/ama-chat157-venv/bin/python -m unittest test_chat_panel test_chat_isolation test_role_endpoint_inventory -q, from src/api | Passed, supplied parent evidence | 80 tests in 39.519s, real Chromium included; final network-failure unsent-input and navigation-guard checks included. Not independently rerun. |
| Focused core / focused agents / complete agents discovery | Passed, supplied parent evidence | 73 / 43 / 109 tests respectively; inspected changed assertions, no duplicate execution. |
| All-package Ruff check, format check and mypy; node syntax | Passed, supplied parent evidence | Core 153 / agents 23 / API 88 source files; no claim that static checks validate semantics or human approvals. |
| Migration regressions | Passed after dependency restoration, supplied parent evidence | 25 tests; initial seven missing-tool-import failures preserved, no source fix inferred. |
| Development evaluation | Failed as expected, generated artifact inspected | Two critical checks in one pre-existing unsupported-claim scenario; fail/disabled. Tokens/cost Unknown, zero actual model calls, no human acceptance/benefit. |
| Supplemental full core/API discovery | Pending / not independently inspected | Already running under parent ownership; neither duplicated nor stopped. No broad pass claimed. |
| Current Web Interface Guidelines and changed chat.js | Independently inspected | Full current source fetched; changed controls reviewed against applicable rules. Repository Fluent/plain-language/ASCII conventions retained. No new scoped UI defect found. |
| Screen reader, full zoom/reflow, human effectiveness, held-out actual serving-model evidence | Unavailable/not performed | Named approvals and evidence absent; not replaced by Chromium or scripted tests. |
| Heavy changed gate / full all gate / exact-head receipt / hosted gates | Not performed | Targeted checks selected; full gate expressly forbidden. No exact-head acceptance, publication receipt or human approval claimed. |

### Scoped Web Guideline Result

src/api/src/zava_forward/api/web/chat.js:34 - pass for changed warning/loading controls: native labelled and described disabled input, explicit manual-route error.

src/api/src/zava_forward/api/web/chat.js:46 - pass for changed submission/refusal/failure handling: native form, live status, retained unsent text and existing unsaved-form guard.

Scope is changed staff controls, not a fresh application-wide audit or
accessibility conformance statement. No CSS, framework, animation, media,
locale or theming change was introduced. Supplied browser evidence is distinct
from this read-only source review.

## Outcome

* Outcome: Not accepted
* Outcome rationale: the full independent Review completed, but RV-001 leaves the approved per-turn consumption reporting criterion unmet. Existing human/semantic residuals alone would allow a qualified Refs-only draft; this new bounded engineering gap blocks publication under the explicit caller rule.
* This is the one original post-implementation Review outcome. Do not replace it after corrections or publication/state/validation-only artifact updates.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, RV-001 | Explicit denied-turn consumption coverage and focused regression; no fix during this Review. |
| Decision gap or invalid assumption | No new rpi-plan route | Approved bounded direction remains intact; human decisions remain with their named follow-up owners. |
| Material evidence gap | Later rpi-research, RV-002 | Claim-level and independently labelled evaluation design subject to authorization. |
| External residual work | Distinct follow-ups, RV-003/004/005 | Human decisions, named accessibility exercise and #440 stabilization respectively. |

* Execution status: Complete.
* Outcome: Not accepted.
* Severity: one Medium implementation defect; two High and two Medium residual/evidence findings; no new Critical/High implementation defect established.
* Publication: blocked by RV-001. No source changes, PR or second Review performed here. Any later correction remains outside this original independently assessed source delta.
* Validation coverage: complete supplied boundary inspected; targeted/static/browser passes recorded as supplied evidence; generated report independently counted; known evaluation failure retained; broad results pending; heavy/full/exact-head/human gates not claimed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md](.copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md) | Current approved bounded engineering plan and follow-ups |
| [.copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md](.copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md) | P01-P03 contracts and implementation-time reconciliations |
| [.copilot-tracking/research/2026-10-27/agent-chat-157-research.md](.copilot-tracking/research/2026-10-27/agent-chat-157-research.md) | Bounded source/issue research and decision limits |
| [.copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md) | Original Complete / Revise critique, preserved |
| [.copilot-tracking/changes/2026-10-27/agent-chat-157-changes.md](.copilot-tracking/changes/2026-10-27/agent-chat-157-changes.md) | Implementation, validation and complete issue matrix |
| [.copilot-tracking/changes/2026-10-27/agent-chat-157-eval.json](.copilot-tracking/changes/2026-10-27/agent-chat-157-eval.json) | Development report: known semantic failure and RV-001 evidence |
| [.copilot-tracking/reviews/logs/2026-10-27/agent-chat-157-review.md](.copilot-tracking/reviews/logs/2026-10-27/agent-chat-157-review.md) | This single independent Review and original outcome |

## Next Steps

Return this record to the active parent. Stop publication on RV-001 and route
it to a later rpi-implement invocation; do not fix source or run another Review
under this task. Preserve Complete / Not accepted and the frozen boundary.
Route RV-002 to later authorized research and RV-003/004/005 to their distinct
owners. No live processing, spend, human approval or issue closure is granted.
