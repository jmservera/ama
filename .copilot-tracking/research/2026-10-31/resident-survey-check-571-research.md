<!-- markdownlint-disable-file -->
---
title: Resident Survey check research - Refs #571
description: Local prompt and acceptance-check reconciliation
ms.date: 2026-10-31
---

## Research Brief

Research the reported `Survey: Missing` baseline failure against the real
loopback resident demo with constructed fixtures. Audience: implementer and
independent reviewer. Output mode: convergence. Identify the root cause,
reconcile check and prompt, and preserve resident acceptance evidence.
No Azure, live accounts, private datasets, paid inference or feature code in
`mvp/`. Research is read-only except this evidence and required session state.

## Research Parameters

* Posture: focused, selected by the bounded issue and named browser check.
* Resolved evidence root: `.copilot-tracking/research/2026-10-31/`.
* Initial areas: `src/api/checks/resident_assistant_browser_check.py`,
  resident chat rules, external-package tests, API README.
* External source: issue https://github.com/jmservera/ama/issues/571,
  retrieved 2026-10-31.
* Explicit limits: local synthetic execution only; pip, installed Chromium.
* Prior knowledge: issue reports RV-003 pre-existing failure; verify rather
  than assume it. Session history lookup found no issue-571 evidence.

## Extension Registry and Participation

Repository instructions selected for source layout, evidence, local gates,
privacy-safe git identity and non-closing issue references. RPI Research
selected for ordered wider/deeper/contrarian investigation. Researcher
delegation skipped: prompt-to-check trace is one tightly coupled uncertainty.
Web-design skills are not initially applicable: no UI edit or redesign planned.
User explicitly requested the complete ordered RPI loop and publication;
automatic continuation is authorized by that request, with no routine prompts.

## Direction Controls

Use branch `fix/resident-survey-check-571` at supplied base `5666bd33`.
Worktree is clean, current branch matches, and no existing open PR was found.
Never weaken resident acceptance evidence. Use only `Refs #571`.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What causes the missing Survey text? | depth | Answered |
| Q2 | What change preserves the intended document evidence? | depth | Answered |
| Q3 | Can the exact browser check execute locally? | straightforward | Answered |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline investigation traced both Survey assertions, full-message routing and
typed document fixtures. The current-base browser check passed in installed
Chromium, without axe. Reflection: the issue's reported baseline is historical,
not a current-base failure; inspect git history before changing runtime code.

#### Wave 2: Deeper

Git history identifies merged #573 (`a0670b58`) as the original correction.
It replaced `documents help` / `forms help` with recognized questions and
introduced fresh-reply assertions. Merged #589 subsequently expanded supported
document paraphrases. The original 2026-10-30 research and Review confirm the
same diagnosis; their adverse and successful outcomes remain untouched.
Reflection: do not reimplement an already delivered fix or describe current
passing code as a failure.

#### Wave 3: Contrarian

Executed the obsolete `documents help` prompt against the actual current
loopback resident app, with own-case document facts and consent. It returns the
host-owned refusal and reproduces the exact failed `Survey: Missing`
assertion. The recognized missing-documents question then passes in its own
fresh reply. Existing HTTP tests deliberately refuse the obsolete prompts.
Reflection: broadening routing or accepting refusal as document evidence would
weaken the contract. Add browser-level refusal/freshness regression after
successful document answers, leaving all positive facts and boundaries intact.

#### Parent Synthesis and Re-entry

Accepted C1-C5: historical stale harness input, not absent document facts.
Selected a narrow additional browser regression plus durable current evidence.
Rejected runtime routing changes and relaxed text checks. No further research
cycle needed: historical source, current browser and negative probe agree.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/571 (2026-10-31) | Three unticked criteria; baseline prompt/check mismatch reported |
| W2 | https://github.com/jmservera/ama/pull/573 (2026-10-31) | Original correction already merged on 2026-10-30 |
| C1 | `src/api/checks/resident_assistant_browser_check.py:32-43,341-380` | Fresh replies and supported questions already retain all document assertions |
| C2 | `src/api/src/zava_forward/api/resident_demo/chat.py:174-230,251-345` | Full-message grammar, explicit refusal, protected safety/consent/legal boundaries |
| C3 | `src/api/tests/test_resident_chat_api.py:756-813` | Recognized document/form HTTP questions and obsolete-prompt refusals already covered |
| C4 | `.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md:34-60` | Original failure and whole-history false-positive risk; preserved |
| C5 | `.copilot-tracking/reviews/logs/2026-10-30/resident-browser-check-571-review.md:99-120` | Original bounded conformant correction, historical browser mutation evidence |
| C6 | `/tmp/ama-571-baseline-20261031/report.json` | Current base full browser check passes; axe Not run, Chromium recorded |

Local contrarian probe output (2026-10-31): obsolete prompt returns explicit
refusal True; reproduced `Locator expected to contain text 'Survey: Missing'`;
recognized prompt returns Survey in its fresh reply. No source mutation,
credential lookup or external app request was used. `/tmp/mv` supplied installed
pip distributions and Chromium; explicit source paths selected this worktree's
API/core/agents rather than its unrelated editable locations.

## Alternatives and Decision State

Select browser-only regression for obsolete document/form prompts after a
successful answer. It must assert explicit refusal, rules metadata, human help
and absence of own-case document facts in that fresh reply. Existing positive
document facts, citations, isolation, consent and manual paths stay unchanged.
Update the API guide to explain the merged correction and added evidence.
Human/AT/live/model acceptance remains unproven. No runtime or UI edits.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: questions answered; ordered waves and reflection complete;
alternatives dispositioned; historical outcomes preserved; sources traceable.
