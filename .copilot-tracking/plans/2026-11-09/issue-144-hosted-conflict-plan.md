# Plan: integrate current main into PR 1141 branch (2026-11-09, Refs #144)

Recorded prospectively before the merge. Research: [research](../../research/2026-11-09-issue-144-hosted-conflict-research.md). Details: [details](../../details/2026-11-09/issue-144-hosted-conflict-details.md).

Pins: HEAD 10d7caeed47bd4638dc62b5754db0302466c4aa6; origin/main d4d6827fe60be651cd922ab9656688c18c978e1d; predicted merge tree c71557173e66f1b6171235f5737e66473d8ca3d6 (prediction only).

## Phases

* [ ] P1: Re-fetch and confirm owner remote head still 10d7caee and main still d4d6827f; stop on movement.
* [ ] P2: Run one ordinary `git merge --no-ff origin/main` on `fix/demo-recovery-144-1109`. No rebase, reset or force.
* [ ] P3: Verify `docs/reference/log.md` keeps both the issue 144 entries and all main entries, with the 2026-11-09 144 header and text byte-identical to HEAD, and that earlier entries are unchanged (append-only).
* [ ] P4: Verify `src/agents` is byte-identical to 63d7f8c1 (queue_azure.py header `x-ms-date` kept) and tabulate the source/test/infra/dependency delta HEAD to the merge result.
* [ ] P5: Run owner demo-targeted tests (see details), with a core `test_paired_equity` run because main changed core.
* [ ] P6: Scoped whitespace and link checks on non-inherited changes only.
* [ ] P7: Single self-review, changes record, state, KB log entry (append), commit clean frozen local candidate.

## Critique (executed once, before the merge)

Verdict: proceed with amendments, all applied.

* Risk: ordinary merge conflicts in `log.md`. Amendment: if textual conflict occurs, resolve by keeping both sides' entries in append order, never dropping either; if intent cannot be resolved, stop and report the exact decision gap.
* Risk: a log entry for this merge is itself a second append to `log.md`. Accepted: append once after the merge commit content is verified, as a separate commit.
* Risk: claiming hosted mergeability from local tools. Amendment: report predicted/observed locally only; hosted CI and mergeability remain unobserved for the new head.
* Risk: whitespace check flags inherited sandbox whitespace from main. Amendment: scope `git diff --check` to the files this lane authors and report inherited findings separately without editing them.
* Risk: erasing adverse records. Amendment: P3 includes an explicit check that no existing tracking record is modified or deleted.

## Tier and limits

Owner demo-targeted tier. No `rpi-checks --all`. No push or GitHub write. Independent coordinator review of the new delta precedes any forward update; hosted CI of the new head must run.
