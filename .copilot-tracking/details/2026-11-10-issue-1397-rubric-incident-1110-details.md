<!-- markdownlint-disable-file -->
# Details: issue 1397 incident documentation

Date: 2026-11-10. Plan: `.copilot-tracking/plans/2026-11-10-issue-1397-rubric-incident-1110-plan.md`.

## Phase 1: README subsection

Target: `.github/rubric/README.md`, new `### Run 42838857558 criterion-set rejection (2026-11-10, Refs #1397, #1383)` after the #1383 process qualification paragraph and before `## Files`. Style: existing heading hierarchy, `*` lists, ASCII punctuation, no em dashes, no bolded list prefixes.

Required content, each item traceable to the research record:

* Framing: dated historical record, documentation only, not a live acceptance, score repair or source-repair grant; #1383 preserved and a different incident; closure of #1397 is an owner decision.
* Failure: run, attempt, event, commit, all jobs `success`, gate decision fields and exact error, baseline unchanged, issue created at 15:03:33Z.
* Submitted inputs: two calls in file order; call 1 placeholder summary and `{}` details (all 20 IDs missing, none extra); call 2 complete 20-key set equal to the registry. No payload pasted beyond shapes and lengths; no grades reconstructed.
* Which call was judged: deduced from the absence of the gate's count message and the key-set rule; the consumed accepted-item bytes were not read.
* Unreconciled: prompt says no one-call quota while the #1383 record shows `Maximum allowed: 1`; whether call 2 was refused or dropped is not shown.
* Consumed identities: registry, gate, adapter, prepare, workflow, lock blobs; `BASE_REF=HEAD` so tools came from the scored checkout; baseline blob, scored commit, run and total.
* Diagnosis: valid fail-closed rejection; recurrence of the #1383 placeholder-first-call class with a different payload and adapter rule; not a new adapter, gate or transport defect; the earlier documentation is neither shown to have fixed nor to have failed to fix the producer.
* Publication and recovery: this run published nothing; successor run 42841391974 and baseline refresh pull request #1398 for `eff05737`; criteria content identical to the previous baseline, so fresh versus carried scoring and any assessment of the `6cc59776` changes are UNKNOWN; `6cc59776` never scored.
* Smallest future engineering action as an owner question requiring separate authority: retain the accepted-item list and gate decision as artifacts; any prompt or pre-append hardening is a separate design question; no waiver or validation relaxation.
* Remaining uncertainty list.

## Phase 2: validation

* `git diff --stat` shows only `.github/rubric/README.md` plus `.copilot-tracking/` additions.
* The #1383 section diff is empty (additions only after its last paragraph).
* Every commit, blob, run, pull request and job identity in the new text is re-derived from git or the supplied files.
* Relative and absolute links resolve; no em dashes; `git diff --check` clean.

## Phase 3: review and commit

One Review recorded in `.copilot-tracking/reviews/2026-11-10-issue-1397-rubric-incident-1110-review.md`; commit message `docs(rubric): diagnose criterion-set rejection at run 42838857558` with `Refs #1397, #1383` and the Copilot trailer.
