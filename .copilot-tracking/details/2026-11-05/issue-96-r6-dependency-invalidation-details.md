<!-- markdownlint-disable-file -->
# Details: issue-96-r6-dependency-invalidation

## Phase 1 forms.schema_impact(registry, bound, digest)

* Lineage: rows of the bound id must have readable definitions, digests equal to `ai_registry.digest(definition)`, versions exactly 1..N and the bound version present with a row digest equal to the draft's `schema_digest` and an equal definition. Any failure returns `status: Unknown`, every bound field cause `schema-lineage-unknown`, `form_wide` the same.
* Bound is latest: `status: Current`, no causes.
* Newer version: compare bound with latest. Form-wide keys `template`, `rule_refs`, `funding`, `reviewer`, `form_type` differing gives every bound field `form-wide-change`. Per field: absent in latest `field-removed`; different digest `field-definition-changed`.
* Closure to a fixed point: a field whose `required_when` (union of old and new) names an affected field gets `condition-depends-on-changed-field`; a field with a `calculation_ref` (old or new) gets `calculation-inputs-undeclared` while any other field is affected.
* Fields only in the latest version are `new_fields`. `affects_draft` is true for any cause, form-wide change or new field; a byte-identical successor is `Superseded` and affects nothing.

## Phase 2 form_review and form_export

* `_report`: field Stale when it has a schema cause or its bound source is not current (source checked even when a newer schema exists). New fields add Unknown issues. `dependency_impact` adds `schema`, `proposals`, `approvals`.
* Proposals: per staged candidate of this case/schema binding: `Current`, `Stale` (source changed or schema cause), `Unavailable` (evidence not readable) or `Unknown` (unknown field or unreadable linkage). Nothing is written.
* Approvals: draft-scoped holds only. A plain Held record is `Held`. An approval-bearing record (status other than Held, or non-null approved_input/approval_evidence) is `Current` only with a well-formed `bound` (`schema_digest`, `input_version`, `field_ids`) whose digest matches, with no form-wide impact, no listed field stale/removed/unknown and no history event for a listed field after the bound input version. Otherwise `Review required` with causes. Malformed records and non-dict ledger entries are `Review required`. Sibling drafts' records and global holds are untouched.
* `_freshness`: schema reason only when the impact affects the draft (or lineage unknown). `form_export.draft_export` returns `schema_impact` outside the hashed body; `export_freshness` adds a schema reason when it affects the draft even if no field is stale (for example a new field).

## Phase 3 tests

New `test_form_dependencies.py` (JSON and SQL stores): single-field change isolates siblings; identical successor affects nothing; condition and calculation propagation; form-wide reference change; malformed/missing lineage stays stale; proposal freshness isolation; approval references (current, field change, malformed binding, sibling draft); export freshness for a new field. Existing tests that registered an identical v2 are amended to a dependency-bearing v2.

## Phase 4

Focused tier plus FULL admission attempt only on an actually free `/tmp/ama-rpi-heavy.lock`; otherwise explicit pending.
