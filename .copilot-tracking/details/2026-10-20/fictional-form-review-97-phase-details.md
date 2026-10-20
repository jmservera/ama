<!-- markdownlint-disable-file -->

# Phase Details: fictional-form-review-97

Plan: .copilot-tracking/plans/2026-10-20/fictional-form-review-97-plan.md

## Pack shape (P1-T01)

Root keys: `is_synthetic` true, `label`, `status` ("NOT APPROVED"), `pack_version`,
`pack_date`, `statements` (not approved, no submission, no payment, no scheme terms,
no signature), `template` (id, version, effective/review dates, freshness policy),
`schema` (exact `forms._schema` definition; `reviewer` is the placeholder
`REGISTERED-REVIEWER-SUBSTITUTED-BY-TEST`), `field_review` (per field: authority
policy summary, evidence, freshness max age days, lineage requirement),
`lineage_expectations`, `roles` (preparer, reviewer, separation rule),
`stale_propagation` (triggers with exact affected and unaffected field/calculation IDs),
`finance_decisions` (list with id, question, value null, status, owner role, evidence
needed), `unmet_authority`.

## Test (P2-T01)

Use `dataset.DATA` staff Programme Manager (`pam@example.test`, role satisfying the
actor guard) as in test_form_staging; substitute reviewer; register on Store and
SqlStore; assert `approval == "Unapproved"`; digest stable. Stale: for each trigger
`affected | unaffected == all field ids` and disjoint, and referenced ids declared.
Decisions: every `value is None`, status exact, `signature` has no date or name.
Roles: preparer != reviewer. Privacy: `privacy.public_issues(ROOT) == []`. No new
runtime code.

## Critique dispositions applied (PC001-PC004)

* Test first asserts the unsubstituted `pack["schema"]` is rejected, then builds a
  derived `registration_request` differing only in `reviewer` and registers it.
* `field_review` maps one-to-one to schema fields; authority, evidence and
  calculation values equal the schema's; referenced IDs are declared.
* Stale propagation and role separation are labelled proposed controls for #98; the
  tests are review-pack data-integrity checks, not runtime behaviour.
* Template and every decision carry explicit status; decision values are null; no
  names, signatures, dates, terms, routes or binding statements appear.

## Validation (P4)

`python -m unittest` for the new test, test_form_staging, test_synthetic_provenance;
ruff check/format/mypy in src/core; then full gate per common contract.

## Clarification 2026-10-20 (process disclosure, appended)

These details were hand-authored without activating rpi-plan and are an UNVERIFIED pre-RPI draft; the text above is unchanged. Executed details: .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md.
