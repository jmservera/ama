<!-- markdownlint-disable-file -->
# Critique: issue-96-r6-dependency-invalidation plan

Executed once on the final candidate plan (self-critique; independent exact-head review remains required). Verdict: proceed with the dispositions below.

* Risk: narrowing schema staleness loosens a conservative control. Disposition (applied): narrowing happens only when lineage and digests verify, every form-wide reference is equal and the field definition digest is equal; any doubt is Unknown/stale. Undeclared calculation inputs and rule-to-field links stay stale, not inferred.
* Risk: inventing an approval schema. Disposition (applied): no approval is created or written; only a read-time evaluation of records that already carry approval fields, treating anything without a well-formed binding as Review required, never Current.
* Risk: changing hashed export body invalidates saved exports. Disposition (applied): `schema_impact` stays outside `BODY_KEYS`.
* Risk: snapshot/report growth. Accepted; fields are small and recorded snapshots stay immutable.
* Overlap: no forbidden file touched; `stale_fields` keys preserved for web consumers.
* Conflicts with confirmed user decisions: none.
