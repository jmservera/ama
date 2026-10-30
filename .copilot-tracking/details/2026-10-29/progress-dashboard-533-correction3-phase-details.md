---
title: Progress lifecycle correction phase details
description: Implementation and evidence expectations for correction3
ms.date: 2026-10-29
---

Task: progress-dashboard-533-correction3. Research C1-C6 is ready.
Boundaries and requirements are owned by the matching plan. Implementation
complete, required heavy validation blocked by foreign shared-lock ownership.

<!-- P01 -->
## P01: Guard and regressions

<!-- P01-T01 -->
### P01-T01: Persistent malformed evidence matrix

Extend the existing auxiliary persistence test into a three-collection test.
Use three mutation modes: replace the complete container, insert a malformed
element into valid history, or insert a labelled row with a malformed action.
Whole-container replacements for every field include null, string, mapping,
boolean, integer and float. These do not retain valid history in that field.
Build each malformed history by retaining complete original valid history
and inserting each invalid row before/after it. Explicitly label the case
synthetic so malformed history cannot make it disappear from admission.
Persist JSON with Store.save; SQLite writes only the constructed case body,
then reopen the corresponding store. Both reads must disclose incomplete
evidence rather than raise. Exact daily/weekly/episode totals should reflect
only the unaffected valid sibling; archive retains unknown dates unbounded
and excludes them for start-only/end-only filters.

Synthetic actions include missing/null, arrays/maps (empty and nonempty),
booleans, integers and floats. Element matrices cover all non-dictionary JSON
types. Positive controls ensure unlabelled dictionary rows and legitimate
synthetic narrative rows are still ignored, and irrelevant auxiliary
dictionary field values do not become schema errors.

<!-- P01-T02 -->
### P01-T02: Explicit lifecycle guards and contract

Require dictionary elements in history alongside existing sibling guards.
Split dictionary validation from synthetic provenance filtering. Return None
for non-string synthetic action before set membership. Preserve all remaining
replay logic. Update API README only, not knowledge-base syntheses or pins.

<!-- P02 -->
## P02: Validation and review

<!-- P02-T01 -->
### P02-T01: Local evidence

Use /tmp/mv tools and install editable core/agents/api there as requested.
Record any missing dependency before restoring it. Set PYTHONPATH to this
worktree's src roots and the owning tests first to avoid duplicate test module
names. Full API/core discovery and browser use one nonblocking shared-lock
admission; if busy, do not wait/poll, run focused tests and mark full/browser
work blocked as applicable. Existing /tmp/ama-533-venv may supply browser
dependencies if /tmp/mv lacks them. Keep logs/assets in a new external /tmp
directory; never read working datasets. Run git diff --check.
The parent's execution context permits the owner-specified /tmp paths, unlike
the critique worker's reported boundary. Keep this distinction explicit and
record actual failures instead of inheriting an unverified worker blocker.

<!-- P02-T02 -->
### P02-T02: Local commits and one Review

Reconcile plan markers, changes, tests and state. Commit source and original
dated research/plan/critique/change evidence with privacy-safe identity and
the requested trailer. Request a fresh independent RPI Review for that exact
source commit and bounded acceptance criteria. Preserve its original outcome;
route any findings to later work, never repeat Review. Commit closeout evidence
locally. Do not push or run az; complete publication gate is not claimed.

## Pre-Review Reconciliation

P01-T01/T02 complete: persistent matrix expanded and one positive-control
method added, production guards and API contract updated. P02-T01 disposition
complete under the caller's targeted fallback: 69 targeted tests pass;
API/core mypy/Ruff pass. Full suites/browser remain explicitly Blocked after
nonblocking admission exit 75, not performed checks. P02-T02 remains active
for candidate commit, one independent Review and local closeout. No source
scope change, acceptance relaxation or repeated critique.

## Local Closeout

P02-T02 complete: candidate 20385e3a950500d11cbb033170961d8b4661d108
contains source and original dated RPI evidence. The single independent Review
is Complete / Not accepted, RV-001 Medium for unavailable required full/browser
checks; no confirmed source defect. Preserve that original result and route
later coordinated evidence work to rpi-research, not another current-task
implementation/Review. The local closeout commit contains only orchestration
and Review evidence. Plan markers are complete as execution dispositions;
validation acceptance remains incomplete. Session stops per explicit caller
direction with no push, az, child task, shared-lock retry or publication claim.
