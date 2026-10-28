---
title: Resident chat safety routing correction research
description: Focused evidence for PR 525 safety thread
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Task Research: resident-chat-520-safety

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher / agent | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/resident-chat-520-safety-research.md |

## Research Brief

* Target: prevent hazard reports being classified as ordinary own-home questions.
* Purpose/audience: evidence for a bounded PR #525 correction of thread
  PRRT_kwDOUU8JX86xVvlj, not whole-issue acceptance.
* Scope: host routing, existing HTTP chat regressions, affected browser journey.
* Non-goals: new advice, legal interpretation, model activation, UI redesign,
  operational reporting, Azure, secrets, .env or private data.
* Criteria: both quoted reports return the exact existing SAFETY answer; plausible
  hazard variants take precedence; ordinary questions keep existing routes.
* Outputs/mode: convergence research, plan, critique, implementation and one Review.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1 missing hazard vocabulary; Q2 ordinary-question boundaries; Q3 validation/publication |
| Codebase scope | src/api resident_demo routing, tests and browser check; src/README.md gate |
| External scope | Named GitHub PR/thread only; no new regulatory sources |
| Internal candidates | chat.py, app.py, test_resident_chat_api.py, resident_assistant_browser_check.py |
| Posture/provenance | Focused, bounded caller task with exact failure reports |
| Completion basis | Material routing contracts and counterexamples covered |
| Evidence root | .copilot-tracking/ |
| Research writes | Evidence and required workflow state only |
| Limits | Nonblocking flock -n retries for at most 40 minutes; no az/Azure |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository guidance, supplied RPI wrapper | Selected: branch, dated evidence, independent critique/Review, full publication gate |
| Skill | rpi-research | Selected: focused three-wave evidence |
| Skill | Frontend/design/accessibility skills | Skipped: backend routing, no web implementation or conformance claim |
| Specialist | RPI researcher | Skipped: one tightly coupled low-volume trace, handled inline |

## User Participation and Research Decisions

Caller provides exact scope and phase authorization; no unanswered intake question.
Remain manual with all four phases explicitly requested, not an indefinite
automatic follow-up session.

## Scope and Success Criteria

Reuse SAFETY byte-for-byte, test priority over home/other topics, preserve ordinary
questions, and record actual validation limits without bypassing publication gates.

## Task Research Requests and Direction Controls

Use feat/resident-chat-520 in this worktree. Pull bot updates fast-forward only;
Conventional Commit with required trailer. PR text retains Refs #520, never a
closing keyword. Reply/resolve only when a published correction is available.
If the mandatory full gate needs prohibited az, commit locally for the coordinator.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Why do both reports return home facts? | Straightforward | Answered, C1 |
| Q2 | Which bounded phrasing rules avoid ordinary-question regressions? | Depth | Answered, C5/C6 |
| Q3 | Which checks and publication constraints apply? | Straightforward | Answered, C4/C7 |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, sector primer, current chat
source/tests and prior logout follow-up state. Prior no-az publication blocker is
historical evidence, not a fresh successful gate. Branch was clean and already
synchronized with its bot commit after fetch and pull --ff-only.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline trace: chat.route checks a small safety token set before ordinary topics.
Neither carbon monoxide/alarm nor smoke/socket is in that set, so home wins.
Reflection: supplied reports follow directly from the source; no new advice needed.

#### Wave 2: Deeper

Inline host trace: typed questions call chat.route, then string topics use
chat.answer; only enum topics can invoke the optional model. The same browser
check sends typed home/document questions through the actual endpoint. Routing
affects that journey, so run it and add both quoted reports to its assertions.
Actual installed reproduction: both reports return `home`; ordinary smoke alarm
documents return documents and CO detector status returns status. System Python
had no namespace distribution; restored pinned project dev distributions in a
task-owned session venv after that observed failure.
Reflection: test exact SAFETY equality, no home details, no appointment action and
zero model calls. No API/request schema or UI change is needed.

#### Wave 3: Contrarian

Challenge: unconditional `co`, `alarm`, `socket`, `water`, `smoking` matching
would intercept ordinary records, smoking-policy or detector questions.
Preserve the existing safety tokens, then use conjunctions of active report
vocabulary and hazard/electrical context. Include CO/carbon-monoxide alarms going
off/beeping/sounding, observed smoke, electrical sparks/smoking/burning,
electric shocks and flooding/leaks involving electrics. Protect detector
documents/status, socket improvements, smoking-policy and unrelated water questions.
Reflection: case-insensitive whole-word token matching is existing prior art;
bounded combinations are simpler and safer than substring matching or a model.
Finite lexical coverage is not a general hazard detection guarantee.

#### Parent Synthesis and Disposition

Accept bounded report/context combinations and negative routing regressions
(C1/C5/C6). Reject blanket new-token matching and model classification because
they change ordinary routes or authority unnecessarily. Reuse SAFETY unchanged
(C2). Defer publication if the mandatory full gate cannot run without az (C4).

#### Cycle Re-entry Evaluation

No new cycle required: source, actual reproduction, request path, browser scope,
counterexamples and publication constraints cover this focused correction.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Current safety set omits both reports; home token matches later | src/api/src/zava_forward/api/resident_demo/chat.py:40 | High |
| C2 | Existing safety answer already contains emergency/human route and no-report notice | src/api/src/zava_forward/api/resident_demo/chat.py:28 | High |
| C3 | HTTP tests exercise constructed residents and exact request schema | src/api/tests/test_resident_chat_api.py:46 | High |
| C4 | Complete gate preflight/infra require az; raw scoped checks cannot replace full receipt | tools/rpi-checks.py:1322; src/README.md:76 | High |
| C5 | Typed route selects host-owned advice, enum topics alone can invoke model | src/api/src/zava_forward/api/resident_demo/app.py:400 | High |
| C6 | Ordinary tokens and word boundaries are existing route semantics | src/api/src/zava_forward/api/resident_demo/chat.py:36 | High |
| C7 | Actual browser check covers typed chat, own-case isolation and callbacks | src/api/checks/resident_assistant_browser_check.py:276; src/api/README.md:271 | High |

No external sources used beyond the caller-named GitHub thread. No legal or
regulatory claim added. No research delegation.

## Findings Mapped to Questions and Evidence

Q1: missing vocabulary, not response generation, is the root cause (C1/C2).
Q2: use report/context combinations with ordinary negative tests (C5/C6).
Q3: focused HTTP/routing units, API suite, Ruff100/format/mypy and actual
resident-assistant browser check; heavy runs under nonblocking shared lock with
bounded retries. Full exact-head publication remains blocked under no-az (C4/C7).

## Alternatives and Decision State

Prefer host-owned bounded lexical matching before ordinary topics. Reject model
classification or new advice: unnecessary authority and scope change. Reject
unqualified alarm/socket/water/CO token matching: likely ordinary-question overlap.

## Open Questions, Risks, and Residual Uncertainty

A finite rule set cannot recognize every possible report or establish safety.
Baseline system Python lacked installed distributions; task-owned session venv
now has editable core, agents and API dev distributions. No secrets read.
Full publication evidence is unavailable under the explicit no-az constraint;
this blocks push/thread resolution, not the correction or local validation.

## Current Decisions / Unresolved Decisions

Confirmed caller constraints above. Select bounded report/context combinations,
reuse safety response, test positive and negative routes. No unresolved design decision.

## Potential Next Research

Only re-enter if request/browser dataflow or counterexamples undermine the bounded fix.

## Planning Readiness

Ready. All three waves executed inline; evidence sufficient for bounded planning.
No additional source research required before Plan.

## Research Disposition and Self-check

Executed, complete. Evidence IDs resolve locally. No source edits during Research.
Self-check: brief, extension provenance, participation, three waves, alternatives,
source locations, risks, disposition and readiness recorded.
