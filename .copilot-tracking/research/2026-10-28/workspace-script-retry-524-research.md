<!-- markdownlint-disable-file -->
---
title: Workspace script retry research
description: Focused evidence for issue 524
ms.date: 2026-10-28
---

# Task Research: workspace-script-retry-524

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md |

## Research Brief

* What to research: missing employee workspace script recovery, startup ordering,
  failure presentation, local static delivery and available public live evidence.
* Why: a transient script failure currently requires a manual refresh.
* Audience: implementer, independent reviewer and owner.
* Scope: issue #524, src/api web startup, static serving and existing tests.
* Non-goals: deployment, Azure access, credentials, private datasets, visual redesign.
* Criteria: each issue acceptance criterion has evidence or an explicit unresolved
  cause / owner-pending live check; preserve native semantics and existing message.
* Requested outputs: dated research, plan, details, changes and independent Review.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Why does startup fail, what bounded recovery preserves dependencies, and how is recovery proven? |
| Codebase scope | src/api, relevant tools and local gate documentation |
| External scope | GitHub issue 524 and public employee-site static responses if discoverable |
| Initial internal candidate areas | app.js, index.html, API README, static route and browser tests |
| Initial external candidate areas | Issue 524, public site URL in repository documentation |
| Research posture | focused |
| Posture provenance | Default for named code target and bounded defect |
| Explicit limits | No Azure, secrets, .env or private datasets; heavy work requires nonblocking /tmp/ama-rpi-heavy.lock |
| Completion basis | Material questions covered with source or explicit missing evidence |
| Edits allowed during research | Evidence and workflow tracking only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | Repository-wide source, evidence, branch and publication rules | Selected |
| Skill | rpi-research | Active research protocol | Selected |
| Skill | web-design-guidelines | Web edits and review | Selected for implementation and review |
| Specialist | RPI Researcher | Registered independent research lanes | Skipped: one tightly coupled startup trace |

## User Participation and Research Decisions

The user explicitly requests the full ordered RPI loop, implementation, commit,
push and PR on fix/workspace-script-retry-524. This is automatic execution consent
at intake, not an inferred switch from an existing manual session. Interaction is
unavailable; ordinary decisions remain bounded by the supplied scope.

## Scope and Success Criteria

The five issue criteria are: cause evidenced or unresolved with checked items;
automatic bounded recovery; unchanged terminal message; failed-first-load test;
post-deployment live verification recorded or explicitly owner-pending.

## Task Research Requests

Use src/, preserve plain language and non-colour signals, run API unittest command
and browser fault injection, observe 100-character Ruff limit, retain original
critique and Review evidence, and publish only through the required local gates.

## Direction Controls

No Azure/deployment, secrets, .env, private data, force push or main writes.
Do not attribute live failure to cold starts, truncation or caching without evidence.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What startup dependency/failure contracts need preservation? | depth | Open |
| Q2 | What local/public delivery evidence can identify the cause? | depth | Open |
| Q3 | What regression checks prove bounded recovery and exhaustion? | straightforward | Open |

## Prior Knowledge Gate

Read original case study, addendum context, reference index and owner memory.
Issue 524 reports intermittent Leaflet delivery and recovery on manual refresh;
that report is evidence of symptoms, not a confirmed infrastructure cause.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline startup, static handler and test discovery found synchronous script tags,
route-specific global checks, and existing Node VM and synthetic Chromium harnesses
(C1-C5). No independent lane warranted delegation.

Reflection: the observed fatal behavior is intentional fail-fast detection, not
proof of a defective Leaflet artifact or particular infrastructure cause.

#### Wave 2: Deeper

Prioritized route-specific dependencies and cancellation. Classic companion scripts
declare top-level lexical constants: do not reload already-present scripts.
Recovery must await readiness before invoking views and suppress obsolete routes
after navigation or sign-out. The static server reads complete bytes and sends an
explicit length, JavaScript MIME type and no-store (C3).

Reflection: preserve dependency predicates; retry only missing files with a
page-lifetime per-path promise, bounded attempts and timeout.

#### Wave 3: Contrarian

Challenged unconditional reload, unbounded route-triggered retry, false-positive
HTTP success and stale navigation. Rejected reload-all because of lexical
redeclarations and duplicate registrations. A successful script load event is not
sufficient: recheck the expected global. Hanging requests need timeout and element
cleanup. Shared pending attempts must not render stale views.

Reflection: no evidence supports changing infrastructure or caching. Public live
transport/cold-start investigation and post-deployment checks remain owner-pending
under the no-Azure boundary; no authentication material or telemetry was accessed.
The issue explicitly accepts an unresolved cause with checked items.

### Parent Synthesis and Disposition

Accept bounded targeted recovery and real-browser fault injection. Reject
reload-all, infinite retry, arbitrary URL fetching and speculative infrastructure
changes. Defer authenticated live status/size/headers/cold-start correlation.
One completed focused cycle covers the implementation decision; a further local
source search cannot establish historical live delivery failures.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/524 (retrieved 2026-10-28) | Owner-reported intermittent /vendor/leaflet.js startup failure; five acceptance criteria |
| C1 | src/api/src/zava_forward/api/web/index.html:34-41 | Synchronous Leaflet and companion scripts precede app.js |
| C2 | src/api/src/zava_forward/api/web/app.js:143-210 | Route predicates detect missing globals, throw unchanged message and render status/alert/native reload button |
| C3 | src/api/src/zava_forward/api/server.py:38-43,182-198,235-247 | Correct JS MIME, no-store, Content-Length and whole-file reads; trusted-proxy authentication can redirect protected assets |
| C4 | src/api/tests/test_role_screens.py:1-60 | Existing unittest invokes Node VM against actual web source |
| C5 | src/api/checks/design_system_browser_check.py:225-277 | Owned synthetic loopback server and Chromium callback; no inherited data/model settings |
| C6 | src/api/src/zava_forward/api/web/role-screens.js:3-5,30-33 | Top-level lexical registry and duplicate-screen guard make reload-all unsafe |
| C7 | src/README.md:60-133 | Scoped tests for small issues; complete gate has shared lock and immutable external receipts |
| W2 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-28) | Preserve native buttons/links, live async feedback and focus; no visual redesign needed |

## Findings Mapped to Questions and Evidence

Q1 answered by C1/C2/C6: preserve exact route predicates, only retry absent
dependencies, await recovery and abort obsolete route rendering.
Q2 unresolved live cause with checked source items C1/C3 and W1; local HTTP bytes,
size and headers will be asserted by the focused browser check.
Q3 answered by C4/C5: Node regression tests and an actual Chromium failed initial
request, successful retry, permanent failure, navigation and sign-out checks.

## Alternatives and Decision State

Select two automatic attempts per missing path after the initial HTML request,
with short increasing delay, finite per-attempt timeout, shared promise across
route changes, and unchanged terminal error. Keep URLs same-origin and fixed.
Do not alter HTML, CSS, auth or server caching. Rejected full-page refresh (loses
state), all-script reload (C6), and server tweaks without live evidence (C3/W1).

## Open Questions, Risks, and Residual Uncertainty

Actual live transport cause and post-deployment behavior remain unverified.
No authenticated live probes, response-size capture, telemetry correlation or
deployment occurred. Known source possibilities include transport interruption
and auth redirect, but neither is established as the actual cause.

## Current Decisions

Worktree starts clean on requested branch, HEAD 413ccaf253fce4566e855bae9d0a924b2a82b506;
no open PR for this branch was returned.

## Planning Readiness

Ready. Research disposition: executed. Source and browser checks can prove
recovery independently of the unresolved live cause. Missing system interpreter
API dependencies were observed; install existing project dev distributions before
validation. Original critique and independent Review remain required.

## Self-check

Complete focused wider/deeper/contrarian cycle; claims have stable evidence IDs;
live uncertainty and boundaries retained; no source changes during Research.
