---
title: Regulatory alert and home chat UX research
description: Issue 215 implementation evidence and bounded research
ms.date: 2026-10-16
---

## Brief and direction

Implement issue #215 on the existing topic branch, using merged #328, #331
and #348. Focused internal research; synthetic development only. No real
staff, private datasets, paid providers, operational approval or new rights.
The owner explicitly requests implementation, review and a PR in this run.
Accessibility skill selected for WCAG 2.2 AA engineering evidence; broader
design skills skipped because this is an existing app task, not marketing.
No delegation needed for the continuous alert/chat trace.

## Cycle 1

### Wider

* C1: `docs/reference/research/ux/regulatory-literacy-for-journeys.md:32`
  defines recognise/apply/interpret needs, missing leases/contracts and safe
  escalation. All seven issue audiences need patterns, not invented staff roles.
* C2: `docs/adrs/0005-regulatory-compliance-assistant.md:20` accepts synthetic
  development only; Juan Manuel Servera owns exercise Legal, Compliance and DPO.

### Deeper

* C3: `src/core/src/zava_forward/core/rule_engine.py:344` already emits noticed,
  result, owner, safe action, clock, citations, dates and exercise labels.
  `/api/law/alerts?case=` applies server audience and field projection.
* C4: `src/api/src/zava_forward/api/web/chat.js:80` already provides bounded
  regulatory lookup and a persisted doubt inbox, but renders a long preformatted
  reply and hides capability failures silently.
* C5: `src/agents/src/zava_forward/agents/regulatory_chat.py:78` supplies structured
  sections and citation metadata. No model change is needed to present them.
* C6: `src/core/src/zava_forward/core/projection.py:38` defines existing staff
  roles; contractors cannot access chat/law. Presentation must not expand rights.

### Contrarian

More AI or client-side legal summaries would weaken provenance and invent value.
Use deterministic structured presentation, plain-language explanations alongside
unaltered quotations, explicit unknown/no-source and failure states. Empty
role-scoped alerts do not establish safety or compliance. Broad WCAG conformance
and staff comprehension cannot follow from automated browser checks.

## Synthesis and readiness

Research disposition: executed. Planning Readiness: Ready.
Reuse server authorization, clocks, immutable citations, doubt receipts and
source-change labels; add an always-visible home alert section outside optional
chat and role-shaped recognition guidance. Define all audience patterns in the
API README without inventing permissions or legal commencement claims.
Test the actual local SQL-backed app with wholly constructed fixtures.
Staff comprehension and comprehensive WCAG certification remain unmet.
No external legal retrieval is needed: no new legal rule or currentness claim.

## Independent review follow-up evidence

Research disposition: reused with focused internal inspection; Ready for P03.
Owner supplies independent CHANGES verdict on d79a737: the workflow runs only
the design-system browser harness, never regulatory_ux_check. That check
requires axe and only measures target size inside keyboard_activate, missing
the cited-lookup summary's designed 44px height. keyboard_walk checks focus, not
target dimensions. The default summary line box is already 24px, so the mutation
must protect the stronger existing 44px design contract, not mislabel 24px as
an AA violation. Newly measured inline citation links are only 18px high;
give those changed-surface targets inline-block 24px minimum-height sizing.
The source-summary CSS rule is therefore not protected by current assertions.
Use actual per-state bounding boxes, not axe alone, to detect its deletion.
No new legal, approval or user-research evidence is introduced.
