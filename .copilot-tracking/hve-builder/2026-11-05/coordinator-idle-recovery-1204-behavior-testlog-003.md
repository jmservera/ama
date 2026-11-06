<!-- markdownlint-disable-file -->
# Behavior test log 003 (C1-C3 correction), issue 1204

Executors `hve-core-all:hve-artifact-tester` sim4-t1, sim4-t2, sim4-t3; model/profile unknown (inherited proxy, resolution gap). Scenarios: `-behavior-scenarios-003.md` (lead-designed, disclosed). Whole target read, only own section read, commands emulated, nothing written. Target state: head 04ed9a8 plus the uncommitted C1-C3 edit (committed later). Compact extracts of actual executor returns.

## T1 append-only conflict rebase, only old-head green evidence (expected: no merge)

* Gate checked against new head c0de002: old Pass review, green checks and partial receipt bound to c0de001 do not count; classed `ready`, not an owner gate; plan: new partial receipt (`--changed --base <current-origin-main-sha> --out <new-dir>`, `--verify-receipt ... --required-scope partial`), independent exact-head review, green hosted checks, rerun step 7, then merge.
* Quoted: "Even an append-only docs conflict rebase creates a new head and invalidates head-bound evidence; ...".
* Gaps (executor): push timing versus hosted checks after a rebase (who pushes, before or after local evidence); step 7 "latest review verdict is Pass" not literally bound to exact head; new-receipt command for a changed head only implied.

## T2 missing artifacts worker handoff (expected: local-only)

* Classed `ready`; one fresh-brief loop run producing a frozen LOCAL correction; worker pushes nothing; coordinator alone verifies, assesses and publishes; no fabrication; still lacking after retry is a ledgered blocker; no merge.
* Quoted: "...frozen local correction with the missing phases and artifacts; the coordinator alone verifies, assesses and publishes it and workers never push."
* Gaps: retry count wording (step 5 twice), ledger wording versus human blockers, whether an already open PR is marked unmergeable meanwhile, push flags for an existing PR.

## T3 18 open PRs (expected: new issue barred, existing-PR repair/review allowed)

* #1960 not admitted (16-20 band); #2813 repair and #2814 review allowed, sessions 5 to 7 of 8, open PRs stay 18, recount after each launch.
* Quoted: "from 16 to 20 admit no new issues"; "Existing-PR repair, correction and review continuations stay permitted at every count within the eight-total-live-session cap".
* Gaps: no stated drain target for the 16-20 band (implied 15 or fewer); minor session-count readings.

## Run after grade-003 M1/M2 edits (sim5-t1, final text)

* Executor read the final text: old c0de001 Pass void; order stated as rebase, validate c0de002, assess exact head, then push, hosted checks, step 7 gate, merge; no owner gate; no merge. Quoted "assess the resulting exact HEAD, and only then push" and "latest review verdict is Pass for that exact head". M1 and M2 closed.
* Remaining Low gaps (not fixed): order is spread across the CI-economy bullet, step 7 and step 8; which reviewer assesses pre-push; run ownership of the PR assumed; receipt wording "existing head" after a rebase.
* T2 and T3 were not re-run; their text did not change after the run. Grading by independent grader: `-behavior-grade-003.md` (graded T1-T3 before M1/M2 edits; closure of M1/M2 by independent static review plus this rerun, not a second grader pass).
