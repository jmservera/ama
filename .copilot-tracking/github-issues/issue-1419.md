---
title: Demo read-only CSV copy of unaccepted handoffs
description: Created child issue of #80 for a synthetic read-only CSV copy of the unaccepted-handoff ageing queue
ms.date: 2026-11-10
ms.topic: reference
---

## Created Issue

* Issue: #1419, https://github.com/jmservera/ama/issues/1419
* Created: 2026-11-10T20:25:18Z, state OPEN when observed (read-only `gh api` GET at 2026-11-10, this session).
* Title: Demo: read-only CSV copy of unaccepted handoffs
* Template: generic; `.github/ISSUE_TEMPLATE` is absent.
* Labels: none. Assignees: none. Organisation issue type: none. Milestone: none.
* Hierarchy: actual sub-issue of #80, which is under #73 (observed parent URL `https://api.github.com/repos/jmservera/ama/issues/80`).
* Refs #83 for the existing ageing projection only. It is a source boundary, not a blocking dependency on human-approved BG-010 / OD-09 thresholds.
* Source of record for the full body and metadata: coordinator-held `issue-unaccepted-handoff-created-2222.json` and `issue-unaccepted-handoff-export-2221.md` (outside this worktree, not copied here).

## Scope as Created

* One synthetic-demo, read-only CSV copy of the existing `GET /api/handoffs/unaccepted` contract, distinct from pending handoffs and the Capacity downloads.
* Initial admission is research and plan only. Implementation waits for explicit coordinator admission and parent ancestry and owned-hunk reconciliation.
* Operational export purpose, retention, actual-record use and approved escalation thresholds are not approved. This issue neither supplies nor waives them.
* Expected eventual ownership: narrow `server.py` CSV dispatch, parser and registry; list-export tests; and only the handoff-panel affordance in `app.js`. No Capacity `ops.js` or `capacity_browser_check.py` edits, no retry or session helpers, no core role, workflow or serializer change.

## Conditional Acceptance Criteria (from the body; not authorization)

* Proposed `/api/handoffs/unaccepted.csv` reuses the `handoffs` authorization and exact unaccepted projection.
* Optional `max_age_hours` parsing matches JSON, with matching 400 errors and no new selector, pagination or default threshold.
* Controlled-clock tests compare every CSV field, row and order to JSON, covering states, reasons, nulls, booleans, empty results and CSV edge cases.
* A truthful, separately labelled handoff-panel download uses the exact route and does not claim a rendered queue.
* Success, denied and invalid reads leave all state unchanged.
* Registry expectations and focused synthetic regression checks pass on a frozen candidate, with independent exact-head review and hosted checks before publication.
* Dated research, plan, details, critique, changes and review evidence document admitted scope and results.

## Boundaries of this Record

* Only the issue's own tracking record. No push, pull request, label, assignee, comment or board write was made by this session.
* Whole #80 and #73 acceptance stay open.
