---
title: Capacity delayed sibling 401 research
description: Bounded investigation for issue 523 and PR 528
ms.date: 2026-10-28
---

## Research Brief

Task 523-delayed-401 / capacity-page-523-delayed-401 follows the preserved
capacity-page-523-correction evidence. Audience: implementer and PR reviewer.
Convergence output; focused posture selected from the owner's named race,
files and acceptance criteria. Scope is the post-read lifecycle guard and the
existing capacity browser harness. No redesign, authentication redesign, cloud,
deployment, secrets, environment files or private data.

## Research Parameters and Direction Controls

Owner explicitly requests the full automatic Research/Plan/Implement/Review
loop, red/green browser proof, focused units/static checks, normal push and
subsequent thread reply/resolution. No routine interaction is needed.
Browser admission must use nonblocking /tmp/ama-rpi-heavy.lock with 60-second
retries for at most 40 minutes. Complete gate is blocked by prohibited az and
must not be attempted. Initial fetch/pull succeeded; clean matching active
branch fix/capacity-page-523 at 2d207b62 includes the rubric bot commit.

## Extension Registry and Participation

Repository instructions and RPI phase skills selected. Web guidelines selected
for the changed ops.js lifecycle surface, fetched from the skill's current
source on 2026-10-28. Public-page design and redesign skills skipped: no visual
design change. Research inline: this is one tightly coupled lifecycle trace;
no separate research worker is justified. Independent critique and final Review
will be separate phase-owned assessments.

## Questions and Candidate Areas

* Where can a successful retry render after session loss?
* How can real browser requests be deterministically ordered to prove it?
* Which existing fixture and validation commands preserve the original scope?

Initial evidence areas: ops.js capacityView, app.js api/route lifecycle,
capacity_browser_check.py, API README and prior correction artifacts.

## Research Cycle Log

### Cycle 1: Wider

Verified the existing correction artifacts, current unresolved thread
PRRT_kwDOUU8JX86xSi-Q and the installed browser harness. Cross-session history
returned no matching branch sessions; repository artifacts supply prior knowledge.
The branch/PR remain active and coherent. Reflection: preserve prior red/green
and full-gate claims as historical, not evidence for this new candidate.

### Cycle 1: Deeper

* C1: `src/api/src/zava_forward/api/web/ops.js:176` awaits Promise.all then
  renders without rechecking me or the captured route signal. go() already
  suppresses errors for ended sessions, but success has no corresponding guard.
* C2: `src/api/src/zava_forward/api/web/app.js:28-38` checks abort after parsing
  each response, but a successful request does not check me. A 401 clears me
  and calls login without aborting the shared route controller.
* C3: `src/api/checks/capacity_browser_check.py:559-644` tests mutation-refresh
  navigation/401 with held packages, but no failed-read sibling concurrent
  with successful retries. Existing supplied_contract_fixture supports a real
  successful threshold mutation with no private data.
* C4: `src/api/checks/capacity_browser_check.py:685-726` already acquires the
  heavy lock nonblocking before generated seed/SQL/browser work. A retry launcher
  can rerun only its busy exit, leaving every actual browser attempt admitted.

Reflection: hold both initial refresh reads, fail one, retain the sibling;
start retry and hold both retry responses; deliver the old sibling's 401;
observe sign-in; release actual successful retry payloads. Wait for retry
continuation completion, then assert sign-in, focus, no capacity or retry
controls, one persisted mutation and no unexpected errors.

### Cycle 1: Contrarian

The per-request abort guard is not sufficient because the 401 does not abort
this signal (C2). Cancelling all siblings or introducing request generations
would widen the change unnecessarily; the requested synchronous post-read
signal/session guard addresses the actual boundary (C1). No await occurs
between that guard and rendering, so no additional concurrent transition can
interleave there. Test both initial failed endpoints to avoid endpoint-order
assumptions. Existing navigation cancellation scenarios remain required.

## Evidence and Alternatives

Accepted C1-C4. Selected: post-Promise.all throwIfAborted followed by a no-session
return. Rejected: changing global login/api or cancelling every sibling, which
would alter unrelated callers. W1: web rules retrieved 2026-10-28 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md;
preserve native controls, focus and error semantics, no unrelated redesign.

## Risks and Residual Uncertainty

Browser proof pending; source trace alone is not regression evidence. Full gate
blocked by barred az. Live deployment verification remains pending owner.
No new regulatory or customer claims, so no knowledge-base synthesis update.

## Planning Readiness

Ready. Research disposition executed, all three waves complete inline.
No further research cycle warranted: exact lifecycle, fixture and orchestration
boundaries identified. Artifact self-check complete; handoff C1-C4 to Plan.
