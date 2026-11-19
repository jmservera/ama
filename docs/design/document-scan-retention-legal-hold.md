---
title: Document scanning, retention and legal hold design
description: Design for scan-before-availability, retention listing and approval, and legal hold on the Blob document store, separating what is built from what is proposed
author: AMA programme
ms.date: 2026-11-17
ms.topic: reference
---

Refs #117. Source decisions: [ADR 0002](../adrs/0002-pilot-readiness-architecture.md) decision 2 and its open items, and PRD requirement DH-003 in the [demonstrator PRD](../prds/zava-forward-retrofit-programme-demonstrator.md). This is a design document only. It changes no source or infrastructure, creates no live resource, and grants no approval. Retention periods, hold authority and the activation of Defender for Storage remain decisions for the named owners.

Labels used below: Built means present in `src/core/src/zava_forward/core/doc_controls.py` or `infra/` at the base commit. Proposed means a design choice for owner review.

## Scope and constraints

* Demo first, desktop only, synthetic data only.
* Retention periods stay the synthetic-demo placeholders until the DPO and Legal approve a schedule (PR-003).
* Legal hold authority sits with the Legal delegate. The system records a hold; it does not decide one.
* Out of scope: chat grounding and the SQL store implementation, which other issues own.

## Scan before availability

### Built

* A document is readable, downloadable or sent to the document-reading assistant only when its scan status is `clean`. Generated documents are exempt.
* Statuses are `clean`, `infected`, `mismatch` and `pending`. `infected` and `mismatch` delete the blob and never create a record. `pending` is unavailable.
* `ZF_SCANNER=local` (default) uses a labelled synthetic signature scanner that gives no malware assurance. `ZF_SCANNER=defender` reads the blob index tag `Malware Scanning scan result`: `No threats found` is clean, `Malicious` is infected, anything else is pending.
* `rescan_pending` is a job entry point that rechecks missing or pending documents and returns counts. Nothing schedules it.
* A local scanner guarding an Azure Blob store logs a warning.

### Proposed

* Fail closed everywhere: any tag read error, missing tag or unknown value stays `pending`.
* Add a pending age limit (proposed 24 hours). A document pending past the limit is reported to the operations owner and stays unavailable; it is never promoted automatically.
* Schedule `rescan_pending` at a short interval (proposed 5 minutes) from a single hosted worker, with the existing bounded and non-deleting behaviour, and alert on a non-zero pending count older than the limit.
* Treat Defender tag writes as a trust boundary: only the Defender service principal may write that tag, and the application identity needs tag read only. Verify this before relying on the tag.
* Acceptance evidence for the real criterion: a Defender-enabled storage account in a non-production subscription, the EICAR test file reaching `infected`, a clean file reaching `clean`, and the document staying unavailable in between. Nothing in this repository has run against a real account.

### Owner decisions

* Service and security owner: enable Defender for Storage on the account (`infra/governance.bicep` keeps Defender plans off by default) and accept its cost.
* Operations owner: cadence, alert route and the pending age limit.

## Retention

### Built

* The retention trigger is the case closing date or an explicit `retention_trigger`, never the upload date. A case with neither has no due documents.
* Placeholder periods in years: EPC 6, Survey 6, Design 6, Consent 3, Funding evidence 7, Photo 3, Other 1. Resident decision records follow a separate schedule.
* `retention_due` lists records past their period and deletes nothing. It is limited to the Retrofit Programme Manager role and is audited by count only.
* `approve_retention_deletion` removes one due document after a named manager approves it. The audit entry holds the identifier, kind and approver, never the file name or content. The record is removed and saved before the blob is deleted.
* Blob versioning is on and soft delete is set to 30 days (`infra/modules/storage.bicep`).

### Proposed

* Treat the approved deletion as logical until storage is purged. Blob soft delete and versions mean bytes remain recoverable for up to 30 days and longer where old versions exist. The design needs one of: delete versions as part of the approved deletion, or a lifecycle rule that expires non-current versions on a period the DPO accepts. Record the chosen period in the retention schedule.
* Add a deletion receipt per approval: identifier, kind, approver, approval date, and the date the last recoverable copy expires.
* Keep the job list-only. Deletion stays a human action per record; a batch approval is not proposed.
* Segregate duties where staffing allows: the approver of a deletion should not be the person who placed or released a hold on the same case.

### Owner decisions

* DPO and Legal: approved periods per record class and the trigger for each (PR-003).
* Record owners: who may approve deletion for each class.
* DPO: acceptable residual period for soft-deleted and versioned copies.

## Legal hold

### Built

* A hold is held on the case, with a short reference restricted to letters, numbers and simple punctuation so it cannot carry case details.
* An active hold blocks retention approval for every document on the case and for resident decision records, and the blocked attempt is audited.
* Placing and releasing a hold is limited to the programme manager role and is audited. The record carries a label stating that a real hold needs the Legal delegate's decision.

### Proposed

* Keep the hold at case level for the demonstrator. A per-document hold is not needed for any current acceptance criterion.
* Require a Legal delegate identity for release in any non-demo use. The retention list already shows a held record as `blocked: legal hold`.

### Owner decisions

* Legal: who may request, place and release a hold, and the evidence they must leave.

## State summary

| Behaviour | Status |
| --- | --- |
| Only clean documents are available | Built, tested with the synthetic scanner and a fake transport |
| Real malware scanning | Open: Defender not enabled, no real account run |
| Scheduled rescan and pending alerting | Proposed |
| Retention list, owner-approved deletion, no content in the log | Built with placeholder periods |
| Purge of soft-deleted and versioned copies | Proposed, needs DPO decision |
| Case-level legal hold blocks deletion | Built |
| Real hold authority and approved retention schedule | Open: human decisions |

## Evidence boundary

The acceptance criterion "Uploads are scanned before availability" stays unmet for real scanning until the Defender activation and the account evidence above exist. This document does not prove it.
