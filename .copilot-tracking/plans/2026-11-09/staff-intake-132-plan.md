---
title: Issue 132 existing-staff-mediated synthetic job pack intake plan
ms.date: 2026-11-09
task_id: issue-132-staff-intake-1109
---

## Task metadata

* Research `.copilot-tracking/research/2026-11-09/staff-intake-132-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09/staff-intake-132-details.md`. Critique `.copilot-tracking/plans/2026-11-09/staff-intake-132-critique.md`. State `.copilot-tracking/rpi-sessions/2026-11-09/staff-intake-132-state.json`.
* Branch `feat/demo-staff-intake-132-1109`, base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`, PR target `feat/demo-quality-workflows-89-1109`. Local commits only. Refs #132 (and Refs #89), never a closing keyword.

## Requirements

* R1 Existing authenticated staff (STAFF_ROLES, no new role or permission) open a synthetic job pack for a work order and see scope, design version, notice flag and one named contact, no health or vulnerability reasons (AC1 supporting evidence).
* R2 Staff record worker-confirmed notes against the versioned checklist through the existing `submit_quality`. First-captured notes are preserved verbatim (no clipping), later corrections append (AC2).
* R3 A distinct durable acknowledgement ("Receipt acknowledged - not accepted") is recorded by staff, separate from submission and independent review. Worker, recorder and acknowledger cannot independently accept (AC3).
* R4 Version/stale rejection, duplicate and offline reconciliation, idempotent replay.
* R5 Independent-review handoff is displayed: awaiting review, who is barred, quality roles, current state from the quality record. Nothing accepts work.
* R6 Cancellation, provider no-show and no-access recovery shown; provider absence is never resident refusal (AC4 remains ticked, now also exposed).
* R7 Configured escalation destination shown; unset is explicit Unknown, never invented, never a contract instruction (AC5 partial: display only).
* R8 Smallest shared hook set; dedicated modules; documented contract for sibling 133.

## Phases

* P1 Core `staff_intake.py` plus `quality.submit_quality(field_receipt=)` hook: view, capture, correct, acknowledge, idempotency, stale, review handoff. Unit tests in `src/core/tests/test_staff_intake.py` (core) over JSON and SQLite stores with restart/readback.
* P2 API hooks: `server.py` route kind `field_intake`, `STAFF_GET` entry, HTTP tests `src/api/tests/test_staff_intake_api.py` (capture, restart/readback, ack, stale, duplicate, offline, denial, privacy, no-show) over the JSON and SQLite store, inventory update.
* P3 Browser: `web/staff-intake.js` screen `staff-job-pack-intake` plus `index.html` tag, content-standard audit entry, unit test with node host harness, then actual served/browser capture. Load and apply current web-design-guidelines and redesign-existing-projects before editing.
* P4 Docs: core and API README sections, knowledge-base log not required (no knowledge-base file change). Changes record and one Review.
* P5 Heavy-resource gate: browser and SQL Server only after actual-holder inspection and nonqueued admission; otherwise record blocked with resume point.

## Phase criteria

* P1 pass: new core tests plus existing `test_job_pack.py`, `test_quality*` and procurement tests pass; ruff and mypy clean on touched files.
* P2 pass: new API tests and `test_role_endpoint_inventory`, `test_procurement_api`, `test_procurement_screens` pass on both stores.
* P3 pass: node harness test and served-browser capture showing capture, acknowledgement and review handoff; keyboard, status and error states checked. Not AT or WCAG acceptance.
* P5 pass: SQL Server and browser checks executed under owned admission, or an explicit blocked record.

## Validation tier

* Focused tier with actual affected integration (owner demo targeted validation). Doubt classification: touches case-body persistence through unchanged SQL, no schema, no permission, no dependency, workflow or Dockerfile change. No full gate; stated, not hidden.

## Out of scope and gaps preserved

* Provider portal, contractor accounts, B2B guests, escalation posting with a named owner, contract instruction, resident consent, QA authority, live or AT acceptance, AC5 completion and the #116 identity model.
