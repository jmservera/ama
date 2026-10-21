# Details: non-operative custody preparation (#122)

Plan: [plan](../../plans/2026-10-21/continuity-custody-preparation-122-plan.md).

## Phase 1: subsection content

File `src/core/README.md`, inside the issue #122 section after "Open owner items". Required elements:

* Status banner: preparation only, non-operative, nothing here is a drill, authority, legal compliance or release acceptance.
* Custody and evidence verification expectations: bundle `verify_export` with `expected_head` from an external copy; sealed year digests; incomplete bundles are not evidence; record which head and by whom.
* Decision rights table with roles or UNASSIGNED/UNAPPROVED gaps.
* Distinct witness requirements.
* Stop, recovery and restart sequence referencing #221 constructed restart.
* Communication owner and audience; stop conditions.
* "What is not evidence" and criteria status.

## Phase 2

One sentence in the #221 section linking to the new subsection.

## Phase 3 and 4

Local link check of anchors, `git diff --stat`, `git status --short --ignored`.
