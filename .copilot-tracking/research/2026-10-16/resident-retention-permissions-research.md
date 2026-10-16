---
title: Resident retention and field permissions research
description: Focused follow-up to issue 86
ms.date: 2026-10-16
---

## Brief

Task identity: issue-86-resident-retention-permissions. Focused convergence
research, owned inline by the RPI parent. Implement only in src; requested
documentation and tracking artifacts are explicit exceptions. No private input,
environment files, uv, history rewriting, or issue closure.

## Questions and opening state

* Where is first recorded resident contact persisted?
* Which server projections and mutation paths expose resident decisions?
* How can synthetic SqlStore evidence be obtained without reading existing data?

## Evidence

* W1: Owner clarification, retrieved 2026-10-16:
  https://github.com/jmservera/ama/issues/86#issuecomment-6209904857.
  Five years begins at first recorded contact, including withdrawn/expired records.
* W2: Owner matrix, retrieved 2026-10-16:
  https://github.com/jmservera/ama/issues/86#issuecomment-6209881675.
  Three staff groups record/view, managers view, contractors flags only,
  AI restricted to approved task needs.
* W3: Issue comments grant full control over resource group ama for this exercise.

## Participation and scope

Repository instructions and RPI skills selected. Inline investigation keeps
the coupled persistence/HTTP trace together. No independent research worker
needed. Owner decisions are authoritative exercise policy, not legal advice.
Existing Azure inventory contains a SQL server and billable application resources.
Prefer an isolated synthetic database over opening existing resident data.

## Cycle 1

Wider: traced core Store, SqlStore, projection, HTTP resident endpoint, existing
retention approval API, role tests and local application fixture.

Deeper:

* C1: src/core/src/zava_forward/core/resident_decisions.py:126 permits
  managers to mutate, while projection.py:126 suppresses coordinator evidence.
* C2: src/core/src/zava_forward/core/store.py:442 records contact timestamps;
  no first-contact marker or retention schedule exists. Imported contacts
  provide historical evidence; a decision date is not contact evidence.
* C3: src/core/src/zava_forward/core/doc_controls.py:240 offers manager-reviewed
  retention listing/deletion and legal holds. Reuse that boundary.
* C4: src/core/src/zava_forward/core/projection.py:78 contractor detail has no
  per-measure flag. Keep its other allow-listed operational fields unchanged.
* C5: src/core/src/zava_forward/core/ai_tasks.py:49 and store.py:_facts expose
  only selected labels, not authority/wishes/safe-route records. Retain this
  narrow task projection; never grant agents a human writer role.

Contrarian: do not infer first interaction from decision, stage, file load,
or the current date. Missing historical contact remains Unknown and prevents
deletion; do not pretend it meets retention evidence. Do not identify residents
by names/address. Existing schema lacks a universal resident identifier;
first-contact evidence belongs to the resident object in the case, and
cross-case identity reconciliation remains a documented limitation. Legal
holds must block deletion. Managers' read-only matrix must also cover the
legacy decision endpoint. Permission evidence is independent of the unrelated
configurable vulnerability-reason gate. No need for a broad new role taxonomy:
existing Liaison Officer represents Neighbourhood/Resident Engagement,
Coordinator represents Retrofit, manager/support roles view only.

## Selected approach

Calendar-year constant, earliest evidenced contact plus immutable marker on
contact recording; deterministic leap-day/withdrawn/expired tests. Expose
retention metadata, manager-reviewed purge through existing retention boundary,
and prevent expired decisions releasing work. Separate resident record/view
sets, registered-human writer binding, flag-only contractor projection.
Use isolated synthetic Azure database and delete resource group afterward,
as explicitly authorized. Existing resources are not evidence inputs.

## Readiness

Research disposition: executed. Planning Readiness: Ready.
One focused wider/deeper/contrarian cycle answered the bounded questions;
another cycle would repeat the same trace. No unresolved owner policy decision.
