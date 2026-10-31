---
title: Resident AI activation 563b plan
description: Apply the accounting ledger privately, enable resident AI, prove it live, Refs #563
ms.date: 2026-10-31
---

## Plan

* [x] P1 Back up the resident app configuration (private, outside Git).
* [x] P2 Enable the two assistant variables on a new single-mode revision; min0/max1 unchanged.
* [x] P3 Live attempt 1 (diagnostic, one sign-in): named the stage, accounting unavailable.
* [x] P4 Apply infra/sql/resident-assistant.sql idempotently via a one-off start of job-cutover-test-init (same image and identity, env restated, job template unchanged, job stays Manual).
* [x] P5 Live attempts with consent: "My home smells like a dead rat" and "How's my case going" (second sign-in).
* [x] P6 Verify invariants; keep AI enabled only because genuine AI answers were observed; otherwise roll back to AI off.
* [x] P7 Record evidence, README note, PR with Refs or Closes by proof.

## Critique (single, final candidate)

Execution Complete, verdict Pass. Compatible findings applied: restate the container env for the job override (a first run lost its env and failed before any SQL connection, no effect); read-only probe before any write; never reset ledger tables; apply only when the principal SID matches the resident identity. No conflict with owner decisions.

## Limits kept

Min replicas 0, all 8 jobs Manual, RG ama untouched, no new endpoints, public access or RBAC, employee estate untouched, USD20 cap and five per hour per resident limit and 2026-11-01T00:00Z expiry in force, at most two sign-ins.
