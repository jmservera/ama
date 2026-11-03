<!-- markdownlint-disable-file -->
# Research: issue-96-r1-held-export

* Task: issue #96 (parent #93), branch feat/issue-96-r1, base main b855aec86.
* Research disposition: executed. Planning Readiness: Ready.

## Prior delivery

* #377 (merged): unapproved schemas and candidate staging (criterion 2 of the issue, raw value/source/hash/locator).
* #510 (merged): isolated per-field review with history, held diagnostics and source/schema freshness (criteria 3 and 4 ticked).
* #888 (open, Refs #98/#96): `diagnostic_freshness` for saved manifests (FR-043 partial). Not redone; this slice avoids `form_review.py`.

## Unmet criteria

* 1 Approved versioned schema: blocked on Finance/template owner authority; no approved template exists.
* 5 Reviewed export never submits or implies eligibility: no export surface exists at all.
* 6 Only dependents stale: partial (field freshness in #510, manifests in #888); rule/calculation/pack-review/approval propagation needs approved rules.

## Chosen slice

A read-only `form_export.draft_export` in a new module: field values with source ID, version, hash and locator, schema/template/input versions, attachments, stale fields, open issues and a content hash; fixed Held, not reviewed, Not submitted, eligibility Not assessed. Advances FR-042 shape and the criterion 5 invariant without any approval authority. No AI, UI, SQL, infrastructure or security change, so the focused tier applies.
