<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 126 RAI Closure and PRD Separation Slice

## Metadata

* Task ID: issue-126-rai-prd-separation
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the bounded Issue #126 RAI closure and PRD separation engineering and documentation slice on `feat/governance-126-rai-prd-separation` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641) under the focused validation tier without claiming live deployment, real OD-36 DPIA or lawful-basis approval, or human/budget-owner sign-off, without adding `.copilot-tracking/` references in `src/` or `docs/`, and committing locally without pushing or opening a PR.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md, .copilot-tracking/research/2026-10-31/closure-audit-batch1-decisions.json, src/core/src/zava_forward/core/governance.py, src/core/tests/test_governance.py, src/core/pyproject.toml, src/core/tests/test_live_doc_links.py, src/api/tests/test_governance_evidence_api.py, docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0002-pilot-readiness-architecture.md, src/core/README.md, docs/reference/README.md, docs/reference/memory.md, docs/reference/log.md, and docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md.
* Decisions, dependencies, and acceptance criteria considered: Contract 1 (`prd_quality_review` and `prd_owner_acceptance` separation in `_rai_view` and `governance_view`), Contract 2 (`affected_dispatch`, `conditional_eu_assurance`, and `EU-COND-01`/`EU-COND-02`/`EU-COND-04` conditional applicability guards in `_rai_view`), Contract 3 (canonical updates across addendum, PRD, ADR 0002, `src/core/README.md`, `docs/reference/README.md`, and append-only `docs/reference/log.md` plus deterministic unit tests resolving closure-audit `PC-002`), worktree `PYTHONPATH=src/core/src:src/core/tests`, directory-mode `ruff`/`mypy` execution in `src/core`, and stripped-container `docs/` skip guard.
* Assessment boundary: Evaluates plan and phase-detail credibility against verified worktree code, tests, tooling rules, and target Markdown files. Cannot evaluate human Product Owner sign-off, live Azure deployment, OD-36 DPIA approval, or legal EU AI Act applicability advice, all of which are explicit non-goals.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / P01-T01 (`prd_quality_review` and `prd_owner_acceptance` separation) | Covered | Detached `deepcopy` constants in `_rai_view` and `governance_view`, closed `RAI_CLAIM_FIELDS` write rejection, 22/22 `dispositions_complete` isolation, and raw storage tampering immunity across JSON and SQLite stores match src/core/src/zava_forward/core/governance.py and src/core/src/zava_forward/core/sqlstore.py (`DOCS` checked document persistence). |
| FR-2 / P01 / P01-T02 (`affected_dispatch`, `conditional_eu_assurance`, `EU-COND-*` guards) | Partial | Exact prompt field values and per-finding guard semantics are sound, but the plan and phase details falsely state `RAI_EU_CONDITIONAL` is already defined in src/core/src/zava_forward/core/governance.py (`PC-003`). |
| FR-3 / P02 / P02-T01 / P02-T02 (canonical docs, KB index, append-only log) | Partial | All six target files and existing `#126` sections are accurately located, but historical version and adverse-outcome tokens differ per document and `docs/case_study_48_addendum.md` does not yet mention PRD `0.21.0` (`PC-004`). |
| NFR-1 (snapshot purity, API compatibility, container skip guard) | Covered | Verified against src/api/tests/test_governance_evidence_api.py and src/core/tests/test_live_doc_links.py; detached read projections and `if not (ROOT / "docs").is_dir(): self.skipTest(...)` preserve backward and container compatibility. |
| NFR-2 / P03 / P03-T01 / P03-T02 (doc invariants, links/anchors, `.copilot-tracking/` rule, quality gates) | Partial | Whole-file zero-`.copilot-tracking/` assertions fail against 363 retained historical occurrences in four target docs (`PC-001`), whole-file anchor checks on `docs/reference/README.md` fail on an unrelated stale `#175` anchor at line 907 (`PC-002`), and per-file token ownership needs explicit mapping (`PC-004`). Directory-mode `ruff`/`mypy` and worktree `PYTHONPATH` safeguards are sound. |

## Verdict

* Verdict: Revise
* Rationale: The core architectural approach (detached server-computed `prd_quality_review` and `prd_owner_acceptance` projections, exact `affected_dispatch` and `conditional_eu_assurance` strings, `EU-COND-01`/`02`/`04` finding guards, in-place `#126` documentation updates, container skip guard, and worktree `PYTHONPATH` / directory-mode `ruff` safeguards) is well-designed, but four verified discrepancies between the plan/details and actual worktree files (`PC-001` through `PC-004`) would cause immediate `NameError` or deterministic `unittest` failures during implementation unless corrected by the planning parent before finalization.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Whole-file `.copilot-tracking/` absence assertions conflict with 363 existing historical references in four target docs

* Related IDs: FR-3, NFR-2, P02, P03, P03-T01, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md, .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md, docs/reference/log.md, docs/reference/README.md, docs/case_study_48_addendum.md, and docs/prds/zava-forward-retrofit-programme-demonstrator.md
* Concern: FR-3, Acceptance Criteria, and P03-T01 (`test_governance_docs_index_and_log_preserve_separation_and_adverse_history`) specify asserting that all six documentation files contain zero `.copilot-tracking/` references. In the current worktree, four of those six files already contain committed historical `.copilot-tracking` strings: `docs/reference/log.md` has 349 matches (append-only history whose prior bytes NFR-2 forbids altering), `docs/reference/README.md` has 8 matches (lines 634, 949, 950, 988, 1023, 1024, 1027, 1041, including the `ama-mentor-deck` working path mandated by `.github/copilot-instructions.md`), `docs/case_study_48_addendum.md` has 3 matches (lines 92, 376, 1507), and `docs/prds/zava-forward-retrofit-programme-demonstrator.md` has 3 matches (lines 121, 1284, 2002). Only `src/core/src/zava_forward/core/governance.py`, `src/core/README.md`, and `docs/adrs/0002-pilot-readiness-architecture.md` have zero matches across the whole file.
* Impact: Implementing P03-T01 as specified either causes `test_governance.py` to fail immediately on pre-existing historical lines or pressures implementation to strip historical `.copilot-tracking` references from unrelated sections and rewrite prior bytes of `docs/reference/log.md`.
* Smallest useful change: Revise FR-3, NFR-2, Acceptance Criteria, P02, P03, P03-T01, and P03-T02 so `test_governance.py` asserts zero `.copilot-tracking` substrings across the full text of `src/core/src/zava_forward/core/governance.py`, `src/core/README.md`, and `docs/adrs/0002-pilot-readiness-architecture.md`, plus zero `.copilot-tracking` substrings within the `#126` / RAI sections of `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/reference/README.md` and within the appended `## [2026-11-15]` entry of `docs/reference/log.md`, paired with a `git diff` check in P03-T02 confirming zero added lines in `src/` or `docs/` contain `.copilot-tracking`.
* Action owner: planning_parent
* Exact resolving evidence: Updated FR-3, NFR-2, Acceptance Criteria, and P03-T01/P03-T02 in .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md and .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md scoping the `.copilot-tracking/` absence assertions to clean whole files, `#126` / `[2026-11-15]` sections on files with historical entries, and added diff lines.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Whole-file heading-anchor check on `docs/reference/README.md` fails on a pre-existing unrelated stale anchor

* Related IDs: FR-3, NFR-2, P02-T02, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md, docs/reference/README.md, docs/reference/research/retrofit-synthetic-data/data-dictionary.md, and src/core/tests/test_live_doc_links.py
* Concern: P03-T01 (`test_modified_governance_docs_resolve_relative_links_and_heading_anchors`) specifies validating every non-fenced relative link and `#heading-anchor` slug across the entire `docs/reference/README.md` file. While `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, and `src/core/README.md` currently have zero broken relative links or heading anchors, `docs/reference/README.md` line 907 contains an unrelated Issue #175 link (`./research/retrofit-synthetic-data/data-dictionary.md#issue-175-acceptance-audit-2026-10-16`) whose target heading in `data-dictionary.md` is now `#issue-175-acceptance-audit-2026-11-02` (`test_live_doc_links.py` checks file existence only, ignoring `#` fragments).
* Impact: Running a whole-file heading-anchor check over `docs/reference/README.md` fails immediately on line 907, either blocking focused validation or causing an out-of-scope edit to unrelated Issue #175 documentation.
* Smallest useful change: Update FR-3 and P03-T01 item 4 so `test_modified_governance_docs_resolve_relative_links_and_heading_anchors` validates all relative file targets across all modified files, full-file `#heading-anchor` slugs on `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, and the `[2026-11-15]` section of `docs/reference/log.md`, and scopes `#heading-anchor` slug validation in `docs/reference/README.md` to its Issue #126 / RAI paragraphs and Project Documents rows.
* Action owner: planning_parent
* Exact resolving evidence: Updated FR-3 in .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md and P03-T01 item 4 in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md scoping anchor checks on `docs/reference/README.md` to `#126` / RAI sections and rows without touching line 907.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Plan and phase details falsely assume `RAI_EU_CONDITIONAL` is already defined in `governance.py`

* Related IDs: FR-2, C2, P01, P01-T02
* Evidence: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md, .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md, and src/core/src/zava_forward/core/governance.py
* Concern: Plan `In Scope` ("reusing closed `RAI_CLAIM_FIELDS` and existing `RAI_EU_CONDITIONAL`") and Phase Details `P01` (`Context` and `Likely Targets`) and `P01-T02` (`Context`) state that `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` is already declared in `src/core/src/zava_forward/core/governance.py`, and omit `RAI_EU_CONDITIONAL` from the constants to add in `P01 -> Likely Targets`. In actual `src/core/src/zava_forward/core/governance.py` (lines 69 to 81), `"EU-COND-01"`, `"EU-COND-02"`, and `"EU-COND-04"` appear only as string literals inside `RAI_UNASSESSED`; `RAI_EU_CONDITIONAL` does not exist anywhere in `src/`.
* Impact: Referencing `fid in RAI_EU_CONDITIONAL` in `_rai_view` without explicitly defining `RAI_EU_CONDITIONAL` raises `NameError: name 'RAI_EU_CONDITIONAL' is not defined` at runtime.
* Smallest useful change: Update Plan `In Scope` and Phase Details `P01` (`Context`, `Likely Targets`) and `P01-T02` (`Context`, `Boundaries`) to state that `"EU-COND-01"`, `"EU-COND-02"`, and `"EU-COND-04"` currently reside in `RAI_UNASSESSED` and explicitly include `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` among the new module constants to define in `src/core/src/zava_forward/core/governance.py`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `In Scope` in .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md and `P01` / `P01-T02` in .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md listing `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` as a constant to add in `src/core/src/zava_forward/core/governance.py`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Pooled historical-version and adverse-outcome token list is not mapped to the canonical files that actually hold each token

* Related IDs: FR-3, P02-T01, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md, .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md, docs/case_study_48_addendum.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0002-pilot-readiness-architecture.md, src/core/README.md, and docs/reference/README.md
* Concern: FR-3, P02-T01, and P03-T01 item 3 group all six target Markdown files together against a single pooled list of preserved versions (`0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`, `Unsigned candidate`, `1cb398c7b90bec05a5700008a97d0cfac494144a`) and adverse/insufficient tokens (`FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, `INVALID_PAYLOAD`). Worktree inspection shows each file owns a distinct subset: `docs/case_study_48_addendum.md` currently lacks `0.21.0` and `Unsigned candidate`; `docs/prds/zava-forward-retrofit-programme-demonstrator.md` lacks `INVALID_PAYLOAD` (which belongs to the RAI report recovery record in the addendum and baseline report) and wraps `Finalize` / `NOT_EVALUATED` across lines 40 to 41 in its top callout; `docs/adrs/0002-pilot-readiness-architecture.md` records `11 PARTIAL` and `2026-10-15` planning-only baseline report acceptance rather than PRD review versions; and `src/core/README.md` records `1cb398c7b90bec05a5700008a97d0cfac494144a`, `v0.14.0`, `DOWNGRADED`, `Open`, and `Unknown`.
* Impact: Without per-document mapping (and whitespace normalization for wrapped prose), `test_governance_docs_index_and_log_preserve_separation_and_adverse_history` either asserts tokens on files that never contained them (causing false test failures or unnatural boilerplate in `ADR 0002` and `src/core/README.md`) or falls back to weak pooled concatenation checks that fail to guard individual documents.
* Smallest useful change: Specify explicit per-document assertion expectations in P02-T01 and P03-T01 item 3 (including referencing unsigned candidate PRD `0.21.0` in the `2026-11-15` addendum `#126` update, mapping `INVALID_PAYLOAD` to `docs/case_study_48_addendum.md` and `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md`, mapping PRD version/review history to `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, mapping `11 PARTIAL` and `2026-10-15` planning-only acceptance to `docs/adrs/0002-pilot-readiness-architecture.md`, mapping `1cb398c7b90bec05a5700008a97d0cfac494144a` / `v0.14.0` / `DOWNGRADED` / `Open` / `Unknown` to `src/core/README.md`, and normalizing whitespace before phrase matching).
* Action owner: planning_parent
* Exact resolving evidence: Updated FR-3, P02-T01, and P03-T01 item 3 in .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md and .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md defining exact per-document preserved tokens and whitespace-normalized matching.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Runtime separation design in `P01-T01` is strong: computing detached `deepcopy` structures for `prd_quality_review` and `prd_owner_acceptance` in both `_rai_view` and `governance_view` while keeping `RAI_CLAIM_FIELDS` closed prevents claim appends (`dispositions_complete == True`), governance approvals, caller mutation, and persisted raw-dict tampering (`Store` and `SqlStore` `DOCS`) from falsifying PRD quality review or owner acceptance.
* Backward compatibility and environment hazards are thoroughly addressed: `src/api/tests/test_governance_evidence_api.py` compatibility, worktree `PYTHONPATH=src/core/src:src/core/tests` isolation, directory-mode `ruff check .` / `ruff format --check .` / `python3 -m mypy` execution respecting `src/core/pyproject.toml` excludes, and the stripped-container `ROOT / "docs"` skip guard from `src/core/tests/test_live_doc_links.py` are all accurately captured.
* Residual risk (explicitly accepted by caller scope): Human Product Owner PRD sign-off on `0.21.0`, fresh `prd-quality-reviewer` execution, OD-36 DPIA/lawful-basis approval, and qualified legal/DPO/safety RAI acceptance remain open human gates outside this engineering slice and must continue to be reported as pending/blocked rather than satisfied.

## Questions or Blocking Evidence Gaps

* None. All four findings are fully resolved from verified worktree files and require no user clarification.

## Limitations

* This critique inspected repository files and tooling configuration statically in read-only mode without modifying code or executing destructive commands; hosted GitHub Actions CI remains unobserved because the caller scope specifies a local-only commit without pushing or opening a PR.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, `PC-003`, and `PC-004` in .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md and .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md, record their disposition in `Critique Disposition`, mark the plan finalized, and proceed to `rpi-implement` without another critique pass.
* User response required: no
