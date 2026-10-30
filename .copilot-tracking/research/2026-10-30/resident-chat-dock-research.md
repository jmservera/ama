---
title: Resident chat fallback and dock research
ms.date: 2026-10-30
---

## Brief and controls

Investigate the resident prompt, grounding, retrieval, parsing and fallback in
src/api and src/agents, then support a tested local fix and accessible resizing
and right-edge docking. Refs #520 and Refs #563.

Focused convergence research; source-only evidence and constructed fixtures.
No live AI, ledgers, credential files, Azure, deployment or live sign-in.
Owner report is a hypothesis, not proof of the failing condition.
The clean owner-selected branch feat/resident-chat-dock-520 starts at d986c4c4;
no open PR was returned. Reuse this branch. No push is authorized.

## Extensions and participation

Repository instructions, RPI phase skills, web-design-guidelines and
redesign-existing-projects selected. Fluent 2, WCAG baseline, plain-language,
native semantics and reduced motion override generic redesign suggestions.
Direct investigation: one continuous code trace does not merit delegation.
Explicit request authorizes the ordered full loop without routine phase prompts.

## Questions and prior knowledge

1. Which host/model boundary causes safe questions to fall back?
2. Is retrieval missing, or is bounded case grounding intentional?
3. How can resizing/docking preserve shared widget focus and scrolling?
4. Which local tests establish behavior without proving live readiness?

Prior knowledge: API README describes finite admission grammar, limited own-case
grounding, protected deterministic routes and a shared nonmodal chat widget.
These claims need verification against source and tests.

## Cycle 1

### Wider

Traced the consent/session guard, full-message host grammar, Azure adapter,
fixed-topic core contract, agents regulatory retrieval and shared widget.
Reflection: the resident path does not use agents retrieval; adding it would
widen data and authority without solving host admission.

### Deeper

Reproduced refusal of "Can you tell me about my case?", "What is happening with
my retrofit?", "There is a smell of dead rat in my house" and "What documents
do I need to upload?" before the model. The exact already-supported dead-rat
example reaches a 1916-byte request, below the 4096-byte limit. Traced strict
JSON keys/source IDs, finish reason, usage, expiry and prepaid accounting.
All inference failures currently share a generic label and reasonless log.
Reflection: fix bounded everyday wording and observability, not model activation.

### Contrarian

Read earlier research and negative tests: complete-message admission is
deliberate. Reject keyword-only admission and arbitrary text passthrough.
Retain appended-action, combined-request, safety/legal/consent guards.
The owner's "always" report cannot be established against live configuration
within this task. Source supports generation already for exact recognised
questions; no claim that live configuration is repaired is justified.
No new research cycle needed: local boundary and alternatives are established.

## Evidence log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Consent and session precede own-row/model access; protected routes bypass AI | src/api/src/zava_forward/api/resident_demo/app.py:380-458 |
| C2 | Whole-message grammar rejects ordinary paraphrases; banned tell blocks polite status requests | src/api/src/zava_forward/api/resident_demo/chat.py:174-320 |
| C3 | Bounded projected guidance/progress, strict source IDs, 4KiB limits, usage and expiry checks | src/api/src/zava_forward/api/resident_demo/aoai.py:128-339 |
| C4 | Default-off explicit managed identity; all failures have indistinguishable labels/logs | src/api/src/zava_forward/api/resident_demo/aoai.py:109-125,342-366 |
| C5 | Agents regulatory retrieval is a separate offline employee source-excerpt path | src/agents/src/zava_forward/agents/regulatory_chat.py:1-110 |
| C6 | Shared nonmodal widget owns focus, bottom following and bounded layout | src/api/src/zava_forward/api/web/chat-widget.js:28-157 |
| C7 | Prior source correction already added generated prose; later research preserves complete-message limits | .copilot-tracking/research/2026-10-30/resident-chat-ai-563-research.md:49; .copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md:45 |
| W1 | Native controls, labels, focus, wrapping, gesture alternatives, safe areas and reduced motion | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md retrieved 2026-10-30 |

## Decision and risks

Select exact polite wrappers plus bounded common paraphrases, preserving
whole-message matching. Expose host-owned fallback reasons without logging
messages, identities or exception details. Keep source/response/payload budgets,
expiry and activation unchanged. For residents only, add native labelled size
ranges and a dock toggle; retain shared-widget defaults for employees.
No persisted text or geometry is needed. Use CSS viewport bounds and no
size animations, keeping scrollable history and composer.

Rejected: broad keyword routing, arbitrary model classification, a second
retrieval/client, raising budgets, automatic activation, custom drag-only
handles, unrelated visual overhaul. Local synthetic tests cannot establish
actual-model correctness, live parity, human usability or AT conformance.

## Evidence and readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Self-check: all questions answered, three waves ordered, alternatives recorded,
source and external claims cited. No research blockers.
