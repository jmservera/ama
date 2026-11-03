<!-- markdownlint-disable-file -->
# Research: issue-98-r1-manifest-freshness

* Task: issue #98 (parent #96), branch feat/issue-98-r1, base main 9a9f9dada.
* Research disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged)

* #377 delivered unapproved schemas and candidate staging (#97 foundation).
* #510 delivered isolated field review (accept/correct/reject with history), held deterministic diagnostics, evidence-linked diagnostic manifests and exact source/schema freshness of working fields. Review RV-001 and RV-002 (`.copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md`) were fixed by later commits inside #510 (c50f0473a, 06988b22e); tests `test_missing_bytes_block_*` and `test_conflicts_exclude_unreviewable_*` exist on main. Nothing to redo.
* Issue boxes 1 and 4 are already ticked.

## Acceptance criteria status

* 2 Validation uses approved rules and reviewer-confirmed inputs only: unmet. Confirmed-input logic exists, but no approved rules exist (Finance and template owner decision FU-FINANCE; `approved_rule_validation` is "Not evaluated").
* 3 Pack links fields, evidence and attachments with template and input versions: unmet as a reviewed pack. Held diagnostic manifests already carry these links; a reviewed pack needs Finance authority.

## Gap found (FR-043, AC-051)

Saved manifests are frozen snapshots; `view` returned them with no signal that their inputs changed (a later review, a changed source, or a newer schema), so a stale manifest looked current. FR-043 asks for exactly the dependent pack reviews to be marked stale for re-review while preserving prior versions.

## Chosen slice

Report `diagnostic_freshness` per saved manifest in `form_review.view`. Needs no approval authority, no new AI, no UI, no SQL or infrastructure change.
