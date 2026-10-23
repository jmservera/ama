<!-- markdownlint-disable-file -->

# Task Research: fictional-form-review-97

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Planning Readiness | Ready |
| Research disposition | executed |
| Artifact path | .copilot-tracking/research/2026-10-20/fictional-form-review-97-research.md |

## Research Brief

Issue #97 first acceptance criterion: "Schema defines field types, units, required
and conditional fields, source authority and evidence". Engineering and durable
candidate staging were delivered in PR #377 (criterion 2 ticked). Owner comment
`#126` 6290697705 (2026-10-20) permits a FICTIONAL versioned form/template and a
Finance authority/binding pack for actual review, NOT an approved template.
Scope: integrate one concrete reviewable synthetic template over the existing
schema contract; no new engine, service, runtime or rebuild of #377.

## Findings

| ID | Evidence | Finding |
| --- | --- | --- |
| R1 | src/core/src/zava_forward/core/forms.py `_schema` | The exact schema contract is a closed key set: id, version, form_type, template, reviewer (registered staff email), funding, rule_refs, fields. Each field has exactly id, section_id, type (string/integer/number/boolean/date/enum), unit, options, required, required_when, source_authority (kind from `Store.KINDS`, unique rank), evidence_required, calculation_ref, category (`value` or human-only declaration/signature/attestation/consent/approval). Funding forms cannot be `Not applicable`. |
| R2 | `register_schema` | Every registration is server-stamped `Unapproved`, null approval evidence; no approval flag can be supplied. A pack therefore cannot create approved status. |
| R3 | `stage_candidates` and src/core/README.md section #97 | Parser/OCR lineage is already staged (kind, parser, version, model version, route evidence, error record, `Supplied, unverified`). Stale-field propagation, field review, validation and pack are #98 and not delivered here. |
| R4 | src/importer/evals/document_form_fixtures.json `form_schema` | An existing 12-field placeholder `SYN-FUND-FORM-1.0` uses a different non-contract shape (name/required/conditional_on string) and has no authority, units per field, lineage or versions. It is generator-owned and registered as DS-DOC-FORM-FIXTURES; it is not modified. |
| R5 | PRD FR-038, AC-046, OQ-015 | Real funding route, templates, scheme terms, field/attachment authority and approver are unresolved Finance/Legal inputs. Unknown route blocks preparation; no current round, eligibility or award terms assumed. |
| R6 | provenance-register.json, src/core/synthetic/privacy.py | `public_issues` fails an unregistered `*.json` under `src/*/evals`; a new public fixture needs a dataset entry with visibility, location, validation contract and dictionary anchor. Emails, phones, postcodes are rejected in public payloads. |
| R7 | owner comment, issue #97 body | Criterion 1 requires actual approved-template authority/binding. A fictional pack supplies a review object only; the criterion stays unmet. |
| R8 | test_form_staging.py | Existing tests build their own small fictional schema; none exercises a complete pack, authority-decision fields or dependency map. A focused fixture test is a genuine gap. |

## Decision Options

| Option | Result |
| --- | --- |
| A. New public JSON fixture under src/core/evals plus KB review note, registered in provenance, with one focused test that registers its schema through the existing `forms.register_schema` on JSON and SQLite stores | Selected: smallest concrete reviewable object, exact compatibility proven, no runtime change |
| B. Edit the 120-family generator fixture | Rejected: generator-owned, different shape, hash-checked |
| C. Add pack loader, validator or API | Rejected: new runtime/engine outside direction |
| D. Markdown only | Rejected: no mechanical compatibility proof with the schema contract |

## Pack content decisions

* Fictional funding-form template `FICT-FUND-FORM`, version 1, funding association
  `Unknown` (scheme, route and evidence null) so the pack cannot imply a real round.
* Fields exercise all six types, units (GBP, m2, kWh/m2/year, none), required and
  conditional requirements, per-field ranked source authority by existing document
  kinds, evidence requirements and a calculation reference, plus human-only
  declaration, signature and approval fields that can never receive candidates.
* Source authority is expressed by existing `Store.KINDS` with fictional policy
  evidence references; none is a real scheme rule.
* Version/freshness: template/rule/source versions with fictional effective dates
  and a `review_by` date; real effective dates are Finance decision fields.
* Lineage expectations restate the delivered staging record (text/csv/ocr) without
  claiming verification; OCR route authority stays unverified.
* Preparer/reviewer separation is a role-level rule over fictional role labels; the
  reviewer registered in the schema is substituted from the test dataset because
  the public payload may not carry email addresses.
* Stale propagation is a declared dependency map (template, rule, source document
  versions to field and calculation IDs) with expected affected/unaffected sets,
  data only. #98 owns runtime propagation.
* Finance authority/binding decision fields are all unresolved nulls with status
  `Unresolved - Finance to supply`: authority holder, scheme and route, template
  source and version, effective dates, rule/terms source, attachment authority,
  approver, approval date, signature, binding statement. No signature or actual
  grant/contract term is invented.

## Constraints and Non-goals

No runtime change, schema engine, API, UI, cloud, private data, payment,
submission, eligibility or approved-template status. Infra runbook, budget/benefits
synthesis, map and cohort documents are not edited. KB index/log are append-only.

## Planning Readiness

Ready. Remaining human-blocked item: actual Finance/Legal template authority and
binding (OQ-015). Criterion 1 stays unticked.

## Clarification 2026-10-20 (process disclosure, appended)

This file was hand-authored by the agent without activating the rpi-research skill and is therefore an UNVERIFIED pre-RPI draft, not an executed RPI Research phase. The text above is unchanged. The genuinely skill-executed record is .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md.
