<!-- markdownlint-disable-file -->
# RPI Phase Details: Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness (#223)

## Metadata

* Task ID: 223-human-review-effectiveness-2305
* Task slug: human-review-effectiveness-223-2305
* Related plan: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/case_study_48_addendum.md

## Phase Index

| Phase ID | Name                                                                        | Status | Detail sections        |
|----------|-----------------------------------------------------------------------------|--------|------------------------|
| P01      | Core Gate, Authority Policy, and Seeded Scenarios                           | Ready  | P01, P01-T01, P01-T02  |
| P02      | Workflow-Only Comparator, Automation-Bias Harness, and Human Session Scoring | Ready  | P02, P02-T01, P02-T02  |
| P03      | Targeted Tests, Documentation, and Strict Validation                        | Ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Core Gate, Authority Policy, and Seeded Scenarios

### Context

`Store.review_ai` (`src/core/src/zava_forward/core/ai_tasks.py`) stamps `review_evidence` and checks post-draft `source_hashes` staleness, while `statement_sources` sets `verified=True` whenever `[[...]]` tokens match keys in `source_labels(case)`. Neither prevents an automation-biased reviewer from accepting a confident, validly cited draft that reverses an open damp/mould safety hazard, repeats a superseded booking note, promises unapproved grant funding, or omits a resident accessibility adjustment.

### Intent

Provide a strictly typed core authority contract, constructed multi-task (`summary` and `message`) scenario set, and deterministic `human_review_gate` returning `gates.GateResult`.

### Boundaries

* Included: `AuthorityPolicy`, `PROVISIONAL_AUTHORITY`, typed `Store`/`ai_tasks` adapters, constructed dataset (`ZF-223-A`, `ZF-223-B`), 8 seeded scenarios (`wrong`, `stale`, `unsupported`, `incomplete`, and valid controls), live case semantic invariants, and `human_review_gate`.
* Excluded: Modifying `store.py`, `ai_tasks.py`, `pyproject.toml`, or `provenance-register.json`.

### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: New module owning authority policy, scenario pack, and `human_review_gate`.

### Dependencies

* None.

### Validation Expectations

* `python3 -m mypy` (`strict = true`), `python3 -m ruff check .`, and `python3 -m ruff format --check .` pass cleanly.

### Completion Evidence

* `human_review_gate` returns `GateResult` (`PASS`, `FAIL`, `UNKNOWN`) compatible with `gates.transition_allowed` across all defect classes, valid controls, and adversarial bypass inputs.

### Unresolved Items

* `OQ-017` human sign-off on role authority and live thresholds remains open and enforced fail-closed when `live=True`.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Define typed Store/ai_tasks boundary, `AuthorityPolicy`, and constructed `summary`/`message` scenario pack

#### Context

`mypy` runs in `strict = true` mode across `src/core`, while `store.py` and `ai_tasks.py` are legacy untyped modules. Furthermore, `privacy.public_issues` requires any file under `src/core/evals/` to be registered in `provenance-register.json`.

#### Intent

Define clean typed wrapper helpers around `Store` and `ai_tasks`, immutable `AuthorityPolicy` (`PROVISIONAL_AUTHORITY` carrying `OQ-017` disclosures), constructed synthetic dataset (`ZF-223-A` and `ZF-223-B` with staff across authorised and unauthorised roles), and 8 citation-valid scenarios spanning `summary` and `message`.

#### Boundaries

* Included:
  * `AuthorityPolicy` frozen dataclass with `policy_id`, `provisional`, `authority_gap`, `approved_by`, `approved_on`, `allowed_roles` (`Mapping[str, tuple[str, ...]]` mapping role -> allowed tasks `("summary", "message")`), and `min_reason_chars`.
  * Constructed synthetic cases `ZF-223-A` (open damp/mould safety hazard, completed survey awaiting technical sign-off, unapproved funding draft, resident large-print adjustment) and `ZF-223-B` (resident awaiting consent decision with BSL interpreter / written confirmation adjustment and open electrical check).
  * 8 `ReviewScenario` specifications (`S-223-01`..`S-223-08`) covering `wrong` (confident summary + hedged message), `stale` (confident summary), `unsupported` (confident summary), `incomplete` (confident summary + confident message), and `none` (hedged summary control + confident message control), with every scenario bullet/sentence using exact `ai_tasks.source_labels(case, reason_ok=...)` labels (`[[Stage: ...]]`, `[[Open safety issues: 1]]`, `[[Safety issue: ...]]`, `[[Funding: ...]]`, `[[Extra support: needed]]`, `[[Case history ...]]`) visible across reviewer roles so `rec["verified"]` is `True` without bullet-dropping (`bullets=True` on `summary`).
  * Offline `Store` harness seeding binds a deterministic synthetic `release_context` (`{"id": ..., "version": ..., "digest": ...}`) and offline `store.ai.run` responder under the reviewing user's own staff account (`rec["user"] == reviewer["email"]`) so `Store.ai_run` emits `source="ai"` and `Store.review_ai(reviewer, rec_id, action, reason, text)` (`reason` `<= 300` chars) executes through the real release and epoch checks without raising `PermissionError`.
* Excluded: Any real resident PII, email addresses matching non-synthetic patterns in public JSON files, or `pyproject.toml` edits.

#### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: Data structures, typed boundary helpers, synthetic store builder, and `DEFAULT_SCENARIOS`.

#### Dependencies

* None.

#### Validation Expectations

* Every scenario seeded through the store builder produces `verified == True` from `ai_tasks.statement_sources` so citation validity alone is proven insufficient on all defective scenarios.

#### Completion Evidence

* `DEFAULT_SCENARIOS` and `AuthorityPolicy` pass strict type-checking and cover all four `AC-070` defect classes plus hedged and confident controls across `summary` and `message`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement fail-closed `human_review_gate` integrated with `gates.GateResult`

#### Context

`zava_forward.core.gates` defines `GateRule(gate, source, effective_date, version, reviewer)` and `GateResult(gate, outcome, reason, owner, correction, rule=None)` where `PASS = "pass"`, `FAIL = "fail"`, `UNKNOWN = "unknown"`, and `transition_allowed` permits progression only when every gate `outcome == PASS`.

#### Intent

Implement `human_review_gate(...) -> GateResult` (plus a structured inspection breakdown helper) so no unreviewed, `HOLD`/`QUARANTINED`, default-accepted, unreasoned, superficially edited, citation-only, stale, memory-justified, placeholder/non-human, or unauthorised review can pass.

#### Boundaries

* Included:
  * Constructs `gates.GateRule(gate="human_review_effectiveness", source="PRD::AC-070; PRD::FR-026; PRD::FR-027; PRD::NFR-009; PRD::OQ-017", effective_date="2026-01-01", version="1", reviewer=...)` and evaluates `effective_date <= (on or date.today().isoformat())` deterministically before returning `GateResult(gate, outcome, reason, owner, correction, rule)`.
  * Unreviewed (`status == "Not reviewed"` or missing `review_evidence` when not `HOLD`/`QUARANTINED`) or missing `AuthorityPolicy` -> `UNKNOWN` with explicit `reason`, `owner`, and `correction`.
  * `rec["status"] in ("Hold", "Quarantined")` -> `FAIL` (`stale_or_quarantined_proposal`).
  * `live=True` with `authority.provisional` or missing valid human `authority.approved_by` or missing `authority.approved_on` -> `FAIL` naming `OQ-017 competent-review authority approval` in `reason`, `owner`, and `correction`.
  * Reviewer validation: `rai_release.named_human(resolved_by)` supplemented by an explicit placeholder/automation token denylist (`tbd`, `todo`, `pending`, `unassigned`, `placeholder`, `workflow`, `model`, `n/a`), presence in `staff` directory (or supplied `staff_member`), role membership in `authority.allowed_roles` (`Resident Liaison Officer`, `Retrofit Coordinator`), and task membership (`rec["task"]`) in that role's permitted tasks.
  * Freshness and provenance validation: `review_evidence` retains `reviewer`, `compared` (`{"ai": ..., "workflow": ...}`), `source_hashes`, and `reason`; live `ai_tasks.source_hashes(store, reviewer_user, rec["case_ids"])` (or `source_snapshot_hashes` with matching `can_see_reason`) equals `review_evidence["source_hashes"]` (`stale_case_sources` on mismatch); refuses both `controls.is_memory_reference(reason)` tokens (`CM-...`, `memory:...`, `chat-memory`) and conversational memory phrases (`"earlier in chat"`, `"the assistant said"`, `"copilot said"`, `"from memory"`).
  * Substantive source-cited reason required on ALL dispositions (`accept`, `edit`, and `reject`): `len(reason.strip()) >= authority.min_reason_chars` (`<= 300` chars) AND `reason` explicitly cites at least one verified case `source_labels` key (and when resolving a discrepancy, one of the discrepancy's resolving case sources). Thus `default_accept` (`reason=""`) and `citation_only` (`reason` relying only on badge validity) receive `FAIL` on every scenario, including valid controls (`gate_passed_count == 0`).
  * Semantic discrepancy validation (combining live case invariants — open hazards not marked clear/resolved or omitted in summary, active resident accessibility adjustments not contradicted or omitted, unapproved funding not claimed awarded/approved/guaranteed, superseded stage claims rejected, zero unresolved `[[...]]` citations in `override_text` — plus optional scenario `forbidden_claims`, `required_facts`, and `resolving_sources`):
    * Discrepant proposal + `disposition == "accept"` -> `FAIL` (`default_accept_missed_critical_defect`, plus `citation_validity_alone_insufficient` when `rec["verified"]` is `True`).
    * `disposition == "edit"` inspects `rec["override_text"]` and requires it to differ meaningfully from a defective `ai_output`, eliminate all forbidden/contradictory claims, include all required case safety/adjustment facts, and contain zero unresolved `[[...]]` citations.
* Excluded: Mutating production `Store.review_ai` signature in ways that could break existing callers.

#### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: `inspect_case_discrepancies`, `human_review_gate`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Unit tests verify `PASS`, `FAIL`, and `UNKNOWN` outcomes and `gates.transition_allowed([result])` behavior across all positive and adversarial cases.

#### Completion Evidence

* `human_review_gate` blocks 100% of defective proposals under default acceptance, citation-only acceptance, automation bias, cosmetic edits, bad reasons, stale sources, and unauthorised/non-human actors.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Workflow-Only Comparator, Automation-Bias Harness, and Human Session Scoring

### Context

`AC-070`, `FR-028`, and `NFR-009` require comparing AI-assisted human review against the exact same workflow-only scenarios (`Store.ai_run(..., mode="workflow")`), reporting detection, corrections, and total review effort while exposing automation bias and supporting blind human trials.

### Intent

Implement deterministic panel evaluation (`competent`, `default_accept`, `automation_bias`, `citation_only`, `unauthorised_competent`), workflow-only effort/accuracy comparison, blind worksheet export, and human-session scoring/pooling.

### Boundaries

* Included: `evaluate_panel`, `run_automation_bias_harness`, `blank_worksheet`, `score_human_session`, `pool_human_sessions`.
* Excluded: Claiming synthetic profile runs satisfy `OQ-017` human trials.

### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: Harness, comparator, worksheet, and pooling functions.

### Dependencies

* P01.

### Validation Expectations

* All scripted panels execute against real `Store` instances with `Store.verify_audit() == True` and `gate_leakage == 0`.

### Completion Evidence

* Comparative report includes per-scenario workflow comparator output, per-defect-class detection rates, corrections, rejections, false rejects, retained `reviewer`/`source`/`reason` audit check, and `total_ai_review_seconds` vs `total_workflow_seconds` (`net_effort_delta_seconds`).

### Unresolved Items

* Real human timing and error thresholds await `OQ-017` participant sessions.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement workflow-paired scenario runner, scripted panels, and effort/detection reporting

#### Context

Each scenario must run both `Store.ai_run(author, case_id, task, mode="workflow")` and the AI proposal review path (`Store.review_ai`) against the identical constructed case so effort and accuracy comparisons are apples-to-apples.

#### Intent

Build `evaluate_panel` and `run_automation_bias_harness` covering all five reviewer profiles and producing structured, JSON-serializable comparative metrics.

#### Boundaries

* Included:
  * Workflow baseline execution per scenario via `Store.ai_run(..., mode="workflow")`, capturing workflow output, citation verification, and baseline workflow effort (`workflow_seconds`).
  * Seeded AI recommendation generation via `Store.ai_run` + `ai_tasks.statement_sources` verification, followed by profile action through `Store.review_ai` and `human_review_gate` evaluation.
  * Profiles:
    * `competent`: authorised `Retrofit Coordinator` / `Resident Liaison Officer` checks case sources on every draft, edits half of seeded defects with accurate source-cited `override_text` + resolving source `reason`, rejects the remaining seeded defects with resolving source `reason`, and accepts valid controls with a source-grounded verification `reason` (`gate_passed_count == len(scenarios)`, `retained_evidence_complete == True`).
    * `default_accept`: rubber-stamps `accept` (`reason=""`) on every proposal without checking sources (`detection_rate == 0.0`, `gate_passed_count == 0`, `gate_leakage == 0`).
    * `automation_bias`: accepts confident + citation-valid (`verified == True`) proposals with a citation-badge-only reason without checking underlying sources, while checking hedged proposals against case sources (catching the hedged `wrong` defect `S-223-05` and verifying hedged control `S-223-07`, while missing all 5 confident defects -> `detection_rate == 1/6`, `gate_leakage == 0`).
    * `citation_only`: accepts every proposal whose `[[...]]` citations resolve (`verified == True`) citing only badge verification rather than case facts (`detection_rate == 0.0`, `gate_passed_count == 0`, `gate_leakage == 0`).
    * `unauthorised_competent`: detects defects accurately with source-cited reasons, but uses a `Retrofit Programme Manager` staff account outside `PROVISIONAL_AUTHORITY.allowed_roles` for `summary`/`message`, failing `human_review_gate` (`detection_rate == 1.0`, `gate_passed_count == 0`).
  * Metrics: `detection_rate`, `detected_count`, `seeded_defect_count`, `by_defect_class` (`wrong`, `stale`, `unsupported`, `incomplete`), `corrections`, `rejections`, `false_rejects`, `gate_passed_count`, `gate_leakage`, `retained_evidence_complete`, `audit_verified`, `total_ai_review_seconds`, `total_workflow_seconds`, `net_effort_delta_seconds`, `automation_bias_exposed`, and `evidence_class`.
* Excluded: Paid LLM calls or external file writes outside `tempfile.TemporaryDirectory`.

#### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: `evaluate_panel`, `run_automation_bias_harness`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `competent` achieves `detection_rate == 1.0`, `false_rejects == 0`, `gate_leakage == 0`, `gate_passed_count == len(scenarios)`; `automation_bias` achieves `0.0 < detection_rate < 1.0` (`1/6`), `gate_leakage == 0`; `default_accept` and `citation_only` achieve `detection_rate == 0.0`, `gate_leakage == 0`; `unauthorised_competent` achieves `detection_rate == 1.0`, `gate_passed_count == 0`.

#### Completion Evidence

* Harness assertions in `test_human_review_effectiveness_223.py` pass deterministically.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Implement `blank_worksheet`, `score_human_session`, and duplicate-safe `pool_human_sessions`

#### Context

When `OQ-017` human participant trials run, reviewers need a blind worksheet without defect/confidence labels, and assurance reviewers need deterministic scoring and multi-reviewer pooling that refuses fabricated or duplicated submissions.

#### Intent

Provide `blank_worksheet()`, `score_human_session(...)`, and `pool_human_sessions(...)`.

#### Boundaries

* Included:
  * `blank_worksheet()`: exports scenario ID, case ID, task, case snapshot, `source_labels`, workflow comparator text, AI proposal text, and empty response template (`disposition`, `edited_text`, `reason`, `review_seconds`) with zero `defect_class`, `confidence`, `forbidden_claims`, or expected answer keys.
  * `score_human_session(submission, ...)`: validates `named_human` reviewer identity, role/email binding, complete scenario coverage (no missing or unknown scenario IDs), positive numeric `review_seconds` per item, executes `Store.review_ai` + `human_review_gate` for every answer, and computes comparative detection and measured effort against the workflow-only baseline.
  * `pool_human_sessions(submissions, ...)`: requires `>= 1` valid human sessions, rejects duplicate normalized reviewer identities, aggregates per-class detection rates and mean/total review effort deltas against the workflow-only comparator, and marks `oq017_live_approved` according to `AuthorityPolicy`.
* Excluded: Writing unrequested files outside caller-provided paths.

#### Likely Targets

* `src/core/src/zava_forward/core/human_review_effectiveness.py`: `blank_worksheet`, `score_human_session`, `pool_human_sessions`.

#### Dependencies

* P02-T01.

#### Validation Expectations

* Unit tests verify zero spoiler keys in `blank_worksheet()`, accurate scoring of competent vs biased human worksheets, rejection of duplicate reviewers or zero/negative timing, and honest `evidence_class` labelling.

#### Completion Evidence

* Worksheet and session-pooling tests pass cleanly under `unittest` and `mypy --strict`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Targeted Tests, Documentation, and Strict Validation

### Context

Repository rules require focused tests that fail without the new controls, concise documentation of new core gates and governance boundaries in `src/core/README.md`, and targeted validation (`mypy`, `ruff check .`, `ruff format --check .`, `unittest -p 'test_*223*.py'`).

### Intent

Author `src/core/tests/test_human_review_effectiveness_223.py`, update `src/core/README.md`, and verify all targeted checks pass cleanly.

### Boundaries

* Included: `src/core/tests/test_human_review_effectiveness_223.py` and `src/core/README.md`.
* Excluded: Running unfiltered `unittest discover -s tests` without `-p`.

### Likely Targets

* `src/core/tests/test_human_review_effectiveness_223.py`: New targeted unit test suite.
* `src/core/README.md`: Concise subsection documenting `human_review_effectiveness.py` (`Refs #223`, `AC-070`, `OQ-017`).

### Dependencies

* P01, P02.

### Validation Expectations

* `cd /home/azureuser/source/ama-demo-wt/feat-223-human-review-effectiveness-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v` exits `0`.

### Completion Evidence

* Zero mypy/ruff issues and 100% passing `test_human_review_effectiveness_223.py` test cases.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author `src/core/tests/test_human_review_effectiveness_223.py`, update `src/core/README.md`, and run targeted validation

#### Context

Tests must exercise every acceptance criterion in Issue #223 plus contrarian bypass vectors so regressions are caught immediately.

#### Intent

Write clear, strictly typed unit tests in `src/core/tests/test_human_review_effectiveness_223.py`, document the module in `src/core/README.md`, and run the exact caller-specified validation command.

#### Boundaries

* Included:
  * Test seeded `wrong`, `stale`, `unsupported`, and `incomplete` defects all carry `verified == True` yet fail `human_review_gate` and `gates.transition_allowed` under `default_accept`, `citation_only`, and `automation_bias`.
  * Test `competent` panel detects all seeded defects (`edit` + `reject`), retains `reviewer`, `source` (`case_ids`, resolving source label, `source_hashes`, `compared` workflow baseline), and `reason`, passes `Store.verify_audit()`, and reports workflow-paired detection, corrections, and effort deltas across `summary` and `message`.
  * Test adversarial gate-gaming failures: cosmetic edit retaining wrong/unsupported text or omitting safety/accessibility facts, edited text adding an unresolved `[[...]]` citation, short/vague reason, unreasoned `accept` on valid control, unrelated source label in reason, canonical (`CM-...`, `memory:...`, `chat-memory`) and conversational (`"earlier in chat"`, `"the assistant said"`) chat-memory reference reasons, non-human and placeholder reviewers (`Copilot`, `system`, `TBD`, `pending`, `workflow`), unauthorised role, task-scope mismatch, `HOLD`/`QUARANTINED` proposal status, post-draft case mutation (`stale_case_sources`), unreviewed recommendation (`UNKNOWN`), and `live=True` under provisional `OQ-017` authority vs named-human approved test fixture.
  * Test `blank_worksheet()`, `score_human_session()`, and `pool_human_sessions()` (including duplicate reviewer and invalid timing rejection).
  * Concise `src/core/README.md` section for `#223`.
* Excluded: Unrelated core test suites.

#### Likely Targets

* `src/core/tests/test_human_review_effectiveness_223.py`
* `src/core/README.md`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Exact targeted `mypy` + `ruff check` + `ruff format --check` + `unittest -p 'test_*223*.py'` command exits `0`.

#### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md`.

#### Unresolved Items

* None.
