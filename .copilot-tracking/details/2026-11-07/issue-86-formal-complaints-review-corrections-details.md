---
title: "Issue 86 formal-complaints adapter: review-correction details"
description: Exact edits, regression designs and failure modes for the three Medium findings, written before any source edit
ms.date: 2026-11-07
issue: jmservera/ama#86
rpi_phase: details
task_slug: issue86-formal-complaints-review-corrections
parent_task_slug: issue-86-formal-complaints-adapter
---

Scope: jmservera/ama#86 only. Plan: `.copilot-tracking/plans/2026-11-07/issue-86-formal-complaints-review-corrections-plan.md`. Line numbers are from head `3445238e` and are orientation only.

## Edit 1: `src/core/src/zava_forward/core/complaints_route.py`

* `STATUSES = ("Pending", "Unconfigured", "Failed", "Unconfirmed", "Acknowledged")`. `Failed` means definite non-send; `Unconfirmed` means no acknowledgement obtained, receipt unknown.
* `class NotSent(RuntimeError)`: a receiver raises it only when it knows nothing reached it. It is not a subclass of `NotConfigured`.
* Replace `FAILURE_REASON` with `NOT_SENT_REASON = "The request was not sent. Nothing reached the receiver."` and `UNCONFIRMED_REASON = "Acknowledgement was not obtained. Whether the receiver has this request is unknown; check with the receiver before sending again."`. `MALFORMED_REASON` becomes the same unknown-receipt statement, used by `parse_acknowledgement` and by `_send`. Remove no public name still imported elsewhere (search before edit; the old name is only used in `_send` and tests).
* Annotations stay strict (no `Any`-shaped escapes beyond the existing untrusted reply parameter).

## Edit 2: `src/core/src/zava_forward/core/resident_decisions.py`

Reservation binding (`_forward`, `_res_service_forward`):

* `_forward` creates `reservation = uuid.uuid4().hex` and passes `dict(body, action="service_forward", reservation_id=reservation)` into `_operation`. The handler stores `reservation_id` on the attempt dict and never mutates the body; the SQL replay on the detached case then reproduces the same attempt.
* Caller input must not choose the identifier: `_forward` overwrites any `reservation_id` supplied in the user body, and `resident_action` refuses a body key of that name from a direct `service_forward_outcome` path (the outcome action is internal; confirm by test that a public caller cannot reach it with a forged attempt, as today via `RESIDENT_ACTIONS`).
* One `with store.lock:` block (re-entrant) encloses the reservation `_operation`, the lookup, the snapshot guard, the envelope build and the registry add, so no same-instance caller can reserve or register in between; the lock is released before `submit` (critique 1). The block finds the request and the attempt with that `reservation_id` (exactly one, else raise `ResidentCommittedError` with the existing "reserved, outcome not recorded" wording). It reads `route["route_key"]` and attempt number from that attempt, never `attempts[-1]`.
* Snapshot guard in that block is point-in-time only (critique 4): if the request is now `Closed` or `req.get("version", 0) != attempt["request_version"]`, skip `submit` and record `status="Failed"`, reason `NOT_SENT_REASON`. Otherwise build the envelope. Closure after the guard and before `submit` returns remains a stated residual.
* In-flight registry: module-level `weakref.WeakKeyDictionary` mapping the store to a set of `(case_id, request_id, attempt)`; added inside the lock block above, discarded in `finally` after the outcome record attempt. `_res_service_forward` refuses `retry_unresolved` when a Pending attempt is in flight on that Store instance. The guarantee is per Store instance, not per process or database (critique 5). If the store is not weak-referenceable the implementation must stop and report rather than fall back to a global `id()` key.
* The outcome record keeps `id=req["id"], attempt=attempt`; `_res_service_forward_outcome` additionally checks `attempt["reservation_id"]` equals a `reservation_id` carried in the outcome body, so an outcome can only complete the exact reservation it came from.

Ambiguity (`_send`, `_res_service_forward`):

* `_send`: `NotConfigured` gives `Unconfigured`; `NotSent` gives `Failed` with `NOT_SENT_REASON`; any other `Exception` and an unparseable reply give `Unconfirmed` with `UNCONFIRMED_REASON`. Log only the exception type name, as today.
* Retry gate: unresolved set is `{"Pending", "Unconfirmed"}`; without `retry_unresolved is True` raise the existing reconcile message. A later `Acknowledged` still blocks every retry. `Failed` and `Unconfigured` retry without the flag.
* A retry after `Unconfirmed` keeps `route_key` (the `idempotency_key`) and increments `attempt`; the earlier attempt stays `Unconfirmed` as honest history; nothing is overwritten.

Named reviewer identity (`_res_service_forward`):

* New helper `_require_named_reviewer(actor, identity)`: refuse with a resolve-identity message when `_identity_status(identity) == "Unknown"`. Use `_identity_value` (casefolded, empty when missing or `None`): for each of `code` and `oid` where the persisted identity has a non-empty value, the actor must have the same non-empty value; a persisted key that is empty is ignored, not compared (`_identity` always carries `oid`, often `None`). At least one key must be compared. Email equality stays the first guard (critique 3).
* For `req["route"] == "Independent review"` call it, then `_require_independent_reviewer(user, req.get("reviewed_identity"))`, and do not call `_owner_rights` (the managerial bypass). For the Complaint route call `_owner_rights` exactly as today.

## Edit 3: `src/core/README.md`

Update the formal-route section (~316): statuses `Unconfigured`, `Failed` (definite non-send), `Unconfirmed` (receipt unknown, explicit reconciliation), `Acknowledged`; the reservation binding; the named reviewer identity rule; and the unchanged limits (no receiver, no destination, no cross-process proof, no receiver-side dedupe). ASCII punctuation only.

## Regression designs (existing file `src/core/tests/test_resident_decisions.py`)

* Use `SyntheticReceiver` extended with modes `record-then-raise`, `not-sent` and a blocking mode driven by two `threading.Event`s (never `sleep`). All waits carry timeouts so a defect fails rather than hangs. Use `ThreadPoolExecutor` and `Barrier`/`Event` as the existing concurrency test does.
* In-flight refusal: thread A calls `forward`; the receiver signals `entered` then waits `release`. The main thread asserts a `retry_unresolved` retry on the same Store instance is refused, releases A (in `finally`, all waits timed), then retries normally and asserts attempts 1 and 2 statuses.
* Binding RED/green seam (critique 2): patch `resident_decisions._operation` with a wrapper that delegates, and after the first (reservation) call exits commits a competing attempt 2 through the store as a second caller would (`with store.lock`, mutate, `store.save()`, as existing tests do). Against the current `attempts[-1]` code A submits and records against attempt 2 (RED); with the fix A's envelope has `attempt == 1`, its outcome lands on attempt 1 and attempt 2 stays untouched and Pending. Record the RED run before editing source.
* Cross-instance variant through `open_store()` (inherited by the SQL subclass): asserts only that the reserved attempt is never misattributed and that the per-instance registry does not claim to see the other instance (critique 5).
* Snapshot guard: the same seam changes the request version or closes it after the reservation commit; assert no receiver call and a `Failed` not-sent record with no receipt fields. Point-in-time only; no test claims freshness through `submit`.
* Ambiguity: record-then-raise and malformed produce `Unconfirmed`, text contains neither "has not been received" nor receipt fields; ordinary retry raises, flagged retry succeeds with the same `idempotency_key`; `NotSent` produces `Failed` and ordinary retry works.
* Identity matrix: code-only, code plus oid, missing and changed code, changed oid, and a bound Entra actor where the existing fixtures allow; a persisted identity with `oid` of `None` must not reject the genuine reviewer. Build the manager-with-changed-identity case by changing the staff list entry's `oid`/`code` for the named reviewer's email (existing fixtures for staff and identity are reused; read them before writing); assert refusal, empty `receiver.envelopes`, unchanged audit/state through the existing `unchanged_failure` helper. Legacy Unknown identity fails closed. Genuine reviewer and non-reviewer refusals remain as in the existing test.
* Existing tests that assert old `Failed` text for `raise` and `malformed` are deliberately updated; the change in expectation is recorded in the Changes record.

## Failure modes to check during implementation

* SQL replay: the handler must be idempotent for the same body (reservation id stable, no uuid inside the handler for the attempt identifier).
* The registry must be released on every exit path, including an outcome-record failure, or a later legitimate reconcile would be refused.
* `ResidentCommittedError` paths from the outcome step keep their wording and still leave Pending.
* Resident reach under holds stays open; identity check must not read hold state.
* Retention deletion still clears `resident_request_ref` and `requested_by`; assert `reservation_id` is opaque and does not leak resident content.

## Focused commands for the later stage (no service)

`PYTHONDONTWRITEBYTECODE=1`, scratch TMPDIR/XDG in an issue-specific `/mnt/ama-gates/` directory, installed distributions with the printed `__file__` origin proof, no `PYTHONPATH=mvp`, no `uv`, no private data: the component's own unittest discovery limited to `test_resident_decisions`, strict mypy from the component's configuration, `ruff check` and `ruff format --check` from the repository configuration. SQL-backed variants are not started; their skips are recorded per test.

## Amendment 1 (before source edit): legacy `Failed` compatibility

* `_res_service_forward_outcome`: for a definite non-send the outcome body carries `not_sent=True` and the handler stores `not_sent: True` on the attempt. `_send` returns it only for `NotSent`; the snapshot guard returns it too. `Unconfirmed` never carries it.
* `_res_service_forward`: `unresolved = [a for a in attempts if a["status"] in ("Pending", "Unconfirmed") or (a["status"] == "Failed" and a.get("not_sent") is not True)]`; refusal needs `retry_unresolved is True`. Message names the receiver check. An `Acknowledged` attempt still blocks everything.
* Reservation id stays caller-independent: `_forward` always overwrites any body value with its own uuid; the handler stores it and does not generate one, so SQL replay is stable.
* Edit 3 README text states legacy `Failed` records are treated as unresolved and not rewritten.
