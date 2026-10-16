---
title: Resident retention restart phase details
ms.date: 2026-10-16
---

## Metadata

Task ID: issue-86-retention-restart. Slug: retention-restart-86.
Plan: .copilot-tracking/plans/2026-10-16/retention-restart-86-plan.md.
Evidence: .copilot-tracking/research/2026-10-16/retention-restart-86-research.md.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Implement and validate restart | Completed; review-ready | P01-T01, P01-T02, P01-T03 |

<!-- rpi:phase id=P01 -->
## P01: Implement and validate restart

The latest owner rule resolves the only product decision in this slice.
Use the common first_contact/remember_first_contact path, not backend-specific
logic. Preserve existing consent, review, permission and deletion controls.
No unresolved blockers. No Azure or Docker work.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reset the contact evidence boundary

Deletion clears resident.first_contact_at and saves only an integer general
contact offset as tombstone metadata beside resident_retention_deleted_at.
first_contact skips that retained prefix; safe-contact history is removed on
deletion and later fresh entries remain eligible. Dates must still be valid,
nonfuture and not before deletion. Old date-only deletion records require
conservative general-contact date filtering and disregard stale cached markers.
Later contacts retain the earliest new start. Multiple approved deletions replace
the boundary. Do not copy contacts or resident fields into a tombstone.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Replace pinning coverage and validate

Canonical target: src/core/tests/test_resident_decisions.py, JSON class inherited
by SQLite. Remove the single owner-rule pinning method named in the plan.
Add at most five methods; no generated tests. Include:

* Reopen after deletion, Unknown origin/due and no implicit revived consent.
* New same-day general contact and fresh safe-contact route; earliest new date
  persists, later contact/decision cannot extend it.
  Exercise each route independently from Unknown, with an old same-day general
  contact at the identical timestamp. Verify no consent revival before a fresh
  scope and Accepted decision; reopen to verify the persisted new period.
* Expiry at the new anniversary, refusal before deletion, second deletion and
  renewal after it. Preserve leap-year logic.
* Old retained contacts, invalid/future dates and legacy date-only tombstones
  cannot pin a new period. Tombstone exact metadata keys/types, no canary content.
  Legacy coverage must include positive recovery from a later-day new contact.
* Existing deletion tests retain complaint/contact records and audit integrity.

Run targeted resident tests, then full core suite and resident API tests with
installed packages; Ruff check/format and mypy in core. Install dev dependencies
only after missing-tool failures, using pip in a venv. Mutation loads the complete
original resident_decisions module from HEAD in a fresh Python process before
Store/tests imports, so helper globals and Store's directly imported alias all
use original behavior. Require semantic assertion failures in the selected new
tests for JSON/SQLite, not import/setup errors. Rerun installed changed code
green afterwards; do not mutate package files. TemporaryDirectory fixtures
clean themselves; isolated pip venv lives in the session workspace.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Document and prepare publication

Depends on P01-T01/P01-T02 for completed claims. Replace README known limit
with the approved rule and explain same-day boundary/legacy conservatism.
Update existing knowledge-base routing row and append dated log entry.
Record validation scope/skips and one post-implementation Review. No issue
acceptance claim; no merge. Authenticate gh identity, use repository-local
noreply email for author/committer and required Copilot trailer. Push existing
topic branch normally and open PR to main with Refs #86 only.
Documentation and validation evidence are complete; publication is explicitly a
post-Review handoff rather than a prerequisite of the Review it depends on.

## Completion evidence

All P01 tasks complete. Full core suite: 482 tests, one explicit isolated Azure
opt-in skip. Targeted resident API: 3 passed. Core Ruff check/format and mypy
passed. Original full-module mutation: all 10 new JSON/SQLite tests failed
semantic assertions, no errors/skips; subsequent changed-code run: 40 resident
tests, one opt-in skip, all executed cases passed. No package files mutated.
Existing behavior records direct resident answers even after expiry but holds
release; the repeated-expiry test correctly checks require_resident_clear
instead of inventing a new decision-recording restriction.
