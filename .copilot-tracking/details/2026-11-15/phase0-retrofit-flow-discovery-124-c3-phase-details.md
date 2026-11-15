<!-- markdownlint-disable-file -->
# Phase Details: Phase 0 Retrofit-Flow Discovery Contract c3 Final Provenance & Dictionary Binding (Issue #124)

## Metadata

* Task ID: issue-124-c3
* Task slug: phase0-retrofit-flow-discovery-124-c3
* Date: 2026-11-15
* Companion plan: .copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-c3-plan.md
* Prior review evidence: .copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-c2-review.md

## Initial Phase Direction and Context

* Phase `P01` resolves `c2` findings `RV-001`–`RV-005` in `src/core/src/zava_forward/core/discovery_contract.py` in one cohesive update.
* Phase `P02` proves each closure with focused adversarial regression tests in `src/core/tests/test_discovery_contract.py`, aligns Phase 0 docs, runs the focused validation suite, and commits locally.

## Test Ownership and Validation Contract

* Canonical test file: `src/core/tests/test_discovery_contract.py`
* Exact removals: `none` (`0` existing tests removed; adjust existing `tampered_validated = replace(validated)` line in `test_flow_report_freezes_nested_mappings_and_verifies_calculation_digest` to `copy.deepcopy(validated)` since external `replace(validated)` is now deliberately blocked by `FR-C3-3`!)
* Maximum new test methods: `5`
* Generated targets: `none`
* Semantic vs regression coverage:
  * Dictionary binding (`AC-C3-1`): `evaluate_property_flow` with extra unapproved stage rejected by `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard` against clean validated dictionary; pre-sign-off evaluation + post-sign-off validation of identical dictionary schema accepted.
  * Pack signer parity (`AC-C3-2`): `Phase0DiscoveryPack(..., owner_validated=True)` with mismatched `flow_report.owner_validated_by`, `dictionary_report.owner_validated_by`, or `constraint_register.owner_validated_by` rejected in constructor.
  * Seal replay & `replace` gate (`AC-C3-3`): external `replace(gapped_report, ..., owner_validated=True, calculation_digest=clean_report.calculation_digest)` and `replace(validated)` rejected even after `clean_report` is signed; `copy.deepcopy(validated)` accepted.
  * Cross-process JSON round-trip (`AC-C3-4`): `subprocess.run([sys.executable, "-c", ...])` verifies `enforce_governance_guard(json.loads(payload), discovery_owner=owner, dictionary=dictionary)` passes in a brand-new process and fails when mutated or checked against an altered dictionary.
* Validation commands (`TMPDIR=/dev/shm`):
  * `PATH="/dev/shm/zf-124-c1-venv/bin:$PATH" TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_discovery*.py' -v`
  * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_live_doc_links.py src/core/tests/test_dependency_rule.py -v`
  * `cd src/core && TMPDIR=/dev/shm python3 -m ruff check . && TMPDIR=/dev/shm python3 -m ruff format --check . && TMPDIR=/dev/shm mypy`

<!-- rpi:phase id=P01 -->
## P01: Implement Dictionary Schema Binding, Pack Signer Parity, `ContextVar` Seal Gate, and Cross-Process Mapping Verification

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add `dictionary_schema_digest` binding, `Phase0DiscoveryPack` signer parity, `_ALLOW_VALIDATED_FLOW_REPORT_INIT` gate, and cross-process `Mapping` verification

* Target file: `src/core/src/zava_forward/core/discovery_contract.py`
* Evidence: `c2` `RV-001`–`RV-005`.
* Implementation context:
  1. `_dictionary_schema_digest(dictionary: LifecycleDictionary) -> str`:
     * Serialize structural fields via `json.dumps(..., sort_keys=True, separators=(",", ":"))` and hash with SHA-256:
       * `stages`: `[(s.order, s.code, s.name, s.kind, s.entry_event, s.exit_event, s.pas2035_role_boundary, s.owner_role) for s in dictionary.stages]`
       * `events`: `[(e.event, e.stage_code, e.meaning, e.distinct_from_note, e.owner_role) for e in dictionary.events]`
       * `timestamps`: `[(t.code, t.applies_to, t.meaning, t.precision_rule, t.non_imputation_rule, t.owner_role) for t in dictionary.timestamps]`
       * `wait_states`: `[(w.code, w.meaning, w.accountable_domain, w.clock_rule, w.unknown_cause_rule, w.owner_role) for w in dictionary.wait_states]`
       * `return_loops`: `[(r.kind, r.meaning, list(r.allowed_target_stages), r.non_inference_rule, r.owner_role) for r in dictionary.return_loops]`
     * Add `dictionary_schema_digest: str = ""` to `LifecycleDictionaryReport` (populated in `summarize_lifecycle_dictionary`) and `FlowDiscoveryReport` (included in `_FLOW_REPORT_DIGEST_KEYS` -> 21 digest keys, `_FLOW_REPORT_SIGNATURE_KEYS`, `_compute_flow_report_digest`, `evaluate_property_flow`, and `to_json_dict()`).
     * Add `_verify_report_matches_dictionary(report_or_mapping: FlowDiscoveryReport | Mapping[str, object], dictionary: LifecycleDictionary) -> None`: requires `dictionary_schema_digest == _dictionary_schema_digest(dictionary)` and checks every `stage_code` in `stage_metrics`, exception key in `state_counts`, `attributed_party` in `waits_by_party` (known wait domains or `"unattributed"`), and return-loop `kind` in `return_loops_by_property` against `dictionary`, raising `GovernanceViolationError` on any mismatch.
     * Call `_verify_report_matches_dictionary` inside `validate_flow_report`, `Phase0DiscoveryPack.__post_init__` (for both candidate and validated packs), and `enforce_governance_guard` BEFORE the candidate `if not owner_val:` return whenever `dictionary is not None` (`PC-002`). On `Phase0DiscoveryPack`, also verify `_dictionary_schema_digest(output.dictionary) == _dictionary_schema_digest(dictionary)` whenever `dictionary is not None` (`PC-001`). Require non-blank `report.dictionary_schema_digest == _dictionary_schema_digest(dictionary)` inside `validate_lifecycle_report`, `Phase0DiscoveryPack.__post_init__` (`owner_validated=True`), and `enforce_governance_guard` (`LifecycleDictionaryReport` when `owner_validated=True`).
  2. `Phase0DiscoveryPack.__post_init__` signer & sub-artifact parity:
     * Verify `self.dictionary_report.dictionary_schema_digest == _dictionary_schema_digest(self.dictionary)` (when non-blank, and required non-blank when `owner_validated=True`) and count parity (`stage_count == len(self.dictionary.stages)`, etc.), plus `_verify_report_matches_dictionary(self.flow_report, self.dictionary)`.
     * When `self.owner_validated` is `True`, require `expected_owner = self.discovery_owner.owner.strip()` to equal `self.owner_validated_by.strip()`, `self.dictionary_report.owner_validated_by.strip()`, `self.flow_report.owner_validated_by.strip()`, and `self.constraint_register.owner_validated_by.strip()`, and require accepted hypotheses in `self.constraint_register.hypotheses` to have `h.owner_validated and h.discovery_owner_validated_by.strip() == expected_owner` while disputed hypotheses remain unvalidated (`not h.owner_validated`).
  3. `_ALLOW_VALIDATED_FLOW_REPORT_INIT` `ContextVar[bool]` gate (`PC-003`):
     * Declare `_ALLOW_VALIDATED_FLOW_REPORT_INIT: ContextVar[bool] = ContextVar("_ALLOW_VALIDATED_FLOW_REPORT_INIT", default=False)` and store 5-tuples `(calculation_digest, dictionary_schema_digest, actor, on_iso, cleaned_note)` in `_VALIDATED_FLOW_REPORT_SEALS`.
     * In `FlowDiscoveryReport.__post_init__`, when `self.owner_validated` is `True`, require `_ALLOW_VALIDATED_FLOW_REPORT_INIT.get()` to be `True` (in addition to 5-tuple `_VALIDATED_FLOW_REPORT_SEALS` membership).
     * Deep-copy container fields first inside `FlowDiscoveryReport.__deepcopy__(self, memo: dict[int, Any]) -> FlowDiscoveryReport`, then set `token = _ALLOW_VALIDATED_FLOW_REPORT_INIT.set(True)` inside `try ... finally: _ALLOW_VALIDATED_FLOW_REPORT_INIT.reset(token)` strictly around `FlowDiscoveryReport(...)` construction (matching `validate_flow_report`).
  4. Cross-process `Mapping` verification:
     * Remove `_EVALUATED_FLOW_REPORT_DIGESTS` / `_VALIDATED_FLOW_REPORT_SEALS` lookup from `_verify_flow_report_mapping`; instead require `dictionary: LifecycleDictionary | None` (`require_validated=True` requires `dictionary is not None`) and call `_verify_report_matches_dictionary(mapping, dictionary)` whenever `dictionary is not None`, alongside 21-field `calculation_digest`, `expected_owner`, zero `gaps`, zero `invalid_accepted_handover_ids`, and strict ISO date checks.
  5. Narrow `FrozenDict` docstring to state `dict`-subclass compatibility with `dataclasses.asdict()` / `json.dumps()` and `verify_digest()` detection of `dict.__setitem__`.
* Completion expectations: Zero bypasses across dictionary swap, pack signer mismatch, `replace()` seal replay, or cross-process JSON `Mapping` verification.

<!-- rpi:phase id=P02 -->
## P02: Adversarial Regression Tests, Documentation Precision, and Focused Validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add focused regression tests (including cross-process subprocess JSON verification) in `test_discovery_contract.py`

* Target file: `src/core/tests/test_discovery_contract.py`
* Completion expectations: Update `tampered_validated = replace(validated)` in `test_flow_report_freezes_nested_mappings_and_verifies_calculation_digest` to `copy.deepcopy(validated)` and add `<= 5` focused tests asserting `AC-C3-1`–`AC-C3-4` (`0` test removals).

<!-- rpi:task id=P02-T02 -->
### P02-T02: Align Phase 0 documentation prose, run focused validation (`TMPDIR=/dev/shm`), and commit `c3` locally

* Target files: `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`.
* Completion expectations: Accurate documentation with zero `.copilot-tracking/` leaks, 100% passing focused checks, and clean local commit before `c3` `rpi-review`.
