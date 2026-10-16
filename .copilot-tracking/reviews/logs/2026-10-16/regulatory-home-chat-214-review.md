---
title: Home-specific cited chat review
description: Single post-implementation review of the bounded offline issue 214 slice
ms.date: 2026-10-16
---

## Scope and Evidence

Task #214 / regulatory-home-chat-214. Full P01-P03 source implementation,
limited to the user-requested offline synthetic slice. This is one Review,
not operational acceptance or an actual-model assessment.

* Research: .copilot-tracking/research/2026-10-16/regulatory-home-chat-214-research.md
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-home-chat-214-plan.md
* Details: .copilot-tracking/details/2026-10-16/regulatory-home-chat-214-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-16/regulatory-home-chat-214-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/regulatory-home-chat-214-changes.md
* User direction, issue body/comments, ADRs 0004/0005/0006.
* src/core/src/zava_forward/core/regulatory_chat.py and tests/regulatory_fixture.py,
  tests/test_regulatory_chat.py; existing lawstore, rulecards, rule_engine,
  source_monitor and chat repository/isolation contracts.
* src/agents/src/zava_forward/agents/regulatory_chat.py, regulatory_eval.py,
  tests/test_regulatory_answers.py and evals/regulatory_chat_results.json.
* src/api/src/zava_forward/api/server.py, web/chat.js,
  tests/test_regulatory_chat_api.py; project READMEs and append-only reference log.

## Opening Review State

Goal: compare the completed bounded implementation with user safeguards and all
eight issue criteria, without converting offline evidence into full acceptance.
Evidence is ready: all source markers checked; changes/details explain current
behaviour, critique dispositions, validation and intentional scope limits.
Initial boundary is API retrieval -> extractive agents -> isolated persistence
-> explicit selected-turn handoff. Review is read-only except this record.
No blocker prevents this local assessment; full operational gates remain open.

## Execution Status

Complete. Exactly one post-implementation Review performed directly against
the supplied coherent integration and recorded execution results. No review
subagents or second Review. Outcome is separate below.

## Plan-to-Change Reconciliation

| Marker | Completed work | Assessment |
| --- | --- | --- |
| P01-T01 | API-owned law/card selection, purpose-minimised fact snapshot, exact five-part extractive response, refusal, historical source envelope and atomic pair write | Reconciled; no provider or agents database path |
| P02-T01 | Synthetic gates, real SQL role reread, guarded history, explicit selected-pair owner inbox, idempotent receipt, panel/resume/doubt/inbox | Reconciled; no automatic sharing or case/rule mutation |
| P03-T01 | Development evaluation, actual same-source card/provision links, rollback/isolation/source/injection/unsupported-question tests | Reconciled within the stated offline boundary |
| P03-T02 | Per-project validation, eight-row acceptance audit, READMEs/log and RPI evidence | Reconciled; commit/push/PR are subsequent delivery administration |

## Implementation-Time Updates and Critique

The final-candidate critique ran once with Revise verdict. PC-001 through
PC-008 have direct dispositions in details. Synthetic admission, repository
atomicity, receiver and historical authorisation, bounded immutable envelopes,
finite purpose/refusal/conflict contracts, falsifiable evaluation, eight-row
audit and actual HTTP flow are present.

Immediately relevant refinements preserve user intent:

* SQL's legacy staff cache does not refresh on every turn. The new path reads
  current SQL staff directly for both sender and named recipient. The HTTP
  revocation tests verify both guarded regulatory and generic history.
* Topic words alone did not establish supported intent. Finite source-lookup
  vocabulary now rejects unrelated questions, even with a hazard keyword.
* JSON repositories only lock; explicit pre-image restoration supplements
  the one repository commit. SQL rollback is tested independently.
* Reference-only/no-permitted-fact results are unknown statements, not invented
  case facts. Observation-bound hashes retain historical fact metadata.

These are compatible local guard refinements, not new user-owned decisions.
The critique was not repeated. The source-write boundary remained src; only
requested RPI evidence and docs/reference/log.md changed outside it.

## Acceptance Assessment

The authoritative eight-row audit is in src/api/README.md. Local source
fragments have exact excerpt/fact equality, version/hash/status/dates;
unsupported output has no factual fragments. Question minimisation excludes
health/contact/report narratives and memory. No model-authored legal conclusion,
future-source application or inferred terms exists in the new closed renderer.
Actual ambiguity/semantic legal intent remains unmeasured; the supported
question vocabulary is intentionally narrow.

Changed approved versions and disagreeing card instructions show both and
require human review; the system does not infer a legal winner. Explicit doubt
copies only one question/answer pair into the unique provisioned Juan Manuel
Servera exercise owner's isolated inbox, with no sender-thread access.
Sources and historical envelopes persist through restart. Generic action
endpoints cannot write into these regulatory threads. Deterministic alerts
and safety holds remain unchanged on negative/unavailable results.

This is a separate optional bounded regulatory path. It does not repair or
certify the existing generic case-chat panel's documented arbitrary-prose
grounding limitations. Its tests and acceptance claims must not be applied
to that earlier path.

## Validation Evidence

All Python test runs use installed editable packages and absolute per-project
PYTHONPATH entries for shared tests; only temporary constructed data is read.

| Command/scope | Status | Evidence |
| --- | --- | --- |
| Core selected unittest: regulatory_chat, chat_panel, chatthreads, rule_engine, rulecards, source_monitor | Passed | 108 tests |
| Agents selected unittest: regulatory_answers, chat_eval, chat_model, chat_fixture, dependency_rule | Passed | 45 tests |
| API selected unittest: regulatory_chat_api, chat_panel, chat_isolation, lawstore, rule_alerts, dependency_rule | Passed with existing skips | 98 ran, 16 optional skips, no failures |
| Project-wide ruff check and format check, core/agents/API | Passed | One vocabulary-literal line-length finding corrected before this Review, final agents checks green |
| Project-wide mypy, core/agents/API | Passed | 96 / 19 / 45 source files respectively |
| Focused final agents answer/evaluation test after lint correction | Passed | Seven tests; frozen report exact equality and two identical evaluations |
| Local loopback app, actual handlers | Passed | Responsive health/case, cited turn, source history, explicit doubt, idempotent receipt, owner inbox, forged/foreign/revoked denial; provider spy forbids calls |
| Fault injection and restart | Passed | JSON/SQLite partial message/receipt and commit failures roll back; post-commit audit failure retains retryable receipt without duplicate |
| JS syntax and git whitespace | Passed | node --check on chat.js; git diff --check |
| Browser interaction, human accessibility/comprehension | Not run | HTTP/static DOM checks do not prove actual browser or human behaviour |
| Actual model, held-out legal set, live source review, 60k stock, Azure SQL | Not run | Expressly offline scope; no operational acceptance claim |

The report records 3/3 exact cited answers and 10/10 expected refusals.
The non-AI comparator uses identical actual card/provision links; chat joins
six permitted home-fact fragments across three answers versus none in cards.
Three structural card/provision/home lookups become one joined request.
This is falsifiable integration value, not observed human savings or AI benefit.

## Findings and Routing

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Actual source/authority/privacy approval remains unmet

* Evidence: ADR 0005 synthetic-only decision, src/core/README.md admission and
  copy semantics, src/api/README.md acceptance audit.
* Impact: Simulated approvals, dataset declarations and privacy references do
  not permit actual staff data or operational legal reliance. Sender deletion
  does not retract an explicitly copied owner thread.
* Destination: Distinct operational-readiness follow-up, owned by Juan Manuel
  Servera as exercise Legal/Compliance/DPO owner; obtain actual source,
  delegate, retention/rights and processing decisions before any real use.
* Classification: Known scope limit, not a defect in this offline slice.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Real-model and staff comparative benefit is unmeasured

* Evidence: src/agents/evals/regulatory_chat_results.json not_evaluated,
  development-set report and README comparison caveats.
* Impact: Passing extractive cases does not satisfy the ADR's actual-model,
  continuing-stock, staff comprehension or net-effort adoption gates.
* Destination: rpi-research in a separately authorised follow-up: establish
  held-out questions, provider/payload/budget permission and human protocol;
  compare with the retained deterministic-card baseline.
* Classification: Material full-acceptance evidence gap outside offline scope.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Broader interaction/conflict coverage is not established

* Evidence: Finite source vocabulary, exact-text/version conflict heuristic,
  static DOM tests and no actual browser/human run.
* Impact: This is not general question understanding, semantic contradiction
  detection, browser accessibility conformance or high-concurrency stress proof.
* Destination: Distinct bounded follow-up if broader chat is adopted: plan
  supported question coverage, semantic conflict review, actual browser/human
  checks and concurrent-request stress evidence without weakening citations.
* Classification: Explicit capability/evidence limits, not expanded active tasks.

## Defects

No high-confidence implementation defect found in the assessed bounded path.
No actual-model, generic-chat or operational conformance verdict is issued.
No source correction or repeated Review is scheduled in this task.

## Plan Follow-Ups, Blockers and Remaining Work

Plan follow-ups are correctly outside P01-P03: actual source/owner/privacy
approval routes to RV-001; actual-model/held-out/staff value and continuing-stock
evidence routes to RV-002; broader interaction validation routes to RV-003.
No implementation blocker remains within the offline slice.
Delivery administration is pending: commit/push/open PR, await owner/coordinator
checks and merge decision, leave issue criteria unticked.

## Outcome and Closeout Routing

Execution: Complete. Outcome: Residual work.
The requested offline implementation is supported; full #214/ADR adoption
is not accepted by this review because the listed broader gates remain unmet.
No conformant full-acceptance claim is made.

| Finding class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defect | None identified in assessed path | No source changes from this Review |
| Decision/operational gap | RV-001 distinct follow-up | Named owner records actual approvals before real reliance |
| Material evidence gap | RV-002 rpi-research follow-up | Authorised held-out/model/staff comparative protocol |
| Non-blocking capability/evidence limits | RV-003 distinct follow-up | Broader questions/conflicts/browser/concurrency only if adopted |

The parent returns to requested delivery administration, not Implement or a
second Review. No child follow-up starts without separate user direction.
