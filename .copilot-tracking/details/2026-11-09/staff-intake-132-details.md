---
title: Issue 132 existing-staff-mediated synthetic job pack intake details
ms.date: 2026-11-09
task_id: issue-132-staff-intake-1109
---

## Shared hook contract (owned by this task, for 133 and the coordinator)

* H1 `src/core/src/zava_forward/core/quality.py`: `submit_quality(..., context_revision=None, field_receipt=None)`. A non-None mapping is stored unchanged as `rec["field_receipt"]` inside the same `_quality_operation`, audit and `save()` as the evidence. No other quality behaviour changes.
* H2 `src/api/src/zava_forward/api/server.py` (C-7: POST dispatch is placed before the broad `packages`/`workorders` procurement branch, tests cover all three actions): `get_kind` returns `field_intake` for `/api/workorders/<id>/field-intake`; GET and POST (`field-capture`, `field-correct`, `field-acknowledge` under `/api/workorders/<id>/`) delegate to `zava_forward.core.staff_intake.handle(store, user, method, parts, body)` which returns `(status, payload)`. The server holds no intake logic.
* H3 `src/core/src/zava_forward/core/projection.py`: `STAFF_GET` gains `field_intake`. Contractor lists unchanged, so a contractor (and Application Administrator view-only) still gets 403.
* H4 `src/api/src/zava_forward/api/web/index.html` one `<script src="/staff-intake.js">` after `role-screens.js`; the script registers one screen through the existing `registerRoleScreen` guarded by `typeof registerRoleScreen === "function"`.
* H5 Tests that inventory shared surfaces: `test_role_endpoint_inventory.py` (GET and POST paths), `test_content_standard.py` AUDITED_FILES.
* Pattern for 133: new dedicated `core/<name>.py` exposing `handle(store, user, method, parts, body)`, one `server.py` delegation line per route, one `STAFF_GET` token, a dedicated `web/<name>.js` with a guarded registration. It must not edit `staff_intake.py`, `quality.py` H1 or the 132 screen, and it must rebase its hook lines after this candidate is merged to parent 89.

## Dedicated module `core/staff_intake.py`

* `handle` routes `GET field-intake`, `POST field-capture|field-correct|field-acknowledge`. Authorization: `projection.is_contractor` refused; all other staff must be registered (same `_work_order_reader`/`_actor` guard as the job pack). No role list is added.
* Stored shape: `rec["field_receipt"]` = `worker_receipt(...)` output plus `notes_version`, `corrections: []`, `acknowledgement`, `recorded_by` (name, code), `order_version`. Quality `items` hold the current notes; `original_notes` never change.
* Capture preconditions: pack ready (`pack["ready"]`), `pack_digest` equals the freshly built digest (otherwise `StaleError` 409 with `hold_reason` from `merge_offline` semantics and the worker's notes echoed back, nothing stored), every note at most 200 characters (reject, not clip), `confirmed is True`, non-empty `worker_name` of at most 80 characters that is not any registered staff email or code (C-4; a matching staff name is already added to `participants` by quality), `capture_ref` 8 to 64 characters of `[A-Za-z0-9._-]`. The reference lookup, stale check and insertion run inside one `_quality_operation` under the store lock, and the replay check runs before the stale check so a valid replay is never rejected after the pack changed (C-2, C-3). A capture reference already stored on this order answers `outcome: duplicate` with the existing receipt, stores nothing, and a different payload under the same reference is a 409 conflict. Offline mode keeps the caller's `captured_at`; online uses server time when omitted. The record is written through `submit_quality(source="Installer")` with `field_receipt` so submission, history event, audit and persistence are one operation.
* Correction (critique C-5 applied): append `{n, at, by(recorder), reason, worker_confirmed_by, notes}` only while the quality state is Submitted and no acknowledgement exists, inside `_quality_operation`; updates the quality items; `original_notes` and earlier entries stay. After acknowledgement the existing quality return and resubmit path owns changes, so an acknowledgement always covers the current notes. Every correction contributor (recorder identity and confirming worker name) is appended to `participants`.
* Acknowledge (critique C-1): runs inside `store._quality_operation`, so failure rolls back JSON state and audit or discards the SQL transaction; records name, email, code, time; appends the acknowledger to `participants` so `_independent` later bars them; appends a history event `field_receipt_acknowledged`; audit; one `save()`. A repeat returns the first acknowledgement unchanged (409 "already acknowledged"). The worker name cannot acknowledge. The state stays Submitted; `status` is "Receipt acknowledged - not accepted".
* View (C-6, closed schema; no other quality or history field is copied; response fields are exactly `index, measure, state, checklist, checklist_version, evidence_version, source, submitted_by, recorded_by, recorded_at, items`, and `field_receipt{capture_ref, mode, captured_at, original_notes, notes_digest, pack_digest, design_version, confirmed_by, corrections, acknowledgement{by, at}, status, accepted}`): pack (job_pack allow-list) plus `receipts` (state from the quality record, `review` block with `review_state`, `independent_review_barred` names, `viewer_review_blocker` from `job_pack.review_blocker`, quality roles), `recovery` (all `visit_recovery` outcomes), `escalation` (configured destination or `Unknown`, `contract_instruction: false`), `boundaries` text. No resident field is read.
* Errors: `ValueError` 400, `PermissionError` 403, `StaleError`/conflict 409, unknown order 404.

## Tests (focused)

* Core: capture then reopen JSON and SQLite stores and read back; notes verbatim; 201 character note rejected; stale digest rejected; duplicate reference idempotent; conflicting duplicate 409; correction preserves original; acknowledgement durable and distinct; acknowledger, worker and recorder denied `accept_quality`, independent QA accepted; privacy canaries absent; offline keeps captured_at; no-show outcomes and escalation Unknown/configured.
* API: same through HTTP, contractor 403, default-deny, inventory.
* Screen: node harness over `staff-intake.js` (render, submit payload, error and duplicate states).
* Browser: served capture of the screen; SQL Server run only if admitted.

## Validation commands (planned)

* `/tmp/zf132-venv/bin/python -m unittest` for the named modules from `src/core` and `src/api`, ruff, mypy on touched files, node harness, served browser run and SQL Server tests under `--lock-timeout 0` admission.
