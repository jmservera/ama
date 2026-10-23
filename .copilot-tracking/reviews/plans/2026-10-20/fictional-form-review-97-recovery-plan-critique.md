<!-- markdownlint-disable-file -->
# RPI Plan Critique: Fictional Finance form/template review pack (#97), recovery

## Metadata

* Task ID: 97-recovery
* Critique date: 2026-10-20
* Plan: .copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: fictional versioned Finance form/template review pack using the existing forms schema contract; no runtime, approval, signature, submission or payment; criterion 1 stays unmet; draft files are unverified and uncommitted.
* Research and evidence considered: .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md (structure only), src/core/src/zava_forward/core/forms.py, src/core/evals/fictional_form_review_pack.json, src/core/tests/test_form_review_pack.py, the DS-FICT-FORM-REVIEW-PACK register diff, docs/reference/README.md and src/core/README.md (grep only), /tmp/ama-wave-20261020-2113-common.md.
* Decisions, dependencies, and acceptance criteria considered: plan and details acceptance criteria, locked test ownership, P01-P03 ordering, critique disposition.
* Assessment boundary: draft content was checked against forms._schema by running `test_form_review_pack test_synthetic_provenance test_form_staging` (35 tests, OK). The critique cannot conclude anything about the not-yet-written KB notes, the changes record, the full gate or hosted checks.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Schema contract compatibility (P01-T01, P01-T02) | Covered | Schema registers on Store and SqlStore as Unapproved; the raw placeholder reviewer is refused. All six `forms.TYPES`, units GBP, m2, kWh/m2/year, two conditional fields and three human-only categories are present. |
| Source authority and evidence | Covered, with a gap | Every field has ranked source policies and evidence_required. Policy evidence_refs are opaque FICT-POLICY-* strings; their unresolved status is only implied by FD-07 (PC-005). |
| Version and freshness | Partial | template version, null effective_from and pack_review_by exist; max_source_age_days and stale_on are not reconciled with stale triggers (PC-001). |
| Parser/OCR lineage | Partial | lineage_expectations match `_processing`, `_locator` and `_source_cells`, but no test ties them to the contract (PC-003). |
| Preparer/reviewer separation | Covered | Three distinct roles, explicit may_not, labelled "Not enforced". Test checks distinctness. |
| Stale propagation | Partial | Four triggers, each exhaustive and disjoint, but fewer than the per-field stale_on values (PC-001). |
| Unresolved Finance decisions | Covered | FD-01..FD-14 all value null and status unresolved; the test asserts exact keys. |
| Not-approved, no-submission, no-payment labels | Partial | Present in the pack label and statements, but the test does not assert the submission or payment wording (PC-002). |
| Plan structure and validation | Partial | Plan does not gate the corrected-content checks it implies (PC-004, PC-006). |

## Verdict

* Verdict: Revise
* Rationale: the draft is largely contract-compatible and honest, but its stale map does not cover the freshness triggers the pack itself declares, and the tests do not lock all owner-direction labels or lineage claims. The plan lets "verify and correct" pass without those checks. All findings are planner-owned corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: field_review stale_on and max_source_age_days have no matching stale triggers

* Related IDs: P01-T01, P01-T02, Functional Requirements (stale map), owner direction on version/freshness and stale propagation
* Evidence: src/core/evals/fictional_form_review_pack.json. field_review uses stale_on values "Survey supersession", "Design supersession", "Funding evidence supersession", "Consent change or withdrawal", "Cost document supersession", "Survey or EPC supersession" and rule-version variants. stale_propagation.triggers holds only ST-TEMPLATE-VERSION, ST-RULE-VERSION, ST-EPC-SUPERSESSION and ST-COST-DOCUMENT-CHANGE. test_stale_map_is_exhaustive_disjoint_and_calculation_consistent checks each trigger internally only.
* Concern: home_ref, survey_date, storey_count, measure_type, funding_mix and resident_consent_recorded declare staleness events that no trigger propagates. Age expiry (max_source_age_days 365) has no trigger either. A reviewer reading the map would conclude those fields never go stale on those events. The plan's claim "stale triggers are exhaustive" is only true per trigger.
* Impact: the stale-propagation element of the owner direction is incomplete, and the test gives false assurance.
* Smallest useful change: add triggers for survey, design, funding-evidence and consent change plus a source-age expiry trigger, or reduce stale_on to values that map to existing triggers. Add to P01-T01 and P01-T02, and make the test assert that every field's stale_on maps to a trigger that lists that field in affected_fields.
* Action owner: planning parent (implementation via rpi-implement)
* Exact resolving evidence: updated JSON plus a passing test asserting field_review stale_on values correspond to trigger ids (for example a `trigger` id key on field_review), and an age-expiry trigger listing every field with a non-null max_source_age_days.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Required no-submission and no-payment labels are not asserted by the test or named in the plan

* Related IDs: P01-T01, P01-T02, Acceptance Criteria, owner direction on labels
* Evidence: the root label contains "No submission, no payment" and statements contain a sentence on submission and payment; test_authority_and_binding_decisions_are_unresolved_and_unsigned asserts only "not a real", "Unapproved", "No Finance" and "criterion 1 remains unmet".
* Concern: the labels are the owner's explicit non-negotiables, yet removal would not fail any test. P01-T01 lists "no-submission and no-payment labels" as included but gives no check.
* Impact: label regression passes silently.
* Smallest useful change: assert "No submission" and "no payment" in PACK["label"] and PACK["statements"], and "NOT APPROVED" in label. State the assertion in P01-T02 validation expectations.
* Action owner: planning parent
* Exact resolving evidence: test assertions present and passing; P01-T02 text names them.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Lineage expectations are unverified prose against the contract

* Related IDs: P01-T01, P01-T02, research C-lineage
* Evidence: lineage_expectations in the pack versus forms._processing, _locator and stage_candidates. Content matches the code today (text zero-based half-open, CSV one-based, OCR route evidence and error record required, human-only fields refused), but test_form_review_pack.py asserts none of it and stage_candidates is untested against the pack schema.
* Concern: lineage is a required owner element, and the plan declares existing staging tests regression-only. If forms.py changes, the pack silently misstates the contract.
* Impact: reviewers may rely on stale lineage claims.
* Smallest useful change: add one test that, with the registered pack schema, confirms stage_candidates refuses a declaration, signature or approval field with PermissionError, and that the recorded list in lineage_expectations equals the processing keys and source keys. Avoid a new harness; reuse the existing document fixture helpers from test_form_staging.
* Action owner: planning parent
* Exact resolving evidence: passing test; P01-T02 updated, including the locked-test-ownership paragraph.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: P01 "verify and correct" lacks an explicit element checklist and cross-file consistency checks

* Related IDs: P01-T01, P03-T01
* Evidence: details P01-T01 says "Element checklist in changes record" but names no elements or check commands. The pack duplicates facts across template, schema.template, calculations, field_review, roles and the register entry, and reviewer substitution is the only equality check.
* Concern: completion evidence is subjective. The checklist should be the owner-direction list: field types, units, required, conditional, source authority, evidence, version, freshness, lineage, separation, stale propagation, unresolved decisions, labels, with the test or file path proving each.
* Impact: the Review cannot independently verify P01.
* Smallest useful change: embed the thirteen-element list in P01-T01 completion evidence, each mapped to a named test or JSON path.
* Action owner: planning parent
* Exact resolving evidence: details file lists the mapping; changes record reproduces it with results.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Source-authority policies are not marked as unresolved fictional proposals

* Related IDs: P01-T01, research on source authority
* Evidence: schema.fields[*].source_authority (kinds and ranks, evidence_ref "FICT-POLICY-*") and schema.rule_refs ("FICT-RULE-SOURCE-UNRESOLVED"); FD-07 field_source_authority is unresolved but the fields carry no status of their own. The contract allows only the exact key set, so a per-field flag cannot be added inside the schema.
* Concern: ranks and kinds could be read as an agreed precedence.
* Impact: minor mis-reading risk.
* Smallest useful change: add a top-level pack statement, asserted by the test, that all source ranks and evidence_refs are fictional proposals pending FD-07 and FD-09.
* Action owner: planning parent
* Exact resolving evidence: statement present and asserted.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Dependencies, sequencing and artifact lifecycle gaps in the plan

* Related IDs: Dependencies, P01-T02, P02-T02, P03-T01, Handoff
* Evidence: plan Dependencies relies on /tmp/ama-97-venv, which is outside the repository and not guaranteed to exist for a fresh agent; the plan lists the exact test command in details but not ruff, format and mypy commands; git status shows the earlier-pass plan, details, research and critique files untracked, and P02-T02 appends to them without saying that they must be committed unmodified before the clarification, or how "append only" is verified on untracked files; the draft pack has no baseline commit to diff.
* Concern: append-only proof and verification of "no runtime file changed" depend on a baseline that does not exist, and the one-pass critique location differs (reviews/ for the earlier critique, reviews/plans/ for this one).
* Impact: weak completion evidence, risk of overwriting preserved originals.
* Smallest useful change: in P03-T01 specify the exact ruff check, ruff format --check and mypy commands; copy hashes of the preserved draft artifacts into the changes record before appending; verify no change under src/core/src with `git diff --stat` and `git status`; say the venv must be recreated with pip if missing.
* Action owner: planning parent
* Exact resolving evidence: changes record containing pre-append SHA-256 values, matching post-append prefix check, and command outputs.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Public README and index wording must not imply template authority

* Related IDs: P02-T01, P02-T02
* Evidence: docs/reference/README.md row for #97 currently states "No actual template authority"; the new row and src/core/README.md pointer are unwritten. Registry entry data_dictionary anchor is `data-dictionary.md#document-and-form-data`, which must exist after P02-T01.
* Concern: new wording could read as a delivered template; the anchor may not resolve.
* Impact: misleading KB entry or broken registry link.
* Smallest useful change: add to P02 validation expectations a check that the anchor exists and that new text contains "fictional", "not approved" and "criterion 1 unmet". Keep the dictionary subsection under the existing heading.
* Action owner: planning parent
* Exact resolving evidence: grep of the anchor heading and the three phrases in each new text; link check recorded.
* Decision route: direct planner correction

## Strengths and Residual Risk

* The draft passes the real contract: registers on both stores, remains Unapproved, uses the reviewer substitution honestly and refuses the placeholder.
* All fourteen Finance decision fields are null and unresolved; the approver role is unassigned; no signatures, emails, scheme terms or real data.
* Stale propagation and separation are labelled proposed and unenforced.
* Residual risk: the pack's fictional content cannot prove criterion 1; the plan correctly keeps it unmet and avoids closing keywords.

## Questions or Blocking Evidence Gaps

* None. No user decision is required.

## Limitations

* Research file was not re-audited claim by claim; findings rest on direct source inspection.
* The privacy checker and provenance behaviour were exercised only through the existing tests.
* Phases P02 and P03 documents do not yet exist, so their credibility is limited to the plan.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: revise P01-T01 and P01-T02 to add the missing stale triggers (or align stale_on) with a test that every field's stale_on maps to a trigger, then apply PC-002 to PC-007 directly and finalize without another critique.
* User response required: no

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md](.copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md](.copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md) | Phase details under critique |
| [src/core/evals/fictional_form_review_pack.json](src/core/evals/fictional_form_review_pack.json) | Draft pack examined |
| [src/core/tests/test_form_review_pack.py](src/core/tests/test_form_review_pack.py) | Draft test examined |

## Next Steps

* Return the verdict to the planning parent, which revises directly (PC-001 to PC-007) and finalizes. No user action is required.
