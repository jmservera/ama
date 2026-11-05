<!-- markdownlint-disable-file -->
# Research: issue 96 r6, exact dependency stale/review-required propagation

Date: 2026-11-05. Base `ead177ef9` (origin/main). Task slug `issue-96-r6-dependency-invalidation`.
Research disposition: executed (new engineering-feasibility research; the historical
[2026-11-04 r5 record](../2026-11-04-issue-96-r5-research.md) is preserved unchanged as dated evidence).
Planning Readiness: Ready.

## Scope and inputs

Bounded part of criterion C6 only: "A source, schema or rule change marks only the dependent proposals
and approvals stale" (FR-043, AC-013, AC-051). Inputs read: issue #96 body/comments, merged-PR list
(#377, #510, #888, #902, #1093) and closure batch 002 (all three supplied JSON files),
`docs/reference/README.md` index entry points, PRD FR-038..FR-044, `src/core/README.md` working-review
section, `forms.py`, `form_review.py`, `form_export.py` and their tests. Historic PR510 adverse review
(`.copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md`, "Not accepted", RV-001/RV-002) is
retained, not replaced; RV-001/RV-002 are reported fixed in later PRs and are not re-litigated here.

## Findings (genuine gap versus existing behaviour)

Existing, not redone:

* Per-field source freshness (`_current`): id/version/hash/kind/bytes; only bound fields go stale.
* Schema freshness: `schema_current = latest == bound` and, when false, every field stale (all-or-nothing).
* Manifest freshness (`_freshness`) and saved export freshness (`export_freshness`) inherit the same
  all-or-nothing schema rule; input changes name only changed fields.

Missing (confirmed by reading code, not by assumption):

1. Schema change is not dependency-aware. Registering a successor version, even one that changes a
   single field, stales every field, and a byte-identical successor still stales everything. The
   issue wording requires "only the dependent" items. Immutable versions with digests make an exact
   field-level diff feasible without any approved rule object.
2. Rule and calculation references: `rule_refs`, `template` and each field's `calculation_ref` are
   versioned references already inside the schema definition. Their change is detectable by diff. No
   approved rule is needed to detect that a reference changed; none is evaluated (`approved_rule_validation`
   stays `Not evaluated`). Linkage between a rule and fields, and between a calculation and its inputs,
   is not declared in the schema, so those links are unknown and must stay stale rather than inferred.
3. Staged proposals (`form_staging` candidates) have no freshness report. A source change or a changed
   field definition leaves them silently looking current.
4. Approval references: the draft-scoped `finance_decision_holds` records carry `approved_input` and
   `approval_evidence`, always null today, and nothing says whether a future approval record is still
   current. No dependency evaluation of such records exists, and a malformed or unbound one would be
   treated as nothing at all.
5. Condition dependency: `required_when` makes one field's requirement depend on another field's
   value, an existing declared lineage that schema-change propagation can reuse.

Feasibility verdict: the r5 conclusion "no unblocked slice" is rejected for this sub-criterion only. The
blocker it cited (no approved rule object to version) does not apply to detecting reference/definition
changes, because the schema registry already versions and digests them. It remains correct for approved
schema (C1), reviewed export (C5) and approved rule evaluation, which stay unmet.

## Existing mechanisms to reuse

* `ai_registry.digest` for definition and field-level comparison; registry rows already hold digests.
* History events carry `field_id` and `input_version`, enabling "changed since approval" without new storage.
* Read-time derivation (README: freshness is evaluated on reads/actions, not pushed to a graph) keeps
  prior versions, history and unrelated decisions untouched.

## AI-registry prerequisite (confirmed, not approved)

Issue #96 depends on the AI task registry. `ai_registry.tasks()` has assistant, retained-path, chat and
concern-pack entries only, each `approval_state` Unapproved and `activation` "denied for live use"; no form
or extraction task is registered (`grep` of `ai_registry.py`). This slice adds no AI dispatch and no
registry entry; it uses the existing manual/recorded field contracts. Operational approval of any AI task
is not claimed.

## Overlap check

Edits planned only in `forms.py`, `form_review.py`, `form_export.py`, form tests and core README. No edit to
`quality.py`, `store.py`, `gates.py`, `projection.py`, ranking-publication, API `server.py` or web `ops.js`.
`role-screens.js` consumes `stale_fields`; keys are kept, so no prerequisite arises. Parent dependency:
#93 via `feat/finance-integration-93`.

## Decision

Implement: (a) exact schema dependency impact (definition diff, form-wide references, condition closure,
undeclared calculation inputs treated as dependent, lineage failure treated as Unknown/stale); (b) read-only
proposal freshness; (c) read-only approval-reference review-required evaluation that never creates or
approves anything; (d) manifest/export freshness using the same impact. Rejected: persisting stale marks
(would write history), inferring rule-to-field links, auto-approving schemas, any AI use.

## Unmet and gated

C1 approved schema, C5 reviewed export, named Finance review, Azure and financial acceptance remain unmet.
