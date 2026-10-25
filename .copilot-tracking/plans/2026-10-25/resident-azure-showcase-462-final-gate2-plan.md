# Issue 462 final gate 2 and exact-source targeted validation plan (2026-10-25T23:28Z)

Prospective; no source edits. Candidate: committed `a15c65d8951429ec776b26db5e0c7dc3aa4f9208` plus this plan commit (candidate = resulting HEAD, recorded below); base
`origin/main` `c8d16059c0c0a22c4ffba88c6b65ac068f64accc` (already an ancestor, no merge).

Admission at 23:26Z: tree clean, 11 GiB available memory, 16 GB disk free, heavy lock free, no runner
process (the only `rpi-checks` text match was this session's own command line), output
`/tmp/ama-462-local-final-gate2` absent, only `ama-350-feedback-sql` running (untouched).

Note on prior evidence: the `after-fix-2` targeted logs record git HEAD `289c0255` because the changes
were uncommitted then. They are NOT evidence for `a15c65d8`. The opted-in SQL 18-test result is in the
`unit` and `after-fix` logs, not in `after-fix-2`.

Steps
1. Frozen worktree `/tmp/ama-462-candidate-a15c65d8`, detached at the exact commit, outside this checkout.
2. Full gate from that worktree: `python3 tools/rpi-checks.py --all --base c8d16059... --lock-timeout 0
   --out /tmp/ama-462-local-final-gate2`. Record PID and log, hand off to the coordinator's schedule.
3. After the gate exits (lock released): one sequential targeted run from a second clean detached
   worktree at the same commit, external `PYTHONPYCACHEPREFIX`, under the shared lock (`flock -n`), one
   task-owned SQL container: opted-in SQL tests (expect 18, 0 skipped), browser check (expect logout
   403, 503 and abort), image check (expect 22 PASS). Statuses captured without pipes; `git diff` hash
   and HEAD recorded before and after.
4. Official `--verify-receipt` against fresh main. A gate failure is not overridden by targeted passes.
