<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #1238 Stale Pending Supersession and Retry/Receipt Verification

## Metadata

* Task ID: issue-1238
* Task slug: core-1238-stale-pending-2346
* Related plan: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md, src/core/src/zava_forward/core/resident_decisions.py, src/core/tests/test_resident_decisions.py, src/core/README.md

## Phase Index

| Phase ID | Name                                                      | Status    | Detail sections          |
|----------|-----------------------------------------------------------|-----------|--------------------------|
| P01      | Atomic Stale `Pending` Supersession in `_res_service_forward` | completed | P01, P01-T01             |
| P02      | Focused Unit Tests and Component Documentation            | completed | P02, P02-T01, P02-T02    |
| P03      | `src/core` Validation Gate                                | completed | P03, P03-T01             |

<!-- rpi:phase id=P01 -->
## P01: Atomic Stale `Pending` Supersession in `_res_service_forward`

### Context

Research (`C5`-`C9`) confirmed that ACs 1-4 of Issue #1238 are already implemented in `src/core/src/zava_forward/core/resident_decisions.py`. However, when an earlier send's outcome write fails after `_send` completes (leaving the attempt persisted with `status == "Pending"` once `_IN_FLIGHT` clears in `_forward`'s `finally` block), a subsequent explicit retry via `service_forward` (`retry_unresolved=True`) appends a new `"Pending"` attempt while leaving the stale `"Pending"` attempt in `"Pending"` indefinitely (`C10`, `C12`).

### Intent

Atomically transition any stale `"Pending"` attempt on the formal route to `"Superseded"` at the exact moment `_res_service_forward` commits a superseding explicit-retry attempt, preserving full attempt history, `route_key` stability, `manual_verified` dual-approval separation, and late-outcome fencing.

### Boundaries

* Included: `ResidentDecisionMixin._res_service_forward` in `src/core/src/zava_forward/core/resident_decisions.py`.
* Excluded: `_forward`, `_record_outcome`, `_outcome_recorded`, `_res_service_forward_outcome`, `_res_service_supersede_authorize`, `SupersessionBinding`, and `complaints_route.py`.

### Likely Targets

* src/core/src/zava_forward/core/resident_decisions.py: Update `_res_service_forward` to mark prior `"Pending"` attempts `"Superseded"` and reflect superseded attempt numbers in the returned audit detail.

### Dependencies

* none

### Validation Expectations

* `python3 -m mypy` and `python3 -m unittest discover -s tests -p "test_resident_decisions.py" -q` in `src/core`.

### Completion Evidence

* `_res_service_forward` transitions prior `"Pending"` attempts to `"Superseded"` only after all preconditions succeed and rolls back cleanly if store persistence fails.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Transition prior `Pending` attempts to `Superseded` in `ResidentDecisionMixin._res_service_forward`

#### Context

In `ResidentDecisionMixin._res_service_forward`:
* Any prior attempt with `status == "Pending"` is included in `unresolved`.
* Resend is refused unless `body.get("retry_unresolved") is True` and `not in_flight(self, c.get("id"), req["id"])`.
* Route-specific permission/independence checks (`_require_named_reviewer` + `_require_independent_reviewer` for `"Independent review"`, `_owner_rights` for `"Complaint"`) and `k.text(body.get("resident_request_ref"), ..., 100)` execute before any mutation of `route["attempts"]`.
* In `_res_service_supersede_authorize`, `manual_verified` supersession sets `status="Superseded"`, `superseded_from="Pending"`, `superseded_at=_time()` alongside `attempt["supersession"]`.

#### Intent

Ensure that when `_res_service_forward` appends superseding attempt `attempt = len(route["attempts"]) + 1` at `now = _time()`, every prior attempt in `attempts` currently in `status == "Pending"` is updated in place:
* `status = "Superseded"`
* `superseded_from = "Pending"`
* `superseded_at = now`
* `superseded_by_attempt = attempt`
without creating or modifying `attempt["supersession"]` and without touching `"Unconfirmed"`, `"Failed"`, or already-`"Superseded"` attempts. When one or more prior `"Pending"` attempts are superseded, include `"prior pending attempt ... superseded"` (pluralized when >1) in the returned case-audit detail string.

#### Boundaries

* Included: In-place status/metadata update on prior `"Pending"` dicts inside `_res_service_forward` after all validation and permission checks succeed, plus audit-detail return text.
* Excluded: Altering non-`"Pending"` attempts, deleting attempt entries, changing `route_key`, or altering `service_supersede_authorize`.

#### Likely Targets

* src/core/src/zava_forward/core/resident_decisions.py: `ResidentDecisionMixin._res_service_forward`.

#### Dependencies

* none

#### Validation Expectations

* Prior `"Pending"` attempt transitions to `"Superseded"` on valid `retry_unresolved=True` reservation; refused or failed reservations leave `"Pending"` untouched; late `_res_service_forward_outcome` calls for the superseded attempt raise `ValueError("There is no pending formal-route attempt to record.")` and trigger `_record_outcome`'s `receipt_ref` warning log and `ResidentCommittedError`.

#### Completion Evidence

* Updated `_res_service_forward` in `src/core/src/zava_forward/core/resident_decisions.py`.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Focused Unit Tests and Component Documentation

### Context

`JsonResidentDecisions` in `src/core/tests/test_resident_decisions.py` is subclassed by `SqlResidentDecisions`, so test methods added to `JsonResidentDecisions` automatically run against both JSON and SQLite backends (`C14`). Test ownership, exact updates, maximum additions, and semantic-versus-regression coverage are locked below for critique review:
* Canonical test target: `src/core/tests/test_resident_decisions.py` (`JsonResidentDecisions`, inherited by `SqlResidentDecisions`). Generated targets: `none`.
* Exact removals: `none` (update one post-retry status-list assertion in `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` from `["Pending", "Acknowledged"]` to `["Superseded", "Acknowledged"]` while keeping all existing pre-retry `"Pending"` assertions).
* Maximum test additions: at most 4 focused test methods in `JsonResidentDecisions` (zero `del sys.modules[...]` usage).
* Semantic vs regression coverage:
  1. Regression update in `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend`: verifies ACs 1-3 + post-retry `["Superseded", "Acknowledged"]` status progression and preserved `idempotency_key`.
  2. Semantic test for explicit-retry supersession audit & idempotency invariants across `"Complaint"` and `"Independent review"` routes (preserved reservation fields, `superseded_from="Pending"`, `superseded_at`, `superseded_by_attempt`, absence of forged `supersession` dict, case audit detail, `delete_resident_records` personal-ref scrubbing).
  3. Semantic edge-case test for refused/rolled-back retries leaving `"Pending"` unchanged, chained stale `"Pending"` retries (`attempt 1 -> superseded_by_attempt=2`, `attempt 2 -> superseded_by_attempt=3` without mutating attempt 1), and non-interference with `"Unconfirmed"`, `"Failed"`, and `manual_verified` `"Superseded"` (`service_supersede_authorize`) attempts.
  4. Semantic fencing test proving a delayed outcome write (`_record_outcome`) targeting a retry-superseded attempt fails closed (`ResidentCommittedError`), logs the stale attempt's `receipt_ref`, and leaves both the `"Superseded"` and `"Acknowledged"` attempts intact.

### Intent

Provide focused, deterministic multi-backend unit tests that fail without P01 and update `src/core/README.md` so documentation matches runtime behavior.

### Boundaries

* Included: `src/core/tests/test_resident_decisions.py` and `src/core/README.md`.
* Excluded: Bulk or single `del sys.modules[...]` hacks, unrelated test files, and `docs/reference/` knowledge-base files (component internals belong in `src/core/README.md`).

### Likely Targets

* src/core/tests/test_resident_decisions.py: Update 1 assertion and add up to 4 focused test methods in `JsonResidentDecisions`.
* src/core/README.md: Clarify explicit `retry_unresolved` supersession of stale `Pending` attempts alongside `service_supersede_authorize`.

### Dependencies

* P01

### Validation Expectations

* All new and existing tests run under both `JsonResidentDecisions` and `SqlResidentDecisions` and pass; Markdown links and diff in `src/core/README.md` are clean.

### Completion Evidence

* Passing unit tests in `src/core/tests/test_resident_decisions.py` and updated `src/core/README.md`.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update and add focused `resident_decisions` unit tests without `sys.modules` deletion

#### Context

`JsonResidentDecisions` already provides helpers `self.pending_attempt(route=...)`, `self.forward(...)`, `self.supersede(...)`, `self.unchanged_failure(...)`, `self.route(...)`, and `self.open_store()` for verifying durable persistence across reopen on both JSON and SQLite stores.

#### Intent

Update `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` and add focused tests in `JsonResidentDecisions` covering:
1. Full audit-field preservation, `superseded_from`/`superseded_at`/`superseded_by_attempt` metadata, absence of `supersession` dual-approval dict, case audit log entry, stable `route_key`/`idempotency_key`, durable reopen state, and `delete_resident_records` scrubbing across `"Complaint"` and `"Independent review"`.
2. Refusal/rollback non-mutation (`retry_unresolved` omitted, `in_flight` active, unauthorized actor, bad `expected_version`, blank `resident_request_ref`, failed reservation `store.save()`), chained stale `"Pending"` retries (`1 -> 2 -> 3`), and preservation of `manual_verified` `"Superseded"` (`service_supersede_authorize`) metadata when followed by `retry_unresolved=True`.
3. Late `_record_outcome` fencing on a retry-superseded attempt (raises `ResidentCommittedError`, logs `receipt_ref` at `WARNING`, preserves `"Superseded"` attempt 1 and `"Acknowledged"` attempt 2).

#### Boundaries

* Included: `JsonResidentDecisions` methods in `src/core/tests/test_resident_decisions.py`.
* Excluded: Any `sys.modules` manipulation or unrelated test classes.

#### Likely Targets

* src/core/tests/test_resident_decisions.py: Formal-route forwarding and supersession test section.

#### Dependencies

* P01-T01

#### Validation Expectations

* Focused test methods fail if P01-T01 is reverted and pass on both `JsonResidentDecisions` and `SqlResidentDecisions`.

#### Completion Evidence

* Test diff and passing `unittest` run in `src/core`.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `src/core/README.md` formal-route supersession documentation

#### Context

`src/core/README.md` (`Formal complaints and independent review forwarding`) currently states in its unresolved-retry paragraph (`lines 536-540`) that a failed outcome save stays `Pending` and lists `Pending`, `Unconfirmed`, and legacy `Failed` without `not_sent` as unresolved, and then in its `Pending supersession` paragraph (`lines 555-595`) describes `service_supersede_authorize` (`manual_verified` two-person supersession without resending). Synchronizing both paragraphs keeps documentation completely consistent with `_res_service_forward` marking stale `Pending` attempts `Superseded` (`superseded_by_attempt`) when an explicit `retry_unresolved` retry reserves a superseding attempt.

#### Intent

Synchronize both the unresolved-retry paragraph and the `Pending supersession` paragraph in `src/core/README.md` so:
* The unresolved-retry paragraph qualifies that a failed outcome save stays `Pending` until superseded and lists `Pending`, `Unconfirmed`, `Superseded`, and legacy `Failed` without `not_sent` as unresolved.
* The `Pending supersession` paragraph contrasts `service_supersede_authorize` (`manual_verified` two-person supersession without resending, recording `supersession`) with explicit `service_forward` (`retry_unresolved=True` when no send is in flight, marking prior `Pending` attempts `Superseded` with `superseded_from="Pending"`, `superseded_at`, and `superseded_by_attempt` without creating a `supersession` dual-approval record), preserving `route_key`, full attempt history, and late-outcome fencing.

#### Boundaries

* Included: `src/core/README.md` formal-route section.
* Excluded: Unrelated README sections or regulatory snapshots.

#### Likely Targets

* src/core/README.md: Formal-route forwarding and supersession paragraphs.

#### Dependencies

* P01-T01

#### Validation Expectations

* Git diff and Markdown readability/link check on `src/core/README.md`.

#### Completion Evidence

* Clean diff in `src/core/README.md`.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: `src/core` Validation Gate

### Context

Repository instructions classify this bounded `src/core` bugfix + unit test + component README update under the focused validation tier, and the caller brief mandates exact `src/core` checks (`mypy`, `ruff check . && ruff format --check .`, and focused `unittest` suite covering `resident_decisions`).

### Intent

Prove zero static-typing, lint, formatting, or behavioral regressions in `src/core`.

### Boundaries

* Included: Executing `mypy`, `ruff`, and `unittest` from `src/core`.
* Excluded: Pushing to remote or altering CI workflows.

### Likely Targets

* src/core/: Validation working directory.

### Dependencies

* P01, P02

### Validation Expectations

* `python3 -m mypy` -> exit `0`
* `python3 -m ruff check . && python3 -m ruff format --check .` -> exit `0`
* `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` -> exit `0`

### Completion Evidence

* Recorded command outputs and exit codes in `.copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md`.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run `mypy`, `ruff check`, `ruff format --check`, and `unittest` suites in `src/core`

#### Context

All three required toolchains (`mypy`, `ruff`, `unittest`) are installed in the local Python 3.12.3 environment.

#### Intent

Run all mandated `src/core` checks and confirm zero warnings/errors and zero `del sys.modules` usage.

#### Boundaries

* Included: `mypy`, `ruff check .`, `ruff format --check .`, `unittest` (`test_resident_decisions.py` and full `src/core/tests`).
* Excluded: Unrelated package installations.

#### Likely Targets

* src/core/: Command execution root.

#### Dependencies

* P01-T01, P02-T01, P02-T02

#### Validation Expectations

* All commands exit `0`.

#### Completion Evidence

* Verification table in `.copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md`.

#### Unresolved Items

* none
