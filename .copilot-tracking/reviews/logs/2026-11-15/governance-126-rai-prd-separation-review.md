<!-- markdownlint-disable-file -->
# Review: Issue #126 RAI Closure and PRD Separation Slice

## Scope and Evidence

* Task ID: issue-126-rai-prd-separation
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Core governance runtime separation of `prd_quality_review` and `prd_owner_acceptance` from RAI baseline report acceptance (`baseline-assessment-and-remediation-planning only`) and remediation claim completion (`dispositions_complete`), disabled affected dispatch and conditional EU assurance applicability guards (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`), synchronized canonical documentation/ADR/index/append-only log updates preserving historical versions and negative/insufficient outcomes, and focused JSON/SQLite/repository-doc invariant tests.
* Plan: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/governance-126-rai-prd-separation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md, `git diff` across `src/` and `docs/`, focused unit/link/API tests, `ruff`, `mypy`, and independent read-only review lens.

## Opening Review State

* Interpreted review goal: Independently verify that all three Issue #126 acceptance contracts (`FR-1` through `FR-3`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`), critique dispositions (`PC-001` through `PC-004`), and repository honesty/hygiene rules are proven by the completed `P01`-`P03` implementation without overclaiming live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — plan markers (`P01`-`P03`), phase details, plan critique (`PC-001`-`PC-004`), changes record, and focused validation results are complete and reconciled.
* Acceptance basis: Caller Issue #126 acceptance criteria (Contracts 1-3 and Rules), approved plan (`FR-1` through `FR-3`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`), and plan critique dispositions (`PC-001` through `PC-004`).
* First comparison boundary: Reconcile `P01` (`governance.py`), `P02` (`addendum`, `PRD`, `ADR 0002`, `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md`), and `P03` (`test_governance.py` and validation runs) against plan requirements and critique dispositions without modifying source or planning files.
* Active read-only boundaries: Read-only across `src/`, `docs/`, and prior `.copilot-tracking/` research/plan/details/critique/changes artifacts; write access restricted solely to `.copilot-tracking/reviews/logs/2026-11-15/governance-126-rai-prd-separation-review.md` and RPI session state transitions.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed on 2026-11-15 across the full declared scope (`P01`, `P02`, `P03`) by comparing the approved plan, phase details, plan critique (`PC-001` through `PC-004`), reconciled changes record, `git diff -- src docs`, focused unit/link/API validation runs, and an independent read-only review lens (`review-lens-126`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01` (`P01-T01`, `P01-T02`) | Core Governance Register PRD Separation and Dispatch/EU Boundaries | Reconciled | `_rai_view` and `governance_view` project fresh `dict(PRD_QUALITY_REVIEW)` and `dict(PRD_OWNER_ACCEPTANCE)` copies without reading stored overrides, and `_rai_view` exposes `affected_dispatch`, `conditional_eu_assurance`, and `RAI_EU_CONDITIONAL` (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) finding guards alongside `live_use`. |
| `P02` (`P02-T01`, `P02-T02`) | Canonical Documentation, ADR 0002, Core Guide, and Knowledge Base Reconciliation | Reconciled | All six target Markdown documents record the 2026-11-15 Issue #126 separation and guard boundaries while preserving historical versions, negative/insufficient outcomes, valid relative links/anchors, zero added tracking-path strings, and strictly append-only EOF changes on `docs/reference/log.md`. |
| `P03` (`P03-T01`, `P03-T02`) | Focused Runtime and Repository Documentation Invariant Tests and Validation | Reconciled | Five focused test methods added in `src/core/tests/test_governance.py` (`<= 8` ceiling, `0` removals) covering JSON, SQLite, and container-safe repository doc/index/log invariants; all focused tests, `ruff`, `mypy`, and diff audits passed. |
| `Follow-Up Items` | Non-engineering human/live prerequisites on Issue #126 | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` implementation and acceptance claims in both `plan.md` and `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01-T01` | `src/core/src/zava_forward/core/governance.py` | Added `PRD_QUALITY_REVIEW` and `PRD_OWNER_ACCEPTANCE` constants and fresh `dict(...)` projections in `_rai_view` and `governance_view` so PRD quality review and Product Owner acceptance stay separate from `baseline.acceptance_scope` (`baseline-assessment-and-remediation-planning only`) and 22/22 `dispositions_complete`. | Verified in `governance.py` and `changes.md`. | Passed JSON and SQLite `test_prd_review_and_owner_acceptance_stay_separate_from_report_and_claims` plus `test_governance_evidence_api.py` (10 tests). | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/governance.py` | Defined `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, `RAI_AFFECTED_DISPATCH`, and `RAI_CONDITIONAL_EU_ASSURANCE`, exposed `affected_dispatch` and `conditional_eu_assurance` alongside `live_use`, and annotated finding rows with `conditional_eu` and `applicability_review`. | Verified in `governance.py` and `changes.md`. | Passed JSON and SQLite `test_live_use_blocked_dispatch_disabled_and_conditional_eu_guards` and `test_inventory`. | Reconciled |
| `P02-T01` | `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md` | Added concise `2026-11-15` Issue #126 reconciliation paragraphs preserving `0.12.0`, `0.14.0`, `0.16.0`, unsigned `0.21.0`, baseline `1cb398c7b90bec05a5700008a97d0cfac494144a`, and all negative/insufficient outcomes without claiming live deployment or human/DPIA approvals. | Verified in `git diff -- src docs`. | Passed `GovernanceDocumentationContractTests`, `test_live_doc_links.py`, and `check-legacy-references.py` (`0` link violations). | Reconciled |
| `P02-T02` | `docs/reference/README.md`, `docs/reference/log.md` | Updated the knowledge-base index `#126` status paragraph (`ms.date: 2026-11-15`) and appended `## [2026-11-15] update | Governance PRD separation and conditional EU assurance boundaries (Refs #126)` at EOF. | Verified pure `+` diff hunk at EOF on `docs/reference/log.md`. | Passed `test_knowledge_index_and_append_only_log_record_issue_126_evidence` and `test_links_anchors_and_no_tracking_leaks_across_governance_surfaces`. | Reconciled |
| `P03-T01` | `src/core/tests/test_governance.py` | Added 2 runtime methods on `EvidenceRegister` and 3 container-safe methods on `GovernanceDocumentationContractTests` using constructed `TRACKING_SEGMENT` so zero literal tracking-path strings exist in `src/`. | Verified 5 added test methods (`<= 8` budget, `0` removals). | Passed 82 discovered tests (`64` executed, `18` opt-in MSSQL skipped, `0` failures). | Reconciled |
| `P03-T02` | `src/core/README.md` (prose alignment), validation suite | Executed unit, link, API, lint, format, type, and diff hygiene checks; aligned explicit `report_acceptance_scope="baseline-assessment-and-remediation-planning only"` field wording in `src/core/README.md`. | Recorded in `changes.md` `## Validation Record`. | All 7 validation checks passed with exit code `0`. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P02-T01` / `P03-T02` (`src/core/README.md`) | Added explicit `report_acceptance_scope="baseline-assessment-and-remediation-planning only"` alongside `separate_from_report_acceptance=True` in `src/core/README.md`. | Triggered by `GovernanceDocumentationContractTests` checking the shared acceptance-scope string across all four governance doc surfaces; local judgment requiring no user decision. | Reconciled in `src/core/README.md` and documented in `changes.md` `## Implementation-Time Plan and Detail Updates`. | Not needed — preserved approved `FR-3` intent and `PC-001`-`PC-004` critique dispositions without changing scope or acceptance criteria. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001` [High] historical tracking-reference scoping, `PC-002` [High] `docs/reference/README.md` `#126` section anchor scoping, `PC-003` [Medium] explicit `RAI_EU_CONDITIONAL` constant definition, and `PC-004` [Medium] per-file whitespace-normalized historical/adverse token mapping) were resolved directly in the plan, phase details, and implementation.
* Material revisions: None. No implementation discovery altered requirements, architecture, scope, dependencies, or acceptance boundaries.
* Dependent-work pause assessment: No pause required; tasks executed sequentially in plan order (`P01` -> `P02` -> `P03`).
* Justification assessment: Supported by direct source, diff, and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Fresh independent `prd-quality-reviewer` assessment and human Product Owner sign-off on consolidated PRD `v0.21.0` (`OD-35` to `OD-55`) | Human Product Owner sign-off and open organisational decisions cannot be satisfied or claimed by engineering code. | Product Owner / independent PRD review workflow | Open non-engineering prerequisite — routed as distinct follow-up outside active `P01`-`P03` acceptance scope. |
| Qualified human, DPO/legal, and safety Responsible AI acceptance, EU AI Act applicability determination, and OD-36 DPIA / lawful-basis sign-off | Explicit caller non-goal (`without claiming live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off`). | Programme Manager, DPO/Legal, and Safety Leads | Open non-engineering prerequisite — routed as distinct follow-up outside active `P01`-`P03` acceptance scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Section-scoped current-status and baseline-digest checks could harden future documentation regression tests

* Related scope: `P03-T01`
* Evidence: `src/core/tests/test_governance.py` (`GovernanceDocumentationContractTests.test_addendum_prd_adr_and_core_guide_record_separation_and_preserve_history` and `test_knowledge_index_and_append_only_log_record_issue_126_evidence`)
* Impact: Current tests verify whole-document presence of all required separation/historical tokens across `addendum`, `PRD`, `ADR 0002`, and `src/core/README.md`, and verify chronological heading ordering plus `[2026-11-15]` section contents on `docs/reference/log.md` (backed by `git diff` EOF verification in `P03-T02`). Future edits elsewhere in a large document could theoretically introduce contradictory wording while leaving historical tokens intact.
* Destination: follow-up
* Smallest useful next action: Optional future test-hardening slice can scope positive current-contract token assertions to each document's `#126` subsection via `_section_text(...)` and optionally assert sibling-copy independence across all four returned `prd_*` dicts in one test.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Documentation prose calls detached server-computed `dict` snapshots "immutable"

* Related scope: `P02-T01`
* Evidence: `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`
* Impact: In governance domain terms, stored register state cannot mutate or override `prd_quality_review` or `prd_owner_acceptance`, and mutating a returned view dictionary does not affect subsequent `governance_view` calls; in Python runtime terms, each call returns a fresh mutable `dict` copy rather than a `MappingProxyType`. Non-blocking terminology nuance only.
* Destination: follow-up
* Smallest useful next action: If governance view schemas are touched in a later core cleanup, consider wording `"detached, server-computed"` in prose or wrapping internal constants in `types.MappingProxyType` while keeping JSON-serializable `dict(...)` view outputs.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| `RV-001` | follow-up | Core test maintenance (optional hardening) | Non-blocking test-specificity hardening; current `AC-1` through `AC-5` and `PC-002` invariants are satisfied and verified by tests + `git diff`. |
| `RV-002` | follow-up | Core documentation maintenance (optional wording polish) | Non-blocking terminology precision (`detached, server-computed` vs `immutable` returned `dict` copies); runtime behavior is safe and JSON-serializable. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Non-blocking optional test/prose polish (`RV-001`, `RV-002`) and external human/legal governance prerequisites tracked in `## Plan Follow-Up Assessment` (fresh PRD `0.21.0` quality review and Product Owner sign-off, real OD-36 DPIA/lawful-basis approval, qualified EU applicability review, and human/budget-owner sign-off before live pilot release).

## Blockers and Remaining Work

* Blockers: None for this engineering and documentation slice.
* Remaining active work: None (`P01`, `P02`, and `P03` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v` | `src/core` JSON, SQLite, and repository doc contracts | Passed | `Ran 82 tests in 13.867s — OK (skipped=18)` (18 opt-in task-owned loopback MSSQL tests skipped by design in focused tier) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_live_doc_links.py" -v` | Live documentation relative links | Passed | `Ran 2 tests in 1.864s — OK` |
| `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_governance_evidence_api.py" -v` | Downstream HTTP API governance evidence compatibility | Passed | `Ran 10 tests in 10.084s — OK` |
| `cd src/core && python3 -m ruff check .` | `src/core` lint | Passed | `All checks passed!` |
| `cd src/core && python3 -m ruff format --check .` | `src/core` format check | Passed | `314 files already formatted` |
| `cd src/core && python3 -m mypy` | `src/core` static type check | Passed | `Success: no issues found in 367 source files` |
| `python3 tools/check-legacy-references.py` & `git diff` audit | Repository link resolution & tracking-leak / append-only audit | Passed | `links: 0 violation(s) in 819 document(s)`; zero added `.copilot-tracking` strings in `src/` or `docs/`; `docs/reference/log.md` diff strictly `+` lines at EOF |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases and tasks (`P01`, `P02`, `P03`), functional and non-functional requirements (`FR-1` through `FR-3`, `NFR-1`, `NFR-2`), acceptance criteria (`AC-1` through `AC-5`), and plan critique dispositions (`PC-001` through `PC-004`) are implemented, reconciled, and verified by passing focused tests, static checks, link checks, and independent review with zero defects, zero decision gaps, and zero overclaims.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Optional test/terminology polish (`RV-001`, `RV-002`) and human/legal Issue #126 prerequisites (Product Owner PRD `0.21.0` sign-off, OD-36 DPIA/lawful-basis approval, qualified EU applicability review, live phase release gates) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`test_governance.py`, `test_live_doc_links.py`, `test_governance_evidence_api.py`, `ruff check .`, `ruff format --check .`, `python3 -m mypy`, `check-legacy-references.py` links, and `git diff` hygiene checks; 18 opt-in MSSQL loopback tests skipped with reason)
* Blockers: None
