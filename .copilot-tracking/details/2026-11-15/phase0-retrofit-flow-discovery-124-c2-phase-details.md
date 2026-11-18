<!-- markdownlint-disable-file -->
# Phase Details: Phase 0 Retrofit-Flow Discovery Contract c2 Hardening (Issue #124)

## Metadata

* Task ID: issue-124-c2
* Task slug: phase0-retrofit-flow-discovery-124-c2
* Date: 2026-11-15
* Companion plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c2-plan.md
* Prior review evidence: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c1-review.md

## Initial Phase Direction and Context

* Phase `P01` closes all five `c1` adversarial bypasses/edge cases in `src/core/src/zava_forward/core/discovery_contract.py` without external dependencies or breaking existing public APIs.
* Phase `P02` locks those invariants with focused adversarial regression tests in `src/core/tests/test_discovery_contract.py`, updates coupled Phase 0 docs concisely, runs the focused validation suite, and commits locally.

## Test Ownership and Validation Contract

* Canonical test file: `src/core/tests/test_discovery_contract.py`
* Exact removals: `none` (`0` existing tests removed)
* Maximum new test methods: `6`
* Generated targets: `none`
* Semantic vs regression coverage:
  * Provenance / tamper refusal (`AC-C2-1`, `AC-C2-2`): blank-digest `replace(...)` forgery refusal on both candidate and validated reports; validated `Mapping` containing unvalidated/gapped `FlowDiscoveryReport`; mutated `asdict(validated)` and `validated.to_json_dict()` refusal; valid `json.loads(json.dumps(validated.to_json_dict()))` acceptance.
  * Container lock (`AC-C2-3`): `FrozenDict.__init__`, `setattr`, and `delattr` `TypeError` assertions alongside `asdict` and `deepcopy` preservation.
  * Cutoff & window boundaries (`AC-C2-4`): incomplete active-work pair with one post-`as_of` timestamp excluded with post-`as_of` gap; `window_end` `23:59:59.500000Z` candidate retained.
* Validation commands (`TMPDIR=/dev/shm`):
  * `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v`
  * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`
  * `cd src/core && TMPDIR=/dev/shm python3 -m ruff check . && TMPDIR=/dev/shm python3 -m ruff format --check . && TMPDIR=/dev/shm mypy`

<!-- rpi:phase id=P01 -->
## P01: Close Provenance, Mapping Guard, `FrozenDict`, and Timestamp Cutoff Bypasses in `discovery_contract.py`

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement evaluated digest provenance, `Mapping` guard parity, `to_json_dict()`, and `FrozenDict.__init__` lock

* Target file: `src/core/src/zava_forward/core/discovery_contract.py`
* Evidence: `c1` `RV-001`, `RV-002`, `RV-003`.
* Implementation context:
  1. `FrozenDict` (`PC-003`):
     * Declare `__slots__ = ("_frozen",)`.
     * Provide `@overload` signatures on `__init__` (`()`, `(Mapping[K, V], /)`, `(Iterable[tuple[K, V]], /)`, `(**kwargs: V)`) over `def __init__(self, *args: Any, **kwargs: Any) -> None`: if `getattr(self, "_frozen", False)` is `True`, raise `TypeError("FrozenDict does not support re-initialization")`; otherwise call `super().__init__(*args, **kwargs)` and `object.__setattr__(self, "_frozen", True)`.
     * Override `__setattr__` and `__delattr__` to raise `TypeError("FrozenDict does not support attribute mutation")`.
  2. Evaluated & validated calculation provenance (`PC-001`):
     * Maintain `_EVALUATED_FLOW_REPORT_REFS: dict[int, weakref.ref[FlowDiscoveryReport]] = {}`, `_EVALUATED_FLOW_REPORT_DIGESTS: set[str] = set()`, and `_VALIDATED_FLOW_REPORT_SEALS: set[tuple[str, str, str, str]] = set()` (storing `(calculation_digest, owner_validated_by, owner_validated_on_iso, validation_note)`). Using a module-private `id(report)` weakref map avoids adding a private dataclass field that `dataclasses.asdict(report)` would copy/serialize.
     * Extract `_compute_flow_report_digest(...) -> str` and call it inside `evaluate_property_flow` before constructing `FlowDiscoveryReport(..., calculation_digest=digest)`, then call `_register_evaluated_report(report)` to register both its weakref instance identity and `_EVALUATED_FLOW_REPORT_DIGESTS.add(digest)`.
     * In `FlowDiscoveryReport.__post_init__`: freeze `_FLOW_REPORT_CONTAINER_FIELDS`, always call `self.verify_digest()` (never auto-populating a blank `calculation_digest`), and when `self.owner_validated` is `True` (after verifying formal human sign-off fields), require `self.calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS` and `(self.calculation_digest, self.owner_validated_by.strip(), self.owner_validated_on.isoformat(), self.validation_note.strip()) in _VALIDATED_FLOW_REPORT_SEALS`.
     * In `validate_flow_report(report, ...)`: verify `report.verify_digest()`, require `_is_evaluated_report_instance(report)` and `report.calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS` (blocking same-cohort `replace(gapped_report, gaps=(), calculation_digest=colliding_digest)`), register `(report.calculation_digest, clean_by, on.isoformat(), clean_note)` in `_VALIDATED_FLOW_REPORT_SEALS`, construct `validated = replace(report, ..., calculation_digest=report.calculation_digest)`, call `_register_evaluated_report(validated)`, and return `validated`.
     * In `Phase0DiscoveryPack.__post_init__`: always run `self.flow_report.verify_digest()`, and when `self.owner_validated` is `True` also require `self.flow_report.calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS` and `(self.flow_report.calculation_digest, self.flow_report.owner_validated_by.strip(), self.flow_report.owner_validated_on.isoformat(), self.flow_report.validation_note.strip()) in _VALIDATED_FLOW_REPORT_SEALS`.
     * Add `FlowDiscoveryReport.to_json_dict(self) -> FrozenDict[str, object]` constructing `FrozenDict[str, object]((k, _freeze_value(v)) for k, v in raw.items())` directly (`PC-003`).
  3. `enforce_governance_guard` parity on `FlowDiscoveryReport`, `Phase0DiscoveryPack`, and `Mapping` (`PC-002`, `PC-003`):
     * Define `_FLOW_REPORT_SIGNATURE_KEYS` as all 20 flow-report-unique keys (the 19 non-`gaps` digest payload keys plus `"calculation_digest"`).
     * `_strict_iso_date(value: object, field_name: str) -> str` accepts `date` (explicitly rejecting `isinstance(value, datetime)`) or a strict 10-character `YYYY-MM-DD` `str` parsed via `date.fromisoformat`, raising `GovernanceViolationError` on any invalid type or value.
     * `_verify_flow_report_mapping(m: Mapping[str, object], *, require_validated: bool) -> None` wraps payload canonicalization and JSON hashing errors (`KeyError`, `TypeError`, `ValueError`) in `GovernanceViolationError`, verifies all 20 digest fields match non-blank `m["calculation_digest"]`, and when `require_validated=True` also verifies `m.get("owner_validated") is True`, `m.get("finding_status") == VALIDATED_FINDING_STATUS`, `not m.get("gaps")`, `not m.get("invalid_accepted_handover_ids")`, `is_valid_human_actor(...)`, `_strict_iso_date(m.get("owner_validated_on"), "owner_validated_on")`, non-blank `str` `validation_note`, `digest in _EVALUATED_FLOW_REPORT_DIGESTS`, and `(digest, clean_by, on_iso, clean_note) in _VALIDATED_FLOW_REPORT_SEALS`.
     * When `"flow_report" in output` on any `Mapping` (candidate or validated), reject non-`FlowDiscoveryReport`/non-`Mapping` values (including `None`), run recursive `enforce_governance_guard(nested_flow, discovery_owner=discovery_owner, dictionary=dictionary)` and (for `Mapping`) `_verify_flow_report_mapping(nested_flow, require_validated=owner_val)`, and when `owner_val` is `True` require `nested_flow` itself to be owner-validated (`nested_flow.owner_validated is True` or `nested_flow.get("owner_validated") is True`).
* Completion expectations: Zero bypasses across dataclass, `replace(...)`, `asdict(...)`, `to_json_dict()`, or nested `Mapping` wrappers.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Fix incomplete active-timestamp `as_of` ordering and `window_end` UTC calendar-date comparison in `evaluate_property_flow`

* Target file: `src/core/src/zava_forward/core/discovery_contract.py`
* Evidence: `c1` `RV-004`, `RV-005`.
* Implementation context:
  1. Candidate window filter: replace `start_dt` / `end_dt` (`23:59:59`) check with `if window_start <= ident_dt.date() <= window_end:` after verifying `ident_dt.date() <= as_of`, retaining timestamps such as `2026-09-30T23:59:59.500000Z`.
  2. Stage active-work timestamp filter: parse `act_s` (when `st.active_started_at.strip()`) and `act_e` (when `st.active_completed_at.strip()`), then check:
     ```python
     if (act_s is not None and act_s.date() > as_of) or (
         act_e is not None and act_e.date() > as_of
     ):
         gaps.append(
             f"Property {st.property_id} stage '{st.stage_code}' active-work timestamp "
             f"is after as_of '{as_of.isoformat()}'"
         )
         continue
     ```
     before checking `if not st.active_started_at.strip() or not st.active_completed_at.strip() or act_s is None or act_e is None:`.
* Completion expectations: Post-`as_of` partial active-work timestamps record an `after as_of` gap and skip the stage row; `window_end` fractional-second candidates are included.

<!-- rpi:phase id=P02 -->
## P02: Adversarial Regression Tests, Documentation Sync, and Focused Validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add focused regression tests for `c1` `RV-001`–`RV-005` in `test_discovery_contract.py`

* Target file: `src/core/tests/test_discovery_contract.py`
* Completion expectations: Add `<= 6` focused regression tests (`0` removals) asserting every `AC-C2-1`–`AC-C2-4` path.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Align Phase 0 documentation, run focused validation (`TMPDIR=/dev/shm`), and commit `c2` locally

* Target files: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`.
* Completion expectations: Accurate documentation with zero `.copilot-tracking/` leaks, 100% green focused validation suite, and clean local Conventional Commit (`Refs #124` + Copilot trailer) before `c2` `rpi-review`.
