---
title: Source change monitoring research
description: Bounded offline evidence for issue 213
ms.date: 2026-10-16
---

## Brief and controls

Implement #213 on the clean existing topic branch
`feat/src-regulatory-change-review-213`, based on merged #210/#211/#212
(HEAD 0f9ba37). Executable writes stay in src/. Documentation and requested
RPI artifacts are permitted exceptions. No private data, environment files,
network scraping, deployment or invented human approvals.
Focused internal research; convergence output. Interaction is unavailable;
the user supplied the owner and offline boundary explicitly.

## Extensions and participation

Repository instructions, ADR 0005 and ADR 0006 selected. RPI phase skills
coordinate evidence. No research delegation: this is one continuous trace.
No external legal research: this change makes no currentness or legal claims.

## Cycle 1

### Wider

* C1 `src/core/src/zava_forward/core/lawstore.py:274`: append-only source
  versions, snapshots and provision index already exist.
* C2 `src/core/src/zava_forward/core/rulecards.py:317`: source changes already
  create per-card review records. #127 is delivered but does not fetch,
  schedule, validate provenance or execute regression tests.
* C3 `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1`:
  orchestrator entry point prints a version; existing scheduled jobs are token
  maintenance and ledger verification, not regulatory monitoring.

### Deeper

* C4 `src/core/src/zava_forward/core/rulecards.py:241`: activate previously
  did not enforce the effective date or a source-review regression gate.
* C5 `src/core/src/zava_forward/core/rule_engine.py:214`: execution requires
  exact reviewed, complete, current source provisions. Candidate discovery
  must not enter the current searchable source set.
* C6 `docs/reference/regulatory/README.md:56`: likelihood and cadence vary by
  source and topic; prose is not a safe machine interval. Require explicit
  High/Medium/Low and positive per-source day interval, retaining the register
  rationale in configuration.

### Contrarian

Appending discovery immediately to reg_version would make latest-version
retrieval select unverified content and invalidate current engine citations.
Reject this alternative. Store candidates separately, content addressed, with
baseline version/hash and immutable provenance. Source publication into the
law store remains a separate verified-ingestion boundary; no candidate is
silently promoted to law. Regression plans must be bound to immutable target
cards, cover their impacted test IDs, and run only after owner assessment.
Detection cannot guess new legal text, approvers, communications or clock rules.

## Synthesis and readiness

Research disposition: executed. Planning Readiness: Ready for the bounded
offline slice. Use existing SQL adapters and rule-card transactions, separate
candidate/change and event tables, explicit source configuration, injected
local observations and deterministic regression fixtures. Reuse existing
per-card source reviews and owner assessment. Add no HTTP endpoints.
Juan Manuel Servera is the exercise Legal, Compliance and DPO owner; all
fixture approvals remain simulated. Live feeds, hosted scheduling, verified
source promotion, staff notification and operational acceptance remain unmet.
No further research cycle is warranted: the named code paths cover the scope.
