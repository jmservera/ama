<!-- markdownlint-disable-file -->
# Research: issue-98-r2-changed-fields

* Task: issue #98 (parent #96), branch feat/field-review-stale-98, base main 5e6d5a837.
* Research disposition: reused (r1 research plus fresh code read). Planning Readiness: Ready.

## Prior delivery (merged)

* #377 and #510 delivered schemas, staging, isolated field review with history, held diagnostics and manifests (criteria 1 and 4, already ticked).
* #888 delivered `diagnostic_freshness` per saved manifest (Stale/Current, stale source fields, re-run action).

## Unmet criteria

* 2 (approved rules): needs Finance/template owner authority; `approved_rule_validation` stays "Not evaluated". Human step.
* 3 (reviewed pack): needs approved template and Finance authority. Human step.

## Gap

A stale manifest said "reviewed inputs changed" without naming which fields. FR-043/AC-051 asks for exact dependents so reviewers re-review only what changed.

## Chosen slice

Add `changed_fields` to each `diagnostic_freshness` entry: fields whose reviewed value or state differ from the manifest snapshot. Core only; no UI, SQL, infrastructure or AI change. Focused tier.
