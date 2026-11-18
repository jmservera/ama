<!-- markdownlint-disable-file -->
# Review: Issue #216 Citation & Refusal Gates and Paired Rule-Card Comparison in `src/core`

## Scope and Evidence

* Task ID: 216-citation-eval-2142
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Owned citation-validity and refusal-accuracy gates measured on graded and adversarial sets plus paired chat-versus-rule-card value comparison and cards-alone surface selection inside `src/core`, preserving `ALLOWED = {"core"}` and strict `mypy`/`ruff`/`unittest` checks
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-research.md; `src/core/src/zava_forward/core/regulatory_eval_gates.py`; `src/core/tests/test_regulatory_eval_gates_216.py`; `src/core/README.md`; bounded independent `rubber-duck` lens

## Opening Review State

* Interpreted review goal: Confirm that the completed `src/core` implementation delivers both locally verifiable Issue #216 acceptance criteria, satisfies `PC-001`..`PC-004`, introduces no safety or fail-open defects, and reconciles all RPI artifacts and validation records.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Plan markers, phase details, critique dispositions, and changes record are complete and reconciled.
* Acceptance basis: Issue #216 criteria 1 and 4; ADR 0005 Evaluation and Chat Ship Test; `PC-001`..`PC-004`; `mypy`, `ruff`, `test_*216*.py`, `test_dependency_rule.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py`.
* First comparison boundary: Compare `src/core` source, test, and README changes against planned contracts and critique dispositions without mutating production files.
* Active read-only boundaries: Review updates only `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md`.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Executed once on 2026-11-14 across the reconciled full-task artifact set (`P01`, `P02`) and independent read-only `rubber-duck` inspection of `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01`, `P01-T02` | Core Regulatory Evaluation Gates and Paired Rule-Card Comparator | Reconciled | Source module created and documented; independent review identified fail-open grading/binding edge cases routed as `RV-001`..`RV-006`. |
| `P02`, `P02-T01`, `P02-T02` | End-to-End Core Verification and Component Documentation | Reconciled | Test suite and `src/core/README.md` subsection created and validated with `mypy`, `ruff`, and `unittest`. |
| `Follow-Up Items` | Out-of-band governance, live staff trial, and optional `src/agents` cleanup | Reconciled | Preserved outside active `P01`/`P02` completion scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`) | `src/core/src/zava_forward/core/regulatory_eval_gates.py` | Added owned citation/refusal gates, graded/adversarial sets, deterministic rule-card projection, paired comparator, and cards-alone surface selector | `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md` | `mypy`, `ruff`, `test_*216*.py` passed | Reconciled; 6 tightening defects (`RV-001`..`RV-006`) routed to child `rpi-implement` loop |
| `P02` (`P02-T01`, `P02-T02`) | `src/core/tests/test_regulatory_eval_gates_216.py`, `src/core/README.md` | Added SQLite/`RegulatoryChat` end-to-end tests and component documentation | `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md` | `test_*216*.py` (7), `test_dependency_rule.py` (2), `test_regulatory_chat.py` (25), `test_gates.py` (31), `test_live_doc_links.py` (2) passed | Reconciled; needs regression cases for `RV-001`..`RV-006` in child loop |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`grade_chat_turn`) | Checked section key set equality rather than insertion-order tuple equality because `RegulatoryChat.encode` persists JSON with `sort_keys=True` | Stored message key order in `SqlStore` / `Store`; local judgment | Recorded in `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md` | Not needed (preserves `PC-002` contract) | Reconciled |
| `P02-T01` (`test_regulatory_eval_gates_216.py`) | Prepended worktree `src/core/src` to `sys.path` before importing `zava_forward.core` | Editable `.pth` in shared user site-packages pointed at primary checkout; local judgment | Recorded in `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md` | Not needed (preserves `PC-004` single-test-file boundary) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`..`PC-004` recorded in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md` (`## Critique Disposition`).
* Material revisions: None during `Implement`; however, independent review identified `RV-005` where `compare_chat_against_rule_cards` unioned provision IDs with prefix URL checks instead of verifying exact per-card provision mappings and exact URLs required by `PC-001`.
* Dependent-work pause assessment: No early resumption occurred.
* Justification assessment: Local implementation judgments were justified; `RV-001`..`RV-006` require a child correction loop before claiming conformant delivery.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional `src/agents` deduplication against `zava_forward.core.regulatory_eval_gates` | Prompt scopes deliverable strictly to `src/core` | Later `src/agents` cleanup task | Distinct follow-up route |
| Operational owner threshold agreement and independent held-out legal benchmark | Human governance sign-off outside local repository execution | Legal, Compliance, and DPO owners | Distinct follow-up route |
| Live staff paired trial across `repairs`, `housing`, and `grants` with authorised pricing | Operational trial and paid model spend outside offline local scope | Programme, Safety, and Finance owners | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `P01` or `P02` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Extractive section grading permits extra unsupported claims around valid quotes

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`grade_chat_turn`) checks substring membership of expected provision quotes and home facts rather than exact extractive section equality, allowing appended unsupported compliance claims to pass `citation_validity` and `answer_contract`.
* Impact: Weakens the extractive citation-validity gate against hallucinated surrounding prose.
* Destination: `rpi-implement`
* Smallest useful next action: Require exact extractive `what_sources_say` and `recorded_home_facts` equality (matching `render_extractive_answer` canonical formatting) in `grade_chat_turn` and add a negative test with appended unsupported claims.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Paired comparator accepts unbound or stale `gates_report` payloads

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards`) checks `gates_report` pass flags without binding the report to a digest of `evaluated_cases` including `actual` outputs.
* Impact: A previously passing `gates_report` reused with mutated `evaluated_cases` could still report `measured_value = True`.
* Destination: `rpi-implement`
* Smallest useful next action: Emit `evaluated_outputs_sha256` (covering canonical case definitions and `actual` outputs) from `evaluate_citation_and_refusal_gates` and require `gates_report["evaluated_outputs_sha256"]` to match `evaluated_cases` in `compare_chat_against_rule_cards`.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Card-arm `hazard_missed` observations do not trigger critical failure severity

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards`) counts `chat_hazard_misses` toward `failure_severity = "critical"` while leaving `cards_hazard_misses > 0` at `failure_severity = "none"`.
* Impact: Violates the plan rule that any observed `hazard_missed is True` in paired trial observations marks `failure_severity = "critical"` and blocks `measured_value`.
* Destination: `rpi-implement`
* Smallest useful next action: Treat `(chat_hazard_misses + cards_hazard_misses + unpaired_hazard_misses) > 0` across any trial observation as `failure_severity = "critical"` and require zero hazard misses across all observations before enabling chat.

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: `OwnerGateAgreement` accepts arbitrary non-blank owner names instead of the named gate owner

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`agreement_gaps`) checks that `owner` is non-blank and distinct from `independent_grader`, without verifying that `owner` matches `LEGAL_GATE_OWNER` (`GATE_OWNERS["citation_validity"]` / `GATE_OWNERS["refusal_accuracy"]`).
* Impact: Allows an agreement signed by an unrelated string to transition `threshold_status` to `"owner_agreed"`.
* Destination: `rpi-implement`
* Smallest useful next action: Require `_canon_name(owner) == _canon_name(LEGAL_GATE_OWNER)` in `agreement_gaps` and add a negative test for mismatched gate owners.

<!-- rpi:review id=RV-005 -->
### RV-005 [High]: Active rule-card link parity checks URL prefixes and unioned provision IDs instead of exact per-card mappings

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards`) checks `startswith("/api/law/cards/")` / `startswith("/api/law/provisions/")` and unions provision IDs across cards rather than verifying exact encoded card/provision links and exact per-card provision correlation against `deterministic_rule_cards(expected_bundle)`.
* Impact: Swapped provisions across cards or wrong link suffixes can pass active link parity.
* Destination: `rpi-implement`
* Smallest useful next action: Verify exact `/api/law/cards/{quote(id, safe='')}` and `/api/law/provisions/{quote(id, safe='')}` links and exact per-card `provisions` parity against `deterministic_rule_cards` for every `answer` case.

<!-- rpi:review id=RV-006 -->
### RV-006 [Medium]: Extreme integer token counts raise `OverflowError` in `cost_per_accepted_check`

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`cost_per_accepted_check`) divides huge Python ints (`10**400 / 1_000_000.0`) directly into float division, raising `OverflowError` instead of failing closed to `"Unknown"`.
* Impact: Unbounded integer token inputs raise an exception rather than returning `"Unknown"`.
* Destination: `rpi-implement`
* Smallest useful next action: Convert token counts through `_finite_float` before float arithmetic and return `"Unknown"` when non-finite or overflowing, with a unit test for `10**400`.

## Defects

* `RV-001` (`High`) -> `rpi-implement`
* `RV-002` (`High`) -> `rpi-implement`
* `RV-003` (`High`) -> `rpi-implement`
* `RV-004` (`High`) -> `rpi-implement`
* `RV-005` (`High`) -> `rpi-implement`
* `RV-006` (`Medium`) -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in extractive section grading |
| `RV-002` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in `gates_report` output binding |
| `RV-003` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in card-arm hazard-miss severity |
| `RV-004` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in named gate-owner binding |
| `RV-005` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in exact per-card provision and URL parity |
| `RV-006` | `rpi-implement` | Child task `216-citation-eval-2142-c1` | Implementation defect in huge-int float conversion |

Later implementation of a routed finding does not require another Review inside this completed parent task; child task `216-citation-eval-2142-c1` executes its own RPI loop.

## Residual Work

* Optional `src/agents` deduplication against `zava_forward.core.regulatory_eval_gates` (outside `src/core` task scope).
* Operational owner threshold agreement, held-out external legal grading benchmark, and live staff paired trial with authorised pricing (human governance prerequisites outside local code scope).

## Blockers and Remaining Work

* Blockers: none for parent task closeout; `RV-001`..`RV-006` are routed to child task `216-citation-eval-2142-c1`.
* Remaining active work: none in parent task `216-citation-eval-2142` (`P01` and `P02` executed).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (318 files) | Passed | Zero issues under `strict = true` |
| `python3 -m ruff check .` | `src/core` | Passed | All checks passed |
| `python3 -m ruff format --check .` | `src/core` | Passed | 265 files formatted |
| `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` | `src/core/tests/test_regulatory_eval_gates_216.py` | Passed | 7 tests passed |
| `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -v` | `src/core/tests/test_dependency_rule.py` | Passed | 2 tests passed (`ALLOWED = {"core"}`) |
| `python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -v` | `src/core/tests/test_regulatory_chat.py` | Passed | 25 tests passed |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_gates.py' -v` | `src/core/tests/test_gates.py` | Passed | 31 tests passed |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -v` | `src/core/tests/test_live_doc_links.py` | Passed | 2 tests passed |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned tasks `P01` and `P02` executed and passed baseline static and runtime checks, but independent `rubber-duck` review identified five High fail-open/binding gaps (`RV-001`..`RV-005`) and one Medium integer-overflow edge case (`RV-006`) that must be resolved in child task `216-citation-eval-2142-c1` before claiming conformant acceptance criteria delivery.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Child task `216-citation-eval-2142-c1` (`RV-001`..`RV-006`) |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Operational governance sign-off, live staff trial, and optional `src/agents` deduplication |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: `mypy`, `ruff check`, `ruff format --check`, `test_*216*.py`, `test_dependency_rule.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py` passed; regression tests for `RV-001`..`RV-006` routed to child task
* Blockers: none

