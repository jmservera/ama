---
title: ADR 0007 Contractor Job Pack and Evidence Intake Delivery (Proposed)
description: Proposed decision to deliver contractor job packs and field evidence as a staff-mediated intake rather than a provider portal, with the identity approach and the owner decisions still needed (Refs #132)
author: AMA programme
ms.date: 2026-11-04
ms.topic: reference
---

## Status

Proposed on 2026-11-04. Not accepted. This record does not close criterion 6 of
issue #132: the owner has not decided, and the provider identity model in #116
is open. It records the recommendation and the evidence so the owner can accept,
change or reject it in one step.

## Context

* The PRD states there is no provider portal and no provider identity claim
  (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`, Profile Journey
  Contract, Provider / contractor contact; non-goal at the portal exclusion).
* Delivered so far, all read-only or pure and merged: PR #873 (core rules in
  `job_pack.py`: allow-listed pack, worker-confirmed receipts, acknowledgement
  separate from independent review, offline merge, no-show recovery, escalations
  that are never contract instructions) and PR #1080 (staff-only
  `GET /api/workorders/{id}/job-pack`, contractors get 403).
* Not delivered: persistence, write routes, a staff screen, accessibility proof.
* The #132 readiness comment asks the owner whether to separate an
  existing-authenticated-staff-only slice from the live contractor identity
  dependency. That answer has not been given.

## Options

| Option | Effect | Cost and risk |
| --- | --- | --- |
| A. Staff-mediated intake (recommended) | A signed-in staff member carries the pack to the worker and keys in the worker's confirmed notes; the worker's name and confirmation are recorded. No contractor account. | Staff effort per job; needs a manual paper or phone path; no new identity surface. |
| B. Provider portal with B2B guest identity | Workers sign in and submit directly. | Contradicts the PRD exclusion; needs the #116 contractor guest model, invitation, lifecycle and conditional access; new security and privacy surface. |
| C. Defer both | Keep read-only pack only. | Criteria 2 to 5 stay unmet. |

## Proposed decision

Choose option A for the demonstrator. Identity approach: only existing
authenticated staff act in the system. A contractor is a named person in a
record (`confirmed_by`), never a signed-in actor, so a worker's confirmation is
a staff-recorded statement and not an identity claim. Option B stays a later
owner decision tied to #116.

## Boundaries that stay in force

* The pack never carries health or vulnerability reasons (PR-002); resident
  consent and choice are unchanged by a provider no-show or cancellation.
* Submission and acknowledgement never accept work. Independent review is by
  someone who did not do, key in or acknowledge the work (no self-approval).
* An escalation or variation goes to a named contract manager or the building
  safety liaison and is never a contract instruction.
* Any AI help stays optional; every step has a manual path and works when AI is
  unavailable. Screens follow the Fluent 2 design system, the WCAG baseline and
  the plain-language content standard.

## Owner decisions needed

* Accept, change or reject option A, recorded with date and name.
* Authorise the existing-authenticated-staff-only slice for persistence and
  write routes without waiting for #116 (the waiver asked for on #132).
* Confirm option B is deferred and who owns the #116 identity decision.

## Next stacked slices once accepted

* Persistence and staff write routes for receipts, acknowledgement and
  escalations, wired to independent quality acceptance (criteria 2 to 5). This
  touches the store and its SQL variant, so it needs the complete local gate.
* Staff screen with manual path, accessibility and plain-language proof
  (criterion 1 complete).
