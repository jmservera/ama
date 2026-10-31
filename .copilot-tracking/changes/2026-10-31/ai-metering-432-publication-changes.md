<!-- markdownlint-disable-file -->
# RPI Changes: AI metering publication remainder

## Metadata and Execution

* Task ID 432-publication; slug ai-metering-432-publication; date 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md
* Scope: full child plan; status Partial, P01 complete; P02 pending.
* Approved targets: runner, runner tests (five methods maximum, removals none),
  related gate README and dated child evidence.
* Source-only boundary: no metering redesign, private data, paid calls or Azure.

## Starting Evidence and Critique Disposition

Read the caller-named previous correction changes first. Previous gate attempt
never started groups or produced a receipt; its original record is unchanged.
Focused research completed all three waves, Ready C1-C5/W1. The sole child
critique is Complete / Revise; PC-001/002/003 directly disposed before source
edits. In-tree evidence will freeze before final gate and sole exact-head
Review. Final result/state live externally and in the durable PR body.

## Validation Intent

P01-T01: existing runner tests and focused Ruff/format/mypy, plus actual
util-linux ownership/invalidity/closure/main-wiring tests on owned fixture locks.
P02: caller-authorised outer flock -w 1800 and full --all gate, fresh external
output/clean committed candidate/current main; per-group exception matrix.

## Remaining Work and Follow-ups

P02-T01, sole child Review and authorised push/main PR remain.
OD-51/prices/billing/batch, resident/historical joins and real pitch delivery
remain distinct parent RV-006 follow-ups. Hosted/human approval remains open.

## Completed Work: P01-T01 Inherited-lock Composition

tools/rpi-checks.py now validates an optional inherited descriptor against the
non-symlink regular shared path, duplicates it, asserts nonblocking exclusive
ownership and retains caller ownership through run/verify. Normal self-locking
admission is unchanged. src/README.md documents the explicit owner-authorised
queued composition; it grants no queue/publication authority.

tools/test_rpi_checks.py adds exactly five methods, removes none and leaves the
parent's two-module/35-method metering tests unchanged. Actual util-linux
composition, descendant FD exclusion, wrong/negative/closed/nonregular/symlink
inputs, contested ownership, pre-yield duplicate disposal, caller survival
through exceptions and main run/verify exclusion all pass.

Validation: 42 runner methods pass (11.661 seconds), with no skips; log
/tmp/ai432-publication-unit-final.log. Existing isolated E/F/I/B/UP Python 3.12
lint, isolated 100-column format and runner mypy pass; git diff --check passes.
An initial generic root Ruff invocation used unrelated repository-wide rules
and failed on inherited/new diagnostics; the repository's actual runner
isolated contract was then used. An initial new SPEC.origin narrowing error
was corrected with the actual test-file-relative runner path. These adverse
observations are retained, not evidence of a failed complete-gate group.

## Current Main and Candidate Preparation: P01-T02

Fetched main is a75bbdffa51ae34b1fcf779250f1f553d566ee93 and already an ancestor;
the explicitly requested git merge --no-edit origin/main returned Already up
to date. No rubric conflict or source merge was necessary. There is no observed
fix/gate-baseline-b023 PR yet; final fresh checks remain required.

This worktree contains inherited ignored developer caches. Do not delete them
or falsely call it a clean gate input: execute the full gate from a new owned
external clean clone of the final committed candidate. No private dataset or
foreign output is read/reused. Freeze committed preparation evidence, then
retain final gate/Review/state in an external dated tracking mirror and the PR
body to preserve matching exact candidate identity.

## Frozen Gate and Review Preparation

P01-T02 implementation/evidence commit:
cae4bba18d1800b571a2016638ef972e72d14559; all P01 tasks complete.
This subsequent preparation commit freezes in-tree evidence; final HEAD is
resolved externally to avoid self-reference. P02 is not yet complete and no
receipt or child Review outcome is claimed.

Owned clean clone: /tmp/ama-ai432-publication-clean-2026-10-31.
Full gate output: /tmp/ama-ai432-publication-gate-2026-10-31-a.
Gate log: /tmp/ama-ai432-publication-gate-2026-10-31-a.log.
Final Review/state/result root:
/home/azureuser/.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/
The PR body retains final identities, per-group evidence and review outcome;
final local files remain immutable/external, not unreviewed post-gate commits.
