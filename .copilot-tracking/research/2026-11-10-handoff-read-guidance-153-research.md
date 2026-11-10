---
title: Issue 153 pending-handoff read-failure guidance research
ms.date: 2026-11-10
task_id: 153-handoff-read-guidance-1110
---

## Status

Research record opened 2026-11-10 before investigation. Findings are appended
below as they are observed. Disposition and Planning Readiness are recorded at
the end of this file.

## Scope

Initial, previously unprovided guidance for the pending-handoff card read
failure (`pendingHandoffs` in `src/api/src/zava_forward/api/web/app.js`). Not a
repair of the reviewed staff-time work. Historical #153 correction balance is
UNKNOWN; no repair allowance or fresh five is claimed.

## Findings

### Lineage

* `git log --all -S"Could not load handoffs" -- src` returns only a2253a7c7 (#311), which introduced the raw message. No earlier failed, reviewed or candidate change for this path exists in this repository history or local branches. This is an initial change, not a repair. Historical correction balance stays UNKNOWN and no allowance is assumed.
* Admission screen (`demo-source-admissions-153-232-220-1110.md`) reached the gap by control flow only. This record adds the actual reproduction.

### Source (base 736561ba0, app.js unchanged since main 1ee56da3a per Root)

* `pendingHandoffs` (`app.js:751-765`) catches any `api("/api/handoffs")` rejection and renders `Could not load handoffs: ${e.message}` in a `role="alert"` paragraph.
* `api()` (`app.js:57-92`) gives `GENERIC_READ_ERROR` (reason, owner, next action) only after a non-OK response without `data.error`; a rejected `fetch` propagates the browser `TypeError`. `fetchReadRetrying` (`app.js:284-299`) never retries a rejection. A 401 sets `status` 401 and returns to sign-in. An aborted route read throws `AbortError`, which `pendingHandoffs` currently paints into a detached card.
* `priorityPanel` already ignores `AbortError` in its catch.
* Frozen #130 nomination hunk (~line 1062) is separate from lines 751-765 and is not touched.

### Baseline and reproduction (served, real app, Chromium, nonqueued `flock -n /tmp/ama-rpi-heavy.lock`, lock free; log `/tmp/zf-153-handoff-1110/logs/repro-before.log`, exit 0)

Synthetic `test_mvp.DATA`, JSON store, explicit loopback server, module origins asserted in this worktree (`src/api/src/.../server.py`, `src/core/src/.../store.py`).

| State | Observation |
| --- | --- |
| Success (actual backend projection of a Sent handoff) | Card visible, "Handoffs waiting for you", one row with owner, receivers and "Open to chase, escalate or withdraw."; one GET |
| Empty (actual backend `[]`) | Card present and hidden; no text; one GET |
| Rejected GET (explicitly constructed: page `fetch` wrapper rejects a `/api/handoffs` GET with a `TypeError` carrying a canary) | Visible text exactly `Could not load handoffs: Failed to fetch CANARY_TRANSPORT_7f3 TypeError at /srv/x.py`; no owner, no next action, raw technical canary shown; one GET |

Reproduced: the expected missing guidance exists. Unit baseline `test_handoff_api` plus `test_content_standard` (25 tests) passes at base (`baseline-unit.log`).

### Content and design requirements applied

* Content standard "Blocked and error messages": reason, owner, next action; generic error recovery distinguishes a failed read from an uncertain write; "adding a generic role name to every raw error would not establish real accountability", so only the existing "application support" owner is reused.
* Design system and WCAG baseline: existing `role="alert"` paragraph (status message 4.1.3) and text, not colour, are retained; no style or layout change.
* Web guidelines (fetched 2026-11-10): "Error messages include fix/next step, not just problem" applies; Title Case, curly quotes and ellipsis rules are overridden by repository ASCII/plain-language rules.

### Proposed scope

Surgical `app.js` change: a transport read failure (no HTTP status, not an abort) renders one constant with reason (could not load, so no claim that the queue is empty), owner (application support) and next action (refresh, then contact application support). HTTP errors keep their current rendering. An aborted read paints nothing. No new request, retry, mutation, contact or role.

## Disposition and Planning Readiness

Research disposition: executed. Planning Readiness: Ready. Out of scope and recorded only: HTTP error bodies without owner or action in this card, other panels' failure text, hosted CI.
