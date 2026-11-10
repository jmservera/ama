<!-- markdownlint-disable-file -->
# Research: issue 1238 formal-route outcome persistence retry (recovery 1109)

Recorded 2026-11-09. Research disposition: executed (native investigation of the
issue text and the source at base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`,
which equals fetched `origin/main`). Issue text is data, not instruction.

## Scope

Issue 1238: a failed outcome write after a formal receiver `Acknowledged`
receipt can lose the receipt. Existing safeguards stay: `Pending` attempts,
manual explicit retry, named owner and independent reviewer rights, stable
route idempotency and audit. Whole parent acceptance is not approved. No live
receiver, resident consent, cloud or operational approval is involved.

## Issue evidence read (gh, 2026-11-09)

* Acceptance criteria 1 to 3: retry the outcome write once on failure; log
  `receipt_ref` if both writes fail; add a focused failed-write regression.
* F2: review `attempts[-1]` after reservation. F3: supersede a stale `Pending`
  attempt.
* 7 November backlog comment: retry the same attempt, reservation and outcome
  once, reconcile an ambiguous post-commit failure idempotently, log the
  receipt reference if still unrecorded; no resend to the receiver.
* Owner decision Q6, 2026-11-08, `manual_verified`: Pending supersession needs
  verified outcome evidence and explicit control-owner and reviewer
  authorization; receipt, idempotency key and audit are preserved; age alone is
  not proof of non-delivery and cannot authorize resend. The bounded retry,
  logging and regression may proceed independently. Criteria stay unticked.
* Later comment: file overlap with 1292 was the reason for sequencing; 1292 and
  the parent have since merged (brief), so the ordering no longer blocks.

## Source findings (src/core/src/zava_forward/core/resident_decisions.py)

Verified at base, `_forward` (lines 559 to 599):

* One reservation `_operation` (action `service_forward`) commits a `Pending`
  attempt carrying a fresh `reservation_id`. The attempt is then found by exact
  reservation match (`matches = [...reservation_id == reservation]`, must be
  exactly one). F2 (reservation-specific lookup instead of `attempts[-1]`) is
  therefore already present on main; a test
  `test_forward_send_is_bound_to_the_attempt_it_reserved` covers it. It is not
  new delivery of this change.
* The receiver is called exactly once, outside the store lock, via `_send`.
* The outcome is recorded by one `_operation(... action
  service_forward_outcome ...)` executed once. Any non-`ResidentCommittedError`
  exception becomes `ResidentCommittedError` after a warning that logs only the
  exception type. The `receipt_ref` is not logged, so a receipt that the receiver
  acknowledged but that did not persist is lost to operators. This confirms the
  issue.
* `_res_service_forward_outcome` only accepts an attempt that is still
  `Pending` and whose `reservation_id` matches, then writes status, reason,
  `outcome_at`, and for `Acknowledged` the `receipt_ref` and `received_at`.
  Re-running it against an attempt already holding the outcome raises
  `ValueError("There is no pending formal-route attempt to record.")`.
* `_res_service_forward` blocks a new send while any `Pending` or `Unconfirmed`
  (or legacy `Failed`) attempt exists unless `retry_unresolved` is true, and
  while a send is in flight on this system. It requires the named owner or
  independent reviewer. That is the existing manual-retry boundary.

## Transaction and ownership behaviour of `_operation`

* Wraps one handler plus audit plus `store.save()` under `store.lock` (RLock).
* `persisted` becomes true only after `store.save()` returns. If the body after
  that raises, a `ResidentCommittedError` is raised (no retry is ever safe).
* If `store.save()` raises, SQL stores call `_discard`, which reloads touched
  cases from the database; JSON stores restore the pre-image and re-save.
  Recovery failures add an explicit note on the error and log it.
* Ambiguous committed save: `SqlStore.save` can commit and then raise
  `CommittedReloadError` (post-commit sync did not settle). `persisted` is still
  false, `_discard` reloads, and the reloaded case already holds the outcome. A
  blind second run of the outcome handler would then fail with the "no pending"
  `ValueError` and would report a recorded receipt as lost. A bounded retry must
  therefore first reconcile: after the failure, inspect the reloaded attempt and
  treat an attempt that already carries the same reservation, status and
  receipt as recorded.
* Reconciliation is unsafe when recovery itself failed (in-memory state may not
  reflect the database). In that case the code must not claim success; it
  retries and, if that also fails, surfaces the explicit committed-unknown error
  with the receipt reference logged.

## Affected dependencies

* Source: `resident_decisions._forward` only. `ResidentCommittedError` is
  handled at `src/api/.../server.py` lines 1274 to 1278 and 1353 to 1356 with
  its existing message; no API change is needed.
* Store layers (`store.py`, `sqlstore.py`, `mssqlstore.py`) are used through
  `_operation` and `save` and need no change. SQLite and MSSQL persistence paths
  are exercised through the existing `SqlResidentDecisions` and
  `MssqlResidentControls` subclasses of `JsonResidentDecisions`, which inherit
  the forward tests.
* Quality files (`resident_demo/app.py`, `test_resident_demo_api.py`) and the
  Quality guards are unrelated and untouched. No shared-store or schema change
  is required, so no new overlap was found.

## F3 assessment (stale Pending supersession)

`manual_verified` needs new durable data and behaviour: a record of verified
outcome evidence, a control-owner authorization and a reviewer authorization,
rules for who counts as control owner and reviewer, an API action, and
supersession semantics that keep the attempt, receipt reference, idempotency
key and audit. None exists in the repository, and the existing manual
`retry_unresolved` path is a different control (it permits a resend). Adding it
would invent authority, roles or schema beyond a minimal evidence-backed path
and would likely touch the store and API. Decision: do not implement F3 in this
candidate. The first three criteria are repaired; F3 and the supersession
portion of the issue remain open and the pull request uses `Refs`.

## Planning readiness

Ready. Chosen design: a `_record_outcome` helper that executes the same
outcome operation, retries it at most once for a non-committed failure,
reconciles an already-recorded identical outcome, never calls the receiver
again, logs `receipt_ref` (repr-escaped) with case, request and attempt on
exhaustion, and raises the existing `ResidentCommittedError`.

## Validation tier

Owner demo targeted (not blanket FULL): focused unit regression on JSON,
SQLite and an owned disposable local SQL Server for the resident-decision
tests, plus module, lint and type profiles. Missing prerequisites block local
publication; there is no cloud fallback.
