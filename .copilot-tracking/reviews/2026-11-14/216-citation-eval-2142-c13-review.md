<!-- markdownlint-disable-file -->
# Review: Child Hardening Pass 13 for Issue #216 (`216-citation-eval-2142-c13`)

## Scope and Evidence

* Task ID: `216-citation-eval-2142-c13`
* Review date: `2026-11-14`
* Review scope: Full task (`P01`: `P01-T01`, `P01-T02`)
* Assessed boundary: `src/core` citation validity and refusal accuracy gates, constituent freshness substantiation, compliance paraphrase refusals, dual-capacity owner agreement, and unit-cost ceiling enforcement (`BRD OD-51` preserved)
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c13-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c13-phase-details.md`
* Plan critique: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c13-plan-critique.md`
* Changes: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c13-changes.md`
* Other evidence considered: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c13-research.md`, `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c12-review.md`, `src/core` validation output, and independent read-only `rubber-duck` review lens

## Opening Review State

* Interpreted review goal: Verify closure of `RV-030`..`RV-033` and `PC-001`..`PC-004` inside `src/core` without regressions or open loopholes in Issue #216's locally verifiable acceptance criteria.
* Review scope: `P01` (`P01-T01`, `P01-T02`) and plan `## Follow-Up Items`.
* Evidence readiness: Plan, phase details, single-pass critique, changes record, and `src/core` test/static-analysis outputs are complete and reconciled.
* Acceptance basis: `AC-01`..`AC-05`, `PC-001`..`PC-004`, and Issue #216 `src/core` acceptance criteria.
* First comparison boundary: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c13-review.md` and session state.
* Initial blockers: None.

## Execution Status

* Execution status: `Complete`
* Review execution evidence: Completed single-pass reconciliation of `c13` artifacts, `src/core` validation (`mypy`, `ruff check`, `ruff format --check`, 16 Issue #216 tests, 58 companion tests), and independent `rubber-duck` adversarial inspection on `2026-11-14`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01-T01` | Implemented `_freshness_entry_valid`, expanded `_REFUSAL_PATTERNS[1]`, dual-owner `agreement_gaps`, and `_compute_cost_per_accepted_check` / `_extract_unit_cost_ceiling` | `Reconciled` | Implemented in `regulatory_eval_gates.py`; 4 edge-case gaps (`RV-034`..`RV-037`) identified during adversarial review |
| `P01-T02` | Updated fixtures, added `test_c13_*`, updated `src/core/README.md`, and ran `src/core` validation | `Reconciled` | All 16 Issue #216 tests and 58 companion tests pass |
| `Follow-Up Items` | Cross-package `src/api` and `src/agents` integration outside caller `src/core` scope | `Reconciled` | Preserved outside `src/core` write boundary |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01-T01` | `src/core/src/zava_forward/core/regulatory_eval_gates.py` | Closed `RV-030`..`RV-033` and `PC-001`..`PC-004` | Code inspection and unit assertions | `mypy`, `ruff`, `unittest` passed | Reconciled; routes `RV-034`..`RV-037` |
| `P01-T02` | `src/core/tests/test_regulatory_eval_gates_216.py`, `src/core/README.md` | Updated fixtures, added `test_c13_*`, and documented dual-owner + unit-cost ceiling rules | Test run and doc-link check | 16 + 58 tests passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P01-T01` (`agreement_gaps` & `_REFUSAL_PATTERNS[1]`) | Added `compliance_owner_id == refusal_owner_id` parity check and modal compliance-treatment / hyphenated sign-off regex branches | `test_c13_*` edge-case assertions within `FR-02`/`FR-03` | Documented in `c13-changes.md` (`Amendments and Divergences`) | Compatible within finalized `PC-003`/`PC-004` scope | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 4 findings (`PC-001`..`PC-004`) were applied before implementation and verified in `c13`.
* Material revisions: None required re-planning during `c13` implementation.
* Dependent-work pause assessment: Sequential execution honored all gates.
* Justification assessment: Supported by repository evidence and `BRD OD-51`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Wire `src/api` HTTP endpoints (`server.py`) and `src/agents` renderer/helpers to `RegulatoryChat.surface` and `render_extractive_answer` | User prompt explicitly restricts edits and verification in this workstream to `src/core` | Separate multi-package PR covering `src/api` and `src/agents` | Distinct cross-package follow-up outside `src/core` |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-034 -->
### RV-034 [High]: Present-participle obligation-satisfaction questions bypass `_REFUSAL_PATTERNS[1]`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_REFUSAL_PATTERNS[1]`) accepts `"Is this damp home meeting its legal obligations?"` (`refuse_question(...) is None`) because the obligation-satisfaction branch matches `do|does|did|has|have` + `met|meet|satisfy|satisfied` and omits `is|are|was|were|will|would|can|could|should` and progressive participles `meeting` / `satisfying`.
* Impact: Progressive-tense compliance/duty questions bypass refusal and select a regulatory lookup purpose.
* Destination: `rpi-implement`
* Smallest useful next action: Expand the obligation-satisfaction and modal subject-compliance branches in `_REFUSAL_PATTERNS[1]` to include `is|are|was|were|will|would|can|could|should` and progressive `meeting` / `satisfying`, with regression coverage.

<!-- rpi:review id=RV-035 -->
### RV-035 [High]: `unknown` card `source_freshness` status accepts misleading `in_cadence` label

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_card_provenance_valid` and `_active_bundle_nonconflicting`) only checks `(fresh_label == OUT_OF_CADENCE_LABEL) == (fresh_status == "out_of_cadence")`, allowing a card with `status == "unknown"` to carry `IN_CADENCE_LABEL` (`"Within monitoring cadence; not proof of legal currentness."`) instead of `source_monitor.card_freshness`'s canonical `"Source monitoring cadence unknown; ask the named owner."`.
* Impact: Unmonitored (`"unknown"`) rule cards can misstate monitoring freshness as `"Within monitoring cadence"` without failing provenance or bundle validation.
* Destination: `rpi-implement`
* Smallest useful next action: Enforce exact 3-way canonical label parity (`in_cadence`, `out_of_cadence`, `unknown`) matching `source_monitor.card_freshness` in both `_card_provenance_valid` and `_active_bundle_nonconflicting`.

<!-- rpi:review id=RV-036 -->
### RV-036 [High]: Post-dated future `agreed_on` dates and synthetic-flagged trial rows are accepted as pre-agreed staff trial evidence

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`agreement_gaps`, `_validate_benefit_thresholds`, `_compute_cost_per_accepted_check`, and `_score_paired_observations`) validates `agreed_on` only via `_valid_iso_day`, accepting post-dated values such as `"9999-12-31"` after the evaluated case `as_of` / `now` clock, and `_score_paired_observations` does not reject observation rows explicitly flagged `"synthetic": True` / `"simulated": True` or post-`now` / pre-`agreed_on` `observed_at` timestamps.
* Impact: Retroactive/future-dated threshold agreements or explicitly synthetic/simulated trial rows could produce `measured_value = True`.
* Destination: `rpi-implement`
* Smallest useful next action: Bound `agreed_on` in `agreement_gaps` (`<= min_case_as_of_day`), `_validate_benefit_thresholds` (`<= eval_day`), `_compute_cost_per_accepted_check` (`<= current.date().isoformat()`), and `compare_chat_against_rule_cards` (`verified_agreement.agreed_on <= eval_day`), validate optional observation `observed_at` (`agreed_on <= obs_day <= eval_day`), and reject observation rows marked `synthetic`/`simulated`.

<!-- rpi:review id=RV-037 -->
### RV-037 [Medium]: Rounded unit-cost ceiling check rejects valid exact costs near 6-decimal half-up boundary, and `RegulatoryChat` lacks optional instance-level ship-gate binding on `ask()`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` checks both `exact_unit_cost <= agreed_unit_ceiling` and `reported_unit_cost <= agreed_unit_ceiling`, falsely rejecting exact cost `0.0080006` (`round -> 0.008001`) under ceiling `0.0080007`; additionally, `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat`) does not yet expose an opt-in instance-level `ship_gate_comparison` / `enforce_ship_gate` guard so `ask()` can enforce the comparison gate when enabled without breaking `#214` unit tests.
* Impact: Valid sub-ceiling exact unit costs near rounding boundaries fail closed erroneously, and `RegulatoryChat` callers inside `src/core` cannot bind a comparison gate once at service construction to guard `ask()` alongside `surface()`.
* Destination: `rpi-implement`
* Smallest useful next action: Compare `exact_unit_cost <= agreed_unit_ceiling` directly in `compare_chat_against_rule_cards`, and add opt-in `ship_gate_comparison: Mapping[str, Any] | None = None` + `enforce_ship_gate: bool = False` on `RegulatoryChat` (used as default comparison in `surface()` and enforced in `ask()` when `enforce_ship_gate=True`).

## Defects

* `RV-034` (`High`) -> `rpi-implement` (child task `216-citation-eval-2142-c14`)
* `RV-035` (`High`) -> `rpi-implement` (child task `216-citation-eval-2142-c14`)
* `RV-036` (`High`) -> `rpi-implement` (child task `216-citation-eval-2142-c14`)
* `RV-037` (`Medium`) -> `rpi-implement` (child task `216-citation-eval-2142-c14`)

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| `RV-034` | `rpi-implement` | Child RPI loop `216-citation-eval-2142-c14` | Implementation defect in `_REFUSAL_PATTERNS[1]` progressive verb coverage |
| `RV-035` | `rpi-implement` | Child RPI loop `216-citation-eval-2142-c14` | Implementation defect in 3-way `source_freshness["label"]` validation |
| `RV-036` | `rpi-implement` | Child RPI loop `216-citation-eval-2142-c14` | Implementation defect in `agreed_on` temporal ordering and synthetic-trial row guards |
| `RV-037` | `rpi-implement` | Child RPI loop `216-citation-eval-2142-c14` | Implementation defect in rounded unit-cost check + opt-in `RegulatoryChat` instance ship-gate support |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Cross-package `src/api` and `src/agents` wiring (`server.py` route integration with `RegulatoryChat.surface` / `enforce_ship_gate=True` and `render_extractive_answer`) remains a distinct multi-package follow-up outside this `src/core`-bounded task.

## Blockers and Remaining Work

* Blockers: None.
* Remaining active work: None in `216-citation-eval-2142-c13`; `RV-034`..`RV-037` routed to child loop `216-citation-eval-2142-c14`.

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 -m mypy` | `src/core` (318 files) | `Passed` | `Success: no issues found in 318 source files` |
| `python3 -m ruff check .` | `src/core` | `Passed` | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (265 files) | `Passed` | `265 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` | `src/core/tests` | `Passed` | `Ran 16 tests in 17.772s - OK` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py` | `src/core/tests` | `Passed` | `Ran 58 tests in 31.899s - OK` |

## Outcome

* Outcome: `Defects found`
* Outcome rationale: `RV-030`..`RV-033` and `PC-001`..`PC-004` were delivered and verified, and independent adversarial review surfaced four concrete `src/core` hardening gaps (`RV-034`..`RV-037`) routed to child loop `216-citation-eval-2142-c14`.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | `rpi-implement` | Resolve `RV-034`..`RV-037` in child RPI loop `216-citation-eval-2142-c14` |
| Decision gap or invalid assumption | `none` | None |
| Material evidence gap | `none` | None |
| Non-blocking residual work | `distinct_follow_up` | Cross-package `src/api`/`src/agents` integration outside `src/core` write boundary |

* Execution status: `Complete`
* Outcome: `Defects found`
* Validation coverage: `mypy`, `ruff check`, `ruff format --check`, 16 Issue #216 tests, and 58 companion `src/core` tests all passed
* Blockers: None
