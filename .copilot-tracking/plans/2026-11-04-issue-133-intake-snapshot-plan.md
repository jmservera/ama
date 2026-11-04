---
title: Plan, issue 133 intake form and snapshot
ms.date: 2026-11-04
---
## Plan

* [x] Phase 1: `intake_form`, `intake_errors`, `to_state`, `from_state` in `aftercare.py`.
* [x] Phase 2: `IntakeFormTests`, `SnapshotTests`; focused tests, ruff, mypy.
* [x] Phase 3: README paragraph and log entry.

Details: [details](../details/2026-11-04-issue-133-intake-snapshot-details.md).

## Critique (one pass)

Executed once. Verdict: proceed. Applied directly: form text passes `neutral_text`; the form has a non-digital channel list and no sensor wording; restore refuses sensor-dismissed concerns, non-human outcome bases and orphan packs so a store cannot weaken a concern; no SQL, API, auth or deployment change, so the focused tier applies. Use Refs #133.
