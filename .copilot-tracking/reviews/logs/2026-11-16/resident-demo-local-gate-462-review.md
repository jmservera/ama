---
title: "Review: resident-demo-local-gate-462"
description: "Single independent review of the Issue #462 local candidate"
ms.date: 2026-11-16
---

## Execution and outcome

* Execution: Complete, single pass, by an independent read-only reviewing agent (rubber-duck) that was not the author, over base `5e0c7f74432ffce73cfeaa672e4e40a605ca6274` plus the uncommitted candidate (threat model, README link, index row, log entry, RPI evidence). It verified each T1 to T10 control claim against code. It did not rerun tests and inspected no Azure state.
* Outcome: Findings (0 Critical, 1 High, 4 Medium, 1 Low). All six are documentation accuracy findings in the new threat model; none is a code defect. Every finding was verified against code before correction (SQL view, `app.py` handler lines, limiter, codec).
* Assessed boundary: `5e0c7f744..` working tree before the candidate commit.

## Findings and routing

| ID | Severity | Finding | Disposition |
|----|----------|---------|-------------|
| R-001 | High | T7 implied a synthetic filter on case rows; the view filters only sensor rows by `source_type = 'SYNTHETIC'` | Corrected in the threat model: case provenance rests on the allowlist and operator verification; free-text fields could carry sensitive content |
| R-002 | Medium | T2 omitted that a shared-password holder can distinguish listed from unlisted emails | Corrected |
| R-003 | Medium | T3 omitted in-memory counters, concurrent overshoot and missing `Retry-After` on 429; scrypt N is configurable | Corrected |
| R-004 | Medium | T5 said only key rotation revokes tokens; logout and restart also do; Origin check compares authority to Host | Corrected |
| R-005 | Medium | T10 omitted the optional local SQLite agenda (bookings and cancellations) and chat log | Corrected |
| R-006 | Low | T1 said only ASCII input; the normalised email must match ASCII, so Unicode case folding can map into it | Corrected |

Corrections were applied directly after the review. They are tightly coupled factual fixes to this candidate's own documents; no second review ran, per the one-pass rule. The prospective research keeps its original rows with an errata note.

## Conformance notes

* The threat model claims no security acceptance, deployment authority or DPO approval.
* No source, workflow, dependency, Dockerfile or infrastructure file changed; the FULL tier is applied because of the issue's explicit requirements.
* Unmet and unclaimed: Azure spend record, deployment and live acceptance; hosted checks; coordinator assessment; human accessibility, copy and Legal or DPO review; whether the historical #444/#455 rubric failure counts as resolved.

## Routed follow-ups

1. Operator-owned: verify the live SQL view and the resident principal's grants before any rollout (T7, T8).
2. Later hardening candidate, not a demo blocker: make the limiter atomic and add `Retry-After` to the login 429 (R-003).
3. Owner pre-spend approval, then the cloud criteria.
