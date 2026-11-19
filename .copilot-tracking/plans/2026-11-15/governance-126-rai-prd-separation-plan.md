<!-- markdownlint-disable-file -->
# RPI Plan: Issue 126 RAI Closure and PRD Separation Slice

## Task Metadata

* Task ID: issue-126-rai-prd-separation
* Task slug: governance-126-rai-prd-separation
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/governance-126-rai-prd-separation-plan-critique.md

## Executive Summary

This plan delivers the remaining bounded engineering and documentation slice for GitHub Issue #126 on branch `feat/governance-126-rai-prd-separation` (targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641). Earlier engineering added the 22-finding constructed Responsible AI (RAI) evidence register, but the 2026-10-31 closure audit (`PC-002`) identified that current PRD quality review and Product Owner acceptance were only separated in historical prose rather than enforced as runtime governance fields, `_rai_view` lacked explicit structured fields for disabled affected dispatch and conditional EU assurance applicability, and `test_governance.py` did not deterministically verify the synchronized addendum, PRD, ADR, knowledge-base index, and append-only log invariants.

To close those engineering and documentation gaps honestly, the implementation adds server-computed immutable `prd_quality_review` and `prd_owner_acceptance` separation records to both `_rai_view` and `governance_view`, defines `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` and adds `affected_dispatch` and `conditional_eu_assurance` alongside `live_use` in `_rai_view` with per-finding conditional applicability guards, updates the existing `#126` sections across the addendum, PRD, ADR 0002, core guide, knowledge index, and append-only log, and proves all three contracts with focused JSON, SQLite, and per-document repository invariant tests.

### User Decisions and Requirements Highlights

* **Separate PRD acceptance from RAI report acceptance and remediation claims**: `prd_quality_review` and `prd_owner_acceptance` must be exposed and enforced in both `_rai_view` and `governance_view` so neither historical report acceptance (`baseline-assessment-and-remediation-planning only`) nor 22/22 remediation claim completion (`dispositions_complete`) can satisfy or overwrite them.
* **Keep live use blocked, affected dispatch disabled, and EU assurance conditional**: `_rai_view` must expose exact `affected_dispatch` and `conditional_eu_assurance` values alongside `live_use`, and `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` must retain their unassessed/conditional guard until qualified applicability review.
* **Synchronize canonical docs and prove invariants in tests without overclaiming**: Update existing documentation, index, and append-only log while preserving historical versions and negative/insufficient outcomes, never reference `.copilot-tracking/` in `src/` or `docs/`, never claim live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off, and leave a frozen local commit without pushing or opening a PR.

### What You May Not Know

* **Worktree import isolation**: The shared host environment has an editable `zava-forward-core` install pointing to `/home/azureuser/source/ama/src/core/src`, so test runs must set `PYTHONPATH=src/core/src:src/core/tests` rather than running global `pip install -e` or importing the wrong worktree.
* **Excluded-file formatting and container test safety**: `src/core/pyproject.toml` excludes `governance.py` and `test_governance.py` from `ruff format`; quality checks must run in directory mode (`ruff check .`, `ruff format --check .`, `python3 -m mypy` inside `src/core`) to avoid reformatting untouched lines, and repository documentation tests in `test_governance.py` must use the `if not (ROOT / "docs").is_dir(): self.skipTest(...)` guard established by `test_live_doc_links.py` so stripped `src/`-only container images remain compatible.

### Unresolved Decisions or Blockers

* None for this engineering and documentation slice. Downstream human Product Owner sign-off, fresh full-PRD quality review on consolidated PRD `0.21.0`, OD-36 DPIA/lawful-basis approval, and qualified human/legal RAI acceptance remain separate non-goals tracked in [Follow-Up Items](#follow-up-items).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) and write all dated tracking artifacts under `.copilot-tracking/` (`2026-11-15`) for Issue #126 (`feat/governance-126-rai-prd-separation` targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641).
* Prove the remaining engineering and documentation acceptance criteria on Issue #126 without claiming live deployment, real OD-36 DPIA/lawful-basis approval, or human/budget-owner sign-off.
* In `src/core/src/zava_forward/core/governance.py` (`_rai_view` and `governance_view`), explicitly expose and enforce that `prd_quality_review` and `prd_owner_acceptance` remain separate from `baseline.acceptance_scope` (`baseline-assessment-and-remediation-planning only`) and from remediation claim completion (`dispositions_complete`), and cannot be satisfied or overwritten by RAI claim appends or report acceptance.
* In `src/core/src/zava_forward/core/governance.py` (`_rai_view`), explicitly include structured fields `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use`, and verify that EU conditional findings (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) preserve their unassessed/conditional guard until qualified applicability review.
* Update `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, related ADRs/guides (`docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`), `docs/reference/README.md`, and `docs/reference/log.md` with supported current evidence preserving historical versions and negative/insufficient outcomes.
* Add focused tests in `src/core/tests/test_governance.py` asserting all three contracts above, including documentation/index/log invariants resolving closure-audit finding `PC-002`.
* Do not reference `.copilot-tracking/` inside `src/` or `docs/`.
* Validate via the focused tier (`python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v`, `ruff check .`, `ruff format --check .`, and `mypy` inside `src/core`, plus documentation link/anchor checks).
* Commit all changes and `.copilot-tracking/` artifacts locally on `feat/governance-126-rai-prd-separation` with the required `Co-authored-by` trailer, and do not push or open a PR.

## Goals

* Enforce runtime read/write separation of current PRD quality review and Product Owner acceptance from RAI baseline report acceptance and constructed remediation claim completion across JSON and SQLite governance views.
* Expose explicit runtime boundaries keeping live use blocked, affected dispatch disabled, and conditional EU AI Act assurance (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) gated on qualified applicability review.
* Synchronize canonical problem specification, PRD, ADR 0002, core guide, knowledge index, and append-only log records while preserving historical versions and adverse/insufficient outcomes, backed by deterministic unit tests in `src/core/tests/test_governance.py`.

## Scope and Non-Goals

### In Scope

* Surgical updates to `src/core/src/zava_forward/core/governance.py` defining `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, `PRD_QUALITY_REVIEW`, and `PRD_OWNER_ACCEPTANCE`, and updating `_rai_view` and `governance_view` (reusing closed `RAI_CLAIM_FIELDS`).
* Focused unit and per-document repository documentation/index/log invariant tests in `src/core/tests/test_governance.py`.
* Concise, factual updates to `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and an append-only `[2026-11-15]` entry in `docs/reference/log.md`.
* Focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`, relative Markdown link/anchor verification, and `src/api` governance test compatibility) and one local frozen commit.

### Non-Goals

* Claiming live pilot deployment, enabling affected dispatch, recording real OD-36 DPIA/lawful-basis approval, signing off the PRD for the Product Owner, or closing any of the 22 open RAI baseline findings.
* Adding new HTTP endpoints, database tables, roles, web UI changes, or mutable PRD-approval API actions.
* Modifying `docs/case_study_48_original.md`, `docs/reference/memory.md`, or `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md`, or rewriting earlier entries in `docs/reference/log.md`.
* Pushing commits to GitHub or opening/updating a pull request.

## Functional Requirements

* FR-1: `_rai_view` and `governance_view` must both return detached copies of `prd_quality_review` and `prd_owner_acceptance` showing unaccepted/pending status (`accepted: False`, `satisfied: False` on quality review, `separate_from_report_acceptance: True`, `separate_from_remediation_completion: True`, `report_acceptance_scope: "baseline-assessment-and-remediation-planning only"`).
  * Observable acceptance criteria: Calling `governance_view` on empty, claim-populated (`dispositions_complete == True`, including `independent-acceptance` claims across all 22 findings), protocol/benefits/release-approved, or raw-dict-tampered JSON and SQLite stores always returns unchanged unaccepted `prd_quality_review` and `prd_owner_acceptance` structures, and `rai_evidence_record` rejects any payload attempting to supply `prd_quality_review` or `prd_owner_acceptance`.
* FR-2: `_rai_view` must expose `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use="BLOCKED pending separate qualified evidence and approvals"`, and every finding row must expose `conditional_eu` (`True` iff `finding_id in RAI_EU_CONDITIONAL`) and `applicability_review` (`"Required before conditional EU assurance applies"` for `EU-COND-01`, `EU-COND-02`, `EU-COND-04`, else `"Not conditional EU check"`).
  * Observable acceptance criteria: Across empty and claim-populated JSON and SQLite stores, `_rai_view` exposes exact `live_use`, `affected_dispatch`, and `conditional_eu_assurance` values, and `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` retain `baseline_status == "NOT_ASSESSED"`, `baseline_verdict == "UNCHANGED"`, `closure == "Open"`, `acceptance == "Unknown"`, `conditional_eu == True`, and `applicability_review == "Required before conditional EU assurance applies"`.
* FR-3: Existing `#126` sections in `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, and `docs/reference/README.md`, plus a newly appended `## [2026-11-15]` entry in `docs/reference/log.md`, must record the PRD review/acceptance separation, disabled affected dispatch, and conditional EU assurance guard while retaining each document's canonical historical versions and negative/insufficient outcomes.
  * Observable acceptance criteria: Deterministic tests in `src/core/tests/test_governance.py` verify whitespace-normalized per-document invariants across all six files (retaining `0.14.0`, `0.21.0`, `Unsigned candidate`, `1cb398c7b90bec05a5700008a97d0cfac494144a`, `FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, and `INVALID_PAYLOAD` in `docs/case_study_48_addendum.md`; `0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`, `Unsigned candidate`, `FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, and `DOWNGRADED` in `docs/prds/zava-forward-retrofit-programme-demonstrator.md`; `11 PARTIAL`, `11 NOT_ASSESSED`, and `2026-10-15` planning-only acceptance in `docs/adrs/0002-pilot-readiness-architecture.md`; `1cb398c7b90bec05a5700008a97d0cfac494144a`, `v0.14.0`, `DOWNGRADED`, `Open`, and `Unknown` in `src/core/README.md`; updated `#126` index status in `docs/reference/README.md`; and the appended `[2026-11-15]` entry in `docs/reference/log.md`), verify relative file links across all modified docs plus `#heading` anchors across full `addendum`/`PRD`/`ADR 0002`/`src/core/README.md`, the `[2026-11-15]` `log.md` entry, and the `#126`/RAI sections of `docs/reference/README.md`, and verify zero `.copilot-tracking` strings across full `governance.py`/`src/core/README.md`/`ADR 0002` and across the `#126` / `[2026-11-15]` sections of `addendum`, `PRD`, `docs/reference/README.md`, and `docs/reference/log.md`.

## Non-Functional Requirements

* NFR-1: Read-only snapshot purity and backward compatibility.
  * Objective threshold or evaluation condition: Zero persistent writes, default initializations, or audit appends during `governance_view`, and 100% pass rate across existing `test_governance.py` and `src/api/tests/test_governance_evidence_api.py` cases.
  * Operating condition or verification approach, if needed: Verified on both JSON `Store` and SQLite `SqlStore` plus stripped-container skip guard when `ROOT / "docs"` is absent.
  * Observable acceptance criteria: Existing governance and API HTTP tests pass without modification, and synthetic no-`docs/` check skips only the repository documentation test cleanly.
* NFR-2: Static quality, Markdown hygiene, and clean diff discipline.
  * Objective threshold or evaluation condition: Zero errors from directory-mode `ruff check .`, `ruff format --check .`, and `python3 -m mypy` inside `src/core`; zero unresolved relative links or scoped heading anchors in modified docs; zero newly introduced `.copilot-tracking/` strings in `src/` or `docs/` (and zero `.copilot-tracking/` strings anywhere in `governance.py`, `src/core/README.md`, `ADR 0002`, and the `#126` / `[2026-11-15]` sections of the addendum, PRD, KB index, and KB log); zero edits to prior lines of `docs/reference/log.md`.
  * Operating condition or verification approach, if needed: Run directory-mode quality checks inside `src/core` without invoking `ruff format` directly on format-excluded file paths, and verify `git diff` byte-preservation on `docs/reference/log.md` and zero added `.copilot-tracking` lines across `src/` and `docs/`.
  * Observable acceptance criteria: All focused validation commands exit `0` and `git status` is clean after the local commit.

## Acceptance Criteria

* `_rai_view` and `governance_view` in `src/core/src/zava_forward/core/governance.py` expose detached immutable `prd_quality_review` and `prd_owner_acceptance` records separate from `baseline.acceptance_scope` (`baseline-assessment-and-remediation-planning only`) and `dispositions_complete`, and reject or ignore attempts to satisfy or overwrite them via RAI claim appends, governance approvals, or stored governance dict tampering.
* `_rai_view` defines `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, exposes `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use`, and preserves the unassessed/conditional applicability guard on `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` across all claim tiers.
* `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` accurately record these boundaries while preserving each file's canonical historical versions, negative/insufficient outcomes, valid Markdown links/anchors, and zero `.copilot-tracking/` references in `#126` / `[2026-11-15]` content and added diff lines.
* `src/core/tests/test_governance.py` contains focused tests proving all three contracts above (including JSON, SQLite, and container-safe per-document doc/index/log invariants resolving `PC-002`), and all focused validation commands pass.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/governance-126-rai-prd-separation-plan-critique.md with Revise disposition resolved directly  |
| Relevant research                | .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md is created by implementation as its evidence record    |
| Planning execution and readiness | Complete and Ready for implementation (`PC-001` to `PC-004` resolved directly)                                                           |
| Continuation context             | Confirmed automatic RPI Agent parent return for automatic continuation to `rpi-implement`                                                |

## Sources

* .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md: Primary Cycle 1 research (`C1`-`C12`, `W1`) covering `PC-002` audit gaps, `governance.py` contracts, documentation targets, and tooling constraints.
* .copilot-tracking/research/2026-10-31/closure-audit-batch1-decisions.json: Closure-audit `PC-002` rejection rationale for Issue #126 criteria 11 and 12 and open criterion 13.
* src/core/src/zava_forward/core/governance.py: Existing `RAI_BASELINE`, `RAI_RESIDUALS`, `RAI_UNASSESSED` (containing `"EU-COND-01"`, `"EU-COND-02"`, `"EU-COND-04"`), `RAI_CLAIM_FIELDS`, `_rai_claim`, `_rai_view`, and `governance_view`.
* src/core/tests/test_governance.py and src/core/tests/test_live_doc_links.py: Existing JSON and SQLite governance test harnesses and container-compatible repository documentation link test pattern.
* docs/case_study_48_addendum.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0002-pilot-readiness-architecture.md, src/core/README.md, docs/reference/README.md, and docs/reference/log.md: Canonical documentation and knowledge-base targets for Issue #126.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce PRD Separation, Disabled Dispatch, and Conditional EU Guards in Core Governance

* Intent: Expose and enforce immutable `prd_quality_review` and `prd_owner_acceptance` separation across `_rai_view` and `governance_view`, and add explicit `affected_dispatch`, `conditional_eu_assurance`, and `EU-COND-01/02/04` applicability guards in `_rai_view`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Expose and enforce `prd_quality_review` and `prd_owner_acceptance` separation in `_rai_view` and `governance_view`

* Requirement and evidence: FR-1, NFR-1 (`C1`, `C2`, `C3`, `C5`, `C6`).
* Expected result: Both `_rai_view` and `governance_view` return detached copies of immutable `PRD_QUALITY_REVIEW` and `PRD_OWNER_ACCEPTANCE` dicts that remain unaccepted (`accepted: False`, `satisfied: False` on quality review) and explicitly separate from `baseline.acceptance_scope` and `dispositions_complete`, ignoring raw storage tampering and rejecting closed-schema claim overrides.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Expose `affected_dispatch` and `conditional_eu_assurance` and wire `RAI_EU_CONDITIONAL` finding guards in `_rai_view`

* Requirement and evidence: FR-2, NFR-1 (`C2`, `C3`, `C4`, `W1`).
* Expected result: `_rai_view` includes `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"` and `conditional_eu_assurance="Applies only after qualified applicability review"` alongside `live_use`, and finding rows expose `conditional_eu` and `applicability_review` preserving unassessed/conditional status on `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` across all claim appends.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Synchronize Canonical Documentation, ADR 0002, Core Guide, and Knowledge Base

* Intent: Record the enforced governance separation, disabled live dispatch, and conditional EU assurance boundaries across existing documentation and the knowledge base while preserving historical versions and negative/insufficient outcomes.
* Dependencies: P01 exact field names and status values.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update addendum, PRD, ADR 0002, and `src/core/README.md` without altering historical versions or adverse outcomes

* Requirement and evidence: FR-3, NFR-2 (`C4`, `C5`, `C6`, `C7`, `C8`).
* Expected result: `docs/case_study_48_addendum.md` (`ms.date: 2026-11-15`), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (retaining `version: "0.21.0"` and `Unsigned candidate`), `docs/adrs/0002-pilot-readiness-architecture.md`, and `src/core/README.md` document the `2026-11-15` `#126` governance fields and boundaries while preserving `0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`, `1cb398c7b90bec05a5700008a97d0cfac494144a`, and all negative/insufficient outcomes (`FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, `INVALID_PAYLOAD`), with zero `.copilot-tracking/` references.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `docs/reference/README.md` and append `[2026-11-15]` entry to `docs/reference/log.md`

* Requirement and evidence: FR-3, NFR-2 (`C9`, `C11`).
* Expected result: `docs/reference/README.md` updates `ms.date: 2026-11-15` and the `#126` status summary with valid relative links, and `docs/reference/log.md` appends one new `## [2026-11-15] update | ... (Refs #126)` section at EOF with zero changes to existing bytes.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add Focused Runtime and Documentation Invariant Tests (`PC-002`) and Validate

* Intent: Prove all three contracts in `src/core/tests/test_governance.py` across JSON, SQLite, and repository documentation/index/log surfaces, and pass all focused validation gates cleanly.
* Dependencies: P01 and P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add focused Contract 1, Contract 2, and Contract 3 (`PC-002`) tests in `src/core/tests/test_governance.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C1`, `C2`, `C10`, `C11`, `C12`).
* Expected result: Up to 8 focused test methods added in `src/core/tests/test_governance.py` (with zero test removals and zero generated targets) covering JSON and SQLite runtime separation, closed-schema claim rejection, 22/22 `dispositions_complete` and governance-action isolation, raw dict tampering immunity, `affected_dispatch` / `conditional_eu_assurance` / `EU-COND-01..04` guards, and container-safe repository doc/ADR/index/log content, historical-outcome retention, relative link/anchor resolution, and `.copilot-tracking/` absence.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run focused validation suite and verify clean git diff invariants

* Requirement and evidence: NFR-1, NFR-2 (`C3`, `C10`, `C11`, `C12`).
* Expected result: `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v`, directory-mode `ruff check .`, `ruff format --check .`, and `python3 -m mypy` inside `src/core`, `test_live_doc_links.py`, and `src/api/tests/test_governance_evidence_api.py` all pass with zero errors and zero `.copilot-tracking/` leaks in `src/` or `docs/`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md

## Dependencies

* Worktree `PYTHONPATH=src/core/src:src/core/tests`: Required so Python resolves `zava_forward.core` from `/home/azureuser/source/ama-demo-wt/feat-126-governance` without mutating shared editable installs.
* Directory-mode quality runners in `src/core`: `ruff check .`, `ruff format --check .`, and `python3 -m mypy` respect `src/core/pyproject.toml` excludes so untouched legacy lines in `governance.py` and `test_governance.py` are not reformatted.
* Container-image `docs/` guard: Repository documentation assertions inside `src/core/tests/test_governance.py` check `if not (ROOT / "docs").is_dir(): self.skipTest("repository docs are not in this image")` so `src/`-only Docker builds remain green while repository checkouts always execute every assertion.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`2026-11-15`): `PC-001` [High] Whole-file `.copilot-tracking/` absence check conflicts with 363 retained historical references | resolved | Scoped whole-file zero-`.copilot-tracking` checks to `governance.py`, `src/core/README.md`, and `docs/adrs/0002-pilot-readiness-architecture.md`, plus `#126` / `[2026-11-15]` section checks on `addendum`, `PRD`, `docs/reference/README.md`, and `docs/reference/log.md` and a `git diff` added-line check in P03-T02. |
| Run 1 (`2026-11-15`): `PC-002` [High] Whole-file heading-anchor check on `docs/reference/README.md` hits unrelated stale `#175` anchor | resolved | Kept full-file relative path checks on all modified docs and full-file `#heading` anchor checks on `addendum`, `PRD`, `ADR 0002`, `src/core/README.md`, and the `[2026-11-15]` `log.md` entry, while scoping `#heading` anchor checks on `docs/reference/README.md` to its `#126` / RAI paragraphs and Project Documents rows. |
| Run 1 (`2026-11-15`): `PC-003` [Medium] `RAI_EU_CONDITIONAL` assumed pre-existing in `governance.py` | resolved | Explicitly added `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` as a new constant to define in `governance.py` in `In Scope`, `P01`, and `P01-T02`. |
| Run 1 (`2026-11-15`): `PC-004` [Medium] Pooled historical/adverse tokens lacked per-file ownership and whitespace normalization | resolved | Mapped exact preserved historical versions and negative/insufficient tokens per canonical document in `FR-3`, `P02-T01`, and `P03-T01` with whitespace normalization (`" ".join(text.split())`) and explicit `0.21.0` unsigned-candidate reference in the addendum `#126` update. |

## Follow-Up Items

* Fresh independent `prd-quality-reviewer` assessment and human Product Owner sign-off on consolidated PRD `v0.21.0` (`OD-35` to `OD-55`): Outside engineering slice scope because human review and open organisational decisions cannot be completed or claimed by code; owned by Product Owner.
* Qualified human, DPO/legal, and safety Responsible AI acceptance, EU AI Act applicability determination, and OD-36 DPIA / lawful-basis sign-off before live pilot release or enabling affected dispatch: Outside engineering slice scope per explicit caller non-goals; owned by Programme Manager, DPO/Legal, and Safety Leads.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md
* Ready phase or task: Complete (`P01`-`P03` complete; ready for `rpi-review`)
* Remaining provisional question or blocker: none
