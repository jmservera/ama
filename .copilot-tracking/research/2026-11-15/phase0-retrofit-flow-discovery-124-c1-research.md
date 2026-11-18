---
description: "Primary evidence artifact for Issue #124 c1 review remediation (RV-001, RV-002, RV-003)"
---
<!-- markdownlint-disable-file -->

# Task Research: phase0-retrofit-flow-discovery-124-c1

| Field              | Value                                                                                  |
|--------------------|----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                             |
| Researcher / agent | rpi-research (invoked by automatic RPI Agent for child task `issue-124-c1`)            |
| Status             | Complete                                                                               |
| Artifact path      | .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md |

## Research Brief

* What to research: Exact code locations, data invariants, container serialization rules, type-checking constraints (`mypy --strict`), existing test assumptions, and documentation touchpoints required to resolve post-implementation review findings `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md` on `feat/gov-124-phase0-discovery`.
* Why it matters: `RV-001` and `RV-002` are `Medium` governance-hardening defects preventing a `Conformant` verdict on Issue #124 (`BG-011`, `RULE-019`), and `RV-003` is a `Low` fidelity defect preserving downstream distinction between `UNKNOWN` and `DISPUTED` wait causes.
* Audience or intended use: Planning (`rpi-plan`), implementation (`rpi-implement`), and final verification (`rpi-review`) in child loop `issue-124-c1`.
* Scope: `src/core/src/zava_forward/core/discovery_contract.py`, `src/core/tests/test_discovery_contract.py`, directly related documentation (`docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, `docs/reference/log.md`), and `.copilot-tracking/` `c1` artifacts.
* Non-goals: CSV extract ingestion adapters, live database/API/UI changes, running the 3,730-test full `src/core` suite or `tools/rpi-checks.py --all`, and pushing or opening a PR.
* Criteria: Every aspect of `RV-001`, `RV-002`, and `RV-003` is traced to exact `path:line` evidence, contrarian compatibility hazards (`dataclasses.asdict`, `mypy --strict`, existing test fixtures) are verified before planning, and zero legacy behavior is broken.
* Requested outputs: Converged remediation design with code-grounded `C#` evidence and `Planning Readiness: Ready`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How to close `RV-001`, `RV-002`, and `RV-003` cleanly in `discovery_contract.py` and `test_discovery_contract.py` with zero regressions? |
| Codebase scope                   | `src/core/src/zava_forward/core/discovery_*.py`, `src/core/tests/test_discovery*.py`, `docs/reference/research/company/`, `src/core/README.md` |
| External scope                   | none (pure offline standard-library contract remediation)                                                                           |
| Initial internal candidate areas | `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md`, `discovery_contract.py`, `test_discovery_contract.py` |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | default (bounded internal remediation task with named source targets and supplied review failure evidence)                          |
| Explicit limits / deadline       | Focused validation tier only (`TMPDIR=/dev/shm`, targeted `test_discovery*.py`, `test_live_doc_links.py`, `test_dependency_rule.py`, `ruff`, `mypy`); local commit only |
| Posture-specific completion basis | focused scope and materiality: all three `RV-*` findings, interactions, and contrarian compatibility checks are grounded in code and runtime probes |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Pure Python 3.12 stdlib in `src/core`; `mypy` runs with `strict = true`; no `.copilot-tracking/` citations in production code, docs, or commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                   | Scoped authority or output contract                                         | Selected / skipped reason                                                       |
|---------------------|------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | AMA Repository Instructions (`applyTo: "**"`)  | Matches workspace root, `src/core/`, and `docs/`       | Focused validation tier, KB log rules, Markdown style, privacy-safe Git email | Selected: governs code, test, KB, and commit rules                              |
| Skill               | `rpi-research`                                 | Active phase skill                                     | Three-wave read-only research artifact contract                             | Selected: mandatory first RPI phase                                             |
| Skill               | `python-foundational`                          | Python 3.12 typing and testing conventions             | Optional general Python patterns                                            | Skipped: repository `src/core` conventions and `mypy --strict` config already explicit |
| Research specialist | `hve-core-all:rpi-researcher`                  | General research lane subagent                         | Bounded independent subagent lane                                           | Skipped (inline): tightly coupled single-module audit across `discovery_contract.py` and `test_discovery_contract.py` |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                             |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------------------|
| Intake           | Non-interactive execution with explicit caller remediation specification for `RV-001`, `RV-002`, and `RV-003`.          | Not needed           | Proceed directly in focused convergence mode under confirmed automatic RPI session.         |
| Direction change | No scope expansion beyond `discovery_contract` and directly coupled tests/docs occurred during research.               | Not needed           | Retain bounded `c1` remediation scope.                                                      |
| Convergence      | All design trade-offs (container freezing vs `dataclasses.asdict`, `as_of` date cutoff, wait counter keys) resolved by code evidence. | Not needed           | Converge on `FrozenDict` + `calculation_digest`, strict baseline/`as_of` filtering, and additive wait keys. |

## Scope and Success Criteria

* Scope: Remediate `RV-001`, `RV-002`, and `RV-003` in `src/core/src/zava_forward/core/discovery_contract.py` and `src/core/tests/test_discovery_contract.py`, plus aligned KB/README notes if user-visible contract fields change.
* Assumptions:
  * Verified: whether any module outside `test_discovery_contract.py` imports `discovery_contract` (confirmed zero external callers in `src/`).
  * Verified: whether `types.MappingProxyType` survives `dataclasses.asdict()` used in determinism tests (disproved by runtime probe; requires `dict`-compatible `FrozenDict` plus `calculation_digest`).
* Success criteria:
  * Every research question is answered with exact `path:line` evidence.
  * Contrarian edge cases in existing tests and stdlib serialization are identified before planning.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. `RV-001`: Refuse `validate_flow_report` with `GovernanceViolationError` when `report.gaps` or `report.invalid_accepted_handover_ids` is non-empty; restrict cohort aggregations in `evaluate_property_flow` to `baseline_candidate_ids` up to `as_of` while recording unmatched-cohort or post-cutoff records in `gaps`; base `zero_event_candidate_ids` strictly on lifecycle event presence; add focused unit tests.
  2. `RV-002`: Freeze nested mappings on `FlowDiscoveryReport` and bind `validate_flow_report` + `enforce_governance_guard` to a verified immutable `calculation_digest`; record and verify `validated_role == owner_role` inside dictionary spec gap checks (`StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, `ReturnLoopSpec` / `lifecycle_dictionary_gaps()`); enforce canonical `REQUIRED_FLOW_STAGE_CODES` order in `LifecycleDictionary.__post_init__`; add focused unit tests.
  3. `RV-003`: Add `unknown_cause_count` and `disputed_cause_count` keys to each `waits_by_party` row in `evaluate_property_flow` while retaining `unknown_or_disputed_count` (and existing `unknown_or_disputed_cause`) for backward compatibility, and assert both counters in `test_discovery_contract.py`.
* Inferred research questions:
  * How do `FlowDiscoveryReport.__post_init__`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` interact with `RV-001` and `RV-002`?
  * Do any existing tests in `test_discovery_contract.py` pass non-baseline `property_id` values or call `dataclasses.asdict()` on `FlowDiscoveryReport`?
* Caller constraints and non-goals: Focused validation tier only; `TMPDIR=/dev/shm`; commit locally with `Refs #124` and Copilot trailer; do not push or open a PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation                          |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------|
| narrow                                                   | Run only targeted discovery/link/dependency tests, `ruff`, and `mypy` (`TMPDIR=/dev/shm`)             | Caller intake       | Constrains validation commands in Plan and Implement                       |
| exclude                                                  | Do not push or run `gh pr create`; leave frozen clean local commit                                    | Caller intake       | Constrains closeout git actions                                            |

## Research Questions

|  # | Sub-question                                                                                                                | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Where do `FlowDiscoveryReport`, `evaluate_property_flow`, `validate_flow_report`, and `enforce_governance_guard` miss gap, cohort, `as_of`, and zero-event invariants (`RV-001`)? | depth           | H        | answered |
| Q2 | How should `FlowDiscoveryReport` freeze nested containers and verify `calculation_digest` without breaking `dataclasses.asdict`, `json.dumps`, or `mypy --strict` (`RV-002`)? | depth           | H        | answered |
| Q3 | How should `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, `ReturnLoopSpec`, and `LifecycleDictionary.__post_init__` enforce `validated_role == owner_role` and canonical stage order (`RV-002`)? | straightforward | H        | answered |
| Q4 | What exact keys exist on `waits_by_party` rows today and how should `unknown_cause_count`, `disputed_cause_count`, and compatibility keys be structured (`RV-003`)? | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `.copilot-tracking/reviews/logs/2026-11-15/phase0-retrofit-flow-discovery-124-review.md`
  * `.copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-research.md`
  * `.copilot-tracking/plans/2026-11-15/phase0-retrofit-flow-discovery-124-plan.md`
  * `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`
* Reused (verified) findings:
  * `GovernanceViolationError` in `discovery_register.py` subclasses `ValueError`, allowing governance and construction checks to raise `GovernanceViolationError` consistently (`C1`).
  * `discovery_contract` has no callers in `src/api`, `src/agents`, `src/orchestrator`, or `src/importer`; only `src/core/tests/test_discovery_contract.py` imports it (`C10`).
* Superseded / stale:
  * Parent review `phase0-retrofit-flow-discovery-124-review.md` recorded `Defects found` on commit `0c2457297` due to `RV-001`, `RV-002`, and `RV-003`; child task `issue-124-c1` remediates those three findings.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; local commit only without push/PR.
* Active research posture and completion basis: `focused`; complete once all three review findings, type/serialization interactions, and existing test assumptions are verified in source and runtime probes.
* Explicit limits or deadline effect: Keeps scope strictly inside `src/core` Phase 0 discovery contract and aligned documentation.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth sweep across `src/` imports of `discovery_contract`, `discovery_register.py`, `discovery_flow.py`, `discovery_contract.py`, `test_discovery_contract.py`, `src/core/README.md`, and `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`.
* Worker evidence relationships or inline fallback: Inline investigation (`C1`–`C12`); all coupled symbols reside in one module and one test module.
* Reflection: Confirmed zero external module callers (`C10`), located all five spec classes, `LifecycleDictionary`, `FlowDiscoveryReport`, `evaluate_property_flow`, `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact control-flow paths for `RV-001`, `RV-002`, and `RV-003` in `discovery_contract.py` and `test_discovery_contract.py`.
* Plan and independent lanes:
  1. Trace `evaluate_property_flow` (`discovery_contract.py:1101-1405`), `FlowDiscoveryReport.__post_init__` (`discovery_contract.py:1087-1098`), and `validate_flow_report` (`discovery_contract.py:1425-1444`).
  2. Trace `StageSpec`–`ReturnLoopSpec` (`discovery_contract.py:235-313`), `validate_*_spec` (`discovery_contract.py:323-370`), `LifecycleDictionary` (`discovery_contract.py:315-320`), and `lifecycle_dictionary_gaps` (`discovery_contract.py:816-880`).
  3. Trace `waits_by_party` construction (`discovery_contract.py:1244-1285`, `1370-1378`) and assertions in `test_discovery_contract.py:455-460`.
* Worker evidence relationships or inline fallback:
  * Q1 -> `evaluate_property_flow` tracks `props_with_activity` across events, stages, waits, and loops (`discovery_contract.py:1138-1290`), merges non-baseline event property IDs via `all_tracked_ids` (`discovery_contract.py:1322`), never checks timestamps against `as_of` cutoff (`discovery_contract.py:1124-1315`), and `validate_flow_report` / `FlowDiscoveryReport.__post_init__` do not block non-empty `gaps` or `invalid_accepted_handover_ids` (`C4`, `C5`, `C6`).
  * Q3 -> Dictionary entry specs store `validated_by` and `validated_on` without `validated_role` (`C2`), so direct dataclass construction bypasses `validate_*_spec` role matching, and `LifecycleDictionary` lacks `__post_init__` enforcement of `REQUIRED_FLOW_STAGE_CODES` (`C3`).
  * Q4 -> `waits_by_party` rows currently emit `unknown_or_disputed_cause` (`discovery_contract.py:1375`, asserted at `test_discovery_contract.py:457`), whereas `RV-003` asks for `unknown_cause_count` and `disputed_cause_count` alongside `unknown_or_disputed_count` (`C5`, `C11`).
* Reflection: Every defect mechanism is pinpointed, but container freezing (`MappingProxyType` vs `dict` subclass) and stricter baseline filtering must be stress-tested against existing tests and Python 3.12 `dataclasses.asdict`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Challenge using `types.MappingProxyType` directly on `FlowDiscoveryReport` dataclass fields.
  2. Challenge restricting `evaluate_property_flow` to `baseline_candidate_ids` against existing unit tests in `test_discovery_contract.py`.
  3. Challenge replacing `unknown_or_disputed_cause` with `unknown_or_disputed_count`.
* Plan and independent lanes: Run read-only Python 3.12 probe for `dataclasses.asdict` with `MappingProxyType` vs immutable `FrozenDict`, and audit every existing test in `test_discovery_contract.py` for non-baseline property IDs and wait-row key names.
* Worker evidence relationships or inline fallback:
  * **Disproved naive `MappingProxyType` field storage**: Python 3.12 `dataclasses.asdict()` falls back to `copy.deepcopy()` for non-`dict` mappings and raises `TypeError: cannot pickle 'mappingproxy' object`, which would break `test_flow_evaluation_is_deterministic_across_repeated_runs` (`test_discovery_contract.py:494`, `C12`). By contrast, a slot-free `FrozenDict(dict[K, V])` subclass overriding every mutating `dict` method (`__setitem__`, `__delitem__`, `clear`, `pop`, `popitem`, `setdefault`, `update`, `__ior__`) to raise `TypeError`, combined with recursive tuple/mapping freezing in `FlowDiscoveryReport.__post_init__` AND a deterministic SHA-256 `calculation_digest` verified in `FlowDiscoveryReport.verify_digest()`, `validate_flow_report()`, `validate_discovery_pack()`, and `enforce_governance_guard()`, blocks runtime mutation AND C-level bypasses while preserving `asdict()`, `json.dumps()`, `replace()`, and `assertEqual(..., {...})` (`C4`, `C9`, `C12`).
  * **Caught two existing test fixtures relying on non-baseline `P2`**:
    1. `test_flow_preserves_unknown_disputed_unattributed_waits_and_counts_return_loops` (`test_discovery_contract.py:417-459`) passes a wait for `P2` while `candidates` only lists `P1`, then expects `P2`'s unattributed wait in `report.waits_by_party[1]` (`C11`). Under `RV-001` cohort restriction, `P2` must be included in `candidates` in that test to remain an in-cohort wait, while new `RV-001` tests verify that unmatched `P-OUTSIDE` records are excluded from aggregations and logged in `gaps`.
    2. `test_flow_flags_malformed_naive_unknown_and_out_of_order_timestamps_without_guessing` (`test_discovery_contract.py:467-481`) passes `P1` with malformed `identified_at` and events for `P2` without listing `P2` in `candidates`, then indexes `report.bg011_assessment_to_ready_to_install_days["P2"]` (`C11`). Adding a valid `BaselineCandidateRecord("P2", "2026-01-12", "c-2")` keeps `P2` in-cohort for the out-of-order and unknown-event assertions while `P1` continues testing malformed `identified_at`.
  * **Caught dual compatibility key name on `waits_by_party`**: Existing `discovery_contract.py:1375` and `test_discovery_contract.py:457` use `unknown_or_disputed_cause`, while `RV-003` refers to `unknown_or_disputed_count`. Emitting `unknown_cause_count`, `disputed_cause_count`, `unknown_or_disputed_count`, and `unknown_or_disputed_cause` preserves 100% backward compatibility with existing callers and tests (`C5`, `C11`).
* Reflection: Contrarian testing prevented three certain regressions before a single line of code was edited.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|--------------------|--------------------------|----------------------------|
| Reject promotion of `FlowDiscoveryReport` when `gaps` or `invalid_accepted_handover_ids` is non-empty across `__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard` | `C4`, `C6`, `C8`, `C9` | accepted | Closes both helper and direct-construction bypasses consistently with `LifecycleDictionaryReport` | Core `RV-001` design |
| Restrict `evaluate_property_flow` aggregations to `baseline_candidate_ids` with timestamps `<= as_of` (UTC calendar cutoff `ts.date() <= as_of`), recording unmatched-cohort and post-cutoff records in `gaps`, and base `zero_event_candidate_ids` strictly on valid in-cohort `<= as_of` lifecycle events | `C5`, `C11` | accepted | Directly resolves `RV-001` while preserving whole-day open-clock arithmetic (`max(as_of_dt, start_dt)`) | Core `RV-001` design |
| Use `MappingProxyType` directly as `FlowDiscoveryReport` field runtime values | `C4`, `C12` | rejected | Breaks `dataclasses.asdict()` (`TypeError: cannot pickle 'mappingproxy' object`) at `test_discovery_contract.py:494` | Recorded as rejected alternative |
| Recursively freeze nested mappings/containers with `FrozenDict(dict)` + `tuple` in `FlowDiscoveryReport.__post_init__` AND bind/verify SHA-256 `calculation_digest` in `FlowDiscoveryReport`, `validate_flow_report`, `validate_discovery_pack`, and `enforce_governance_guard` | `C4`, `C6`, `C8`, `C9`, `C12` | accepted | Prevents accidental in-place mutation (`TypeError`), preserves `asdict`/`json.dumps`/`mypy --strict`, and detects `object.__setattr__` or `dict.__setitem__` tampering (`GovernanceViolationError`) | Core `RV-002` design |
| Add `validated_role: str = ""` to all five dictionary spec dataclasses, populate it in `validate_*_spec`, verify `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`, and enforce canonical `(1..10, REQUIRED_FLOW_STAGE_CODES)` flow-stage order in `LifecycleDictionary.__post_init__` | `C2`, `C3` | accepted | Closes direct-construction role bypass and out-of-order stage construction (`RV-002`) | Core `RV-002` design |
| Emit `unknown_cause_count` (`cause_code` in `{"UNKNOWN", ""}`) and `disputed_cause_count` (`cause_code == "DISPUTED"`) alongside `unknown_or_disputed_count` and `unknown_or_disputed_cause` on `waits_by_party` rows | `C5`, `C11` | accepted | Satisfies `RV-003` and retains full backward compatibility with `test_discovery_contract.py:457` | Core `RV-003` design |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope saturated; every requirement in `RV-001`, `RV-002`, and `RV-003` plus contrarian compatibility hazards is verified against exact code lines and Python 3.12 stdlib behavior.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: tightly coupled single-package remediation across `discovery_contract.py` and `test_discovery_contract.py` fits direct inspection in under five file reads.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | `GovernanceViolationError` subclasses `ValueError`, so raising it satisfies both governance and `ValueError` callers | `src/core/src/zava_forward/core/discovery_register.py:74` | view | high | Shared exception across Phase 0 discovery modules |
| C2  | `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec` lack `validated_role`, so `.validated` only checks `validated_by` and `validated_on` | `src/core/src/zava_forward/core/discovery_contract.py:235` | view | high | Lines `235-313`; `validate_*_spec` is at `323-370` |
| C3  | `LifecycleDictionary` has no `__post_init__` check enforcing canonical `REQUIRED_FLOW_STAGE_CODES` order `1..10`; `lifecycle_dictionary_gaps` only checks sorted numeric orders `1..10` | `src/core/src/zava_forward/core/discovery_contract.py:315` | view | high | Also `lifecycle_dictionary_gaps` at `816-880` |
| C4  | `FlowDiscoveryReport` stores mutable nested `dict` containers, lacks a verified `calculation_digest`, and `__post_init__` does not reject non-empty `gaps` or `invalid_accepted_handover_ids` when `owner_validated=True` | `src/core/src/zava_forward/core/discovery_contract.py:1058` | view | high | Lines `1058-1098` |
| C5  | `evaluate_property_flow` aggregates non-baseline and post-`as_of` records without recording cohort/cutoff gaps, computes `zero_event_candidate_ids` from `props_with_activity` across stages/waits/loops, and only emits combined `unknown_or_disputed_cause` in `waits_by_party` | `src/core/src/zava_forward/core/discovery_contract.py:1101` | view | high | Lines `1101-1405` |
| C6  | `validate_flow_report` checks owner readiness and zero dictionary gaps via `_require_ready_owner_and_dictionary`, but never rejects non-empty `report.gaps` or `report.invalid_accepted_handover_ids` | `src/core/src/zava_forward/core/discovery_contract.py:1425` | view | high | Contrast with `validate_lifecycle_report` at `965` |
| C7  | `PAS2035_EVIDENCE_PROVENANCE_NOTE` and KB synthesis document the BSI PAS 2035:2023 overview boundary (`gap-pas-2035-licensed`) and open human gates (`OD-14`, `OD-16`, `OD-18`, `OD-36`) | `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md:29` | view | high | Also `src/core/README.md:1447` |
| C8  | `Phase0DiscoveryPack.__post_init__` and `validate_discovery_pack` delegate to `flow_report.owner_validated` and `validate_flow_report` | `src/core/src/zava_forward/core/discovery_contract.py:1855` | view | high | Lines `1855-1965` |
| C9  | `enforce_governance_guard` checks `owner_validated`, `finding_status`, `discovery_owner`, `dictionary`, and `DISPUTED` hypothesis status, and should also reject validated `FlowDiscoveryReport` / `Phase0DiscoveryPack` instances with gaps, invalid handovers, or tampered `calculation_digest` | `src/core/src/zava_forward/core/discovery_contract.py:1992` | view | high | Lines `1992-2046` |
| C10 | Repository-wide search under `src/` shows only `src/core/tests/test_discovery_contract.py` imports `discovery_contract` | `src/core/tests/test_discovery_contract.py:9` | grep | high | Zero downstream breakage risk outside `src/core` |
| C11 | Two existing tests in `test_discovery_contract.py` pass `P2` wait/event records without including `P2` in `candidates`, and line `457` asserts `unknown_or_disputed_cause` | `src/core/tests/test_discovery_contract.py:417` | view | high | Lines `417-482` |
| C12 | `test_flow_evaluation_is_deterministic_across_repeated_runs` calls `json.dumps(asdict(evaluate_property_flow(...)), sort_keys=True, default=str)`, which raises `TypeError` on `MappingProxyType` but succeeds cleanly on immutable `FrozenDict(dict)` | `src/core/tests/test_discovery_contract.py:494` | view | high | Verified via Python 3.12 probe |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Wait counter field naming: `discovery_contract.py:1375` and `test_discovery_contract.py:457` use `unknown_or_disputed_cause` (`C5`, `C11`), whereas `RV-003` prose refers to retaining `unknown_or_disputed_count`. Resolved by preserving `unknown_or_disputed_cause` AND adding `unknown_or_disputed_count` alongside `unknown_cause_count` and `disputed_cause_count` so all existing and specified callers succeed.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Reject non-empty `gaps` and `invalid_accepted_handover_ids` in `FlowDiscoveryReport.__post_init__`, `validate_flow_report`, `Phase0DiscoveryPack.__post_init__`, and `enforce_governance_guard`; filter `evaluate_property_flow` records to `baseline_candidate_ids` and UTC `ts.date() <= as_of`, log unmatched-cohort and post-cutoff records in `gaps`, and compute `zero_event_candidate_ids` strictly from valid in-cohort `<= as_of` lifecycle events. | `C4`, `C5`, `C6`, `C8`, `C9`, `C11` | high | Ready for implementation; update the two `P2` fixture setups in `test_discovery_contract.py` so `P2` is an explicit baseline candidate where intended. |
| Q2 | Freeze all nested dicts/sequences on `FlowDiscoveryReport` recursively via an immutable `FrozenDict(dict[K, V])` + `tuple` coercion in `__post_init__` AND compute/verify a deterministic SHA-256 `calculation_digest` across `FlowDiscoveryReport`, `validate_flow_report`, `validate_discovery_pack`, and `enforce_governance_guard`. | `C4`, `C6`, `C8`, `C9`, `C12` | high | Ready for implementation; preserves `dataclasses.asdict`, `json.dumps`, `replace`, and `mypy --strict`. |
| Q3 | Add `validated_role: str = ""` to `StageSpec`, `EventSpec`, `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec`; set it in `validate_*_spec`; require `validated_role == owner_role` in `.validated` and `lifecycle_dictionary_gaps()`; and enforce canonical `(1..10, REQUIRED_FLOW_STAGE_CODES)` flow stage sequence in `LifecycleDictionary.__post_init__`. | `C1`, `C2`, `C3` | high | Ready for implementation. |
| Q4 | Track `party_unknown` (`cause_code.strip() in (UNKNOWN, "")`) and `party_disputed` (`cause_code.strip() == WAIT_CAUSE_DISPUTED`) separately in `evaluate_property_flow` and emit `unknown_cause_count`, `disputed_cause_count`, `unknown_or_disputed_count`, and `unknown_or_disputed_cause` on each `waits_by_party` row. | `C5`, `C11` | high | Ready for implementation. |

## Key Discoveries

* Python 3.12 `dataclasses.asdict()` cannot deepcopy `types.MappingProxyType`, raising `TypeError: cannot pickle 'mappingproxy' object` (`C12`). Using a recursive `FrozenDict(dict)` freeze plus a verified SHA-256 `calculation_digest` delivers both immediate `TypeError` immutability on nested container mutation and cryptographic tamper rejection on `validate_flow_report` / `enforce_governance_guard`.
* Restricting `evaluate_property_flow` cohort aggregations to `baseline_candidate_ids` exposes two existing tests (`test_discovery_contract.py:417` and `:467`) that omitted `BaselineCandidateRecord("P2", ...)` as a shorthand (`C11`); updating their candidate tuples keeps those tests focused on their intended invariants while new dedicated tests verify unmatched-cohort and post-`as_of` exclusion and gap reporting.
* Requiring `validated_role == owner_role` on all five dictionary spec dataclasses (`C2`) and canonical `REQUIRED_FLOW_STAGE_CODES` order in `LifecycleDictionary.__post_init__` (`C3`) closes direct-dataclass construction bypasses without altering `build_default_lifecycle_dictionary()` or `validate_*_spec()` call signatures.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Targeted hardening of `src/core/src/zava_forward/core/discovery_contract.py`, focused unit tests in `src/core/tests/test_discovery_contract.py`, and brief documentation sync in `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`, `src/core/README.md`, and `docs/reference/log.md`.
* Rationale: Resolves `RV-001`, `RV-002`, and `RV-003` completely using pure Python 3.12 stdlib primitives, satisfies `mypy --strict` and `dataclasses.asdict()`, and preserves backward compatibility across all 87 existing discovery tests.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`, `C12`
* Implementation impact:
  * `src/core/src/zava_forward/core/discovery_contract.py`
  * `src/core/tests/test_discovery_contract.py`
  * `docs/reference/research/company/phase0-retrofit-flow-discovery-contract.md`
  * `src/core/README.md`
  * `docs/reference/log.md`
* Confidence: high: every code path and stdlib behavior was directly inspected and probed.

File tree:

```text
src/core/
  README.md                                              (modify)
  src/zava_forward/core/discovery_contract.py            (modify)
  tests/test_discovery_contract.py                       (modify)
docs/reference/
  log.md                                                 (modify)
  research/company/phase0-retrofit-flow-discovery-contract.md (modify)
```

### Alternative: Raw `types.MappingProxyType` on `FlowDiscoveryReport` fields

* Approach: Replace nested `dict` values on `FlowDiscoveryReport` with `types.MappingProxyType` instances.
* Trade-offs: Zero custom class lines, but crashes `dataclasses.asdict()` (`copy.deepcopy`) with `TypeError: cannot pickle 'mappingproxy' object` and requires custom JSON serialization hooks.
* Evidence refs: `C4`, `C12`
* Rejection rationale: Breaks `test_flow_evaluation_is_deterministic_across_repeated_runs` (`test_discovery_contract.py:494`) and standard dataclass serialization idioms.

### Alternative: Digest-only tamper detection without freezing nested `dict` instances

* Approach: Leave nested `dict` containers mutable on `FlowDiscoveryReport` and only check `calculation_digest` inside `validate_flow_report` and `enforce_governance_guard`.
* Trade-offs: Detects tampering when guard functions run, but allows silent in-memory mutation after `validate_flow_report` returns if a downstream consumer mutates a report dictionary without re-calling `enforce_governance_guard`.
* Evidence refs: `C4`, `C6`, `C9`
* Rejection rationale: Combining `FrozenDict` deep container immutability AND `calculation_digest` verification blocks mutation at write time (`TypeError`) AND detects C-level attribute/dict tampering at guard time (`GovernanceViolationError`).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure `FrozenDict` method overrides satisfy `mypy` under `strict = true` with clean type signatures.
* Follow-up: Optional CSV extract adapter mapping synthetic year-one CSV tables into `discovery_contract` records remains deferred outside Phase 0 rule-layer scope (`docs/brds/retrofit-flow-discovery-brief.md`).
* Residual uncertainty: Real-world Zava North Homes human approvals (`OD-14`, `OD-16`, `OD-18`, `OD-36`) remain external human governance gates by design (`C7`).

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Reject `FlowDiscoveryReport` validation/promotion when `gaps` or `invalid_accepted_handover_ids` is non-empty, restrict `evaluate_property_flow` aggregations to `baseline_candidate_ids` up to `as_of`, and base `zero_event_candidate_ids` strictly on lifecycle events | confirmed | caller / review `RV-001` | Closes fail-closed promotion and baseline/cutoff boundaries | `C4`, `C5`, `C6`, `C11` | Implemented in `P01`, tested in `P02` |
| Enforce deep `FrozenDict` + `tuple` immutability and verified SHA-256 `calculation_digest` on `FlowDiscoveryReport`, `validated_role == owner_role` on all dictionary specs, and canonical `REQUIRED_FLOW_STAGE_CODES` order in `LifecycleDictionary.__post_init__` | confirmed | caller / review `RV-002` + `C12` | Prevents post-sign-off container mutation and direct-init bypasses while preserving `asdict` | `C2`, `C3`, `C4`, `C9`, `C12` | Implemented in `P01`, tested in `P02` |
| Add `unknown_cause_count` and `disputed_cause_count` alongside `unknown_or_disputed_count` and `unknown_or_disputed_cause` on `waits_by_party` rows | confirmed | caller / review `RV-003` + `C11` | Preserves separate `UNKNOWN` vs `DISPUTED` counts with zero backward-compatibility breakage | `C5`, `C11` | Implemented in `P01`, tested in `P02` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Real-world Zava North Homes Phase 0 nomination, dictionary sign-off, 12-month extract, and finding validation (`OD-14`, `OD-16`, `OD-18`, `OD-36`) | Named human Executive Sponsor and Discovery Owner decisions on company data | Zava North Homes Executive Sponsor / Discovery Owner | Keeps default seed artefacts stamped `owner_validated=False` | follow-up (non-blocking for software contract) |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Synthetic CSV extract loader schema mapping (`support/synthetic-data/retrofit-flow/zava-forward-year-one/`) | Connects synthetic CSV extracts to `evaluate_property_flow` when sponsor requests extract tooling | Sponsor/owner request beyond Phase 0 contract | deferred | `C7` |

## Planning Readiness

* Status: Ready
* Decision state: Converged remediation design selected across `RV-001`, `RV-002`, and `RV-003`.
* Evidence basis: `C1`–`C12`
* Preconditions met: Exact target lines, type rules, serialization behavior, existing test fixture adjustments, and focused validation commands are established.
* Blockers: none
* Smallest action to change readiness: none (`Ready` for `rpi-plan`)

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                  |
| Lane evidence or inline fallback | Inline investigation (`C1`–`C12`); single-module scope did not warrant subagent fan-out    |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (`C1`–`C12`)                                                                         |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | Confirmed automatic RPI Agent (`issue-124-c1`), automatic continuation to `Plan`           |

## Advisory Next Step

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (`C1`–`C12`)                                                                         |
| Output mode and planning support | `convergence`; yes — single evidence-backed remediation design selected                    |
| Acting owner                     | Confirmed automatic RPI Agent                                                              |
| Required gates or confirmations  | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), pre-transition state write (`passed`) |
| Continuation result              | Automatic continuation to `rpi-plan`                                                       |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/phase0-retrofit-flow-discovery-124-c1-research.md    |
| Notes for planning or re-entry   | Include explicit adjustment of the two `P2` test fixtures (`C11`), `FrozenDict` + `calculation_digest` (`C12`), and focused validation commands with `TMPDIR=/dev/shm`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All `RV-001`–`RV-003` paths and contrarian interactions are fully evidenced in `C1`–`C12`; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none
