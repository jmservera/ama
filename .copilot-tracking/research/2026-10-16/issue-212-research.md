---
title: Issue 212 deterministic checks research
description: Bounded source and runtime investigation
ms.date: 2026-10-16
---

## Brief

Implement #212 in src, with approval, SQL, safety and identity boundaries
preserved. Focused research, caller-selected targets. No legal interpretation,
private data, cloud deployment, or invented approval. RPI quick parent owns
continuation; the explicit end-to-end request authorizes eligible phases.

## Cycle 1

### Wider

* C1 `docs/adrs/0005-regulatory-compliance-assistant.md:166`: architecture
  3/4 specifies five results, SQL facts, three triggers and alert hygiene.
* C2 `docs/adrs/0006-src-layout-and-cutover.md:74`: separate projects and
  tests outside packages. Existing branch feat/src-rule-engine-212 is clean,
  has no PR, and contains merged #211 at 9dda3a3.
* C3 GitHub #212 body and comments retrieved with gh on 2026-10-16:
  acceptance unchanged after src cut-over; use Refs, not Closes.

### Deeper

* C4 `src/core/src/zava_forward/core/rulecards.py:170`: immutable prose
  cards, distinct author/owner lifecycle, only exercise cards currently
  allowed. Seeds are drafts. No approved executable duration exists.
* C5 `src/core/src/zava_forward/core/lawstore.py:401`: versioned sources
  and exact provision lookup expose status, dates and completeness.
* C6 `src/core/src/zava_forward/core/sqlstore.py:39`: SQL case bodies and
  row versions supply a bounded home/case snapshot.
* C7 `src/api/src/zava_forward/api/server.py:390`: card mutations need
  trusted-proxy owner capabilities; authority/date are server-derived.
* C8 `src/core/src/zava_forward/core/workflows.py`: hazard intake and
  release already have independent human evidence and code-owned holds.

### Contrarian

Executing prose or guessing statutory durations would manufacture legal
interpretation. Reject that alternative. Add an optional immutable executable
contract to a new card version, visible before its existing human approval.
Old cards without such a contract remain unknown, never silently upgraded.
Consultations/historical/future/partial or missing citations cannot establish
an active clear. Engine failure must not participate in hazard intake.
Do not claim operational acceptance from fictional approvals or local tests.

## Synthesis

Research disposition: executed. Planning Readiness: Ready.
One focused inline cycle suffices: the tightly coupled trace establishes
all extension points. Repository instructions selected; external legal
research skipped because no new legal assertion or activation is authorized.
Python foundational guidance applies during implementation. No independent
research worker needed. Remaining live SQL/Azure, staff comprehension,
legal approval and tenant assignment evidence is unavailable, not invented.
