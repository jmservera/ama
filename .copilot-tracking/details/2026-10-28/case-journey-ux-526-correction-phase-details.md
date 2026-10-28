---
title: Case journey unsaved-edit correction details
description: Task-level completion evidence and implementation boundaries
ms.date: 2026-10-28
---

## P01

### P01-T01

C1: session retains document output node only, not upload form. aiNotes snapshots
submitted replacement before await and displays it read-only after success.
Test document text/reason after call and proposal refresh; submit Edit and check
read-only replacement and recorded review state.

### P01-T02

C3/C5: merge live proposal captures with unresolved session snapshots. Restored
live controls own their current values, clean controls remove older snapshots,
and explicit recovery discard removes its saved keys. A disconnected loader
must neither restore nor erase the active session cache. Verify clears only
actually submitted metadata; preserve JSON for previous-revision recovery.
Test overlapping delayed assistant loaders and own verification.

### P01-T03

C2: reuse refresh's before/after comparison. Let callers pass immutable snapshots
captured before mutation; recorded form must not clear its unsaved flag when
later edits differ. Upload must capture document kind before FileReader too.
Test held upload/handoff/resident responses and assert request body differs from
later retained dirty values. Include failure path and file-input handling.

### P01-T04

C4: after checklists resolve, restore selected measure first, paint the matching
version and restore versioned evidence. Avoid repaint discarding evidence during
same-case refresh; failure must be explicit. Preserve different-measure/version
drafts separately rather than applying stale evidence.
Funding: key draft by record_id (manual initial identity if absent); older
edits remain read-only/copyable with identity, no stale review actions. Test
new AI text vs prior dirty text through further refresh and explicit discard.

## P02

P01-T01 through P01-T04 completed with browser evidence in the changes artifact.
P02-T01 completed with static/types, API units and locked Chromium/axe.
Original independent Review is Complete / Not accepted, with RV-001/RV-002
routed to the distinct checklist-findings later implementation. Its local
repairs/tests are recorded separately and do not change that verdict.
P02-T02 local commit remains; P02-T03 is blocked.
Shared snapshot/cache helpers also retain changed file inputs and copyable later
edits when a successful handoff removes its form. This is tightly coupled
completion of P01-T03, not a new feature or scope expansion.

### P02-T01

Run node syntax checks on changed JS, relevant existing API semantic/design/
content tests and full API discovery where available. Use installed .venv;
missing-dependency failure permits restoring declared packages. Run Ruff check
and format on changed Python at 100 columns. Under bounded nonblocking flock,
execute existing journey and assistant checks with synthetic data only. Pinned
axe 4.10.3, actual Chromium, preserve stepper assertions.

### P02-T02

Independent fresh reviewer activates rpi-review, writes only its review artifact
and reports confidence-backed defects with scope and outcome. Required human
checkboxes stay unchecked. Original outcome preserved; new findings route to
later work rather than repeated Review.

### P02-T03

Resolve gh authenticated id/login, set local noreply author/committer identity;
commit code and dated evidence with required trailer. Fetch upstream before
publication. Complete repository-required publication checks without invoking
az; if this conflicts, record the exact blocker rather than fake a receipt.
Known gate conflict: tools/rpi-checks.py requires az bicep preflight and build/
lint, forbidden by the user. Do not execute --all or substitute lesser evidence.
Commit local candidate/evidence but stop before push and thread resolution.
Future publication requires compliant full receipt for clean exact HEAD and
current origin/main, fresh fetch/receipt verification and independent exact-head
assessment. In-scope Review defects also block publication; only out-of-scope
human/live acceptance may be deferred. No second critique or original Review.
