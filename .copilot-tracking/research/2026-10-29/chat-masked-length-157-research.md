<!-- markdownlint-disable-file -->
---
title: Masked chat question length research
description: Focused research for issue 157 and PR 503 redaction expansion
ms.date: 2026-10-29
---

# Task Research: chat-masked-length-157

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md |

## Research Brief

* What to research: why a question below 1,000 characters is silently truncated after redaction, and how to reject it without dispatch.
* Why it matters: preserve the actual question and the existing explicit context-limit fallback.
* Audience or intended use: bounded implementation and independent review for #157 / #503.
* Scope: core chat panel, redaction/neutralisation contracts and existing chat tests.
* Non-goals: changing redaction, context caps, UI, SQL, approval boundaries, rubric scores or publication.
* Criteria: verify both original and masked length, preserve normal questions, prove no model dispatch on expansion overflow.
* Requested outputs: dated full RPI evidence, focused chat tests and Ruff checks, local Conventional Commit only.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Where is length admission checked, and which regression proves the actual failure? |
| Codebase scope | src/core chat_panel, chat_privacy, chat_isolation and chat tests |
| External scope | None; GitHub issue/PR lifecycle inspection only |
| Initial internal candidate areas | src/core/src/zava_forward/core/chat_panel.py; src/core/tests/test_chat_panel.py |
| Initial external candidate areas | None |
| Research posture | focused |
| Posture provenance | Default for named target and supplied reproduction |
| Explicit limits | No push, no az, no manual rubric score edits; local commit |
| Completion basis | Material questions answered and contrary boundary behavior verified |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | All source and tracking paths | Branch, evidence and commit rules | Selected |
| Skill | rpi-research | Bounded internal investigation | Three waves and evidence IDs | Selected |
| Specialist | RPI Researcher | Registered internal research agent | Independent research lane | Skipped: one tightly coupled trace, handled inline |
| Skill | Web/design skills | Backend-only Python change | Web guidance | Not applicable |

## User Participation and Research Decisions

No intake question is necessary: the owner provided target, behavior, fixture,
commands, branch and commit/publication boundaries. All four phase movements
are explicitly requested; manual mode is retained.

## Scope and Success Criteria

The original raw-input check remains. Redaction overflow must produce
LIMIT_REACHED without sending a truncated question. Existing redaction and
ordinary admitted questions must retain behavior.

## Task Research Requests and Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Fix masked length, not only raw length | Owner | Guard after redaction and before neutralisation |
| Add below-cap/expanded-over-cap regression | Owner | Use repeated synthetic postcode and trailing question |
| Focused chat tests; Ruff check and format --check | Owner | Record exact commands and results |
| Local commit, no push, no az, no score edits | Owner | Publication and cloud work excluded |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does admission currently miss redaction expansion? | straightforward | Open |
| Q2 | Which existing fixtures prove overflow and preserve valid boundaries? | straightforward | Open |

## Prior Knowledge Gate

Read original/addendum, reference index, owner memory, housing association
primer, src gate guide and prior chat-review-fixes state. Prior work completed
separately; inherited SQL/publication blockers are not acceptance for this fix.
Baseline e833fc8c, clean working tree, branch feat/agent-chat-157, open PR #503.
Supplied 977/2,297 character reproduction remains to be verified.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Located core panel and its owning tests and project commands. The panel defines
MAX_QUESTION_CHARS = 1000 and LIMIT_REACHED; source is typed Python, not UI.
Reflection: follow the one admission path and existing fallback assertions.

#### Wave 2: Deeper

The sole panel admission checks raw length only (C2). Redaction replaces each
postcode with "[postcode removed]" (C3); neutralise slices before escaping (C4).
Verified with the installed editable Python 3.12 source: "NE1 1AA " repeated
120 times plus "What stage is it?" is 977 raw / 2,297 masked characters; the
trailing question disappears after neutralise(..., 1000).
Reflection: reject the expanded input using the existing fallback, not a larger cap.

#### Wave 3: Contrarian

Checked whether storage bounding, no-case behavior or refusal precedence
already prevents the defect. Storage clamps masked text at MAX_CONTENT, not
the question cap; general/advisory sources still permit dispatch. Refusals
precede length handling and must keep that order (C2).
The limit path deliberately persists the masked user turn and workflow reply;
it does not reject before storage. Preserve that behavior (C2, C5).
An exact masked boundary can use 981 "x" characters plus " NE1 1AA": 989 raw,
1,000 masked. It should still dispatch the entire trailing placeholder.
Reflection: strict greater-than on both lengths preserves the inclusive limit.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Add masked-length condition to current guard | C1-C4 | Accepted | Same fallback, before prompt construction, no scope expansion |
| Increase cap or dispatch truncated text | C2-C4 | Rejected | Changes semantics rather than rejecting loss of question |
| Add pre-storage return | C2, C5 | Rejected | Would change existing turn persistence/audit behavior |
| Check exact-cap expanded text still dispatches | C3-C5 | Accepted | Protects inclusive boundary and ordinary redaction |

#### Cycle Re-entry Evaluation

No further cycle required: actual reproduction and opposite boundary verified,
single caller path inspected, all material scope questions answered.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Question cap is 1,000 and explicit context-limit message exists | src/core/src/zava_forward/core/chat_panel.py:193 | High |
| C2 | Raw-only length check after refusal and storage, before dispatch | src/core/src/zava_forward/core/chat_panel.py:386-436 | High |
| C3 | Redaction replaces postcode with longer marker | src/core/src/zava_forward/core/chat_privacy.py:56,90-97 | High |
| C4 | neutralise truncates to limit before delimiter escaping | src/core/src/zava_forward/core/chat_isolation.py:42-45 | High |
| C5 | Existing fixture records prompts; storage expansion test spans modes | src/core/tests/test_chat_panel.py:166-199,268-295 | High |

### External Evidence

No external sources used.

## Findings, Alternatives and Decision State

Q1 answered by C1-C4: add `or len(masked) > MAX_QUESTION_CHARS` to the current
guard. Q2 answered by C3-C5: use the existing StoredQuestionTests model spy and
synthetic dataset; cover case-bound and general/advisory sources, assert
fallback, workflow-only response, no citations and zero calls. Add exact-cap
expanded-text acceptance coverage. This is the selected convergence recommendation.

## Open Questions, Risks and Further Research

No research blockers. Preserve current masked turn/fallback persistence.
Focused validation does not establish full publication or live acceptance.
The supplied postcode example was verified exactly with NE1 1AA; SW1A 1AA
would be 1,097 raw characters and is not a valid below-cap reproduction.

## Planning Readiness

Ready. Research disposition: executed. Self-check: three ordered inline waves,
evidence-backed recommendation, boundaries and alternatives recorded.
Parent continuation: Plan, explicitly requested by the owner; no automatic
session is inferred and no publication is authorized.
