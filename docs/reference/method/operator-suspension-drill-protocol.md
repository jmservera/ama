---
title: Operator Suspension and Manual Fallback Drill Protocol
description: Witnessed drill steps and blank record for restart authority and fallback evidence (Refs #221)
ms.date: 2026-11-03
ms.topic: reference
---

## Purpose and Status

This is a protocol and blank record only. No drill has been run, no restart
authority has been appointed and no corrective test has been accepted. The
constructed tests in `src/api/tests/test_operator_suspension.py` prove the
mechanism with fixture actors; they do not satisfy the human parts of
PRD AC-072 and NFR-014 or BRD RULE-024 and RULE-020 (OD-35).

## Preconditions

* A named restart authority under OD-35 and RULE-020 is appointed by the
  Building Safety lead and the sponsor with the digital owner. Record the
  appointment elsewhere and cite it; do not infer it from this page.
* The drill uses synthetic data and a synthetic incident only.
* Manual case work and emergency and statutory hazard response stay open for
  the whole drill. If either is blocked, stop the drill and record it as a
  failure.
* If the AI task or its service is unavailable, the drill proceeds on the
  manual path; AI availability is not a precondition.

## Steps

1. Seed a synthetic critical incident or threshold breach for one AI task.
2. A different authorised operator suspends the affected task.
3. Check that new dispatch and reliance on pending or ready proposals are
   blocked, and that a manual case and a hazard response can still be started.
4. Check the incident record names the impacted version set, scope, owner,
   evidence, containment, resident impact, remediation and restart authority.
5. Attempt restart before corrective tests exist. It must be denied.
6. Record corrective tests, accepted by a competent human reviewer.
7. A distinct authorised human, not the proposer or the operator who
   suspended, approves restart. A second attempt by the proposer must fail.
8. Confirm the affected scope stays paused until step 7 completes.

## Blank Drill Record

| Field | Entry |
| --- | --- |
| Drill date and synthetic scenario | |
| Appointed restart authority and appointment reference | |
| Operator who suspended | |
| Witness (programme and safety professional) | |
| Manual case work stayed available (yes or no, evidence) | |
| Hazard response stayed available (yes or no, evidence) |  |
| Restart denied before corrective tests (yes or no, evidence) | |
| Corrective tests accepted by (name, date) | |
| Distinct restart approver (name, date) | |
| Defects or follow-up actions | |

A completed record is evidence for #221 criteria 5 and 6 only when each field
is filled by the named people. An agent must not complete it.
