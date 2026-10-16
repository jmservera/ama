---
title: Regulatory evaluation gates post-implementation review
description: Single evidence-based RPI review for issue 216
ms.date: 2026-10-16
---

## Opening Review State

* Interpreted review goal: Independently assess correctness, safety and evidence integrity for issue #216.
* Review scope: All current tracked changes and untracked agents graders, fixtures, evaluations and tests, plus core freshness tests.
* Evidence readiness: Current plan, details, critique, research and changes artifacts located for regulatory-eval-gates, 2026-10-16. Detailed comparison pending.
* Acceptance basis: Supplied owner requirements and current reconciled task artifacts; synthetic-only ADR 0005 acceptance is not operational approval.
* First comparison boundary: Plan and critique dispositions against implementation, report and test evidence.
* Active read-only boundaries: No nested agents; only this canonical review record may be written. No source, plan, changes, private datasets, .env, .vscode or legacy prototype mutation.
* Initial blockers: None identified before comparison.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One direct post-implementation assessment of the supplied boundary, with source/test/report inspection and write-free negative controls. No nested agents or implementation changes.
* Implementation execution is separately partial: P01, P02 and P03-T01 are recorded complete; P03-T02 review/delivery was pending at entry. Commit, push and PR creation have not occurred as part of this review.

## Scope and Evidence

* Task ID: issue-216 / regulatory-eval-gates.
* Review date: 2026-10-16.
* Branch: feat/regulatory-eval-gates-216. Existing dirty implementation was preserved.
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-eval-gates-plan.md.
* Details: .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md.
* Latest and only supplied critique: .copilot-tracking/plans/2026-10-16/regulatory-eval-gates-critique.md. Its actual location differs from the skill's default reviews/plans location; there is no competing artifact set.
* Research: .copilot-tracking/research/2026-10-16/regulatory-eval-gates-research.md.
* Changes: .copilot-tracking/changes/2026-10-16/regulatory-eval-gates-changes.md.
* Session handoff: .copilot-tracking/rpi-sessions/2026-10-16/regulatory-eval-gates-state.json.
* Authority basis: docs/adrs/0005-regulatory-compliance-assistant.md, Evaluation and accepted synthetic-development boundary; original case study, addendum, knowledge-base index, memory and sector primer consulted for context. No legal-currentness conclusion is made.

The complete tracked diff was inspected:

| Files | Review boundary |
| --- | --- |
| docs/reference/README.md; docs/reference/log.md | New routing entry and append-only evidence/limitation claims |
| src/agents/README.md; src/agents/pyproject.toml | Acceptance audit, commands, packaging/type-check configuration |
| src/agents/evals/registry.json; src/agents/evals/regulatory_chat_results.json | Registration and legacy report migration |
| src/agents/src/zava_forward/agents/regulatory_eval.py; src/agents/tests/test_regulatory_answers.py | Coordinated legacy producer, golden equality and retained counts |
| src/api/README.md; src/api/src/zava_forward/api/server.py; src/api/src/zava_forward/api/web/chat.js; src/api/tests/test_regulatory_chat_api.py | Card collection/history decoration, rendered historical labels and loopback regression |
| src/core/README.md; src/core/src/zava_forward/core/regulatory_chat.py; src/core/src/zava_forward/core/source_monitor.py | Shared read-only cadence semantics and chat projection |

All supplied untracked source additions were inspected:

| Files | Review boundary |
| --- | --- |
| src/agents/src/zava_forward/agents/regulatory_gates.py | Pure citation/template, rule, refusal and comparison graders |
| src/agents/evals/regulatory_gates_cases.json; src/agents/evals/regulatory_gates_results.json; src/agents/evals/run_regulatory_gates.py | All 24 cases, complete recorded report and runner |
| src/agents/tests/regulatory_gate_fixture.py; src/agents/tests/test_regulatory_gates.py | Frozen oracle, actual-retrieval harness, scale/SQL profiles and negative controls |
| src/core/tests/test_source_freshness.py | Entire new freshness regression suite |

Relevant unchanged renderer, core retrieval, regulatory fixture, rule-engine item/alert identity, source-monitor write/cadence contracts and fictional home generator were also read. No private datasets, .env, .vscode or mvp/prototype content were accessed or changed.

## Plan-to-Change Reconciliation

| Current scope | Changes evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Independent per-check evaluation; legacy aggregate migration | Partial correctness | Frozen source/fact expectations and exact reply/sections are independent of retrieval, but visible card output is ungraded and summary classifications can misdescribe unsafe output; RV-001/RV-003. |
| P01-T02 | 24 adversarial questions; generated 60,000-home baseline | Partial correctness | Profile counts, fixed seed/as-of and unset recall threshold reconcile; result item identity is discarded before grading; RV-002. |
| P02-T01 | Shared cadence visibility on HTTP collection/history and chat | Reconciled | Exact due equality, last-success anchor, future latest failed attempt, missing storage and mixed-source reduction are implemented without activation/alert writes. |
| P03-T01 | Component validation, report and audit | Executed, with bounded evidence | Supplied full-suite evidence is recorded separately below. Review reproduced the pure baseline and found negative-control gaps not covered by those passing tests. |
| P03-T02 | One review, then delivery | Pending parent continuation | This record supplies the one review. Defects require disposition and targeted validation or explicit readiness-blocker disclosure before completion claims. No second review is requested. |
| Follow-Up Items | Owner/human/continuing-stock gaps | Reconciled outside scope | Still unmet and explicitly excluded from local acceptance; residual items below. |

## Completed Work Assessment

* The report correctly distinguishes 60,000 generated fictional identities and 120,000 stateless checks from continuing-stock ingestion, Azure SQL performance and real operational recall. Review reproduced the complete recorded deterministic_baseline object exactly using the actual pure evaluation/profile/generator functions.
* All ten hazard profiles and five automated-decision profiles have nonzero expected coverage. Recorded state totals reconcile to 120,000; actionable expected states to 78,000; required hazard flags to 42,000. The recall target remains null. Existing omission negative controls make a missing hazard result critical even while recall remains baseline-only.
* The independently authored source/fact oracle rejects extra citation/fact fragments, wrong source metadata, false refusals, reply-only conclusions and changed conflict escalation. It does not validate every newly visible answer field; RV-001.
* Missing staff comparison always selects cards_only, including an empty comparator input. Structural same-role/source-version pairs do not become staff benefit. Explicit bounded synthetic-development chat admission is unchanged.
* Source freshness reads do not construct SourceMonitor or initialize tables. Card reduction is overdue first, otherwise unknown for incomplete coverage, otherwise in-cadence. Collection/history and chat call the same read model. The UI uses textual labels and historical as-of values, with an unknown fallback for older stored turns.
* Existing legacy evaluator, report version, registry and golden test migrate together. The 13 historical cases and 3/3 cited-answer and 10/10 refusal evidence remain; the misleading top-level passed field is removed without removing a test.
* Exact method inventory against HEAD: 12 agents additions, six core additions and one API addition, totaling 19 of the maximum 45; zero methods removed. The modified legacy test retains its method identity.
* No changed executable files fall outside src/. Requested documentation and RPI artifacts are consistent with scope. No infrastructure, private-data, legacy prototype, approval or live-rule mutation is introduced.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and planning state | Assessment |
| --- | --- | --- | --- |
| P01-T01/P01-T02 | Critique required frozen oracle and complete closed template | Details name independent source/fact/kind expectations and mutation controls before implementation | Intent preserved; implementation still has RV-001/RV-002 blind spots. No divergent decision needed to fix them. |
| P01-T02 | Changes record describes automated-source fixture refinement | Both rule purposes were already in the approved scope and explicit profile contract | Justified refinement, not scope expansion or owner threshold agreement. |
| P02-T01 | Critique pinned missing-storage, multi-source and future-failure truth table | Plan, details, code and tests agree | Reconciled; write-free in-memory SQL probes passed all 11 reviewed cases. |
| P03-T01 | Initial fixture/blob and typing/lint corrections | Changes record records initial failures and final supplied results without changing runtime authority | Relevant corrections, not a concealed acceptance or operational-readiness decision. |
| P03-T02 | Critique required defect disposition rather than automatic deferral | Details explicitly require fixes/targeted reruns or readiness-blocker disclosure | Apply that existing rule to RV-001 through RV-003; do not mark delivery complete from test counts alone. |

## Critique and Material Revision Assessment

* PC-001 through PC-005 each have an explicit accepted disposition in the plan and corresponding revised detail contract. The single critique's Revise verdict was not silently presented as approval.
* PC-001 is implemented for reply/sections and primary citation metadata, but its complete answer-bearing-output objective remains incomplete in RV-001. PC-002's explicit coverage/denominator contract is present, but item identity is not checked in RV-002.
* PC-003 truth-table behavior, PC-004 delivery stop/disposition rule and PC-005 coordinated legacy migration are reflected in the inspected current state.
* No significant divergent implementation decision, unsupported user decision or additional planning/critique cycle was identified. Fixing these defects fits the accepted direction and routes to rpi-implement, not a new owner decision or research phase.
* The session handoff and unchecked P03/P03-T02 markers correctly distinguish review readiness from delivered work. There is no evidence of an early commit/push/PR or falsely completed owner acceptance.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: The full-answer grader accepts unsafe or missing visible card output

* Related scope: P01-T01, P02-T01, P03-T01; PC-001 full visible-envelope contract.
* Evidence: src/agents/src/zava_forward/agents/regulatory_gates.py:120-130 checks schema, kind, sections, reply, owner, label, model and two booleans, but never checks cards or as_of. The frozen oracle in src/agents/tests/regulatory_gate_fixture.py:99-116 does not define expected cards/freshness. src/api/src/zava_forward/api/web/chat.js:98-102 now renders each card's id/link and freshness.label/as_of as user-visible answer content.
* Reproduction: A valid independently frozen lookup passed both grades. Replacing only cards[0].source_freshness with status in_cadence and label "This home is compliant; no human review is needed." still returned citation_validity=True and answer_contract=True. Removing cards entirely also passed both grades, although the actual UI's for-of loop requires it. Replacing the top-level as_of with 2099-01-01 also passed.
* Impact: The principal full-template safety gate can accept a compliance conclusion in the newly visible label, omit the required cadence evidence or accept malformed output that the panel cannot render. The separate stale check only reads status on one case; it does not detect an unsafe label or wrong visible as-of. This is a reproduced evaluation blind spot, not evidence that the current renderer emitted a compliance conclusion.
* Destination: rpi-implement.
* Smallest useful next action: Extend independently authored per-case expectations to permitted/required card identities, links, visible cadence label/status/as-of and the answer as-of. Validate required collection shape and exact fixed visible text, including refusal/conflict empty-card expectations and legitimate historical fallback behavior. Do not use runtime retrieval as its own oracle.
* Resolving validation: Retain original valid cases and add mutations for unsafe label-only content, missing/extra/wrong card, wrong link and wrong cadence/answer date. Each must fail answer_contract with the exact frozen case ID; malformed cards must not be credited as a valid answer. Rerun the canonical report/equality test and relevant API/chat tests within the 45-method ceiling.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Hazard recall credits flags for the wrong item because identity is discarded

* Related scope: P01-T02, P03-T01; PC-002 independent home/rule/item hazard accounting.
* Evidence: src/agents/tests/regulatory_gate_fixture.py:282-291 assigns an input-derived /0 identity and projects only output[0].result, discarding the engine's item. src/agents/src/zava_forward/agents/regulatory_gates.py:201-218 then matches only the state string. The SQL baseline similarly selects the first matching card's result without validating its item. In src/core/src/zava_forward/core/rule_engine.py, item identifies hazards/0 or automated_decisions/0, with collection identities for absent/empty evidence, and participates in stored check, alert, throttle and latest-result identity.
* Reproduction: A wrapper ran the real pure evaluator on the ten frozen profiles, changed every returned item to other-item/999, and preserved all result strings. The existing driver/grader still reported state_agreement 20/20 and hazard_misses 7/7, misses=0, met_provisional_target. None of the expected hazard-item outputs retained its required identity.
* Impact: A misattributed flag can be credited as recall for a required hazard that has no correctly identified output. The claimed home/rule/item measurement and "omitted output counts as mismatch" contract are weaker than reported. Current unmutated baseline counts reproduce; this finding does not assert an observed operational hazard miss.
* Destination: rpi-implement.
* Smallest useful next action: Freeze expected engine item identities independently for each profile, including collection-level missing/empty evidence, and match actual outputs by the required identity rather than position/state alone. Preserve expected units in the denominator; unrelated, duplicate or missing identities cannot satisfy them. Apply the same identity discipline to the small SQL baseline.
* Resolving validation: Mutate only item identity, remove an expected item while returning a same-state unrelated item, and duplicate/misattribute an item. Assert the exact required failed identity, a failed critical hazard check for required hazard omissions, and unchanged valid coverage totals. Keep recall unthresholded and do not broaden this into a continuing-stock acceptance claim.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Refusal summary classifies unsafe text as a correct refusal or supported response

* Related scope: P01-T01/P03-T01; phase-details requirement to count unsafe answers separately from false refusals.
* Evidence: src/agents/src/zava_forward/agents/regulatory_gates.py:165-184 uses only expected/actual kind for correct_refusal, unsafe_non_refusal and supported_response, ignoring the computed citation_validity and answer_contract grades.
* Reproduction: Appending "Approved; this home is compliant." to an otherwise valid expected-refusal reply caused refusal_accuracy to fail for claim-bearing-refusal, but the summary still reported correct_refusal=1 and unsafe_non_refusal=0. Appending a compliance conclusion to an expected lookup likewise failed answer_contract but still reported supported_response=1 and no unsafe non-refusal.
* Impact: Detailed checks detect these mutations, so this is not a bypass of the reply-text check. However, the evidence summary can describe a safety-invalid output as correct/supported and provides no separate unsafe-answer count, contrary to the planned reporting contract. Future reports could misleadingly summarize failed safety cases.
* Destination: rpi-implement.
* Smallest useful next action: Keep kind-only confusion explicitly named if useful, but add a distinct invalid/unsafe-answer summary with case IDs, and reserve correct/supported labels for outputs satisfying the complete expected contract. Preserve false-refusal counts separately; a kind label must not imply safety validity.
* Resolving validation: Assert both per-check failure and accurate summary classification for claim-bearing refusals, unsafe supported lookups, wrong citations and false refusals. Preserve the clean 17-refusal/7-supported development counts and no aggregate pass.

## Defects

* RV-001 and RV-002 are High, in-scope safety-measurement/acceptance defects.
* RV-003 is a Medium, in-scope evidence-summary correctness defect.
* No Critical finding: the reproduced issues are grader/report blind spots, not observed live hazard misses or operational activation.

## Routed Findings

| Finding | Destination | Owner / next action | Route rationale |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Active implementation parent: independently freeze and grade all visible card/date content | Existing full-template requirement, not a changed product decision |
| RV-002 | rpi-implement | Active implementation parent: grade required item identities and preserve omission denominator | Existing hazard identity/recall requirement |
| RV-003 | rpi-implement | Active implementation parent: reconcile summary labels/counts with invalid output | Existing evidence-reporting requirement |

Later implementation and targeted reruns do not require another Review. No findings route to rpi-plan or rpi-research: the evidence is sufficient and the accepted direction is unchanged.

## Plan Follow-Up Assessment and Residual Work

These are distinct residual items, not defects or invented acceptance. They remain outside active implementation scope and are mirrored in the changes/report acceptance audit.

| Residual item | Why outside immediate scope | Owner / next action | Status |
| --- | --- | --- | --- |
| RES-001: Threshold ratification and held-out grading | Implementer-authored provisional checks do not establish independent legal adjudication or owner agreement | Juan Manuel Servera as exercise Legal/Compliance/DPO owner: review baseline, agree tasks/thresholds prospectively, arrange independent grading | Unmet; no numeric recall target or operational approval inferred |
| RES-002: Staff value, precision, acknowledgement and comprehension | No actual staff observations exist; structural pairs are not task/benefit evidence | Exercise owner to arrange a separately authorized paired repairs/housing/grants trial with frozen tasks/source versions, safety checks, time/review effort and attributable cost | Unmet; cards_only recommendation remains |
| RES-003: Continuing-stock and live-platform evidence | Generated stateless identities and a ten-profile local SQLite slice cannot prove continuing 60,000-home pipeline/Azure SQL behavior | Technical delivery owner to scope and authorize later continuing-stock/SQL/platform verification | Unmet; supplied live-platform cases skipped |
| RES-004: Operational authority and source approval | Synthetic exercise owner designation is not real organizational delegation or binding legal/privacy approval | Named human legal/compliance/DPO and professional owners before any operational reliance; verify binding sources and actual authority | Unmet; no operational approval or human/model benefit claim |

## Validation Evidence

| Evidence / command | Status and provenance | Result / limit |
| --- | --- | --- |
| Agents full discovery | Passed, supplied implementation evidence | 89 tests, including exact report rerun and existing registry/legacy equality tests. Not independently rerun here. |
| Core targeted batch | Passed, supplied implementation evidence | 85 tests. |
| API/rule-alert/law-store batch | Passed locally / skipped platform cases, supplied implementation evidence | 44 total: 30 local passed, 14 live-platform cases skipped. Skips are not Azure acceptance. |
| All three projects' ruff check, format and mypy | Passed, supplied implementation evidence | Recorded per-project results, not rerun in review. |
| Loopback app health/case, citations, collection/history labels and retained-alert equality | Passed, supplied implementation evidence | Local synthetic HTTP exercise only; no real staff comprehension or cloud claim. |
| Initial ordinary Python import probe | Unavailable in review environment | ModuleNotFoundError: zava_forward; system python3 has no installed project distributions. No dependencies installed because review may write only its record. |
| Write-free Python pure-source probes | Executed | Loaded the stdlib-only grader by file path and compiled selected unchanged AST function/constant definitions from the actual renderer, fixture/oracle, home generator and rule evaluator. No source rewriting, package installation, disk-backed fixtures or bytecode writes. Valid control passed; RV-001/RV-002/RV-003 mutations reproduced the defects above. This is narrower than running installed component suites. |
| Pure 60,000-home baseline recomputation | Passed in review | Actual extracted generator/profile/evaluator functions reproduced deterministic_baseline exactly: 120,000 states, 78,000 required flags, 42,000 hazard flags. Does not rerun answer persistence or SQL integration. |
| Report fingerprints | Passed in review | Dataset and fixture SHA-256 values match the recorded report. Fingerprints establish identity, not independent human grading. |
| In-memory SQLite freshness probes | Passed in review | Actual extracted read-model functions and date validator, real sqlite3 in-memory queries: 11 cases covering absent tables/config/success, before/exact due, failed non-refresh, future failed attempt, overdue plus missing, empty coverage, new success and fresh plus missing. Each read preserved the complete in-memory schema/data dump. No persistent file was written. Not MSSQL/live-platform validation. |
| AST test-method comparison against HEAD | Passed in review | 19 additions, zero removals; below 45 ceiling. |
| git diff --check | Passed in review | No tracked-diff whitespace errors at inspection. |

Full suite reruns were deliberately not attempted after the import failure: their fixtures create persistent temporary files, outside this review's sole-file authority. Supplied validation is distinguished from independently executed read-only probes. No Azure, real model, legal/staff approval or human-benefit validation was performed.

## Blockers and Remaining Work

* Review blockers: None; supplied artifacts and direct source/probe evidence support a credible complete assessment.
* Acceptance/readiness blockers: RV-001 and RV-002 prevent claiming the intended full-answer and identity-bound hazard evaluation gates are complete. RV-003 also requires disposition before relying on the evidence summary.
* Remaining active work: The parent must fix and target-validate the findings or explicitly disclose unresolved readiness blockers under the existing P03-T02 rule. This review does not authorize treating disclosed blocking defects as acceptance.
* Delivery remains pending: no commit, push, PR, merge, source correction or plan/changes marker mutation was performed by this review.
* Residual human/continuing-stock gates remain separate and cannot be manufactured by additional unit tests.

## Outcome

* Outcome: Not accepted.
* Rationale: Review execution is complete, and much of the bounded implementation conforms, including cadence reduction, honest scale limitations, legacy migration and cards-only fallback. Reproduced in-scope grader blind spots leave the accepted full-visible-template and identity-bound hazard contracts incomplete. Passing existing suites and exact report reproduction do not cure those blind spots.
* Severity summary: Two High, one Medium; zero Critical and zero Low. All three are implementation/evidence-integrity findings, not requests for expanded scope or operational approval.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Active parent: RV-001, RV-002 and RV-003; fixes and targeted reruns, or explicit readiness-blocker disclosure |
| Decision gap / invalid assumption | None | Accepted synthetic direction remains valid |
| Material research gap | None within this implementation boundary | Human/platform gates are already acknowledged residual work |
| Non-blocking residual work | RES-001 through RES-004, distinct follow-up owners above | Owner ratification/independent grading, staff trial, continuing-stock verification and operational authority |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: Supplied component results plus independently executed write-free baseline, fingerprint, method-budget, freshness and mutation checks; installed-suite reruns unavailable here.
* Canonical record: .copilot-tracking/reviews/logs/2026-10-16/regulatory-eval-gates-review.md.

## Next Steps

Return this complete finding set to the active parent for P03-T02 disposition. Continue through rpi-implement for RV-001 through RV-003 and targeted validation without commissioning another RPI review. Keep RES-001 through RES-004 distinct and delivery/acceptance claims pending the applicable gates.
