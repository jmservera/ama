<!-- markdownlint-disable-file -->

# Task Research: capacity-page-523-correction

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md |

## Research Brief

* What to research: RV-002 draft loss on refresh retry and RV-003 incomplete browser proof.
* Why it matters: The prior candidate cannot be published with these findings or missing runtime evidence.
* Audience or intended use: Correction-cycle planning and independent review for issue #523.
* Scope: Existing capacity implementation, browser check, shared route/draft contracts and local gate.
* Non-goals: Azure, deployment, secrets, environment files, private datasets, unrelated RV-004/005/006 fixes.
* Criteria: Repeated failed retries retain drafts; successful recovery does not replay mutations;
  browser assertions prove real packages/orders, destination content and expected successful reads.
* Requested outputs: New dated research, plan, critique, implementation and Review evidence.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which recovery path retains drafts, and which assertions prove actual route/read success? |
| Codebase scope | Capacity UI, browser check, API tests, local validation tools |
| External scope | Current web-interface guidelines only |
| Initial internal candidate areas | Prior Review, ops.js, app.js, capacity_browser_check.py, API README, rpi-checks.py |
| Initial external candidate areas | Official web-interface-guidelines source |
| Research posture | focused |
| Posture provenance | Default for named, bounded defects and supplied failure evidence |
| Explicit limits / deadline | Heavy lock: nonblocking flock every 60 seconds, at most 40 minutes; Ruff 100 |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No Azure, secrets, .env, private data or foreign gate output |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | Repository-wide | Branch, privacy, evidence and full local gate | Selected |
| Skill | rpi-research | RPI wrapper | Three ordered evidence waves | Selected |
| Skill | web-design-guidelines | Changed web code | Fresh rules before edits and review | Selected |
| Research specialist | hve-core-all:rpi-researcher | Registered | Independent evidence lane | Skipped: one tightly coupled trace, direct investigation |
| Skill | redesign-existing-projects | Existing app | Visual redesign | Skipped: no design improvement requested |

## User Participation and Research Decisions

Caller explicitly selected a new complete correction cycle and authorized commit,
push and PR on the existing branch. Existing parent state is automatic/running;
this is its selected child, not an inferred manual-to-automatic transition.
No interaction is needed or available. Earlier artifacts remain unchanged.

## Scope and Success Criteria

Use only task-owned synthetic fixtures/resources. Preserve resident/manager authority,
native controls, draft guards and mutation semantics. Live verification remains pending
the owner. Publication requires real local SQL/browser results and a current full receipt.

## Task Research Requests

Fix RV-002/RV-003, obtain missing RV-001 runtime evidence with expressly authorized
lock retries, and publish with Refs #523 only after the required gates.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | RV-002 and RV-003 source correction | Caller 2026-10-28 | No unrelated visual fixes |
| change | Retry nonblocking heavy admission every 60s for at most 40m | Caller 2026-10-28 | Supersedes earlier no-poll coordination restriction for this execution |
| exclude | Azure, secrets, .env, private datasets | Caller 2026-10-28 | Constructed local fixtures only |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How can read-only retry retain all unsaved capacity forms on repeated failure? | depth | H | open |
| Q2 | Which page/read/row assertions establish real manager navigation success? | depth | H | open |
| Q3 | How can local SQL/browser and exact-head publication gates run safely? | straightforward | H | open |

## Prior Knowledge Gate

Read the original Review and automatic parent state. Treat historical runtime
claims as unverified until repeated at the new candidate. Repository baseline
documents and memory were read; no customer or legal claims are changed.

## Research Cycle Log

### Cycle 1

Focused, inline investigation; no independent uncertainty warrants delegation.

#### Wave 1: Wider

The original review, current capacity go/load helpers, shared route and browser
harness were read. RV-002 is confirmed: go's new retry invokes route(), whose
same-hash failure replaces the workspace. RV-003 is confirmed: manager inventory
only rejects one heading and only observes HTTP failures, not failed transports.
The branch is clean at intake and contains the earlier implementation in
ac8d4037; the old Review correctly describes its own earlier uncommitted boundary.
Reflection: prioritize a capacity-local read-only recovery closure and exact
route/read assertions; avoid global route/draft redesign.

#### Wave 2: Deeper

appointmentDrafts captures unsaved form values, checked state, expansion and
appointmentContext immediately before show(), after both reads succeed.
Thus local capacityView retry leaves the original DOM intact on failure and
already restores drafts on success. A no-mutation invocation of go reuses that
behavior and status region without changing global route semantics.
The manager destinations have specific headings and read endpoints; some catch
errors inline, so a heading alone is insufficient. Capacity rows can be counted
and compared to the real response IDs. Generated legacy orders lack contract
authority: a safe real mutation fixture should use the existing manager-only
configure action (no offer/consent/authority fabricated).
Reflection: regression must distinguish saved form from another unsaved form,
including context, checkbox and expansion, and count successful POSTs.

#### Wave 3: Contrarian

Changing the global same-hash guard would prompt for discard and still lose drafts
when accepted, rather than fulfill safe recovery. Stashing only at error rendering
is also unnecessary: the existing success-only replacement already preserves the
live DOM. A retry must not call the prior mutation again. Navigation/session
cancellation must not write an error to an obsolete view; add captured-signal and
session guards to go's recovery path. A heading-only check remains weak on finance
and time, which catch errors inline; require successful expected reads plus
destination-specific content. Known injected errors must be explicitly scoped,
not globally ignored.
Reflection: no new material uncertainty requires another cycle; real execution
remains an implementation/publication gate, not a reason to expand research.

#### Parent Synthesis and Disposition

Accept capacity-local read-only go() retry and exact route/read/row assertions.
Reject global router changes and mutation replay. Defer RV-004/005/006 and live
verification. Research disposition: executed; complete focused three-wave cycle.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/ops.js:134-173 | Draft snapshots and mutation/refresh go; retry currently calls route |
| C2 | src/api/src/zava_forward/api/web/ops.js:247-265 | Draft capture/restore runs only after successful reads |
| C3 | src/api/src/zava_forward/api/web/app.js:167-211 | Same-hash router failure replaces app without draft confirmation |
| C4 | src/api/checks/capacity_browser_check.py:144-201 | HTTP-only failure tracking and permissive route heading |
| C5 | src/api/src/zava_forward/api/web/app.js:363-455,1258-1310 | Queue, overview, visits and funding reads and real rendered content |
| C6 | src/api/src/zava_forward/api/web/panels.js:418-426; timecapture.js:3-43; assistants.js:104-123; role-screens.js:41-67 | Other manager destinations and inline error cases |
| C7 | src/core/src/zava_forward/core/appointments.py:218-236 | Existing configure action persists provisional threshold evidence |
| C8 | src/README.md:76-163; tools/rpi-checks.py:2175-2268 | Committed exact-head full gate, nonblocking admission and verification contract |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-28) | Native retry, live status, unsaved draft and error guidance; no visual redesign |

## Findings Mapped to Questions and Evidence

Q1 answered by C1/C2/C3/C7: reuse go without a mutation, preserving DOM on failed
reads and restoring current unsaved appointment drafts on success.
Q2 answered by C4/C5/C6: exact headings, destination content, expected browser GET
success, row identity/count, and unexpected HTTP/transport failures.
Q3 answered by C8: owned generated SQL/browser checks under heavy admission;
commit original RPI evidence before complete exact-head gate and later assessment.

## Alternatives and Decision State

Selected: bounded capacity recovery closure and expanded existing harness.
Rejected: shared-router overhaul, fabricated mutation success, SQLite-only proof,
and blanket ignoring failed requests. No unresolved design decision.

## Open Questions, Risks, and Residual Uncertainty

Real SQL/browser/full-gate results and live causality are not yet established.

## Planning Readiness

Ready. Research disposition: executed, complete.
Self-check: all questions mapped, three waves ordered, citations present,
no source edits, exclusions retained. RPI parent may proceed to Plan.
