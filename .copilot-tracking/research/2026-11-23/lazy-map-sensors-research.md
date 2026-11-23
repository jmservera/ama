---
title: Lazy map sensor loading research
ms.date: 2026-11-23
---

# Task Research: Lazy map sensors

## Executive Summary

Research complete. `/api/map` synchronously calls `map_sensors` for all shown
points. Each authorized home requires authorization and a latest-reading query;
up to 100 homes are processed per map draw. Ordinary map loads can avoid this
work entirely. Sensor summaries should load for the selected home instead.

## What You May Not Know

The stale/offline checkbox depends on bulk sensor summaries. The owner selected
keeping it as an explicit opt-in exception to click-only loading.

## Findings

### Map requests wait for sensor SQL reads

C1 establishes that the map route always supplies a sensor provider. C2 shows
the provider authorizes each home and calls the bounded summaries loop; C3
shows one latest-reading query per admitted home. This is evidence-backed,
with high confidence from the source trace. No live timing claim is made.

### Selected-home summaries can reuse the same permission projection

C4 shows `showHome` currently renders the values embedded in map points.
A single-home read can reuse C2 unchanged, retaining consent, restricted,
unavailable, stale and offline states without returning sensor history.

### Bulk filtering must be explicit

C4 shows the checkbox currently only filters already-loaded client data.
It must trigger an opted-in map read instead. Ordinary draws, panning and
selection must not require summaries for unrelated homes.

## Recommendation and Alternatives

Select default lightweight maps, a single-home summary route using the existing
`map_sensors` projection, and `sensors=1` only while the stale/offline checkbox
is checked. Defer selected requests with cancellation and selection-generation
guards. Do not fetch history just to show two latest values.

Rejected: retaining eager bulk summaries (does not meet the request); removing
the filter (owner chose otherwise); mapping the full history endpoint into the
summary shape (unnecessary data and duplicate status logic).

## Scope and Questions

* Goal: remove unselected-home sensor work from initial map loading.
* Audience: application maintainers.
* In scope: staff map, sensor requests, directly related tests and documentation.
* Out of scope: visual redesign, deployment, private datasets, unrelated PDF.
* Q1: Which requests or server projections load sensor readings for map homes?
* Q2: Which existing selected-home endpoint can preserve sensor states?
* Q3: How can tests prove zero sensor-detail requests before selection?
* Output mode: convergence.

## Decisions and Feedback

* D1: User selected end-to-end automatic work.
* D2: User approved carrying the existing PDF modification onto a topic branch;
  that file will not be edited or committed.
* D3: Owner selected `opt-in`: retain the stale/offline filter and bulk-read only
  when checked. No further material decision is unresolved.

## Risks and Open Questions

Preserve permission boundaries, sensor-error messaging, accessible list access
and correctness when requests resolve after selection changes.

## Planning Readiness and Next Step

Research disposition: executed, complete. Planning Readiness: Ready (C1-C4).
Decision participation: agent-owned in automatic mode. No research blockers.
Next: automatic Plan; focused local tests and exact-head review remain required.

## Research Record

### Method and Boundaries

Focused posture, narrowed from balanced because this is a bounded performance
bug with supplied UI evidence. Candidate areas: map loader, map projection,
selected-home sensors, existing map tests. No external product research or
private data is needed. No helpers. No explicit deadline.

Evidence root: `.copilot-tracking/research/`; date comes from the current user
timestamp, 2026-11-23. Primary evidence file:
`.copilot-tracking/research/2026-11-23/lazy-map-sensors-research.md`.

### Extensions and Participation

Repository instructions and API README selected for source/test conventions.
Web Interface Guidelines fetched on 2026-11-23 for scoped web changes.
Design-redesign skills skipped: no visual design change is requested.
Prior sessions identify map browser regression work; source is authoritative.
No material intake ambiguity remains after the branch decision.

### Research Cycle Log

Cycle 1:

* Wider: read map request, map panel, and existing map API/source tests.
  Reflection: bulk server work, rather than a separate browser sensor request,
  explains the reported wait.
* Deeper: traced route -> store projection -> `map_sensors` -> per-home summary.
  Reflection: the existing summary projection preserves every required state.
* Contrarian: inspected filtering, keyboard activation, map redraw and route
  disposal. Reflection: filtering is a valid explicit bulk exception, confirmed
  with the owner. Late responses must not replace another home's values.
* Synthesis: accept C1-C4; select lazy summaries with opt-in bulk reads. No
  additional cycle is needed because the source contracts answer Q1-Q3.

### Evidence Log

| ID | Source or location | Claim or finding |
| --- | --- | --- |
| C1 | `src/api/src/zava_forward/api/server.py`, `/api/map` | Always passes bulk sensor callback |
| C2 | `src/core/src/zava_forward/core/assistants.py`, `map_sensors` | Existing authorization, role restriction, cap and logged failure |
| C3 | `src/core/src/zava_forward/core/sensor_map.py`, `summaries`, `summary` | Per-home latest query and consent check, no history |
| C4 | `src/api/src/zava_forward/api/web/app.js`, `mapPanel` | Embedded sensor display, keyboard activation and client-only filter |
| W1 | [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) | Retrieved 2026-11-23; async status, semantics and focus rules |

No contradictions remain. All questions answered; no helpers used. Scope,
evidence states, alternatives, decisions, cycle, readiness and source references
checked. Only live performance magnitude remains unmeasured.
