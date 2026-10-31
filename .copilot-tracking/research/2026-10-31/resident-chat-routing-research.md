---
title: Resident rules-mode chat routing research
description: Focused investigation of own-case intent routing and protected boundaries
ms.date: 2026-10-31
---

## Research brief

Task identity: resident-chat-routing. Owner-reported live symptom on 2026-10-31:
"How's my case going" and "Is my case blocked?" refuse with AI off.
Audience: API maintainers and independent reviewers. Output mode: convergence.
Posture: focused, selected from the owner's bounded bug report.
Evidence root: `.copilot-tracking/research/2026-10-31/`.

## Direction controls and extensions

Preserve exclusion checks, safety precedence, specialist routes and unknown
refusal. Extend only own-case status, documents, forms and home/address routing.
No AI activation, deployment, private data, secrets or external inference.
Owner requests focused unit tests, Ruff and mypy, publication to the existing
`fix/resident-chat-routing` branch and Refs #520 / Refs #563.
The current source guide's dated owner policy permits focused validation for
small issues. This resolves the broader standing full-gate wording for this
bounded fix; hosted CI and independent review remain required.

Selected: repository instructions, rpi-research and UX content standard.
Skipped: web design skills (backend-only change), regulatory research (no changed
legal claim), research workers (one tightly coupled internal trace).
Non-interactive execution: the explicit full-loop request authorizes phase
progression; no new routine decision is needed.

## Questions and candidate areas

1. Where does natural wording fall through?
2. Which existing answers and safety checks must remain authoritative?
3. Which regression and application tests prove routing without AI?

Candidates: resident demo chat, resident assistant, resident chat/application
tests, API README and content standard. No external research is needed.

## Research cycle log

Cycle 1 Wider: inspected chat routing and repository/customer/content guidance.
Initial finding: exact full-message matching narrows legitimate own-case wording.
Cycle 1 Deeper: verified the fixed-topic core answers and existing HTTP tests.
Personal requests require explicit record-use permission and current identity.
No answer contract, case selector or activation configuration needs changing.

Cycle 1 Contrarian: the existing regression matrix deliberately rejects mixed
intents, extra instructions, arbitrary suffixes, markup and other-case IDs.
A bare keyword presence check would break those protections. Preserve exact
legacy matches, then use bounded per-topic vocabulary with own-record anchors
and question intents; reject embedded punctuation and unknown words.
No research worker ran. Inline investigation covered the single continuous
trace. Additional research would be redundant for this bounded scope.

## Evidence log and findings

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `src/api/src/zava_forward/api/resident_demo/chat.py:170` | `_record_question` only accepts exact full-message phrase patterns; both reported questions fall through |
| C2 | `src/api/src/zava_forward/api/resident_demo/chat.py:237` | Safety runs first; exclusions, regulations, consent, appointments and repair precede record routing |
| C3 | `src/core/src/zava_forward/core/resident_assistant.py:80` | `advise` already returns grounded progress/next step, document facts and fixed form advice |
| C4 | `src/api/tests/test_resident_chat_api.py:496` | Existing matrix rejects complete-question suffix attacks and mixed topics, including without forbidden keywords |
| C5 | `src/api/src/zava_forward/api/resident_demo/app.py:399` | HTTP boundary enforces record permission, request shape, current own-case access and optional provider selection |
| C6 | `docs/reference/research/ux/content-standard.md:22` | Refusals should give everyday wording, a person-owned help path and a useful next action |
| C7 | `src/README.md:63` and `src/README.md:309` | Dated focused-tier policy permits relevant unit/static checks without a full receipt for small fixes |

## Alternatives and decisions

Selected bounded keyword/intent fallback after existing exact matches and
exclusions (C1-C4). Reject substring-only routing because appended unrelated
instructions would enter generated routes if AI were separately activated.
Reject adding only two exact phrases because it leaves the broader reported
own-case intents broken. Preserve specialist precedence, unknown refusal and
all existing activation boundaries (C2-C5).

## Risks and residual uncertainty

Finite vocabulary will still refuse unsupported phrasing. It is not universal
language understanding or a safety classifier. Named human review of candidate
resident copy and live acceptance remain unperformed; no deployment is allowed.
Existing configured optional-AI routes are unchanged, not activated here.

## Planning readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: evidence locations recorded, three waves completed, scope/alternatives
and residuals explicit. Parent next action: Plan with C1-C7, no research blockers.
