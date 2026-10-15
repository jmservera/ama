---
title: Hazard referral and retrofit hold research
description: Issue 85 evidence and bounded implementation readiness
ms.date: 2026-10-15
---

## Research Brief

Task `85`, slug `src-hazard-referral-85`. Execute the full RPI loop for
hazard referral and retrofit holds, not hazard-service ownership.
Audience: implementer and PR reviewer. Output mode: convergence.
Research root: `.copilot-tracking/research/2026-10-15/`.

## Research Parameters and Direction Controls

Focused internal research, selected because the caller supplied the issue,
accepted architecture and named implementation surfaces.
Work only on `feat/src-hazard-referral-85` in the supplied worktree.
New code/tests belong in `src/`; no new `mvp/` code, private data, operational
clock rules, nonportable SQL or deployments. Preserve human decisions and
resident consent. The caller explicitly requests automatic full-loop execution,
commit, push and PR creation, but no merge.

## Extension Registry and Participation

Repository `.github/copilot-instructions.md` applies throughout.
Selected RPI phase skills for the full lifecycle. Domain architecture is
supplied by accepted ADR 0006; no architecture redesign is requested.
Research stays inline because the implementation trace is tightly coupled.
No interaction is available; owner-decision gaps will remain explicitly unmet.

## Questions and Candidate Areas

1. What issue criteria and owner updates are actually available?
2. Which merged workflow, projections, persistence and HTTP patterns are reusable?
3. How can receipt, acceptance, hold scope and externally owned times be recorded
   without claiming hazard categorisation, clocks or closure authority?
4. What local validation can be reproduced without private data or live services?

## Research Cycle Log

Cycle 1 opening: Wider examines issue/ADR/parity and existing surfaces; Deeper
traces state, authorisation, persistence and tests; Contrarian tests authority
boundaries, legacy hazards and unintended progression/release paths.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/85, retrieved 2026-10-15 with
  `gh issue view 85 --comments` and JSON retrieval. Four unchecked criteria;
  JSON returns no comments. No unseen owner update is assumed.
* W2: https://github.com/jmservera/ama/pull/296 through
  https://github.com/jmservera/ama/pull/302, retrieved 2026-10-15.
  All seven PRs report MERGED.

## Findings, Alternatives and Readiness

### Wider reflection

The issue has no comments at retrieval, despite the caller's warning about
updates. The accepted src decision and seven merged moves are present.
The existing workflow already persists hazard dictionaries in the case body;
no new schema or replacement service is necessary.

### Deeper evidence

* C1: `docs/adrs/0006-src-layout-and-cutover.md:166` defines one-way
  dependencies. `docs/architecture/mvp-to-src-parity-matrix.md:209` assigns
  workflows to core; line 297 places legacy HTTP workflow tests in api.
* C2: `src/core/src/zava_forward/core/workflows.py:276` currently conflates
  referral with ownership and has no receipt/acceptance evidence. Repair and
  release lack required external evidence; negative indexes select hazards.
* C3: `src/core/src/zava_forward/core/store.py:131` gates unresolved hazards;
  line 300 projects case detail. JSON/SQLite/SQL Server use the same inherited
  workflow and persisted case body, so no SQL statement needs adding.
* C4: `src/core/src/zava_forward/core/projection.py:24` holds note keys and
  removes all hazard records from contractor detail. New external references
  and narrative source fields must also be withheld from no-need roles.
* C5: `src/api/src/zava_forward/api/server.py:588` wires legacy actions;
  `src/api/src/zava_forward/api/web/app.js:561` exposes categorisation-like
  labels and repair completion without a service reference.
* C6: `src/core/tests/test_handoff_lifecycle.py:1` demonstrates JSON/SQLite
  durable semantic testing. `src/api/tests/test_handoff_api.py:1` provides
  loopback HTTP patterns. Existing building blockers remain independent.
* C7: `docs/brds/agentic-retrofit-programme-brd.md` RULE-003 and FR-003
  reserve classification, clocks, action and closure for the hazard service.
  The issue's BRD FR-015 pointer now names tenure, not hazard referral. Use
  issue text plus RULE-003/FR-003 rather than silently renumber requirements.

### Deeper reflection

Reuse the workflow, ledger, role projection, persistence and independent
building/consent gates. Record a home-scoped retrofit hold and separately
evidenced sent/received/accepted events. Sender retains chase responsibility
until explicit acceptance; the retrofit case owner never transfers here.
External service timing observations are read-only assertions with provenance,
not locally calculated legal deadlines.

### Contrarian wave and reflection

Retaining the legacy repair/release buttons unchanged would leave an evidence
bypass. Tighten them to require external service evidence, separate receipt and
acceptance, a safety actor and an independent hold-release reason. Preserve
legacy stored hazards without inventing missing receipt/awareness history.
Do not call released holds closed hazards. Reject negative/bool/fractional
indexes, replayed events and forged actor fields. Hazard referral must remain
available during AI outages and retrofit/building pauses, including closed
retrofit records. Scope only the linked home; no new building-wide authority.

### Alternatives and parent disposition

Accepted: extend existing workflow with explicit referral evidence and hold
semantics; retain report category/urgency only as unverified observations.
Rejected: a second hazard service or statutory clock engine, because RULE-003
forbids this. Rejected: reusing case handoff acceptance to transfer retrofit
ownership, because hazard acceptance is a distinct responsibility.
Deferred: approved operational thresholds, transport proof from the real
repairs service, real model/SQL Server/Azure and human acceptance.

### Readiness and continuation

Research disposition: executed. Planning Readiness: Ready for the bounded
engineering slice, not operational or full issue acceptance. One complete
wider/deeper/contrarian cycle answered the implementation questions; further
internal searches would not produce missing owner/live evidence.
Explicit full-loop caller authority permits parent-owned transition to Plan.
No legal rule is added or activated. No specialist delegation was needed.
