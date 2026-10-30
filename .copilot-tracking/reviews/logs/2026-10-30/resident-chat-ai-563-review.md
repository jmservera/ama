---
title: "Independent Review: resident-chat-ai-563"
description: "Original post-implementation Review for issue 563."
ms.date: 2026-10-30
---

## Opening Review State

* Goal: assess the complete supplied resident generated-answer requirement, implementation and dated RPI evidence once.
* Scope: git diff against HEAD 7c131156 plus src/api/checks/resident_generated_answer_browser_check.py. Untracked dated RPI artifacts are evidence, not production additions.
* Evidence readiness: named research, plan, details, critique and changes artifacts exist; comparison and external validation-log inspection are pending.
* Acceptance basis: consented free-text housing questions reach grounded generated prose when enabled; deterministic guarded routes, fixed-topic guidance-ID behavior, honest fallback, minimal generated label and collapsed sources remain intact.
* First comparison: current plan markers and critique against changes and actual source.
* Authority: read-only except this single Review record; no fixes, source/plan/state/changes edits, delegation, paid inference, private data, cloud inspection, commit or push.
* Initial blockers: none identified. Complete local publication gate is explicitly deferred until after implementation/evidence commit.
* Guidelines: current source retrieved successfully on 2026-10-30 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md; apply to actual changed assistant.js, not an unrelated UI audit.

## Scope and Evidence

* Task: issue-563, resident-chat-ai-563; original independent post-implementation Review, 2026-10-30.
* Baseline: HEAD 7c131156, branch feat/resident-chat-ai-563.
* Production/documentation boundary: src/api/README.md; src/api/src/zava_forward/api/resident_demo/aoai.py, app.py, chat.py, web/assistant.js; src/core/src/zava_forward/core/resident_assistant.py.
* Test boundary: src/api/tests/test_resident_aoai.py, test_resident_chat_api.py; src/api/checks/chat_widget_browser_check.py; new src/api/checks/resident_generated_answer_browser_check.py.
* All five supplied dated research/planning/implementation/critique artifacts were read. Untracked dated artifacts, including session state, are lifecycle evidence, not production additions. Session state was not modified.
* Necessary context: original/addendum framing, reference index and memory, housing-association primer, owner design/content/WCAG baselines, existing advisor contracts and immediately surrounding routing/consent/response code. No wider repository audit.
* External validation root: /home/azureuser/.copilot/session-state/0187b0f6-c98e-4159-80bc-4c269348ac7c/files/. External paths identify supplied evidence only; no external evidence was written by Review.
* Excluded: secrets, .env, private datasets, Azure/live configuration, actual model calls, deployment, commit/push, source fixes and another Review.

## Execution Status

* Review execution: Complete. The complete supplied requirement/diff/evidence boundary was assessed once, without delegation.
* Plan execution: P01/P01-T01 and P02/P02-T01 have implementation/local evidence. P03/P03-T01 remains unchecked because Review and subsequent local persistence form one combined task. This Review does not claim the later commit or full gate occurred.
* Outcome: Not accepted, because RV-001 is a material implementation-boundary defect. Completed review execution is not implementation acceptance.
* Severity summary: Critical 0; High 0; Medium 1; Low 2. RV-002/RV-003 are declared follow-ups, not implementation defects.

## Plan-to-Change Reconciliation

| Current scope | Changes and direct evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 source diagnosis and generation | chat.route adds repair; app._assistant dispatches typed supported questions to answer_question; AzureAdvisor requests answer/source-ID prose | Reconciled | Both old source limitations are addressed; repair classification is overbroad, RV-001 |
| P01-T01 fixed-topic/protected behavior | Explicit topic still calls answer; existing safety/legal/consent/appointment and instruction guards precede repair keywords | Partial conformance | Named existing guard examples remain deterministic, but newly admitted unrelated/action examples do not, RV-001 |
| P01-T01 consent, projection and accounting | Exact boolean gate precedes row lookup; same session binding, reservation/request and post-response authority check reused | Reconciled | No new storage, retry, default activation or tariff change |
| P01-T01 resident UI and guide | Changed consent disclosure, generated label/detail and repair guidance; README explains configuration and semantic limitations | Reconciled | Scope remains native existing UI; no framework or shared-widget redesign |
| P02-T01 tests and browser evidence | Eight new unit methods, one new browser check and one related existing browser expectation; verified resident suite and browser reports | Reconciled within local evidence | Scripted transport and engineering checks are not actual-model/live/human acceptance |
| P03-T01 Review/persistence | This original Review is now recorded; local commit/full gate still pending | Intentionally incomplete | Leave combined phase/task unchecked until parent reconciles subsequent work |
| Follow-Up Items | Owner activation/actual-model/live evidence and human/AT approval | Open and explicitly outside local scope | RV-002/RV-003 preserve distinct owner follow-ups |

## Completed Work Assessment

| Marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | chat.py, app.py | The dead-rat-like example now reaches generated-question dispatch when enabled. Disabled mode has an explicit AI-not-enabled label, honest inability, no-report wording and human help. Unrelated/action false positives remain, RV-001. |
| P01-T01 | aoai.py, core/resident_assistant.py | New protocol and prose contract are implemented, not merely a new canned-ID selector. Output requires exact keys, bounded nonempty/control-character-checked text and unique permitted nonempty source IDs. Host resolves source descriptions; model URLs cannot replace them. |
| P01-T01 | aoai.py | _request preserves precommitted reservation before token/transport, request/reply/usage bounds, finish/tool-call rejection and accounting. Expiry is checked before work and after generated output; fixed-topic consistency validation remains in _answer. |
| P01-T01 | app.py | Missing/false/string consent is rejected before case read; generated method receives the existing own-case projection, not the database row. Reply is discarded after revoked access through the existing fresh view_for check. |
| P01-T01 | web/assistant.js | Disclosure now truthfully permits question/limited-case transmission. Generated content receives thin metadata plus visible unapproved/incorrect/advisory/human-help detail; existing escaping/native details remain. |
| P02-T01 | API tests and checks | Passing supplied checks cover consent, own-case exclusion, invalid output/fallback, accounting/expiry, late revocation, explicit-topic compatibility and browser transport/rendering. The existing negative-route suite does not cover RV-001 examples. |
| P01/P02 | src/api/README.md | Source causes, optional four-setting activation prerequisites, uninspected live configuration, unchanged expiry and actual-model/human evaluation gates are explicit. |

Source-ID validation is structural attribution, not proof that generated assertions are entailed by those sources. The implementation and guide explicitly acknowledge that limitation; Review does not misclassify it as solved or invent model-quality evidence.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01/P02 grounding fixture | Unknown synthetic stage "Survey" could not truthfully produce the expected canonical survey update; fixture now uses "Survey being booked" | Directly related fixture correction; no production mapping/fallback changed; compatible with planned projected grounding |
| P02 shared browser | Dead-rat assertion changed from unknown refusal to explicit disabled-AI repair fallback | Intentional feature contract, not removal of consent/human-help assertions; shared implementation/CSS unchanged |
| P02 legacy fixture | Scripted legacy status guidance changed from contact to unknown for the fake unknown-stage case | Preserves existing fixed-topic consistency validation |
| P02 generated browser | Consent change intentionally clears a draft; test now re-enters it after permission | No application bypass; actual consent ordering remains checked |
| P01 host notice | Repair inability/no-report notice retained separately from generated text and rendered in detail | Immediate implementation of the accepted host-owned authority boundary |
| Plan/detail completion | P01/P02 checked; P03 deliberately unchecked | Reconciled with changes and parent handoff. Research header still says "In progress", but executed disposition and planning readiness explicitly resolve its lifecycle meaning; no credible-boundary blocker. |

No material or divergent product decision was discovered. These descriptive updates preserve confirmed intent and do not require a replacement critique. RV-001 is failure to implement the existing boundary, not a request for expanded scope.

## Critique and Material Revision Assessment

* Original critique remains Complete / Pass, with no PC-xxx findings. It was neither edited nor superseded.
* The implementation preserves its core decisions: extend the existing advisor, keep explicit-topic guidance IDs, default off, unchanged 2026-11-01 expiry, existing accounting and no cloud action.
* Repair false positives were not accepted by that critique: its coverage explicitly requires unrelated/action messages to retain host routes. RV-001 therefore does not invalidate the historical planning verdict or require another critique.
* No evidence of dependent work resuming before required critique; no significant unresolved product decision was identified.

## Changed UI: Web Interface Guidelines

### src/api/src/zava_forward/api/resident_demo/web/assistant.js

Pass for changed lines 214, 223 and 272-278 against the freshly fetched source. Consent remains a labelled native checkbox with a shared hit target, question controls retain names/labels, disclosure is not hover-only, content uses text rather than HTML, and detail remains ordinary text in the existing polite log. No changed-line file:line guideline defect identified.

The whole actual assistant.js was read to assess its changed integration. Existing native actions, Intl date formatting, consent-generation fencing and error/recovery paths remain intact. Owner-required ASCII/sentence-style content and the specifically requested resident label take precedence over generic curly-quote/Title Case preferences. Image/media, hydration, drag, dark-theme and new animation rules introduce no changed-code obligation here.

Shared widget code/CSS is unchanged. Existing browser evidence supports native collapsed keyboard sources, focus, wrapping, reduced motion and current styling. Desktop and 320px/200% generated screenshots were inspected: the thin label is evident; the extreme narrow/large-text view has substantial wrapping and nested scrolling. Overflow assertions alone do not prove comfortable usability or WCAG/AT acceptance, which remains RV-003. No unrelated shared-component defect is added to this diff.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Route |
| --- | --- | --- | --- |
| Deployment activation and actual-model/live relevance | Local-only source repair expressly excludes Azure changes, paid inference and live acceptance | Owner separately authorizes settings/access/budget/tariff review and authenticated actual-model evaluation | Distinct deployment/live follow-up, RV-002 |
| Resident/content and assistive-technology acceptance | Scripted Chromium/axe does not provide human comprehension, semantic model quality or AT approval | Resident/content and accessibility owners assess representative journeys before operational acceptance | Distinct human/AT follow-up, RV-003 |

These remain outside active implementation completion and issue-closure claims.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Repair keyword matching now forwards unrelated and action requests to generation

* Related scope: P01-T01 deterministic action/out-of-scope boundary; P02-T01 negative routing coverage.
* Exact evidence: src/api/src/zava_forward/api/resident_demo/chat.py:191-217 accepts any occurrence of repair, rat, broken and other broad words without checking housing relevance or these action intents. src/api/src/zava_forward/api/resident_demo/app.py:424-435 then sends every such repair classification to answer_question when enabled.
* Bounded reproduction: a bytecode-disabled, no-inference comparison of HEAD 7c131156's route and the candidate route returned unknown -> repair for "Write a poem about a rat", "How do I repair my car?", "Tell me a joke about a broken robot", "Please report the rat smell to my housing officer" and "Contact repairs about the leak in my home". "Book repairs" remains unknown and the desired dead-rat home question correctly changes unknown -> repair.
* Cause/impact: the new broad keyword branch bypasses the intended deterministic refusal for unrelated messages and unhandled action requests. With valid consent and enabled AI, these now transmit the question plus own-case grounding and consume a reservation/model call. A prompt instruction to stay on task or not contact anyone is not preservation of the required host-owned deterministic route. No actual model call was made to establish this finding, and no claim that the model executes an external action is made.
* Existing coverage: src/api/tests/test_resident_chat_api.py:test_protected_and_unrelated_questions_never_reach_generation checks weather, approve/book/cancel and a few guards, but not unrelated repair-word contexts or report/contact intents.
* Destination: later rpi-implement, within the accepted direction.
* Smallest useful next action: constrain admission to housing repair questions and keep report/contact-action requests host-owned; add negative regressions for these examples asserting neither advisor method/reservation/transport runs while retaining the dead-rat positive path. Do not solve this by invoking the model to classify an otherwise refused message.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Deployment and actual-model/live acceptance remain an explicit owner follow-up

* Evidence: plan Follow-Up Items; src/api/README.md owner deployment prerequisite; generated-browser-complete/results.json explicitly says scripted Azure transport and no actual model/cloud call.
* Impact: local source delivery does not prove a running deployment is enabled or that a real model answers relevantly. Public-template omissions are not evidence of actual cloud settings. Default-off and 2026-11-01T00:00:00Z tariff expiry deliberately remain.
* Destination: distinct owner deployment/live-acceptance follow-up, not rpi-implement or a local research blocker.
* Next action: separately authorize activation/access/SQL/budget/tariff checks and actual-model/authenticated live Playwright evaluation before claiming issue acceptance. No authorization is inferred by Review.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Human content and assistive-technology acceptance remain outstanding

* Evidence: plan Follow-Up Items; generated-browser-complete/results.json human_AT_live_acceptance="Not run"; resident-assistant-browser/report.json explicitly records human/AT acceptance as not run and distinguishes simulated reflow/text resize from native zoom.
* Impact: passing scripted transport, structural citations, axe and geometry cannot establish semantic correctness, resident comprehension or accessibility conformance. The 320px/200% screenshot especially requires task-level usability assessment, not an overflow-only conclusion.
* Destination: distinct resident/content and accessibility owner follow-up.
* Next action: evaluate generated and fallback journeys with representative human/content and AT checks before operational acceptance; preserve manual/human channels meanwhile.

## Defects

* RV-001 is the sole identified implementation defect within the supplied boundary. No Critical/High finding and no significant decision gap were identified.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Parent routes bounded host-admission/refusal correction and negative regressions | Accepted deterministic boundary is not fully implemented |
| RV-002 | Distinct deployment/live follow-up | Owner separately authorizes and proves activation/model/live behavior | Explicitly excluded operational acceptance work |
| RV-003 | Distinct human/content/AT follow-up | Resident/content and accessibility owners | Local engineering evidence is not human approval |

Later implementation of RV-001 does not require this Review to run again. Do not overwrite or soften this original finding set.

## Blockers and Remaining Work

* Review blockers: none; sufficient evidence exists for this verdict.
* Acceptance blocker in the assessed implementation: RV-001.
* P03 remaining work belongs to the parent: preserve this original Review, reconcile its finding, and perform authorized local persistence using authenticated noreply identity, Copilot trailer and Refs #563 only. This Review commits nothing and makes no issue-closure claim.
* Complete local RPI gate has not run. It is intentionally planned after the implementation/dated-evidence commit; no current receipt or publication readiness exists. The parent must attempt it with external output and preserve any prerequisite failure honestly. No push, hosted approval, protection change or cloud fallback is authorized.

## Validation Evidence

| Check/evidence | Status | What this Review established |
| --- | --- | --- |
| Complete baseline diff plus new browser source | Inspected | All changed production/docs/tests and new check compared, not just selected hunks |
| Current Web Interface Guidelines retrieval | Passed, directly observed | Fresh source fetched before changed-UI assessment |
| resident-units-verified.log | Passed, supplied log inspected | Ran 147 tests in 64.594s; OK, seven existing opt-in SQL skips; not rerun by Review |
| API Ruff check/format; full mypy | Passed as supplied implementation evidence | Changes record reports 59 formatted files and mypy 113 files; standalone raw tooling logs not present in the named evidence root, so not independently re-executed or overstated |
| Focused core Ruff/format/mypy and six tests | Passed as supplied implementation evidence | Reported in changes/details; not independently rerun |
| JS syntax | Passed as supplied implementation evidence | node --check reported; no changed shared code |
| generated-browser-complete/results.json and source | Passed, receipt/source inspected | Real loopback app, scripted transport; consent-before-request/reservation, own-case prompt/exclusion, generated text escaping, keyboard sources, thin label, fallback/withdrawal, no external requests/page errors |
| Generated screenshots | Inspected | Seven PNGs exist, not the eight stated in changes: six viewport/text combinations plus unavailable. This count slip does not remove a promised scenario or affect routing proof. Desktop/narrow screenshots visually sampled; not every PNG re-inspected. |
| shared-widget-browser/results.json and sibling .log | Passed, supplied receipts inspected | Owned synthetic apps, keyboard/focus/race/error/withdrawal behavior and pinned axe; model/human AT not run |
| resident-assistant-browser/report.json and sibling .log | Passed within engineering scope | 32 scans, no recorded violations, no console errors/external requests; incomplete axe items remain, not a conformance claim |
| axe-4.10.3.min.js | Inspected | Exact supplied pin; SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb |
| Bounded route comparison | Reproduced by Review | External task runtime Python with PYTHONDONTWRITEBYTECODE=1; compared current route with in-memory git-show baseline; no application server, network or model call; RV-001 examples confirmed |
| git diff --check 7c131156 | Passed, directly run | No whitespace error reported |
| Full local gate / SQL opt-in integration | Not run / skipped as declared | Post-commit full gate pending; seven existing SQL skips do not prove SQL integration |
| Actual-model/live, human/content/AT and hosted approval | Not run | Outside this local Review; RV-002/RV-003 and parent publication gates remain |

The superseded initial test/browser failures remain described in changes rather than erased. Review did not perform a full matrix or convert execution of scripts into actual-model outcomes.

## Outcome

* Review execution: Complete.
* Outcome: Not accepted.
* Rationale: the real source repair, local positive-path evidence and UI integration are substantially present, but RV-001 violates an explicit host-owned routing boundary. Planned local persistence/full gate and separate operational/human acceptance remain unperformed, not implicitly passed.
* Original critique: preserved Pass. No second Review, human approval or issue closure is asserted.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement, RV-001 | Parent routes host-admission/refusal correction and tests |
| Decision gap or invalid assumption | None identified | No new product decision requested |
| Material research gap | None blocking the local verdict | No rpi-research invocation required |
| Non-blocking residual work | Distinct follow-ups, RV-002/RV-003 | Owner deployment/live; resident/content/accessibility acceptance |

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md](.copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md) | Source diagnosis and evidence limits |
| [.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md](.copilot-tracking/plans/2026-10-30/resident-chat-ai-563-plan.md) | Requirements, markers and follow-ups |
| [.copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md](.copilot-tracking/details/2026-10-30/resident-chat-ai-563-phase-details.md) | Detailed implementation/validation obligations |
| [.copilot-tracking/changes/2026-10-30/resident-chat-ai-563-changes.md](.copilot-tracking/changes/2026-10-30/resident-chat-ai-563-changes.md) | Implementation history and local evidence |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-chat-ai-563-plan-critique.md) | Original Complete / Pass critique |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-chat-ai-563-review.md) | This original complete finding set |

## Next Steps

Return Complete / Not accepted to the active parent. Parent owns later rpi-implement routing for RV-001 and the authorized local persistence/full-gate sequence; keep P03 unchecked until its combined obligations are reconciled. Preserve RV-002/RV-003 as separate follow-ups. No user action is required by this Review, and no second Review is requested.
