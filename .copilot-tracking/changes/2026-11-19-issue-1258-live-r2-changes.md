# Changes: issue 1258 live rerun (2026-11-19)

Tier: FOCUSED. No `src` file changed; `rpi-checks.py --all` not run; nothing pushed.

## Files

* `docs/reference/research/issue-1258-live-r4-2026-11-19.md` and folder `issue-1258-live-r4-2026-11-19/`: criteria proof and raw outputs.
* `docs/reference/README.md`, `docs/reference/log.md`: index row and log entry.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Sync new archive ancestors before confirming | Proven (real ext4 order) | `strace-order.txt` |
| 2 Post-link sync failure keeps record, `committed_unconfirmed` | Proven by tests (mocked); kernel injection proven in run 3 | 110 tests OK |
| 3 Syscall-order regression, red before fix | Proven offline; pre-fix raw output not retained | tests |
| 4 Retry, private stage, audit, path-free 409/503, original date | Proven offline | 110 tests OK |
| 5 Original RPI, FULL receipt, independent exact-head review, hosted checks | Unproven; not provable for the demo | needs `--all`, a reviewer and a pushed head |
