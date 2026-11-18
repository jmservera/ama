<!-- markdownlint-disable-file -->
# RPI Changes: Issue #221 Operator Suspension, Incident and Restart Record (Criteria 5 & 6)

## Metadata

* Task ID: issue-221-operator-suspension-2235
* Related plan: .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-221-operator-suspension-2235-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Full plan (`P01`, `P02`) implemented and verified with 0 `mypy` errors, 0 `ruff check` / `ruff format --check` errors, 151 passing relevant unit tests in `src/core`, and 138 passing relevant unit tests in `src/api`.

## Execution Summary

Completed full-plan implementation for Issue #221 Criteria 5 (`RULE-024`) and 6 (`NFR-014`): added strictly typed `zava_forward.core.restart_authority` (including OID-linked `actors_for_store` Entra/password cross-provider identity separation), wired `RULE-024` authority validation and three-person separation across `governance.py` (`release_record`, `breach_record`, `breach_restart`) and `continuity.py` (`suspend`, `restart_propose`, `restart_decide`), updated `src/core/README.md`, and verified comprehensive unit and end-to-end `NFR-014` suspension, manual fallback, statutory Awaab's Law hazard continuity, and distinct-human restart drills across `src/core` and `src/api`.

## Completed Work

### P01: Core RULE-024 Restart Authority Validation (`P01-T01`, `P01-T02`)

* Created `src/core/src/zava_forward/core/restart_authority.py` (`P01-T01`) with strict type annotations implementing `RULE_024`, `UNAPPOINTED_RESTART_AUTHORITY`, `actor_snapshot`, `reject_automatic_restart`, `validate_restart_authority` (rejecting blank, placeholder, composite placeholder, unappointed `"Unavailable..."` strings unless explicitly permitted for emergency containment, `controls.MEMORY_REF` chat-memory references, AI/automation/system designators, and disallowed-actor self-designation via non-echoing `ValueError`/`PermissionError` contracts), and `ensure_distinct_restart_actor` (enforcing distinct actor email/oid/code against all prior roles without short-circuiting).
* Updated `src/core/src/zava_forward/core/governance.py` (`P01-T02`) so `breach_record` validates `restart_authority` against the breach-recording actor, refuses chat-memory citations in `evidence`/`containment`/`resident_impact`/`remediation` via `controls.evidence_text`, and stamps `restart_rule="RULE-024"`, `automatic_restart=False`, and `actor`; updated `breach_restart` to enforce three-person separation across breach recorder, release recorder (resolved via `self.staff`), and restart authoriser, validate `b["restart_authority"]` and `authority_ref` with `authority_error=PermissionError`, reject chat-memory citations in `remediation_evidence`, and stamp `restart_rule="RULE-024"` and `automatic_restart=False`.
* Updated `src/core/src/zava_forward/core/continuity.py` (`P01-T02`) so `suspend` preserves emergency containment when `restart_authority` is omitted while rejecting invalid/self-designated explicit `restart_authority` and `automatic` flags, refuses chat-memory citations in incident fields, and stamps `restart_rule="RULE-024"` and `automatic_restart=False`; updated `restart_propose` and `restart_decide` to reject `automatic` flags, refuse chat-memory citations in corrective fields, validate `s["restart_authority"]` and `authority_ref` with `authority_error=PermissionError`, and enforce distinct human actor separation across suspender, corrective proposer, and restart decision-maker on both `"Restart"` and `"Keep suspended"` outcomes.
* Updated `src/core/README.md` (`P01-T02`) under `Guardrail breach (RULE-024, AC-078)` to document the strengthened `restart_authority` validation and breach/release/restart actor separation.

### P02-T01: Core RULE-024 Unit Tests and End-to-End NFR-014 Drill Suite

* Created `src/core/tests/test_operator_suspension_drill.py` (strictly typed under `mypy` with zero `pyproject.toml` changes) covering `RestartAuthorityUnitTest` (blank, placeholder, composite placeholder, unappointed default, chat-memory, AI/automated designators, valid human titles, self-designation, non-short-circuiting distinct-actor checks, and privacy-canary non-echo assertions) and `OperatorSuspensionDrillMixin` on both `Store` (`JsonOperatorSuspensionDrillTest`) and `SqlStore` (`SqlOperatorSuspensionDrillTest`) proving three-person separation, emergency unnamed-authority containment, full statutory Awaab's Law hazard workflow progression during active guardrail breach + AI suspension, mutual independence of safety holds and `RULE-024` guardrail pauses, and durable reopen verification.
* Extended `src/core/tests/test_governance.py` (`test_breach_names_restart_authority_and_blocks_automatic_restart`) with placeholder, unappointed-default, AI/automatic, chat-memory, self-designation, and release-recorder separation assertions on `JsonGov` and `SqlGov`.

### P02-T02: API HTTP End-to-End NFR-014 & RULE-024 Drill Suite and Validation

* Added `test_nfr_014_http_breach_hazard_and_rule_024_restart_drill` in `src/api/tests/test_operator_suspension.py` (preserving existing `test_nfr_014_suspension_and_manual_fallback_drill` untouched) exercising the complete 8-step `NFR-014` HTTP + `TrustedProxyProvider` + `SqlStore` + `Assistants` drill: queued pending / ready / running in-flight proposals, HTTP `/api/continuity/suspend` + `/api/governance/breach` with `RULE-024` authority validation and non-echoing privacy canary checks, emergency omitted-authority containment, blocked dispatch and proposal reliance, quarantined late completion, unaffected AI task continuity, manual call fallback on unaffected home, statutory Awaab's Law hazard raise + specialist referral/receipt/acceptance/repair progression on the breach-paused and AI-suspended home, negative HTTP 400/403 restart matrix (`PasswordProvider` untrusted route, premature, failing test, `automatic=True`, placeholder/mismatched `authority_ref`, suspender/proposer/breach-recorder/release-recorder self-approval), `"Keep suspended"` retention, distinct OID-bound `Programme Support Officer` `ai_restart` and `/api/governance/restart` clearance, restored constructed drill dispatch while retaining live `actual_hold=True`, and intact audit ledger verification.

## Implementation-Time Plan and Detail Updates

* **Classification: Immediately relevant current-state update (`actors_for_store` Entra OID resolution and `release_record` `actor_snapshot`)**: Executing the new `TrustedProxyProvider` HTTP drill in `P02-T02` revealed that Entra proxy sessions carry pseudonymous `email = "e-<12hex>@entra.invalid"` (`display_email = <email claim>`) linked to roster staff records (`email`, `name`, `code`) via immutable `oid`. Added `actors_for_store` plus `display_email` and `bound` matching in `restart_authority.py`, stamped `actor=actor_snapshot(user)` on `governance.release_record`, and resolved `self.staff.get(rel_email)` in `governance.breach_restart` so self-designation and self-approval are blocked across Entra and password identities in both directions. Reflected in `AC-1` and `P02-T02` details without changing scope or user decisions.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 329 source files` (0 errors) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `All checks passed!` and `276 files already formatted` (0 errors) |
| `PYTHONPATH=src:tests python3 -m unittest test_operator_suspension_drill test_governance test_hazard_referral test_rai_release test_rai_release_invalidation test_rai_threshold_live_approval_guard -v` | `src/core` | Passed | `Ran 151 tests in 42.047s — OK (skipped=17)` (full `src/core` discovery also ran 3,414 tests with 0 failures in any governance, continuity, workflow, or store module; 3 unrelated IoT/CLI modules require uninstalled `azure-iot-hub` SDK or installed console scripts outside this worktree) |
| `python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 280 source files` (0 errors) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `All checks passed!` and `196 files already formatted` (0 errors) |
| `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests python3 -m unittest test_operator_suspension test_continuity test_continuity_epoch_export test_rai_harm_threshold_incident test_assistant_restart_non_replenishment -v` | `src/api` | Passed | `Ran 138 tests in 126.203s — OK (skipped=39)` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `AC-1`, `AC-2`, `AC-3` checked; `AC-4` awaits Review artifact and local commit)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining implementation items)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None within `rpi-implement` scope (`AC-4` closes upon `rpi-review` artifact write and local branch commit).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md, `## Follow-Up Items`
* Live operational `OD-35` appointment and witnessed human drill record: Outside immediate software scope (`docs/reference/method/operator-suspension-drill-protocol.md`); owned by Building Safety Lead, Executive Sponsor, and Project Owner before operational pilot release (`actual_hold=True` remains enforced in software).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`); remaining: none
* Validation coverage: `mypy` (0 errors in `src/core` and `src/api`), `ruff check` & `ruff format --check` (0 errors in `src/core` and `src/api`), `src/core` relevant unit tests (`151` passed, `0` failed), `src/api` relevant unit tests (`138` passed, `0` failed)
* Blockers: none
* Current plan and detail updates: Entra OID cross-provider `actors_for_store` and `release_record` `actor_snapshot` refinement recorded in `plan.md` (`AC-1`), `phase-details.md` (`P02-T02`), and `changes.md`
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved)
* Follow-up items: Live operational `OD-35` appointment and witnessed human drill record
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: confirmed automatic RPI Agent
