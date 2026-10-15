# Changes: issue #114

* mvp/zavaforward_mvp/ledger.py, store.py: per-year digests and verification, `--seal-years`/`--by-year`.
* mvp/zavaforward_mvp/loadcheck.py: new load harness.
* mvp/zavaforward_mvp/recovery.py: new erasure, register, backup, reapply.
* mvp/tests/test_recovery.py: 7 tests. mvp/README.md: evidence and open items.
* Validation: full mvp suite 478 tests OK (85 skipped, need SQL Server). Local load run, 60,000 synthetic homes, 30 s: list p95 0.28 s, detail 0.30 s, write 0.33 s, 0 errors.
* Divergence: none. Knowledge base files unchanged, so no index or log entry.
