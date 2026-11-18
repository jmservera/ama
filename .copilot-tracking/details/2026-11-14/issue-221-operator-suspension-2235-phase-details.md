<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #221 Operator Suspension, Incident and Restart Record (Criteria 5 & 6)

## Metadata

* Task ID: issue-221-operator-suspension-2235
* Task slug: issue-221-operator-suspension-2235
* Related plan: .copilot-tracking/plans/2026-11-14/issue-221-operator-suspension-2235-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/issue-221-operator-suspension-2235-research.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/method/operator-suspension-drill-protocol.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Implement RULE-024 Restart Authority Validation in Core | ready | P01, P01-T01, P01-T02 |
| P02 | Add Comprehensive RULE-024 & NFR-014 End-to-End Drill Tests and Validate | ready | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement RULE-024 Restart Authority Validation in Core

### Context

Research (`C5`, `C6`, `C8`, `C9`, `C14`, `C15`) established that while `governance.py` and `continuity.py` stamp `restart_rule="RULE-024"` and `automatic_restart=False`, both modules accept placeholder strings (`"TBD"`, `"none"`, `"unknown"`, etc.), chat-memory citations, AI/automation attributions, and self-designation by the recording/suspending operator; `continuity.restart_propose` does not block `automatic=True` or validate `restart_authority` beyond `.startswith("Unavailable")`; and `governance.breach_restart` does not enforce separation between the post-breach `RULE-020` release recorder (`rel["recorded_by"]`) and the restart authoriser. At the same time, contrarian checks (`C4`, `C8`, `C14`, `C15`) proved three critical invariants: (1) omitted `restart_authority` on `continuity.suspend` must still default to `"Unavailable: OD-35 authority unappointed"` so immediate incident containment never fails closed; (2) human job titles containing `"Assistant"` or `"Services"` (such as `"Assistant Director of Assets"`) must remain valid; and (3) `continuity.control_record` must keep free-text `restart_authority` redacted for non-reason viewers.

### Intent

Centralize `RULE-024` authority validation and distinct-human separation in a strictly typed `zava_forward.core.restart_authority` module and wire it cleanly into `governance.py` and `continuity.py`.

### Boundaries

* Included: `src/core/src/zava_forward/core/restart_authority.py`, `src/core/src/zava_forward/core/governance.py`, `src/core/src/zava_forward/core/continuity.py`, and `src/core/README.md`.
* Excluded: Changing HTTP route paths or auth schemes in `src/api/src/zava_forward/api/server.py` (`server.py` already maps `ValueError` -> 400 and `PermissionError` -> 403 and enforces `trusted_route` on `/api/continuity/restart-decide`), altering audience-limited redaction of `restart_authority`, or completing the human drill record in `docs/reference/method/operator-suspension-drill-protocol.md`.

### Likely Targets

* `src/core/src/zava_forward/core/restart_authority.py`: New strictly typed `RULE-024` validation helper.
* `src/core/src/zava_forward/core/governance.py`: `breach_record` and `breach_restart` authority validation, actor metadata recording, and breach/release/restart actor separation.
* `src/core/src/zava_forward/core/continuity.py`: `suspend`, `restart_propose`, and `restart_decide` authority validation, `automatic` refusal, actor separation, and `restart_rule="RULE-024"` stamping on restart decision records.
* `src/core/README.md`: Accurate documentation of `RULE-024` validation and actor separation.

### Dependencies

* None.

### Validation Expectations

* `python3 -m mypy` in `src/core` strictly checks `restart_authority.py` with 0 errors.
* `python3 -m ruff check . && python3 -m ruff format --check .` in `src/core` passes with 0 errors.

### Completion Evidence

* `restart_authority.py` exists, is imported by `governance.py` and `continuity.py`, and passes `mypy --strict` and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Create strictly typed `restart_authority.py` validator module

#### Context

`src/core/pyproject.toml` applies `mypy` (`strict = true`) and `ruff` (`E,F,I,B,UP`, line-length 100) to all new modules in `src/zava_forward/core/`. Placing `RULE-024` authority and distinct-person validation in `restart_authority.py` ensures full strict static type checking and avoids duplicating subtle token/actor logic across `governance.py` and `continuity.py`.

#### Intent

Provide pure, deterministic functions for validating `restart_authority` / `authority_ref`, rejecting automatic restarts, and verifying distinct human actors across email, name, staff code, and Entra OID.

#### Boundaries

* Included:
  * Constants: `RULE_024 = "RULE-024"`, `UNAPPOINTED_RESTART_AUTHORITY = "Unavailable: OD-35 authority unappointed"`.
  * Privacy non-echo rule (`PC-002`): NO error message in `restart_authority.py` may interpolate raw `value` or actor PII (`email`, `name`, `code`, `oid`), preventing privacy-canary leakage into HTTP error responses or `_incident_action` denial audit logs.
  * `reject_automatic_restart(body: Mapping[str, Any]) -> None`: raises `PermissionError("RULE-024 forbids automatic restart after a guardrail breach or operator suspension.")` if `"automatic"` is present and not `False` / `None`.
  * `validate_restart_authority(value: object, *, label: str = "the restart authority (OD-35)", limit: int = 200, allow_unappointed_default: bool = False, disallowed_actors: Sequence[Mapping[str, Any] | str | None] = (), authority_error: type[Exception] = ValueError) -> str`:
    * Strips string and checks `1 <= len(text) <= limit` (else `ValueError(f"Enter {label} (up to {limit} characters).")`).
    * Rejects chat-memory citations via `controls.is_memory_reference(text)` with `ValueError(f"Do not cite chat memory as {label}; record an accountable human authority under RULE-024.")`.
    * When `allow_unappointed_default=True` and `text == UNAPPOINTED_RESTART_AUTHORITY`, returns `UNAPPOINTED_RESTART_AUTHORITY`.
    * Rejects exact casefolded placeholder values (`unknown`, `unavailable`, `none`, `null`, `n/a`, `na`, `tbd`, `todo`, `tbc`, `pending`, `placeholder`, `unapproved`, `unappointed`, `unassigned`, `unset`, `default`, `self`, `same operator`, `same person`, `-`, `--`, `?`), `startswith("unavailable")` (case-insensitive), and word-boundary placeholder tokens/phrases (`tbd`, `todo`, `tbc`, `placeholder`, `unappointed`, `unassigned`, `unapproved`, `same operator`, `same person`) by raising `authority_error` citing `RULE-024` (`PC-002`, `PC-003`).
    * Rejects AI/automated attributions: word tokens in `{"ai", "bot", "automation", "automated", "automatic", "copilot", "llm", "cron", "daemon"}` or multi-word phrases `("ai assistant", "ai agent", "automated system", "autonomous agent", "system auto")` by raising `authority_error` citing `RULE-024` (preserving human titles like `"Assistant Director of Assets"` or `"Building Safety Services Lead"` and all existing fixtures `"OD-35 demo"`, `"Delegation ref D-1"`, `"Constructed fixture authority, not OD-35 appointment"`, `"SYNTHETIC-MUTATION-PRIVATE-122"`).
    * Rejects self-designation against every entry in `disallowed_actors` (checking normalized `email` and `oid` exact/substring matches plus alphanumeric-boundary `(?<![A-Za-z0-9])...(?![A-Za-z0-9])` matches on non-empty `code` and `name` with `len >= 3`) by raising `PermissionError` citing `RULE-024` (`PC-003`).
  * `actor_snapshot(user: Mapping[str, Any]) -> dict[str, Any]`: captures `email`, `name`, `code`, `role`, `oid`, `auth_source` cleanly.
  * `ensure_distinct_restart_actor(user: Mapping[str, Any], *prior_actors: Mapping[str, Any] | str | None, prior_role_description: str) -> None`: inspects every non-None item in `prior_actors` without short-circuiting (`PC-001`), checks normalized `email`, `name`, `code`, and `oid` collisions, and raises static `PermissionError` citing `RULE-024` if the same person attempts to adjudicate or authorise restart.
* Excluded: Store persistence or HTTP routing.

#### Likely Targets

* `src/core/src/zava_forward/core/restart_authority.py`: New module.

#### Dependencies

* `src/core/src/zava_forward/core/controls.py` (`is_memory_reference`).

#### Validation Expectations

* `mypy` and `ruff` pass with 0 issues on `restart_authority.py`.

#### Completion Evidence

* Unit tests in P02-T01 exercise valid human names, role/delegation strings, unappointed sentinel mode, placeholders, memory refs, AI tokens, and actor collisions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce RULE-024 authority and actor separation in `governance.py` and `continuity.py`

#### Context

Both `governance.py` (programme/home/archetype/work-package/workstream guardrail breaches) and `continuity.py` (AI task/release incident suspensions) enforce `RULE-024`. Wiring both through `restart_authority.py` closes all remaining gaps identified in Wave 2 (`C5`, `C6`).

#### Intent

Ensure every breach/suspension record and every restart proposal/decision enforces `RULE-024` without breaking emergency suspension or privacy redaction.

#### Boundaries

* Included:
  * In `governance.breach_record`: validate `restart_authority` via `validate_restart_authority(body.get("restart_authority"), allow_unappointed_default=False, disallowed_actors=(user,), authority_error=ValueError)`, reject memory references in `evidence` / `containment` / `remediation`, and include `actor=actor_snapshot(user)`, `restart_rule="RULE-024"`, and `automatic_restart=False`.
  * In `governance.breach_restart`: call `reject_automatic_restart(body)`; resolve `rel_staff` from `self.staff` matching `rel.get("recorded_by")` so email-only release records carry `name`/`code`/`oid` (`PC-001`); verify `ensure_distinct_restart_actor(user, b.get("actor"), b.get("recorded_by"), prior_role_description="recorded the breach")` AND `ensure_distinct_restart_actor(user, rel_staff, rel.get("recorded_by"), prior_role_description="recorded the post-breach release decision")`; re-validate stored `b.get("restart_authority")` with `authority_error=PermissionError` (`disallowed_actors=(b.get("actor"), b.get("recorded_by"))`); validate `authority_ref` via `validate_restart_authority(body.get("authority_ref"), label="the restart authority reference", allow_unappointed_default=False, disallowed_actors=(b.get("actor"), b.get("recorded_by")), authority_error=PermissionError)` (`ValueError` for blank/overlong/memory-ref, `PermissionError` for non-blank unappointed/placeholder/AI/self-designated, `PC-002`); enforce `authority == expected_authority` (else `PermissionError`); validate `remediation_evidence` with `no_memory=True`; and stamp `restart_rule="RULE-024"` and `automatic_restart=False` on `b["restart"]`.
  * In `continuity.suspend`: resolve raw `body.get("restart_authority")`; if `None`, default to `UNAPPOINTED_RESTART_AUTHORITY`; validate via `validate_restart_authority(raw, allow_unappointed_default=True, disallowed_actors=(user,), authority_error=ValueError)`; include `name` in `actor` snapshot alongside `email`, `role`, `code`, `oid`, `auth_source`.
  * In `continuity.restart_propose`: call `reject_automatic_restart(body)`; validate `s.get("restart_authority")` via `validate_restart_authority(..., allow_unappointed_default=False, disallowed_actors=(s.get("actor"), s.get("recorded_by"), user), authority_error=PermissionError)` (converting blank/missing stored authority into `PermissionError("Restart requires an appointed OD-35 restart authority before proposal.")`); include `name` in `proposal["actor"]`.
  * In `continuity.restart_decide`: call `reject_automatic_restart(body)`; enforce `ensure_distinct_restart_actor` UNCONDITIONALLY before branching on `decision` (`PC-001`) against both suspender (`s.get("actor")`, `s.get("recorded_by")`) and proposer (`prop.get("actor")`, `prop.get("by")`) so neither suspender nor proposer can adjudicate `"Restart"` or `"Keep suspended"`; when `decision == "Restart"`, validate stored `s.get("restart_authority")` (raising `PermissionError` if blank/unappointed/invalid) and `body.get("authority_ref")` via `validate_restart_authority(..., disallowed_actors=(s.get("actor"), s.get("recorded_by"), prop.get("actor"), prop.get("by")), authority_error=PermissionError)` (`PC-002`), and enforce exact equality `authority_ref == s["restart_authority"]` (`PermissionError`); stamp `restart_rule="RULE-024"` and `automatic_restart=False` on `rec`.
  * Update `src/core/README.md` governance bullet to reflect `RULE-024` distinct human authority and breach/release/restart separation.
* Excluded: Changing `continuity.control_record` free-text redaction.

#### Likely Targets

* `src/core/src/zava_forward/core/governance.py`
* `src/core/src/zava_forward/core/continuity.py`
* `src/core/README.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing `test_governance.py`, `test_continuity.py`, `test_continuity_epoch_export.py`, `test_rai_harm_threshold_incident.py`, and `test_operator_suspension.py` pass without regression.

#### Completion Evidence

* Updated modules and `README.md` cleanly enforce all `RULE-024` invariants.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Add Comprehensive RULE-024 & NFR-014 End-to-End Drill Tests and Validate

### Context

Issue #221 Criterion 6 (`NFR-014`) and Criterion 5 (`RULE-024`) require end-to-end automated verification that:
1. Guardrail breach and incident suspension records name and validate `restart_authority` per `RULE-024` (rejecting blank, placeholder, non-human, memory-cited, and self-approved authorities).
2. During suspension / guardrail breach pause, AI task dispatch and reliance on pending/ready/in-flight proposals are blocked and routine progression on paused homes/archetypes is halted, **while manual case work on unaffected homes AND emergency/statutory Awaab's Law hazard response (`raise_hazard`, hazard referral, specialist receipt, acceptance, and repair completion) on the paused/affected home itself continue without AI or governance-pause obstruction**.
3. Premature, failing-test, non-constructed, automatic, unappointed, placeholder, mismatched-authority, untrusted-route, and self-approved (breach recorder, suspender, proposer, or release recorder) restart attempts are refused, and only a distinct authorised human clears the drill hold while keeping live `actual_hold=True`.

### Intent

Add focused, high-signal unit and end-to-end drill tests in `src/core` and `src/api`, and verify zero static or runtime errors across both packages.

### Boundaries

* Included: `src/core/tests/test_operator_suspension_drill.py` (new strictly typed module), `src/core/tests/test_governance.py`, and `src/api/tests/test_operator_suspension.py`, plus running `mypy`, `ruff check`, `ruff format --check`, and `unittest`.
* Excluded: Modifying unrelated test files or running live external cloud tests.

### Likely Targets

* `src/core/tests/test_operator_suspension_drill.py`
* `src/core/tests/test_governance.py`
* `src/api/tests/test_operator_suspension.py`

### Dependencies

* P01.

### Validation Expectations

* In `src/core`:
  * `python3 -m mypy` -> 0 errors
  * `python3 -m ruff check . && python3 -m ruff format --check .` -> 0 errors
  * `PYTHONPATH=src:tests python3 -m unittest discover -s tests -v` -> all pass
* In `src/api`:
  * `python3 -m mypy` -> 0 errors
  * `python3 -m ruff check . && python3 -m ruff format --check .` -> 0 errors
  * `PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests python3 -m unittest discover -s tests -v` -> all pass (`PC-004`)

### Completion Evidence

* Recorded command outputs and pass counts in `.copilot-tracking/changes/2026-11-14/issue-221-operator-suspension-2235-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `src/core` RULE-024 unit tests and end-to-end NFR-014 guardrail/continuity drill suite

#### Context

`src/core` owns both `governance.py` (`breach_record` / `breach_restart` / `guard_case_event`) and `continuity.py` (`suspend` / `restart_propose` / `restart_decide`) as well as `workflows.py` (`raise_hazard`, `log_call`, hazard referral lifecycle). A strictly typed drill test module in `src/core/tests/test_operator_suspension_drill.py` (typing store instances as `Any` so `src/core/pyproject.toml` requires zero edits while keeping full `mypy --strict` checking across the test module, `PC-004`) plus `GovMixin` tests in `src/core/tests/test_governance.py` give direct coverage on both JSON `Store` and SQLite-backed `SqlStore`.

#### Intent

Verify every `RULE-024` authority validation rule and execute the complete `core` `NFR-014` suspension + guardrail pause + manual fallback + statutory hazard response + distinct-human restart drill on both `Store` and `SqlStore`.

#### Boundaries

* Included:
  * `src/core/tests/test_operator_suspension_drill.py`:
    * `RestartAuthorityRule024Tests`: tests valid human names and job titles (including `"Assistant Director of Assets"` and `"Building Safety Services Lead"`), blank/overlong strings, exact and composite placeholders (`"TBD"`, `"OD-35: TBD"`, `"none"`, `"N/A"`, `"unknown"`, `"Unavailable: OD-35 authority unappointed"`, `"Unappointed: awaiting sponsor"`), valid `controls.MEMORY_REF` citations (`"CM-0123456789ab"`, `"memory:thread-1"`, `"chat-memory"`, `PC-003`), AI/automation attributions (`"AI assistant"`, `"copilot"`, `"automation bot"`), non-echoing privacy canary preservation on errors (`PC-002`), unappointed default allowance for `suspend`, exact and embedded self-designation refusal (`email`, `name`, `code`, `oid`), and `reject_automatic_restart`.
    * `CoreSuspensionAndFallbackDrillMixin` run against both `JsonDrillTests` (`Store`) and `SqlDrillTests` (`SqlStore`):
      1. Records both an AI task suspension (`store.suspend`) and a home/archetype guardrail breach (`store.breach_record`) naming a human `restart_authority`, asserting `restart_rule == "RULE-024"` and `automatic_restart is False`.
      2. Verifies omitted-authority suspension succeeds with `UNAPPOINTED_RESTART_AUTHORITY` for immediate containment while blocking `restart_propose` and `restart_decide`, and explicit placeholder/AI/self-designated `restart_authority` is rejected.
      3. Verifies AI gate blocks suspended scope and `guard_case_event` pauses routine `log_call` on the breach-paused home while manual `log_call` succeeds on unaffected homes.
      4. Verifies emergency & statutory Awaab's Law hazard response (`store.raise_hazard` with Awaab's Law metadata + specialist hazard referral / receipt / acceptance) succeeds unimpeded on the breach-paused and AI-suspended home itself (`RULE-024` / `NFR-014`).
      5. Verifies negative restart matrix (before corrective proposal / post-breach release, failing test, `automatic=True`, placeholder/mismatched `authority_ref`, breach-recorder self-approval, release-recorder self-approval, suspender self-approval, proposer self-approval, and suspender/proposer attempting `"Keep suspended"`).
      6. Verifies `"Keep suspended"` by a distinct third human leaves the AI task suspended, then re-proposal + distinct third human approval (`restart_decide` on SQL store + `breach_restart` after post-breach `Release`) clears the drill hold, records `restart_rule == "RULE-024"`, and restores `guard_case_event`-gated `log_call` on the previously paused home while the unreleased safety hazard hold appropriately remains independent until repair/hazard release (`PC-004`).
  * `src/core/tests/test_governance.py`: add focused `RULE-024` negative checks in `GovMixin` (`breach_record` placeholder/AI/self-designation rejection and `breach_restart` release-recorder self-approval rejection).
* Excluded: HTTP layer (covered in P02-T02) and `src/core/pyproject.toml` edits.

#### Likely Targets

* `src/core/tests/test_operator_suspension_drill.py`
* `src/core/tests/test_governance.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `python3 -m mypy`, `ruff check`, `ruff format --check`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -v` in `src/core` succeed with 0 errors.

#### Completion Evidence

* Passing test output for `test_operator_suspension_drill` and `test_governance`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Strengthen `src/api` HTTP end-to-end NFR-014 operator suspension and fallback drill tests and run full validation

#### Context

`src/api/tests/test_operator_suspension.py` tests the live HTTP `App` + `SqlStore` + `Assistants` stack. Replacing the duplicate `drill(self)` wrapper in `test_nfr_014_suspension_and_manual_fallback_drill` (since `test_incident_snapshot_and_reopen` already executes `drill(self)` which leaves 5 open suspensions, `PC-004`) with a dedicated, isolated 8-step HTTP + `TrustedProxyProvider` / `PasswordProvider` drill proves all 8 steps of `docs/reference/method/operator-suspension-drill-protocol.md` over the actual API routes (`/api/continuity/suspend`, `/api/continuity/restart-propose`, `/api/continuity/restart-decide`, `/api/governance/release`, `/api/governance/breach`, `/api/governance/restart`, `/api/cases/.../hazard`, `/api/cases/.../call`, `/api/continuity`).

#### Intent

Prove the complete HTTP + assistant + workflow fallback + statutory hazard + distinct OID-bound restart drill end-to-end and verify clean `mypy`, `ruff`, and full `unittest` runs across `src/api` and `src/core`.

#### Boundaries

* Included:
  * `src/api/tests/test_operator_suspension.py`:
    * Keep `test_nfr_014_suspension_and_manual_fallback_drill` intact for regression coverage and add `test_nfr_014_http_breach_hazard_and_rule_024_restart_drill` on a clean `Base` fixture (`PC-004`) walking the explicit 8-step protocol over `TrustedProxyProvider` Entra principals (verifying `actors_for_store` cross-provider OID/roster separation as well): (1) queued pending, reviewed ready, and running in-flight proposals before breach; (2) `/api/continuity/suspend` + `/api/governance/breach` naming `RULE-024` `restart_authority` (plus verifying default unappointed containment on another task vs HTTP 400/403 rejection of blank, `"TBD"`, `"AI bot"`, and self-named `restart_authority` without echoing confidential canary values); (3) blocked new dispatch, blocked ready/pending reliance, quarantined in-flight completion, and unaffected AI task isolation; (4) complete incident snapshot & continuity view verification (`restart_rule == "RULE-024"`, `automatic_restart is False`, `actual_hold is True`); (5) manual case call fallback on unaffected home AND emergency/statutory Awaab's Law hazard raise + referral progression on the affected/paused case during active suspension; (6) HTTP 400/403 denial of premature, failing-test, `automatic=True`, mismatched/placeholder `authority_ref`, `PasswordProvider` untrusted-route restart, suspender/proposer self-approval, and release-recorder self-approval restarts, plus `"Keep suspended"` via `TrustedProxyProvider` retaining suspension; (7) passing `constructed-fixture` corrective proposal by distinct `Retrofit Programme Manager` followed by distinct OID-bound `Programme Support Officer` (`ai_restart` via `TrustedProxyProvider`) approval and post-breach `/api/governance/release` (`scope_kind="tranche"` by `self.pm`) + distinct `Programme Support Officer` `/api/governance/restart` clearance (`PC-004`); (8) restored constructed drill task dispatch and cleared home pause (`log_call` succeeds) while `actual_hold` remains `True` and ledger export verifies cleanly.
  * Full validation commands in `src/core` and `src/api` (`mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests`).
* Excluded: Modifying `server.py` unless a test reveals an unexpected HTTP status mapping issue.

#### Likely Targets

* `src/api/tests/test_operator_suspension.py`

#### Dependencies

* P01-T02, P02-T01.

#### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `unittest` suites pass with 0 errors in both `src/core` and `src/api`.

#### Completion Evidence

* Clean `mypy`, `ruff`, and `unittest` logs recorded in `.copilot-tracking/changes/2026-11-14/issue-221-operator-suspension-2235-changes.md`.

#### Unresolved Items

* None.
