<!-- markdownlint-disable-file -->
# Research: issue-96-r3-status-record

Disposition: executed. Planning Readiness: Ready.

## Delivered already

* Merged: #377 (unapproved schemas, candidate staging), #510 (working accept/correct/reject reviews, held diagnostic manifests), #888 (saved-manifest freshness), #902 (held read-only draft export), #1083 (changed fields on stale manifests).
* Open on this branch: #1093 (export freshness check, Refs #96).
* Issue ticks: criteria 2, 3, 4 met. Unmet: 1, 5, 6.

## Finding: inherited review defects are no longer open in code

The 2026-10-27 review left RV-001 (historical values returned without source bytes) and RV-002 (conflict alternatives not freshness-qualified) as Medium. Current `form_review.py` checks source availability for every retained value, history entry, snapshot and attachment (`_visible`, `_digest`) and qualifies conflict alternatives by current source and policy (`_report`). Tests cover both: `test_missing_bytes_block_stale_rejected_and_replaced_retained_history`, `test_missing_snapshot_only_sources_block_each_retained_snapshot_surface`, `test_conflicts_exclude_unreviewable_alternatives_without_removing_staging`. The original review file is preserved unchanged; this record only notes the later evidence. Passing tests are evidence of behaviour, not an acceptance decision.

## Gap analysis for unmet criteria

* 1: needs a Finance/template owner to supply an approved versioned template, field/source policy and route (OQ-015, FD-01..14). Human decision.
* 5: a reviewed export needs approved template and rules plus a named human reviewer. Only Held diagnostic exports exist. Blocked by criterion 1.
* 6: source and schema staleness is exact and proven for drafts, manifests and (in #1093) exports. Rule, calculation and approval propagation needs approved rules and approvals that do not exist.

## Slice chosen

No engineering slice advances an unmet criterion without inventing authority. Docs-only status record: this evidence set and a knowledge-base log entry. No source change.

## Boundaries

No AI, UI, SQL, infrastructure, security or deployment change; focused tier. Manual path remains the working review. Resident consent and human approval are untouched.
