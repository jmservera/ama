<!-- markdownlint-disable-file -->
# RPI Phase Details: PR 507 evidence corrections

## Metadata

Task ID/slug: pr507-evidence-corrections, 2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/pr507-evidence-corrections-plan.md.
Research: .copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct delivery and recovery evidence

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reconcile pack, KB and external PR body

Correct existing sentences under Registry sequence, Local test reassessment
and acceptance, and the B6 table. Qualify 31 fixture passes and 374/1/7 as
original/discarded, not current. Current suite result is 355/18/7.
Use src/README.md registered under solution-code for the proposed later PR;
keep #302's actual delivered guides historical. Explain no present reopening
of B6 or score increase. No newly created numbered PR or guaranteed gain.

Add a dated correction section with exact immutable prior integrated commit,
base and hash, contrasting the original candidate's de87d9e0 hash. State that
the current correction changes that frozen delta rather than claiming the
old hash still identifies this worktree. Production docs may link public
Git commits/compares, never tracking artifacts.

Update the current index synthesis and append log only; do not rewrite old
log or tracking outcomes. Create /tmp/pr507-body.md with a suggested title,
documentation-only summary, honest validation boundaries, original/current
frozen references and Refs #198. No GitHub metadata write.

Completion: both supplied comments reconciled everywhere in this section and
external description; original score/acceptance uncertainty preserved.

<!-- rpi:phase id=P02 -->
## P02: Validate and prepare independent Review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validate focused tests and evidence contracts

Use /tmp/mv/bin/python for migration and actual prepare/matcher assertions.
Missing pytest was reproduced during Research. An isolated external
--target install of pytest is permitted after this missing-dependency failure;
no dependency manifest change, new test tooling or shared venv mutation.
Set that tooling directory on PYTHONPATH only for pytest itself, never a legacy
application import workaround. Retain external logs in session storage.

Run existing selectors for registered/src/excluded files and changed-file gate
evidence; measure full unchanged rubric result if useful. No test additions or
removals. Assert actual registry membership for src/README.md (B6) and absence
for .github/rubric/README.md; actual prepare must not score this doc-only change.
Check new/changed Markdown relative targets and anchors, frozen pre-correction
hash, immutable inputs against starting HEAD/main, full old log prefix,
original evidence identity, and no closing-keyword references in new body.
No full application/heavy/publication checks for local-only bounded docs.

Completion: commands, exact exits/results and honest adverse/skipped evidence.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence, freeze correction and hand off

Depends on P02-T01. Changes artifact owns result evidence; plan and details
mark P01/P02 complete only after corresponding work. Hash the three-doc
diff against immutable base and the external body before one independent
Review. Reviewer may write only its canonical artifact, cannot fix content.
Parent handles commit and final state afterward; no same-task Review repeat.
Authenticate gh user and configure repository-local noreply email before
Conventional Commit with Refs #198 and required Copilot trailer.
Verify clean worktree, email/trailer and hashes. No push.

## Current Completion State

P01/P02 and all tasks complete. Planning Complete / Ready. Sole critique Complete /
Revise; PC-001 rejected because its worker-local filesystem restriction cannot
override the caller's explicit parent output/environment paths. Preserve the
requested destinations and isolate test tooling in session storage. No blocker
or unresolved decision; no second critique.
Validation: full rubric 355 passed/18 failed/7 skipped (unchanged inherited
failure set), focused 14 passed/2 inherited failures/84 deselected, migration
25 passed. Actual prepare/matcher, synthetic B6 changed-citation contracts,
two changed links/anchors, original evidence/protected bytes, append-only log
and whitespace pass. Initial validation import error resolved with the tool's
own sibling import directory; no application import workaround/source edit.
Correction freeze and external body hash recorded in changes; sole independent
Review ready. Parent commit and final metadata verification follow that Review.
