<!-- markdownlint-disable-file -->
# Review: Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness (#223)

## Scope and Evidence

* Task ID: 223-human-review-effectiveness-2305
* Review date: 2026-11-14
* Review scope: full_task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Assessed boundary: `src/core` engineering acceptance criteria for GitHub Issue #223 (`AC-070`, `FR-026`, `FR-027`, `FR-028`, `NFR-009`, `OQ-017`), `Store.ai_run` / `Store.review_ai` / `gates.GateResult` runtime integration, automation-bias and blind human-session harness, `src/core/README.md` documentation, and targeted static/unit/privacy checks.
* Plan: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/human-review-effectiveness-223-2305-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md; `src/core/src/zava_forward/core/human_review_effectiveness.py`; `src/core/tests/test_human_review_effectiveness_223.py`; `src/core/README.md`

## Opening Review State

* Interpreted review goal: Verify that the completed `src/core` implementation satisfies all five locally verifiable Issue #223 acceptance criteria, resolves `PC-001` through `PC-004` without drift, preserves fail-closed `OQ-017` human-oversight boundaries, and passes targeted `mypy`, `ruff`, `unittest`, and synthetic-privacy validation.
* Review scope: full_task (`P01` through `P03`)
* Evidence readiness: Ready; research, ready plan, phase details, single-pass plan critique, reconciled changes record, implementation module, test suite, and documentation are present and dated `2026-11-14`.
* Acceptance basis: `FR-223-01`..`FR-223-04`, `NFR-223-01`, `NFR-223-02`, `AC-1`..`AC-5`, and `PC-001`..`PC-004` dispositions in `.copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md`.
* First comparison boundary: Reconcile `P01`–`P03` markers, implementation-time local judgment refinements, and `PC-001`–`PC-004` runtime contracts against `human_review_effectiveness.py` and `test_human_review_effectiveness_223.py`.
* Active read-only boundaries: Read-only verification across repository sources and prior RPI phase artifacts; write authority restricted to this canonical review record (and parent RPI state record).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass full-task review on 2026-11-14 across `.copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md`, `.copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-14/human-review-effectiveness-223-2305-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md`, `src/core/src/zava_forward/core/human_review_effectiveness.py`, `src/core/tests/test_human_review_effectiveness_223.py`, `src/core/README.md`, and an independent read-only adversarial lens (`rubber-duck`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | P01: Core Gate, Authority Policy, and Seeded Scenarios | Reconciled | `[x]` markers in plan match implemented `AuthorityPolicy`, `PROVISIONAL_AUTHORITY`, `DEFAULT_SCENARIOS` (`S-223-01`..`S-223-08`), `inspect_discrepancies`, and `human_review_gate` (`gates.GateResult` + `gates.GateRule`). |
| `P02` (`P02-T01`, `P02-T02`) | P02: Workflow-Only Comparator, Automation-Bias Harness, and Human Session Scoring | Reconciled | `[x]` markers in plan match implemented `evaluate_panel`, `run_automation_bias_harness`, `blank_worksheet`, `score_human_session`, and `pool_human_sessions`. |
| `P03` (`P03-T01`) | P03: Targeted Tests, Documentation, and Strict Validation | Reconciled | `[x]` markers in plan match `test_human_review_effectiveness_223.py`, `src/core/README.md`, and passed static/unit/privacy checks. |
| `## Follow-Up Items` | `OQ-017` authority appointment and blind human sessions | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` completion claims in both plan and changes record; `live=True` fails closed under `PROVISIONAL_AUTHORITY`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/human_review_effectiveness.py` | Defined `AuthorityPolicy`, `PROVISIONAL_AUTHORITY` (`rai_release.AUTHORITY_GAP`), constructed two-case dataset (`ZF-223-A`, `ZF-223-B`), and 8 citation-valid scenarios across `summary` and `message` covering `wrong`, `stale`, `unsupported`, `incomplete`, and hedged/confident valid controls (`none`). | All 8 scenarios carry resolving `[[...]]` citations (`citation_verified == True`). | `mypy`, `ruff`, `test_seeded_defects_all_carry_valid_citations_across_tasks_and_classes` (`Passed`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/human_review_effectiveness.py` | Implemented fail-closed `human_review_gate` returning `gates.GateResult` + `gates.GateRule` compatible with `gates.transition_allowed`, enforcing reviewed status, `HOLD`/`QUARANTINED` refusal, `live=True` `OQ-017` block, `is_valid_human_identity`, role/task scope, `ai_tasks.source_hashes` freshness, non-memory substantive case-source-cited `reviewer_reason`, and discrepancy verification across `accept`, `edit`, and `reject`. | Blocks default accept, citation-only, automation bias, cosmetic edits, memory citations, stale cases, and unauthorised/provisional actors. | `mypy`, `ruff`, `test_adversarial_gate_bypasses_and_staleness_fail_closed`, `test_live_mode_fails_closed_until_named_human_oq017_approval` (`Passed`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/human_review_effectiveness.py` | Implemented `evaluate_panel` and `run_automation_bias_harness` pairing AI reviews 1-to-1 with `Store.ai_run(..., mode="workflow")`, checking `Store.verify_audit()`, and reporting detection (`overall` and `by_defect_class`), corrections, rejections, false rejects, zero gate leakage, and workflow effort deltas. | `competent` achieves `detection_rate == 1.0`, `gate_passed_count == 8`, `gate_leakage == 0`; `default_accept` and `citation_only` achieve `gate_passed_count == 0`; `automation_bias` achieves `1/6` detection and `automation_bias_exposed == True`. | `mypy`, `ruff`, `test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort`, `test_automation_bias_default_accept_citation_only_and_unauthorised_fail_gate` (`Passed`) | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/human_review_effectiveness.py` | Implemented spoiler-free `blank_worksheet`, `score_human_session`, and duplicate-rejecting `pool_human_sessions` preserving `oq017_live_approved=False` until named human authority exists. | Serialized worksheet omits all defect/confidence/solution spoilers; duplicate reviewer emails/names and non-positive/boolean timings raise `ValueError`. | `mypy`, `ruff`, `test_blank_worksheet_has_no_spoilers_and_human_sessions_pool_safely` (`Passed`) | Reconciled |
| `P03-T01` | `src/core/tests/test_human_review_effectiveness_223.py`, `src/core/README.md` | Added 6 focused multi-assertion unit tests covering `AC-1`..`AC-5` and documented the module and `OQ-017` boundary in `src/core/README.md`. | All targeted checks exit `0`; `synthetic.privacy.public_issues` returns `[]`. | `mypy`, `ruff check .`, `ruff format --check .`, `unittest -p 'test_*223*.py'` (`Passed`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` / `P02-T01` offline `Store` helper | Set `store.ai.fast = "synthetic-eval-223"` and `store.ai.strong = "synthetic-eval-223"` so `ai_registry.legacy_deployment(task, store.ai)` matches the offline proposal's deployment in `Store.release_current`. | Runtime check of `Store.release_current` (`store.py`); ordinary local judgment within `PC-002` intent. | Documented in `.copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md`. | Not needed (preserves `PC-002` offline `Store.review_ai` execution). | Reconciled |
| `P01-T01` scenario citations (`S-223-01`..`S-223-08`) | Aligned resident-decision inline citations to `[[Resident decision: Not recorded]]` matching `resident_decisions.resident_status` output in `ai_tasks.source_labels`. | Runtime citation check (`verified == True` across all 8 scenarios); ordinary local judgment within `PC-002`. | Documented in `.copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md`. | Not needed (preserves `AC-1` and `PC-002`). | Reconciled |
| `P02-T01` / `P02-T02` `gate_leakage` counter | Counted `gate_leakage` only when `allowed and not detected` so competent edits/rejections that resolve seeded defects report `gate_leakage == 0`. | Unit test check on `competent` panel; ordinary local judgment matching `FR-223-03` (`gate_leakage == 0` across all panels). | Documented in `.copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md`. | Not needed (matches `FR-223-03` specification). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` (`gates.GateResult`/`GateRule` exact signature and `effective_date`), `PC-002` (offline `Store.ai_run`/`review_ai` release binding, same-user ownership, `override_text`, `compared`, `HOLD`/`QUARANTINED`, 3-arg `source_hashes`, `source_labels`), `PC-003` (mandatory substantive case-source-cited `reviewer_reason` across `accept`, `edit`, and `reject`), and `PC-004` (placeholder/automation actor token refusal and conversational memory phrase refusal) are all resolved in the plan and verified in `human_review_effectiveness.py` and `test_human_review_effectiveness_223.py`.
* Material revisions: None required during implementation; all three implementation-time refinements were ordinary local judgments preserving approved architecture and acceptance criteria.
* Dependent-work pause assessment: No pause required; tasks executed in dependency order (`P01` -> `P02` -> `P03`).
* Justification assessment: Supported by static, runtime, and audit-chain evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Appoint competent-review authority holders and owner-defined oversight thresholds under `OQ-017`, then run blind human reviewer sessions using `blank_worksheet()` and `pool_human_sessions()` before enabling `live=True` release gating | Requires named human governance appointments (Sponsor, Programme, Safety, DPO/Legal, Assurance) and real human participant trials that cannot be fabricated by software or role agents | Programme Owner / Assurance Lead (`OQ-017`) | Open governance follow-up; kept outside active `P01`–`P03` scope, enforced fail-closed when `live=True`, and routed to distinct follow-up item. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Harden standalone `human_review_gate` against tampered in-memory records and `scenario=None` discrepancy-source binding

* Related scope: `P01-T02` (downstream API/orchestrator wiring hardening beyond `Store.review_ai`-mediated records)
* Evidence: `src/core/src/zava_forward/core/human_review_effectiveness.py` (`human_review_gate`, `inspect_discrepancies`)
* Impact: Within `Store.review_ai`, `review_evidence.disposition`, `compared`, and `resolved_by` are written atomically by `Store`. However, if a downstream caller invokes `human_review_gate` standalone (`scenario=None` or with caller-supplied `staff_member` / mutated dicts), preferring `store.staff[resolved_by]` over `staff_member`, checking `review_evidence["disposition"] == rec["reviewer_action"]` and `compared["ai"] == rec["ai_output"]`, and deriving expected resolving `source_labels` directly from `inspect_discrepancies` classes when `scenario is None` (plus hashing hazard priority/detail subfields beyond `source_labels` and rejecting contradictory "repaired and released" + "open safety issue" text) would close adversarial caller-tampering vectors.
* Destination: follow_up
* Smallest useful next action: Add cross-field record integrity checks, discrepancy-derived resolving source expectations when `scenario=None`, and extended hazard-field snapshot checks when wiring `human_review_gate` into live API/orchestrator surfaces.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Retain per-row reason/edit payloads in `score_human_session` and bind `live=True` to approval date and pooled trial thresholds

* Related scope: `P02-T02` (post-`OQ-017` human trial execution readiness)
* Evidence: `src/core/src/zava_forward/core/human_review_effectiveness.py` (`human_review_gate`, `score_human_session`, `pool_human_sessions`)
* Impact: `score_human_session` verifies `Store.verify_audit()` inside an ephemeral workspace and returns aggregate metrics plus per-scenario disposition/gate outcomes, while `live=True` checks `not authority.provisional`, `is_valid_human_identity(authority.approved_by)`, and ISO `approved_on`. Retaining `reviewer_reason`, `edited_text`, and optional participant-measured `workflow_seconds` in `score_human_session` output rows — and requiring `approved_on <= evaluation_date` plus an attested pooled human-trial receipt on `AuthorityPolicy` for `live=True` — will strengthen durable auditability once real `OQ-017` human sessions run.
* Destination: follow_up
* Smallest useful next action: Extend `score_human_session` row exports with `reviewer_reason`/`edited_text`, support measured participant workflow seconds alongside `scenario.workflow_seconds`, and enforce `approved_on <= on` + pooled trial attestation on `AuthorityPolicy` before live gate activation.

## Defects

* None in declared `P01`–`P03` engineering scope (`AC-1` through `AC-5` and `PC-001` through `PC-004` satisfied).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up item | Core / API integration follow-up task | Non-blocking defense-in-depth hardening for standalone untrusted callers (`scenario=None` / mutated dicts) beyond `Store.review_ai`-backed Issue #223 criteria |
| `RV-002` | Distinct follow-up item | `OQ-017` human-trial runner enhancement task | Non-blocking human-session evidence retention and live-approval date/trial-receipt binding ahead of real participant sessions |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `OQ-017` human governance follow-up: Named human appointments for competent-review authority and owner-defined oversight thresholds, followed by blind human participant sessions using `blank_worksheet()` and `pool_human_sessions()` (`Refs #223`).
* `RV-001`: Cross-field record integrity, `scenario=None` discrepancy-to-source mapping, and sub-label hazard snapshot hardening for standalone `human_review_gate` callers.
* `RV-002`: Per-row `reviewer_reason`/`edited_text` retention, optional participant-measured workflow timing, and `approved_on <= evaluation_date` + trial-receipt check in `score_human_session` / `AuthorityPolicy`.

## Blockers and Remaining Work

* Blockers: None for local engineering delivery (`OQ-017` remains an explicit human governance prerequisite preventing Issue #223 full closure; commit uses `Refs #223`).
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (329 source files) | Passed | `Success: no issues found in 329 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (276 files) | Passed | `276 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v` | `src/core/tests/test_human_review_effectiveness_223.py` | Passed | `Ran 6 tests in 0.730s — OK` |
| `synthetic.privacy.public_issues(repo_root)` | Repository synthetic provenance guard | Passed | `[]` (zero unregistered `evals/` files or privacy issues) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All declared phases and tasks (`P01`–`P03`), functional and non-functional requirements (`FR-223-01`..`FR-223-04`, `NFR-223-01`, `NFR-223-02`), Issue #223 locally verifiable engineering acceptance criteria (`AC-1`..`AC-5`), and plan critique dispositions (`PC-001`..`PC-004`) are implemented in `src/core`, documented in `src/core/README.md`, and verified by targeted `mypy`, `ruff`, `unittest`, and synthetic-privacy checks. No material defects or decision gaps remain in active scope; `RV-001`, `RV-002`, and `OQ-017` human trials are routed cleanly as distinct non-blocking follow-up items while `live=True` fails closed.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | Distinct follow-up items (`RV-001`, `RV-002`, and `OQ-017` governance/participant sessions) | Select ranked follow-up in automatic RPI session or defer until `OQ-017` human appointments complete |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy` (329 files), `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*223*.py' -v` (6/6 passed), and `synthetic.privacy.public_issues` (`[]`)
* Blockers: None for engineering scope (`OQ-017` human sign-off and real participant trials remain open governance prerequisites; use `Refs #223`)

