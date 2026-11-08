# Plan: issue 107 final FULL preparation (prospective, no execution)

Date: 2026-11-08. Written before any record other than the research file; one critique follows (see the critique file). Details are inline here.

## Objective

Freeze an ignored-clean candidate and a literal, reviewed future FULL handoff. No source, test, runner, store, rubric or production change.

## Phases

1. Verify state and read trusted code (done; research file).
2. Author plan, run one critique, record dispositions.
3. Author changes record, one author Review and state JSON; commit as records only.
4. Freeze and report. EXIT; do not wait on the shared gate.

## Future FULL plan (needs a later explicit coordinator admission event)

Preconditions to re-verify at admission, not now: logical and physical heavy holder free (1258 finished), `/tmp/ama-rpi-heavy.lock` has no holder, enough RAM and disk, no native session, cwd/branch/ignored-inclusive clean, HEAD equals the frozen head, `git fetch origin main` and use the actual current `origin/main` as the base.

If main has moved by then, plan one normal merge before the gate, prospectively recorded and committed first, then re-freeze. Do not rebase, amend or force.

Literal command (never loaded from a receipt):

```text
python3 tools/rpi-checks.py --all --base <actual-current-origin-main> --out /home/azureuser/.local/share/ama/gates/g107-final-full-r1 --jobs 2 --lock-timeout 0 < /dev/null
```

* Output path must not exist; refuse an existing path.
* The runner owns the canonical lock; no outer lock. `--lock-timeout 0` exits rather than queues.
* Console capture goes to a separate external file outside the runner's `--out` tree (for example `/home/azureuser/.local/share/ama/gates/g107-final-full-r1.console.log`); never pre-create or write inside `--out`. Capture the runner status itself: redirect without a pipeline and read `$?` at once, or with `tee` read `${PIPESTATUS[0]}`, never tee's status. Amended after critique.
* Report requested `--jobs 2` against the actual `receipt.jobs` and `test_shards`; do not weaken admission.
* Selected tier: FULL; fresh images, all maintained groups, actual disposable SQL.
* On any failure or unexpected skip: preserve all output, no overwrite, resume only with a new output under the runner's rules and a distinct admission. A `--lock-timeout 0` refusal can leave the output directory but no receipt: preserve it and start any new attempt at a new path (`--resume` needs an eligible failed receipt). Amended after critique.
* On success: keep the receipt external, no tracked or untracked write afterwards, then `git fetch origin main` and `python3 tools/rpi-checks.py --verify-receipt <out>/receipt.json --base <actual-current-origin-main>` (default full scope). A moved main means no current-pass claim.

Acceptance beyond the exit code: the two `ok` lines in the SQL log listed in the research file, with neither skipped.

## Ordering and freeze rules

* Research, plan, critique and dispositions, changes, Review records are committed before any FULL run. All later reporting is external.
* Identity: authenticated `gh api user`, repo-local noreply email, Conventional Commit, Copilot trailer, `Refs #107` and `Refs #104` only.
* No push, PR or issue mutation, no checkbox, no cleanup.

## Boundaries

Prepared is not executed. Actual MSSQL results, the receipt, independent exact-head review, hosted checks and human approvals remain open.
