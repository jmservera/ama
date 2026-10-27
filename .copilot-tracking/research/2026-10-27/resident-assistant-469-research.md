<!-- markdownlint-disable-file -->
---
title: Resident assistant 469 research
description: Bounded advisory assistant research and owner decision note
ms.date: 2026-10-27
---

## Research Brief

Design and prototype an own-case advisory resident assistant for #469, child
of #466. Audience: owner and PR reviewers. Output mode: convergence, preparing
planning. Posture: focused, selected for the named existing resident surface.
Write root: `.copilot-tracking/research/2026-10-27/`.

## Research Parameters and Direction Controls

No Azure changes, private datasets, secrets, verifier, or external model calls.
Use synthetic fixtures and existing generated-stock lineage only. Real provider
must remain disabled. Additional budget ceiling USD 5 through 2026-10-31.
Separate UI panel; preserve sibling work and MAX_MAPPINGS. Stack on
feat/resident-interactive. Owner explicitly requests the full automatic loop
and targeted checks rather than the long local publication gate.

## Extension Registry and Participation

Repository instructions and RPI phase skills selected. Web guidelines selected
for the separate panel, with Fluent 2, WCAG and content standards authoritative
over generic aesthetics. Research specialist delegation skipped: this is one
continuous, bounded integration trace. No interaction required: scope supplied.

## Questions and Candidate Areas

1. How is each request bound to the current resident case?
2. Which projected facts are safe and sufficient for status/documents/form help?
3. How can an optional real provider remain unable to leak facts or spend here?
4. What evidence supports a sub-USD 5 future activation proposal?

Starting internal areas: resident_showcase, resident_demo server/UI/tests and
component READMEs. External areas: current web guidelines, Azure managed identity
and model pricing documentation. Findings and the three-wave log follow.

## Research Cycle Log

1. Wider: inspected resident domain, HTTP boundary, UI, tests, component commands
   and UX standards. C1-C4 establish a small, isolated panel and authenticated POST.
   Reflection: no existing document-request evidence exists in the showcase row.
2. Deeper: traced view_for through signed session, fresh row fetch and authorise.
   Inspected constant status mapping and unknown-stage handling. Retrieved W1-W3.
   Reflection: model text generation is unnecessary for the three bounded tasks;
   preserve authoritative plain-language status and explicit unknown documents.
3. Contrarian: challenged free-text generation, keyword injection filters, process
   budget counters and dynamically retrieved pricing. Free text can contain secrets;
   regex filters cannot establish isolation, and per-process caps reset. Pricing
   page returns `$-`, not a usable quote. Select explicit topic controls and local
   response rendering; real adapter sees only an enum and returns the same enum.
   Reflection: useful deterministic advice can ship without pretending there is
   AI generation or activating a model. Future activation remains owner-gated.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/resident_demo/app.py:119-141 | view_for authenticates cookie, fetches one case and rechecks admission |
| C2 | src/core/src/zava_forward/core/resident_showcase.py:421-446 | positive view allowlist; status and next step are constant mappings; no requested-documents field |
| C3 | src/api/src/zava_forward/api/resident_demo/app.py:185-205 | POST has existing origin/CSRF/body-size boundary to reuse |
| C4 | src/api/src/zava_forward/api/resident_demo/web/demo.js:30-100 | view render composes independent native panels; no framework needed |
| C5 | docs/reference/research/ux/content-standard.md:25-56 | plain ASCII, optional rules-based help, explicit AI/template labels and human decisions |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-27) | native labelled controls, live async feedback, focus and reduced motion |
| W2 | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/managed-identity (retrieved 2026-10-27, page dated 2026-08-04) | managed identity grants short-lived Entra tokens without app-stored API keys |
| W3 | https://azure.microsoft.com/en-us/pricing/details/azure-openai/ (retrieved 2026-10-27) | estimate/region-dependent pricing; retrieved prices unresolved `$-`; no verified numeric quote |

## Findings Mapped to Questions

Q1: reuse C1 for every assistant request, including revocation, with no case
selector accepted. Q2: status from C2; document requests unknown; form help
generic, explicitly not a completed form or submission. Q3: bounded topic enum
in/out, no resident facts, questions, secrets or history in model prompts; locally
render own-case facts only. Q4: spend USD 0 now; future durable global reservation
and reviewed tariff required, not a process-local promise.

## Alternatives and Decision State

Accepted: deterministic provider by default, explicit topic selector, typed
provider protocol, optional Azure adapter disabled by default and not wired to
runtime configuration. Reject free-form chat for this prototype: unnecessary
injection and accidental-secret surface. Defer generated language and document
request grounding until separately evaluated and connected to actual own-case
document requests. This preserves sibling #467/#468 ownership.

## Design note for owner decision

Recommend local rules for this increment (USD 0); consider Azure OpenAI
GPT-4.1 mini versus GPT-4.1 nano only after owner verifies deployment availability,
tariff, region and processing terms. No availability or price claim is made.
ManagedIdentityCredential supplied by a future host composition is preferred;
vault-backed credentials are a separately reviewed alternative, not browser
settings or checked-in keys.

The adapter will require explicit enablement, a reviewed Azure endpoint,
short-lived token callback and durable atomic budget-reservation callback.
Reserve at most USD 4 for inference and leave USD 1 headroom within the owner's
USD 5 additional ceiling through 2026-10-31 UTC. No retries; refuse at expiry,
on reservation failure or malformed model output. A conservative per-call
reservation must cover the bounded token payload under verified rates. Reservation
cannot be implemented as a resettable in-memory counter in a future live host.

No tools, submissions, consent, appointments, safety/legal/financial decisions
or invented requests. Only same topic IDs may return from a model; untrusted
output never renders. Test malformed/injection topics, cross-resident IDs in
payload/query/header, revocation, CSRF, provider failures, no prompt/log leakage,
disabled provider zero transport calls, budget/expiry and browser keyboard/reflow.

## Planning Readiness and Research Disposition

Research disposition: executed. Planning Readiness: Ready for local prototype,
not real-provider activation. Cycle complete; additional discovery would not
change the local bounded design. Open decisions: owner model/tariff/credential
composition and durable global budget control. Full long gate not run per
explicit owner scope. Self-check: questions mapped, three waves executed,
sources and unresolved pricing recorded; no source changes during Research.

## Design note for owner decision

No model or credential route is approved or activated.
