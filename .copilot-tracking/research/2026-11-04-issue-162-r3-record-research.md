---
title: Issue 162 third record research
ms.date: 2026-11-04
---

Research disposition: executed (delta check). Planning Readiness: Ready.

## Delivered evidence (merged PRs)

* #286: criteria 1 to 5 (server-side owner keying, role matrix extension, projection reuse, owner-only prompts, injection test set).
* #650: break-glass refusals audited with purpose; OD-46 options proposed.
* #879: demo-only break-glass disclaimer on the response and every audit entry.
* #711, #842: earlier dated verification records.

## Delta

* `origin/main` is at 281d4b0e8. No code or policy change touches chat isolation since #842.
* Owner decision 2026-11-02: keep open until DPO and Legal decide OD-46. No decision is recorded in the repository.
* Focused evidence run on this head: `test_chat_isolation` in src/api, 32 tests, OK.

## Unmet

* Criterion 6, policy decided: human decision (owner with DPO and Legal). The demo-only note is not a DPO or Legal decision.

## Slice choice

No source slice is justified. Docs-only record PR; no knowledge-base file changed.
