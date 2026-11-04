<!-- markdownlint-disable-file -->
# Research: issue-96-r2-export-freshness

Disposition: executed (reused r1 research for schema and report internals). Planning Readiness: Ready.

## Delivered already (merged PRs)

* #377 unapproved schemas and candidate staging; #510 working reviews with per-field accept/correct/reject; #888 saved-manifest freshness; #902 held read-only draft export.
* Open #1083 (Refs #98) lists changed fields on stale manifests; it edits `form_review.py`, so this slice avoids that file.
* Issue ticks: criteria 2, 3, 4 met. Unmet: 1, 5, 6.

## Gap

A held export is a content-hashed copy a person may keep or pass on. Nothing tells them when it is out of date, or whether it was altered. Criterion 6 asks that a change mark only dependent items stale. Rule and calculation propagation needs approved rules (not available), but export freshness can be proven now.

## Slice chosen

`form_export.export_freshness`: read-only comparison of a saved export with the current review. Reports Current, Stale (dependent fields only, with unaffected fields), Invalid (hash mismatch or incomplete) or Unavailable. Schema or rule-reference change changes `schema_digest` and stales all schema-bound fields (the existing report rule).

## Boundaries

No writes, AI, UI, SQL, infrastructure, security or deployment change; focused tier. Manual path: the working review. Resident consent and human approval are untouched; the result never sets reviewed, submitted or eligible.

## Unmet after this slice

1 (approved schema needs Finance/template authority), 5 (no reviewed export exists), 6 (rule, calculation and approval propagation needs approved rules and approvals).
