<!-- markdownlint-disable-file -->

# Implementation Plan: fictional-form-review-97

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Research | .copilot-tracking/research/2026-10-20/fictional-form-review-97-research.md |
| Details | .copilot-tracking/details/2026-10-20/fictional-form-review-97-phase-details.md |
| Status | Planned; critique executed once (Revise), PC001-PC004 applied in details: .copilot-tracking/reviews/2026-10-20/fictional-form-review-97-plan-critique.md |

## Objective

Deliver a fictional, versioned, reviewable form/template and Finance
authority/binding pack for #97 using the existing `forms` schema contract. No
approval, signature, submission, payment, grant term or runtime change.

## Phases

### Phase 1: Pack fixture

* [ ] P1-T01 Create src/core/evals/fictional_form_review_pack.json (labels, template identity, freshness, schema definition, field authority/evidence/lineage table, roles, stale dependency map, Finance decision fields, not-approved statements).
* [ ] P1-T02 Register DS-FICT-FORM-REVIEW-PACK in provenance-register.json (public, root_label contract) and add a data-dictionary subsection.

### Phase 2: Focused test

* [ ] P2-T01 Add src/core/tests/test_form_review_pack.py: pack schema registers through `forms.register_schema` on JSON and SQLite stores as `Unapproved`; stale map references only declared fields/calculations and expected sets are exact; every Finance decision field is unresolved/null; preparer and reviewer roles differ; human-only fields have no candidate path (existing refusal); labels present; privacy checker passes.

### Phase 3: Knowledge base

* [ ] P3-T01 Add review note docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md (review questions, decision fields, how to use, what the pack does not prove).
* [ ] P3-T02 Update src/core/README.md #97 section with a short pointer; update docs/reference/README.md index row and append-only docs/reference/log.md entry; set ms.date where files change.

### Phase 4: Validation

* [ ] P4-T01 Focused tests, privacy/provenance tests, ruff/format/mypy for core, markdown link review.
* [ ] P4-T02 Commit, original Review, final commit, full local gate, receipt verification, freeze.

## Acceptance Mapping

Issue criterion 1 remains unmet: actual Finance/Owner authority and binding is
absent. Criterion 2 is already delivered (#377). No closing keywords.

## Risks

* Public-payload privacy patterns reject emails, so the registered reviewer is substituted by the test.
* The fixture could be mistaken for an approved template; labels repeat on the root, template, every decision field and the KB note.
* `forms` contract drift is caught by the registration test.

## Clarification 2026-10-20 (process disclosure, appended)

This plan was hand-authored without activating the rpi-plan skill; its critique was a read-only subagent review, not an rpi-plan-critique run. It is an UNVERIFIED pre-RPI draft and the text above is unchanged. The executed plan is .copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md.
