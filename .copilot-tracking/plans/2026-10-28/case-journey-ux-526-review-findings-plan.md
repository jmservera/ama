---
title: Case journey 526 routed findings implementation
description: Later invocation implementing original Review findings without repeating Review
ms.date: 2026-10-28
---

## Authority and boundary

User explicitly requests fixes to independent review defects and publication.
Research/design and original critique remain reused, not repeated. The original
Complete / Defects found review is immutable evidence. This later invocation
preserves requirements and needs no new planning decision or research.

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate RV-001..004

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Restore local journey import parity and receipt command contract

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Clear only explicitly submitted fields, preserve async review drafts by ID/revision, recount document outputs

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Targeted regressions and admitted real-browser validation

<!-- rpi:phase id=P02 -->
### [ ] P02: Commit and publish

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Commit original evidence and corrections with safe identity

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Full clean candidate gate, current-main receipt verification and independent exact-head assessment

<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Non-force topic push and gh pr create with Refs #526

Write boundary: relevant web helpers/panels/checks, runner and regression tests,
related documentation and new continuation artifacts only. Validation uses
constructed local data; heavy work owns the bounded shared lock only while
executing. No Azure, secrets, .env, private records, relaxed gates or fabricated
acceptance. Preserve previous failed logs. Screen-reader/staff/live acceptance
remain owner work. No second original Review is required by this later invocation.

## Current evidence

P01 complete: journey-10 passes 37 axe states, keyboard and actual 200% zoom,
same-card failed/successful action preservation and real constructed document
upload/read/review counts. assistants passes 27 scenarios including delayed
same-revision restoration and changed-revision recovery. Focused API 24 tests
and runner 31 tests pass, with existing Ruff/format/mypy. Full candidate gate
and exact-head publication assessment remain mandatory P02 work.

Implementation/evidence commit: 7bfaaf87c2efbffeab514fff0a1edb2744d7955c.
Both author and committer use the authenticated GitHub noreply identity.
This plan reconciliation is committed before the final gate. Post-commit
gate/publication progress stays in the external authoritative state:
/home/azureuser/.copilot/session-state/6bcc4a04-4f23-4381-a2b9-4c4dd0f4bb2e/files/publication-526-state.json.
No tracked receipt or retrospective success commit can invalidate the final gate.
