---
title: "Resident chat routing RPI Review"
description: "Single independent source-only post-implementation assessment."
ms.date: "2026-10-31"
---

## Scope and Evidence

* Task ID: resident-chat-routing
* Review date: 2026-10-31
* Review scope: Full supplied source-only task boundary.
* Plan: .copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md
* Original critique: .copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md
* Research: .copilot-tracking/research/2026-10-31/resident-chat-routing-research.md
* Changes: .copilot-tracking/changes/2026-10-31/resident-chat-routing-changes.md
* Source: src/api/src/zava_forward/api/resident_demo/chat.py
* Tests: src/api/tests/test_resident_chat_api.py
* Documentation: src/api/README.md

## Opening Review State

* Interpreted review goal: Independently assess bounded rules-only own-case navigation, useful refusals, complete-message grammar and preservation of existing safety and consent routing.
* Review scope: Full supplied source, tests, documentation and RPI evidence, not deployment or AI activation.
* Evidence readiness: All supplied artifacts exist; substantive comparison and bounded validation pending.
* Acceptance basis: Owner requirements, current plan and details, original PC-001/PC-002 dispositions and implementation evidence.
* First comparison boundary: Reconcile P01/P02 evidence and pending parent-owned P03 with current source changes before testing behavior.
* Active read-only boundaries: Source, plan, details, critique, research and changes are read-only. Only this canonical review record may be written. No nested agents, remote model calls, deployment, publication or heavy gate.
* Initial blockers: None identified at opening; no outcome claimed before comparison.

## Execution Status

* Execution status: Complete
* Review execution evidence: One independent Review compared the complete supplied artifact set, full current chat module, full existing chat test module, all three changed-file diffs and directly relevant authority/content/validation context. Read-only in-memory validation passed on 2026-10-31. No nested delegation or second Review occurred.
* Implementation execution: P01/P02 complete. P03-T01 is satisfied by this record; marker updates and P03-T02 publication remain parent-owned and were not performed here.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Ordered fallback after legacy record matches | Reconciled | Added _natural_record_question and final fallback call; safety, exclusions and specialist ordering are unchanged. |
| P01-T02 | Four refusal examples and housing-officer help | Reconciled | Existing no-action prohibition, task-limit source and advisory notice remain. All four quoted examples route to supported answers. |
| P02-T01 | Three new methods; positive/negative matrices; inherited attack coverage | Reconciled | 49 natural positives and 39 explicit negatives; all 28 original test methods are AST-identical to HEAD. The existing shared record matrix gains the natural positives without removing legacy rows. |
| P02-T02 | README and focused validation | Reconciled | README accurately qualifies finite recognition and no deployment/activation. Changes retain initial failures, correction and isolated dependency restoration before the final passing results. |
| P03-T01 | Independent Review outstanding at implementation handoff | Reconciled | This is that one Review. An unchecked parent marker is not missing implementation or a reason to repeat Review. |
| P03-T02 | Conditional exact-candidate publication | Pending parent | No commit, gate receipt, push, PR, hosted approval or merge is claimed by this Review. Publication must remain conditional on acceptable outcome and exact-candidate evidence. |
| Follow-Up Items | Named human review, live acceptance and #563 activation | Reconciled | Explicitly outside this source-only fix; RV-001 routes the outstanding resident-copy/live evidence to a distinct follow-up, not active implementation. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/resident_demo/chat.py | Natural own-case STATUS, DOCUMENTS, FORMS and home questions reuse existing answers | Whole-character envelope followed by ordered topic-specific re.fullmatch; legacy matching remains first | Independent pure routing checks and reported HTTP suite | Conformant within the finite supported grammar. |
| P01-T02 | src/api/src/zava_forward/api/resident_demo/chat.py | Useful unsupported-question examples without authority expansion | Exactly four examples; housing-officer path; unchanged task-limit source, no-action language and Advice notice | Existing/new refusal assertions inspected; reported suite passes | Conformant; resident acceptance remains a distinct follow-up. |
| P02-T01 | src/api/tests/test_resident_chat_api.py | Grounding/isolation, malformed clauses, exclusions and inherited protections | Positive HTTP rows compare answer/sources to explicit topics and reject C-2/email leakage; no action/callback; protected helper spies on provider/advisor/accounting/token/transport | 3,485 independent pure route assertions; reported 90 focused tests | Conformant; no legacy test removals or method edits. |
| P02-T02 | src/api/README.md | Describe actual finite fallback and authority limits | Resident-chat section describes grammar, examples, refusal and unapproved-copy boundary | Diff review; reported Ruff/mypy passes; independently passed diff check | Conformant; no new legal claim or activation claim. |

### Full-message and authority assessment

* The envelope rejects unknown punctuation, markup, digits, identifiers, embedded question punctuation and NULs before fallback classification. Apostrophe normalization is confined to fallback; alphabetic tokens retain order and repetitions. Space/apostrophe separators and trailing question/exclamation/full-stop punctuation are admitted deliberately; this is a finite intent recognizer, not a grammatical correctness or universal language-understanding claim.
* Each intent branch uses re.fullmatch against the complete normalized sentence. No branch accepts an arbitrary suffix, repeated subject or second question simply because all tokens are in an allowed vocabulary. The two explicit PC-001 status examples and equivalent document/form/home repeats refuse. Independent concatenation of every natural-positive pair adds 2,401 negative checks and all refuse.
* Legacy exact matches still precede the fallback. The original 28 test methods are AST-identical, not merely present. Existing RECORD_QUESTIONS rows remain and now include all 49 natural positives, extending eight suffix variants and one prefix attack to every new phrase.
* Hazard assessment runs before polite-envelope removal and exclusions. Exclusions remain before regulations, consent, appointment and repair handling; record classification remains last. Existing active-hazard combinations still route to safety, even when combined with injection or booking text. Specialist responses are not incorrectly forced to unknown by the new record grammar.
* src/api/src/zava_forward/api/resident_demo/app.py still requires explicit use_record=True, validated request shape, authenticated session binding and current own-case lookup, and rechecks authority before responding. Record navigation cannot supply another resident/case selector.
* STATUS answers remain the existing recorded progress/next-step summary. Asking whether a case is blocked does not introduce a new blockage determination, diagnosis or approval. DOCUMENTS preserve mandatory record facts/sources, FORMS remain general advice and home remains the signed-in address/improvements view.
* No app, core, AI configuration, infrastructure, frontend or dataset change is present in the supplied diff. With AI off, these routes use existing rules answers; protected host routes never invoke the optional advisor. Existing mocked configured-AI regression paths remain unchanged except that recognized natural phrases inherit eligibility, as already specified by the plan. This is not #563 activation or a remote model call.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 and P02-T01 | Strengthened vocabulary/anchor design to ordered full-message grammar and allowed-vocabulary repeat negatives | Original PC-001 and confirmed owner requirement to retain complete-message refusal; no divergent decision required | Plan functional requirements, phase completion contract, actual helper and tests align | Original Complete / Revise preserved; PC-001 direct disposition recorded | Compatible correction, not a new scope or unaccepted decision. |
| P03 | Explicit material-Review publication stop condition | Original PC-002; owner requires no silent deferral of material defects | Plan critique disposition, P03-T01 details and changes handoff all state the stop rule | Original Complete / Revise preserved; PC-002 direct disposition recorded | Compatible governance correction; parent must apply the condition to P03-T02. |
| P02-T01 | Corrected the repair preservation test helper, not production routing | Initial two assertion failures: repair is an existing eligible optional generated route, unlike protected host routes | Changes explain failure; current test checks repair separately with AI off | No material plan revision needed | Supported correction preserving intended repair behavior. |
| P02-T02 | Restored missing project distributions in isolated environment and used manifest-pinned static tools | Initial mypy missing/untyped imports; pip identified absent project/Azure distributions | Changes preserve failed check and restoration, then report pinned Ruff 0.17.1 and mypy 2.4.0 passes | No manifest or accepted-scope change | Reconciled. Earlier plan tool versions describe the initial environment, not the final pinned run. |

## Critique and Material Revision Assessment

* Latest supplied critique is the original independent Complete / Revise record, with two High planning findings. It remains unchanged; this Review does not retroactively relabel that verdict.
* PC-001: directly disposed by current ordered grammar, complete-message requirement and concrete all-allowed-word malformed/repeated-clause matrices. Source comparison and independent route checks substantiate the disposition.
* PC-002: directly disposed by explicit conditional publication wording across plan disposition, P03-T01 details and changes handoff. No unresolved material acceptance finding was identified here; execution alone still does not authorize publication.
* Material revisions: neither correction changes confirmed user intent, answer authority, dependencies or active source scope. No new planning decision or research gap requires routing.
* Dependent-work pause assessment: current details state readiness after direct dispositions and P01/P02 completion; changes identify the ordered grammar as PC-001 implementation. No evidence of unaccepted significant/divergent work resuming early exists in the supplied boundary.
* Justification assessment: supported. Full historical event timing is not independently reconstructed; current-state reconciliation is credible without claiming unavailable historical evidence.
* Headline readiness/handoff prose in the plan remains its planning-stage context. Checked P01/P02 markers, detailed execution summary and changes handoff establish current completion. Pending P03 is accurately parent-owned, not an implementation defect.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Named human resident-copy review and live acceptance | Source-only constructed-data evidence cannot establish resident understanding or approve deployment | Parent retains a distinct resident-copy/live-acceptance follow-up; engage the authorized resident-content/service owner before actual use | Open, nonblocking for this source-only fix; RV-001. |
| #563 AI activation | Owner-gated activation is explicitly excluded; preserving mocked configured behavior is not activation | Owner/parent retain #563's separate activation decision and evidence gate | Open, separate owner gate, not a defect or active task addition. |

Unresolved plan follow-ups remain outside active P01/P02 implementation, completion and acceptance claims. P03 publication is parent continuation, not residual implementation.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Resident-copy and live acceptance remain unperformed

* Finding class: Nonblocking residual work; not an implementation defect.
* Related scope: Plan Follow-Up Items; P01-T02's candidate refusal copy and P02-T02's documentation qualification.
* Evidence: .copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md and .copilot-tracking/changes/2026-10-31/resident-chat-routing-changes.md explicitly separate named human review/live acceptance; src/api/README.md states the finite routing is not approved resident-facing copy; docs/reference/research/ux/content-standard.md likewise disclaims real-resident testing/approval.
* Impact: Constructed local tests establish routing and source contracts, not that real residents understand blockage summaries, receipt wording or refusal examples. Source conformance must not be presented as actual resident acceptance or approval to activate/deploy.
* Destination: Distinct resident-copy/live-acceptance follow-up, owned by the parent coordinating the authorized resident-content/service owner. Preserve #563's separate owner activation gate.
* Smallest useful next action: Carry this existing follow-up explicitly into parent/PR scope qualifications, and obtain named copy review and authorized live-acceptance evidence through separate work before resident-facing release. Do not add it to this fix or run another Review here.
* Publication materiality: Nonblocking for the scoped source-only candidate; blocks any unsupported claim of resident approval or live acceptance.

## Defects

* None identified in the supplied source-only implementation boundary.
* Severity counts: Critical 0; High 0; Medium 0; Low 1, solely the explicitly nonblocking residual RV-001.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct resident-copy/live-acceptance follow-up | Parent carries qualification; authorized human service/content owner supplies later acceptance evidence | Existing outside-scope human/live evidence, not failed source acceptance. |

Later implementation of a routed finding does not require another Review. No later rpi-implement, rpi-plan or rpi-research invocation is recommended for this candidate because no source defect, decision gap or material evidence gap was found.

## Residual Work

* RV-001 retains the existing named human copy/live-acceptance follow-up.
* #563 remains separately owner-gated. No activation or deployment is authorized by this result.
* Finite supported wording remains an accepted limitation, not a defect or inferred obligation to build general natural-language understanding.

## Blockers and Remaining Work

* Material Review blockers: None.
* Remaining active implementation: None in P01/P02.
* Parent continuation: Reconcile P03-T01 to this single completed Review, retain the original critique and Review results, and perform authorized P03-T02 exact-clean-candidate checks/publication. No source or plan marker was modified here.
* Publication not performed or verified: This is a dirty working-tree source assessment, not an exact committed-head receipt or a hosted/human approval. Any later source correction or candidate change needs resolving evidence and appropriate candidate validation; no second Review is inferred.

## Validation Evidence

| Command or inspection | Scope | Status | Summary |
| --- | --- | --- | --- |
| Read-only inline Python, using the supplied routing-venv/bin/python -B and PYTHONDONTWRITEBYTECODE=1 with the supplied PYTHONPATH from src/api | Pure routing matrices, inherited suffix/prefix checks, all natural-question pair concatenations; AST comparison to git show HEAD:src/api/tests/test_resident_chat_api.py | Passed, independently executed | Exit 0; 3,485 route assertions; 49 natural positives, 39 explicit negatives, 2,401 concatenated natural-clause negatives. All 28 legacy test methods AST-identical; exactly three added methods. No fixture setup, HTTP, file-backed database, bytecode/cache write or model call. |
| git diff --check | Current scoped working-tree changes | Passed, independently executed | Exit 0; no whitespace errors. |
| PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python -m unittest test_resident_chat_api test_resident_demo_api test_resident_chat_agenda test_resident_assistant_api -q | Four focused API modules | Passed, implementation-reported | Changes record: exit 0; 90 tests; no skips; 64.116 seconds. Tests use constructed loopback data and mocked AI transport. This Review inspected evidence and tests, but did not rerun file-backed HTTP fixtures under the read-only/no-temporary-file boundary. |
| python -m ruff check . | API project | Passed, implementation-reported | Changes record: exit 0; all checks passed with restored pinned Ruff 0.17.1. Not independently rerun. |
| python -m ruff format --check . | API project | Passed, implementation-reported | Changes record: exit 0; 67 files already formatted. Not independently rerun. |
| python -m mypy | API/core/agents typing boundary | Passed, implementation-reported | Changes record: exit 0; 126 source files, restored pinned mypy 2.4.0. Initial missing-package failure is preserved, not hidden. Not independently rerun. |
| Full/heavy gate, browser, real SQL, deployment, remote model calls and live resident acceptance | Outside supplied source-only Review authority | Skipped | Owner explicitly prohibits heavy gate/deployment/model calls/publication. No web source changed; browser/design review is inapplicable. Real resident acceptance remains RV-001, not a claimed pass. |

The independent inline run imported fixture definitions without calling setUp or creating temporary resources. The inline process also checked ORDINARY_QUESTIONS, REPAIR_HOST_ROUTES, HAZARD_REPORTS and REPAIR_QUESTIONS. Its count is additional Review evidence, not a replacement claim for 90 executed HTTP/component tests.

## Outcome

* Outcome: Conformant
* Outcome rationale: Both reported questions and all requested topic families route to existing rules answers after preserved exclusions/specialist handling. Complete normalized requests are consumed by ordered fullmatches; admitted-word repeated/mixed clauses refuse; original tests remain intact. Copy and documentation accurately retain authority and finite-coverage limits. Original PC-001/PC-002 dispositions are substantiated. The only finding is already-declared outside-scope human/live acceptance.
* Acceptance limit: Source-only conformance, not deployment readiness, real resident approval, AI activation, hosted approval or an exact-head publication receipt.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source correction requested. |
| Decision gap or invalid assumption | None | No re-planning requested. |
| Material evidence gap | None | No research re-entry requested. |
| Nonblocking residual work | Distinct resident-copy/live-acceptance follow-up, RV-001 | Parent preserves qualification; authorized human owner provides later evidence. |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Complete source/plan/evidence comparison; 3,485 independent pure route assertions and legacy-method preservation; implementation-reported 90 focused tests and pinned static checks.
* Material blockers: None.
* Parent handoff: P03-T01 complete by this record; P03-T02 remains conditional parent-owned work. Preserve one Review and the original critique; no deployment or #563 activation.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-chat-routing-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-chat-routing-review.md) | Canonical single independent Review. |
| [.copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md](.copilot-tracking/plans/2026-10-31/resident-chat-routing-plan.md) | Current requirements, markers and dispositions. |
| [.copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md](.copilot-tracking/details/2026-10-31/resident-chat-routing-phase-details.md) | Completion and parent continuation contracts. |
| [.copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md](.copilot-tracking/plans/2026-10-31/resident-chat-routing-critique.md) | Unchanged original Complete / Revise critique. |
| [.copilot-tracking/research/2026-10-31/resident-chat-routing-research.md](.copilot-tracking/research/2026-10-31/resident-chat-routing-research.md) | C1-C7 scope and evidence. |
| [.copilot-tracking/changes/2026-10-31/resident-chat-routing-changes.md](.copilot-tracking/changes/2026-10-31/resident-chat-routing-changes.md) | Original implementation and validation evidence. |
| [src/api/src/zava_forward/api/resident_demo/chat.py](src/api/src/zava_forward/api/resident_demo/chat.py) | Full routing and fixed host response boundary. |
| [src/api/tests/test_resident_chat_api.py](src/api/tests/test_resident_chat_api.py) | Changed matrices and preserved legacy tests. |
| [src/api/README.md](src/api/README.md) | Finite routing and authority documentation. |
| [src/api/src/zava_forward/api/resident_demo/app.py](src/api/src/zava_forward/api/resident_demo/app.py) | Consent, own-case and optional advisor boundary. |
| [src/core/src/zava_forward/core/resident_assistant.py](src/core/src/zava_forward/core/resident_assistant.py) | Existing rules-answer contracts. |
| [src/README.md](src/README.md) | Dated focused-tier and publication policy. |
| [docs/case_study_48_original.md](docs/case_study_48_original.md) | Preserved project context. |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Optional resident service and approval boundaries. |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base index. |
| [docs/reference/memory.md](docs/reference/memory.md) | Owner context, not evidence. |
| [docs/reference/research/sector/housing-association-primer.md](docs/reference/research/sector/housing-association-primer.md) | Customer-sector context, not invented company facts. |
| [docs/reference/research/ux/content-standard.md](docs/reference/research/ux/content-standard.md) | Plain-language and human acceptance limits. |

## Next Steps

The active parent records P03-T01 completion and this Conformant outcome, carries
RV-001 as a distinct nonblocking follow-up, and performs only its separately
authorized P03-T02 exact-candidate validation/publication actions. No new RPI
command, source correction, second Review, deployment or AI activation is
requested by this assessment.
