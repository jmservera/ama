---
title: Resident retention restart evidence
ms.date: 2026-10-16
---

## Task and disposition

Task ID: issue-86-retention-restart. Slug: retention-restart-86.
Research disposition: reused. Planning Readiness: Ready.

* `gh issue view 86 --comments` was the first command. The latest retention
  decision requires five years from the first contact recorded after deletion.
  Earlier one-month, decision-date and permanently expired rules are superseded.
* ADR 0006 places the implementation at
  src/core/src/zava_forward/core/resident_decisions.py, not src/core/resident_decisions.py.
* first_contact currently scans all general contacts plus the cached marker and
  safe-contact history. Deletion removes scoped payload but preserves general
  contacts and the original marker, permanently pinning expiry.
* Store.log_call appends general contacts then calls remember_first_contact;
  safe_contact_record appends a separate history then calls the same helper.
  Both must restart the same clock, including contact later on deletion day.
* Existing JsonResidentDecisions tests are inherited by SqlResidentDecisions.
  Both reopen persisted stores. The Azure test is opt-in and will not be run.
* The clean topic branch feat/retention-restart-after-deletion-86 has no prior
  PR and equals fetched origin/main. Reuse it for this independent slice.
* General contacts and complaint outcomes have separate purposes. This change
  must not delete them or claim historical SQL/ledger/backups are erased.
* No private dataset, environment file, Docker or Azure access is required.

## Design evidence

General contacts are append-only in the application. A deletion tombstone can
retain only their count, alongside the existing deletion date, to distinguish
pre-deletion entries from later entries even within the same minute/day.
Clear the cached first-contact marker on deletion. Ignore the retained contact
prefix when establishing the new origin; keep the first later contact pinned
until another approved deletion. For previously persisted date-only deletions,
exclude contacts on/before that date conservatively because same-day ordering
cannot be recovered. Fresh safe-contact history is already post-deletion.

## Boundaries

No retention-policy change before deletion, consent inference, automatic purge,
permission change, SQL syntax/schema change or operational acceptance claim.
Issue #86 retains independent human and live-platform acceptance work.
