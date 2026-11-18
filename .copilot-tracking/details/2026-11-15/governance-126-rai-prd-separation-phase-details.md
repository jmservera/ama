<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 126 RAI Closure and PRD Separation Slice

## Metadata

* Task ID: issue-126-rai-prd-separation
* Task slug: governance-126-rai-prd-separation
* Related plan: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/governance-126-rai-prd-separation-research.md, .copilot-tracking/research/2026-10-31/closure-audit-batch1-decisions.json, src/core/src/zava_forward/core/governance.py, src/core/tests/test_governance.py, src/core/tests/test_live_doc_links.py

## Phase Index

| Phase ID | Name                                                                               | Status | Detail sections        |
|----------|------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Enforce PRD Separation, Disabled Dispatch, and Conditional EU Guards in Core Governance | ready  | P01, P01-T01, P01-T02  |
| P02      | Synchronize Canonical Documentation, ADR 0002, Core Guide, and Knowledge Base      | ready  | P02, P02-T01, P02-T02  |
| P03      | Add Focused Runtime and Documentation Invariant Tests (`PC-002`) and Validate      | ready  | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Enforce PRD Separation, Disabled Dispatch, and Conditional EU Guards in Core Governance

### Context

`src/core/src/zava_forward/core/governance.py` implements `GovernanceMixin`, `_rai_claim`, and `_rai_view` over the fixed 22-finding Responsible AI baseline (`RAI_RESIDUALS` + `RAI_UNASSESSED` at `RAI_BASELINE = "1cb398c7b90bec05a5700008a97d0cfac494144a"`). Currently:
* `_rai_view` exposes `baseline["acceptance_scope"] = "baseline-assessment-and-remediation-planning only"`, `dispositions_complete`, and `live_use = "BLOCKED pending separate qualified evidence and approvals"`, and includes `"EU-COND-01"`, `"EU-COND-02"`, and `"EU-COND-04"` inside `RAI_UNASSESSED`, but does not define a separate `RAI_EU_CONDITIONAL` constant or expose `prd_quality_review`, `prd_owner_acceptance`, `affected_dispatch`, or `conditional_eu_assurance`, nor does it surface conditional EU applicability guards on finding rows.
* `governance_view` returns `protocol`, `benefits`, `captures`, `value_claims`, `releases`, `breaches`, and `rai_evidence`, without top-level `prd_quality_review` and `prd_owner_acceptance` separation fields.

### Intent

Make the separation of current PRD quality review and Product Owner acceptance from RAI baseline report acceptance and constructed remediation claim completion, as well as disabled affected dispatch and conditional EU applicability boundaries, explicit and immutable in runtime governance views.

### Boundaries

* Included: Module-level immutable constants (`RAI_EU_CONDITIONAL`, `PRD_QUALITY_REVIEW`, `PRD_OWNER_ACCEPTANCE`, `RAI_AFFECTED_DISPATCH`, `RAI_CONDITIONAL_EU_ASSURANCE`) and read-projection updates in `_rai_view` and `governance_view` inside `src/core/src/zava_forward/core/governance.py`.
* Excluded: New API routes, new SQLite/MSSQL tables, mutable PRD sign-off endpoints, changes to `protocol_*`, `benefits_*`, `value_claim_*`, `release_record`, or `breach_*` semantics, and reformatting untouched lines of `governance.py`.

### Likely Targets

* src/core/src/zava_forward/core/governance.py: Add `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, `PRD_QUALITY_REVIEW`, `PRD_OWNER_ACCEPTANCE`, `RAI_AFFECTED_DISPATCH`, and `RAI_CONDITIONAL_EU_ASSURANCE` constants; expose `deepcopy` copies in `_rai_view` and `governance_view`; wire `RAI_EU_CONDITIONAL` into finding projections.

### Dependencies

* None.

### Validation Expectations

* Detached read checks verify neither `_rai_view` nor `governance_view` mutates caller-supplied or stored `governance` dicts, and caller mutation of returned `prd_quality_review` or `prd_owner_acceptance` dicts cannot bleed across calls.
* Existing `test_governance.py` and `src/api/tests/test_governance_evidence_api.py` continue to pass unchanged.

### Completion Evidence

* Updated `src/core/src/zava_forward/core/governance.py` passing unit, lint, format-check, and mypy checks.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Expose and enforce `prd_quality_review` and `prd_owner_acceptance` separation in `_rai_view` and `governance_view`

#### Context

Closure-audit rejection `PC-002` on Issue #126 criterion 11 noted that historical documentary review did not provide a merged runtime assertion preserving current PRD quality review and owner acceptance independently from baseline report acceptance (`baseline-assessment-and-remediation-planning only`) and remediation claim completion (`dispositions_complete`). `_rai_claim` already enforces strict closed-key validation (`body.keys() != RAI_CLAIM_FIELDS`), rejecting extra payload keys on `rai_evidence_record`.

#### Intent

Expose detached, server-computed `prd_quality_review` and `prd_owner_acceptance` separation dictionaries on both `_rai_view` and `governance_view` that remain unaccepted/unsatisfied regardless of claim appends, `dispositions_complete`, governance approvals, or injected keys in raw persisted `governance` dictionaries.

#### Boundaries

* Included:
  * Define `PRD_QUALITY_REVIEW` with keys `status` (`"Pending fresh independent PRD quality review (prior pre-merge resident draft FAIL / Validate BLOCKED / Finalize NOT_EVALUATED)"`), `satisfied` (`False`), `accepted` (`False`), `separate_from_report_acceptance` (`True`), `separate_from_remediation_completion` (`True`), and `report_acceptance_scope` (`"baseline-assessment-and-remediation-planning only"`).
  * Define `PRD_OWNER_ACCEPTANCE` with keys `status` (`"Unsigned candidate pending separate human owner acceptance"`), `accepted` (`False`), `separate_from_report_acceptance` (`True`), `separate_from_remediation_completion` (`True`), and `report_acceptance_scope` (`"baseline-assessment-and-remediation-planning only"`).
  * Include `prd_quality_review=deepcopy(PRD_QUALITY_REVIEW)` and `prd_owner_acceptance=deepcopy(PRD_OWNER_ACCEPTANCE)` in both `_rai_view` and `governance_view`, ignoring any `raw.get("prd_quality_review")` or `raw.get("prd_owner_acceptance")` present in storage.
* Excluded: Any endpoint or helper that flips `accepted` or `satisfied` to `True` without human repository PRD sign-off.

#### Likely Targets

* src/core/src/zava_forward/core/governance.py: Constants near `RAI_BASELINE`, `_rai_view` return dict, and `governance_view` return dict.

#### Dependencies

* None.

#### Validation Expectations

* Semantic unit assertions verify `prd_quality_review` and `prd_owner_acceptance` on both `governance_view(...)` and `governance_view(...)["rai_evidence"]` across empty stores, 22/22 `independent-acceptance` claim completion (`dispositions_complete is True`), approved protocol/benefits/release state, rejected `rai_evidence_record` payloads carrying `prd_quality_review` or `prd_owner_acceptance`, and tampered raw `governance` storage dicts on both JSON and SQLite stores.

#### Completion Evidence

* Exact fields returned by `_rai_view` and `governance_view` and verified by `test_governance.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Expose `affected_dispatch` and `conditional_eu_assurance` and wire `RAI_EU_CONDITIONAL` finding guards in `_rai_view`

#### Context

`"EU-COND-01"`, `"EU-COND-02"`, and `"EU-COND-04"` currently reside in `RAI_UNASSESSED` in `governance.py` as the conditional EU AI Act subset matching the 2026-10-14 RAI baseline report. Issue #126 criterion 13 requires explicit runtime fields showing live use stays blocked, affected dispatch stays disabled until appropriate evidence and qualified approvals exist, and conditional EU assurance applies only after qualified applicability review.

#### Intent

Define `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, expose the exact structured fields `affected_dispatch` and `conditional_eu_assurance` alongside `live_use` in `_rai_view`, and mark `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` finding rows with explicit conditional EU applicability guards that remain unassessed/open across constructed claim appends.

#### Boundaries

* Included:
  * Define module constant `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")` next to `RAI_UNASSESSED`.
  * In `_rai_view` top-level return dictionary, include:
    * `affected_dispatch="DISABLED until appropriate evidence and qualified approvals exist"`
    * `conditional_eu_assurance="Applies only after qualified applicability review"`
    * alongside `live_use="BLOCKED pending separate qualified evidence and approvals"`.
  * In `_rai_view` per-finding dictionary, compute `eu_conditional = fid in RAI_EU_CONDITIONAL` and include:
    * `conditional_eu=eu_conditional`
    * `applicability_review="Required before conditional EU assurance applies" if eu_conditional else "Not conditional EU check"`
    while preserving `baseline_status="NOT_ASSESSED"`, `baseline_verdict="UNCHANGED"`, `closure="Open"`, `acceptance="Unknown"`, and `evidence_adequacy="Not independently established"`.
* Excluded: Making any legal conclusion on EU AI Act classification or altering `RAI_CLAIM_FIELDS`.

#### Likely Targets

* src/core/src/zava_forward/core/governance.py: `_rai_view` finding projection loop and return dictionary.

#### Dependencies

* P01-T01 shared `_rai_view` dictionary structure.

#### Validation Expectations

* Semantic unit assertions verify `_rai_view` top-level `live_use`, `affected_dispatch`, and `conditional_eu_assurance` strings, verify that `conditional_eu` is `True` exclusively on `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` (3 of 22 findings), and verify that appending `implemented/source-tested`, `deployed-observed`, or `independent-acceptance` claims to `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` leaves `baseline_status`, `baseline_verdict`, `closure`, `acceptance`, `conditional_eu`, `applicability_review`, `live_use`, `affected_dispatch`, and `conditional_eu_assurance` unchanged on both JSON and SQLite stores.

#### Completion Evidence

* Updated `_rai_view` projection verified across JSON and SQLite test subclasses.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Synchronize Canonical Documentation, ADR 0002, Core Guide, and Knowledge Base

### Context

Issue #126 criterion 12 requires updating the existing addendum, PRD, ADRs, and knowledge index/append-only log with supported current evidence while preserving historical versions and negative/insufficient outcomes. All six target Markdown files already contain dedicated `#126` sections from `2026-10-18` (and earlier `2026-10-14` / `2026-10-15` baseline entries).

### Intent

Record the `2026-11-15` runtime separation of `prd_quality_review` and `prd_owner_acceptance`, `affected_dispatch` disabled boundary, and `conditional_eu_assurance` (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) applicability guard across all six canonical documentation and knowledge-base files without altering historical versions, negative/insufficient outcomes, or prior append-only log entries.

### Boundaries

* Included:
  * Canonical targets: `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
  * Generated targets: `none`.
* Excluded: `docs/case_study_48_original.md`, `docs/reference/memory.md`, `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md`, any `.copilot-tracking/` string in `src/` or `docs/`, em dashes, bolded-prefix list items, or edits to existing bytes in `docs/reference/log.md`.

### Likely Targets

* docs/case_study_48_addendum.md: Update frontmatter `ms.date: 2026-11-15` and extend `Constructed RAI Evidence Register Engineering` with a dated `2026-11-15` bullet/paragraph preserving `2026-10-14`, `2026-10-15`, and `2026-10-18` records and adverse outcomes.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: Extend `Constructed Finding-Evidence Engineering` with a dated `2026-11-15` paragraph preserving `version: "0.21.0"`, `Unsigned candidate`, historical versions (`0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`), and prior `FAIL` / `Validate BLOCKED` / `Finalize NOT_EVALUATED` / `PARTIAL` / `NOT_ASSESSED` / `DOWNGRADED` outcomes.
* docs/adrs/0002-pilot-readiness-architecture.md: Extend `Finding-Evidence Register Engineering` under `Responsible AI Audit Outcome and Live Release Gate` with a concise `2026-11-15` paragraph.
* src/core/README.md: Update `Constructed RAI evidence claims` to document `prd_quality_review`, `prd_owner_acceptance`, `affected_dispatch`, `conditional_eu_assurance`, and `EU-COND-01`/`EU-COND-02`/`EU-COND-04` finding fields.
* docs/reference/README.md: Update frontmatter `ms.date: 2026-11-15` and the `#126` status paragraph to reflect the enforced PRD separation, disabled affected dispatch, and conditional EU applicability guard.
* docs/reference/log.md: Append one `## [2026-11-15] update | Issue #126 RAI PRD acceptance separation and conditional EU dispatch guards (Refs #126)` entry at EOF.

### Dependencies

* P01 exact field names and string constants.

### Validation Expectations

* Plain ASCII punctuation in new prose, `*` for unordered lists, no em dashes, no bolded-prefix list items, zero `.copilot-tracking/` references, byte-identical prefix on `docs/reference/log.md`, and 100% resolved relative Markdown links and `#heading` anchors.

### Completion Evidence

* Clean `git diff` across the six Markdown files and passing `test_live_doc_links.py` plus new `test_governance.py` documentation invariant tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update addendum, PRD, ADR 0002, and `src/core/README.md` without altering historical versions or adverse outcomes

#### Context

Each of the four technical specification and architecture documents has an existing `#126` subsection from `2026-10-18` describing `_rai_view` and `governance_view`. Extending those subsections in place follows repository conventions ("Integrate research findings into the relevant section instead of appending an unrelated running log" and "Update existing addendum/PRD/ADRs ... preserving historical versions and negative/insufficient outcomes").

#### Intent

Document the `2026-11-15` runtime enforcement of `prd_quality_review` and `prd_owner_acceptance` separation, `affected_dispatch` disabled status, and `conditional_eu_assurance` (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) applicability guard across the addendum, PRD, ADR 0002, and `src/core/README.md` while keeping historical versions and negative/insufficient outcomes intact.

#### Boundaries

* Included: `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, and `src/core/README.md`.
* Excluded: Changing PRD `version: "0.21.0"` or sign-off table entries, claiming live deployment or OD-36 DPIA/owner sign-off, or referencing `.copilot-tracking/`.

#### Likely Targets

* docs/case_study_48_addendum.md: Frontmatter `ms.date` and `Constructed RAI Evidence Register Engineering (2026-10-18)` section.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: `Constructed Finding-Evidence Engineering (2026-10-18, #126)` section.
* docs/adrs/0002-pilot-readiness-architecture.md: `Finding-Evidence Register Engineering (2026-10-18, #126)` section.
* src/core/README.md: `Constructed RAI evidence claims (2026-10-18, #126)` section (preserving existing heading slug linked from `src/api/README.md`).

#### Dependencies

* P01.

#### Validation Expectations

* Preserve heading anchor `#constructed-rai-evidence-claims-2026-10-18-126` in `src/core/README.md` so `src/api/README.md` cross-links continue to resolve cleanly.
* Retain each file's canonical historical versions and negative/insufficient outcomes (explicitly referencing unsigned candidate PRD `0.21.0` in the `2026-11-15` addendum `#126` update alongside existing `0.14.0`, `1cb398c7b90bec05a5700008a97d0cfac494144a`, `FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, and `INVALID_PAYLOAD`; retaining `0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`, `Unsigned candidate`, `FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, and `DOWNGRADED` in `docs/prds/zava-forward-retrofit-programme-demonstrator.md`; retaining `11 PARTIAL`, `11 NOT_ASSESSED`, and `2026-10-15` planning-only acceptance in `docs/adrs/0002-pilot-readiness-architecture.md`; and retaining `1cb398c7b90bec05a5700008a97d0cfac494144a`, `v0.14.0`, `DOWNGRADED`, `Open`, and `Unknown` in `src/core/README.md`).

#### Completion Evidence

* Diff review and automated assertions in `test_governance.py` and `test_live_doc_links.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `docs/reference/README.md` and append `[2026-11-15]` entry to `docs/reference/log.md`

#### Context

Knowledge-base conventions require updating `docs/reference/README.md` and appending an entry to `docs/reference/log.md` whenever project documentation and knowledge-base records change materially, without rewriting any earlier log entry.

#### Intent

Update `docs/reference/README.md` (`ms.date: 2026-11-15` and the `#126` constructed RAI evidence register paragraph) and append a concise `[2026-11-15]` update record at the end of `docs/reference/log.md`.

#### Boundaries

* Included: `docs/reference/README.md` and EOF append on `docs/reference/log.md`.
* Excluded: Editing `docs/reference/memory.md`, editing any prior entry in `docs/reference/log.md`, or referencing `.copilot-tracking/`.

#### Likely Targets

* docs/reference/README.md: Frontmatter `ms.date` and `#126` governance register summary paragraph.
* docs/reference/log.md: Append `## [2026-11-15] update | ... (Refs #126)` at EOF.

#### Dependencies

* P02-T01.

#### Validation Expectations

* Prefix of `docs/reference/log.md` before the new `## [2026-11-15]` heading is byte-for-byte identical to `HEAD`, all relative links in `docs/reference/README.md` and the new `docs/reference/log.md` entry resolve to existing files and anchors, and zero `.copilot-tracking/` references appear.

#### Completion Evidence

* `git diff docs/reference/log.md` shows pure additions at EOF; `test_governance.py` and `test_live_doc_links.py` pass.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add Focused Runtime and Documentation Invariant Tests (`PC-002`) and Validate

### Context

`src/core/tests/test_governance.py` tests `GovernanceMixin` over both JSON (`Store`) and SQLite (`SqlStore`) via `Gov`/`JsonGov`/`SqlGov` and `EvidenceRegister`/`SqlEvidenceRegister`. Closure-audit rejections `PC-002` specifically flagged missing runtime assertions preserving PRD quality review and owner acceptance separation and missing test assertions verifying documentation, ADR, index, and append-only log updates and retained adverse outcomes.

### Intent

Add focused, high-signal tests in `src/core/tests/test_governance.py` covering Contracts 1, 2, and 3 (`PC-002`) and execute the focused validation tier cleanly.

### Boundaries

* Included:
  * Test ownership: `src/core/tests/test_governance.py` (with read-only regression runs of `src/core/tests/test_live_doc_links.py` and `src/api/tests/test_governance_evidence_api.py`).
  * Exact test removals: `none`.
  * Maximum test additions: up to 8 test methods across `EvidenceRegister` (inherited by `SqlEvidenceRegister`, so runtime assertions run on both JSON and SQLite!) and one `GovernanceDocumentationContractTests(unittest.TestCase)` class in `src/core/tests/test_governance.py`.
  * Canonical targets: `src/core/src/zava_forward/core/governance.py`, `src/core/tests/test_governance.py`, `src/core/README.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/reference/README.md`, `docs/reference/log.md`.
  * Generated targets: `none`.
  * Semantic-versus-regression coverage:
    * Semantic coverage: (1) `prd_quality_review` and `prd_owner_acceptance` separation from `baseline.acceptance_scope` and 22/22 `dispositions_complete` across all claim tiers (`independent-acceptance`), closed-schema claim write rejection, protocol/benefits/value-claim/release isolation, detached return copies, and raw storage tampering immunity on JSON and SQLite; (2) `live_use`, `affected_dispatch`, `conditional_eu_assurance`, and `EU-COND-01`/`EU-COND-02`/`EU-COND-04` conditional applicability guards before and after claims on JSON and SQLite; (3) repository documentation, ADR 0002, core README, KB index, and KB log invariants verifying current separation/dispatch/EU records, preserved historical versions and baseline commit, retained negative/insufficient outcomes, resolved relative Markdown links and `#heading` anchors, and absence of `.copilot-tracking/` references.
    * Regression coverage: Existing 22-finding inventory, replay/conflict/CAS/SQL-rollback tests in `test_governance.py`, `test_live_doc_links.py`, and `src/api/tests/test_governance_evidence_api.py`, plus synthetic stripped-container skip check when `ROOT / "docs"` is absent.
* Excluded: Modifying `src/core/pyproject.toml`, running `ruff format` directly on format-excluded file paths, or mutating shared Python site-packages.

### Likely Targets

* src/core/tests/test_governance.py: Add runtime methods on `EvidenceRegister` (executed for both JSON and SQLite) and `GovernanceDocumentationContractTests`.

### Dependencies

* P01 and P02.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v` exits `0`.
* Inside `src/core`: `ruff check .`, `ruff format --check .`, and `python3 -m mypy` all exit `0`.
* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_live_doc_links.py" -v` exits `0`.
* `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_governance_evidence_api.py" -v` exits `0`.

### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add focused Contract 1, Contract 2, and Contract 3 (`PC-002`) tests in `src/core/tests/test_governance.py`

#### Context

`EvidenceRegister` in `src/core/tests/test_governance.py` is subclassed by `SqlEvidenceRegister`, so adding runtime contract methods to `EvidenceRegister` automatically proves parity on both JSON `Store` and SQLite `SqlStore`. Adding `GovernanceDocumentationContractTests` in the same module (guarded by `if not (ROOT / "docs").is_dir(): self.skipTest("repository docs are not in this image")`, plus a dedicated unit check verifying that guard with `unittest.mock.patch`) ensures `python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v` exercises all three prompt contracts directly while preserving Docker image testability.

#### Intent

Author concise, non-redundant tests in `src/core/tests/test_governance.py` that fail without P01/P02 and prove Contracts 1, 2, and 3 (`PC-002`).

#### Boundaries

* Included:
  * Runtime tests on `EvidenceRegister`:
    1. `test_prd_review_and_owner_acceptance_stay_separate_from_report_and_remediation`: verifies `prd_quality_review` and `prd_owner_acceptance` in both `governance_view` and `governance_view["rai_evidence"]` before claims, after 22/22 `independent-acceptance` claims (`dispositions_complete is True`), after `protocol_freeze`/`protocol_approve`/`benefits_record`/`benefits_approve`/`release_record`, after mutating returned view copies, after rejecting `rai_evidence_record` payloads with `prd_quality_review` or `prd_owner_acceptance`, and after injecting raw `prd_quality_review="PASS"` / `prd_owner_acceptance="Accepted"` into persisted `governance` document state.
    2. `test_live_use_affected_dispatch_and_eu_conditional_guards_hold`: verifies `live_use`, `affected_dispatch`, and `conditional_eu_assurance` exact strings, verifies `conditional_eu` and `applicability_review` across all 22 findings (exact 3 `EU-COND-*` matches), and verifies appending `independent-acceptance` claims to `EU-COND-01`, `EU-COND-02`, and `EU-COND-04` leaves `baseline_status="NOT_ASSESSED"`, `baseline_verdict="UNCHANGED"`, `closure="Open"`, `acceptance="Unknown"`, `conditional_eu=True`, and `applicability_review="Required before conditional EU assurance applies"` unchanged.
  * Documentation/KB invariant tests on `GovernanceDocumentationContractTests`:
    3. `test_governance_docs_index_and_log_preserve_separation_and_adverse_history`: normalizes whitespace (`" ".join(text.split())`) and verifies per-document expectations across `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` (plus `docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md` immutability), asserting each document records the PRD quality/owner acceptance separation, disabled affected dispatch, and conditional EU applicability review boundary; preserves its canonical historical versions (`0.14.0` and `0.21.0` `Unsigned candidate` in addendum; `0.12.0`, `0.14.0`, `0.16.0`, `0.21.0`, and `Unsigned candidate` in PRD; `v0.14.0` and `1cb398c7b90bec05a5700008a97d0cfac494144a` in `src/core/README.md`) and retained adverse/insufficient outcomes (`FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, and `INVALID_PAYLOAD` in addendum; `FAIL`, `Validate BLOCKED`, `Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, and `DOWNGRADED` in PRD; `11 PARTIAL`, `11 NOT_ASSESSED`, and `2026-10-15` planning-only acceptance in ADR 0002; `DOWNGRADED`, `Open`, and `Unknown` in `src/core/README.md`); asserts zero `.copilot-tracking` strings across the entire text of `src/core/src/zava_forward/core/governance.py`, `src/core/README.md`, and `docs/adrs/0002-pilot-readiness-architecture.md`, and zero `.copilot-tracking` strings inside the `#126` / RAI sections of `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/reference/README.md` and inside the appended `## [2026-11-15]` entry of `docs/reference/log.md`.
    4. `test_modified_governance_docs_resolve_relative_links_and_heading_anchors`: parses non-fenced relative Markdown links across `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and the `[2026-11-15]` section of `docs/reference/log.md`, asserting every relative file target resolves, asserting full-file `#heading-anchor` slug resolution on `addendum`, `PRD`, `ADR 0002`, `src/core/README.md`, and the `[2026-11-15]` `log.md` entry, and asserting `#heading-anchor` slug resolution on the `#126` / RAI paragraphs and Project Documents rows of `docs/reference/README.md` (plus testing the container skip guard when `ROOT / "docs"` is absent).
* Excluded: Trivial constant-mirroring tests or reformatting existing lines in `test_governance.py`.

#### Likely Targets

* src/core/tests/test_governance.py: `EvidenceRegister` and `GovernanceDocumentationContractTests`.

#### Dependencies

* P01 and P02.

#### Validation Expectations

* All existing and newly added tests in `test_governance.py` pass under `unittest` and `ruff check .` / `ruff format --check .` / `mypy` in `src/core`.

#### Completion Evidence

* Passing verbose test output showing both JSON and SQLite `EvidenceRegister` runs plus `GovernanceDocumentationContractTests`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run focused validation suite and verify clean git diff invariants

#### Context

Focused validation requires running `test_governance.py`, `ruff check .`, `ruff format --check .`, and `mypy` inside `src/core`, plus documentation link/anchor verification and coupled API governance regression safety.

#### Intent

Verify every code, test, lint, format, typecheck, link/anchor, and diff-hygiene requirement before transitioning to `rpi-review`.

#### Boundaries

* Included: Running the focused validation commands, checking `git diff` on `docs/reference/log.md` and `.copilot-tracking/` exclusion across `src/` and `docs/`, and recording exact outputs in `.copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md`.
* Excluded: Pushing to remote or opening a PR.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/governance-126-rai-prd-separation-changes.md: Record implementation and validation receipts during `rpi-implement`.

#### Dependencies

* P03-T01.

#### Validation Expectations

* Zero test failures, zero ruff lint/format issues, zero mypy errors, zero broken relative links or scoped heading anchors, and zero added `.copilot-tracking/` references in `git diff -- src docs`.

#### Completion Evidence

* Complete changes artifact reconciled with plan checkboxes and session state.

#### Unresolved Items

* None.
