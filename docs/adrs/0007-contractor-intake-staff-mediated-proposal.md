---
title: ADR 0007 Contractor Job Pack and Evidence Intake Delivery (Proposed)
description: Proposed decision to deliver contractor job packs and field evidence as a staff-mediated intake rather than a provider portal, with the identity approach, a reported owner direction for the synthetic demonstrator only, and the owner decisions still needed (Refs #132)
author: AMA programme
ms.date: 2026-11-11
ms.topic: reference
---

## Status

Proposed. This ADR as a whole is not accepted, and a provider portal and the
provider identity model in #116 are not decided.

Current delta (2026-11-11): the owner's direction for the synthetic
demonstrator only is reported in
[Owner Direction Reported for the Synthetic Demonstrator](#owner-direction-reported-for-the-synthetic-demonstrator-2026-11-09-refs-132).
It is not formal acceptance of option A or of this ADR, not company Legal,
Compliance, DPO or identity-owner approval, and not production approval. This
record does not tick any criterion of issue #132.

Snapshot at 2026-11-04 (earlier text, kept as history): "Proposed on
2026-11-04. Not accepted. This record does not close criterion 6 of issue
#132: the owner has not decided, and the provider identity model in #116 is
open. It records the recommendation and the evidence so the owner can accept,
change or reject it in one step."

## Context

The bullets below are the 2026-11-04 snapshot. The current delta follows them.

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

Current delta (2026-11-11): the three snapshot statements "Not delivered", "the
owner has not decided" and "That answer has not been given" are historical.
The staff intake for the synthetic demonstrator is now delivered, and an owner
direction on the staff-only slice is reported on the issue. See the sections
below for exact scope and limits.

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

## Owner Direction Reported for the Synthetic Demonstrator (2026-11-09, Refs #132)

Status: owner direction reported for the synthetic demonstrator only. The
overall status of this ADR stays Proposed. This is not formal acceptance of
option A or of the ADR, and not company Legal, Compliance, DPO or
identity-owner approval.

Source: [issue 132 comment 6753054374](https://github.com/jmservera/ama/issues/132#issuecomment-6753054374),
created 2026-11-09T22:22:47Z by the repository owner's account, read afresh on
2026-11-11. Complete text:

```text
Owner decision2026-11-09: "Proceed with existing-staff-mediated synthetic demo intake". This authorizes separating an existing-authenticated-staff-only synthetic job-pack/evidence intake slice from the unresolved contractor identity dependency. Worker confirmation, receipt/acknowledgement and independent QA acceptance remain separate; no self-approval. Provider portal/contractor identity, new accounts/permissions, actual contract instructions, resident consent and live/production acceptance are NOT authorized. Beginning scoped RPI readiness/implementation preparation; no unsupported acceptance ticks or whole-issue closure. This supersedes the earlier missing staff-slice owner decision, not the remaining production identity gates.
```

Provenance: this is a relayed source. The comment is posted from the owner's
account and quotes the owner's words, but the original 2026-11-09 owner message
was not found in the repository or a bounded local history lookup, so this
record does not independently authenticate it. The comment does not adopt the
text of option A, so this record does not call it formal acceptance of option A.

What the direction covers: a staff-mediated route for the synthetic
demonstrator, where only existing authenticated staff act and a worker is a
named person in the record (`confirmed_by`), never a signed-in actor. Staff
identity authority is the unchanged, bounded owner decision in
[ADR 0002](./0002-pilot-readiness-architecture.md#entra-authoritative-staff-access-owner-decision-2026-10-24-refs-360)
(2026-10-24); the rest of ADR 0002 stays Proposed and its release gates stay
open. No new identity architecture is selected here.

Current implementation, as evidence and not as approval:

* `src/api/src/zava_forward/api/auth.py` offers `ZF_AUTH=password`, a
  development provider refused when `ZF_ENV=production`, and
  `ZF_AUTH=trusted-proxy` for platform Entra sign-in. Fixture logins and the
  `ZavaForward.Contractor` role label are not a contractor identity model and
  do not authenticate actual workers or actual staff.
* `src/core/src/zava_forward/core/staff_intake.py` refuses the Contractor role
  and records the worker as a named person. See the
  [core README](../../src/core/README.md#staff-mediated-field-evidence-intake-132-slice-3).
* Delivered, verified from merged pull requests on 2026-11-11: PR 1425 (capture,
  correction and acknowledgement for the synthetic staff-mediated intake), PR
  1432 (tests for inventory-held independent acceptance and handover, test
  only) and PR 1438 (keyboard-probe declaration repair for the staff intake
  screen, test only). Accessibility acceptance and live acceptance are not
  established.
* Still undelivered: an escalation write path. The named variation and
  escalation owner is unknown; the intake shows "Unknown - not configured".
  That is the separate, unmet criterion of issue #132.

Not authorized and not decided here: provider portal, contractor identity or
B2B guest model (#116), new accounts or permissions, public access, provider
send, contract instruction, resident consent, and live or production
acceptance. Option B stays a production decision with its deferral and the
owner of #116 not confirmed. The PRD (`in-review`, unsigned) keeps the
exclusion in its [Profile Journey Contract](../prds/zava-forward-retrofit-programme-demonstrator.md).

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

Snapshot at 2026-11-04 (kept as history):

* Accept, change or reject option A, recorded with date and name.
* Authorise the existing-authenticated-staff-only slice for persistence and
  write routes without waiting for #116 (the waiver asked for on #132).
* Confirm option B is deferred and who owns the #116 identity decision.

Current delta (2026-11-11):

* Owner direction reported for the synthetic demonstrator only: the
  staff-mediated route and the existing-authenticated-staff-only slice, per the
  comment quoted above. Formal acceptance of option A or of this ADR is not
  recorded.
* Still open and unknown: confirmation that option B is deferred for
  production and who owns the #116 identity decision; real worker identity,
  lawful basis and any Legal, Compliance, DPO or identity-owner approval; the
  named variation and escalation owner (a separate criterion of issue #132).

## Next stacked slices once accepted

Snapshot at 2026-11-04 (kept as history; the first bullet is partly delivered,
see the current delta):

* Persistence and staff write routes for receipts, acknowledgement and
  escalations, wired to independent quality acceptance (criteria 2 to 5). This
  touches the store and its SQL variant, so it needs the complete local gate.
* Staff screen with manual path, accessibility and plain-language proof
  (criterion 1 complete).

Current delta (2026-11-11): capture, correction and acknowledgement with the
staff screen are delivered for the synthetic demonstrator (PR 1425, with PR
1432 and PR 1438 as test follow-ups). The escalation write path and a named
escalation owner remain undelivered, and accessibility and live acceptance
remain unproven.
