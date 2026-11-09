# E4 owned SQL validation (appended evidence, 2026-11-09)

* Source 677429759, HEAD 287c70ecc, clean tree; src identical. Original review and adverse busy-probe evidence untouched.
* One nonqueued flock admission; script files/sql-1288-e4.sh; out dir sql-run-141828 under session files/logs-1288-e4/.
* Disposable SQL Server 2022 (16.0.4305.5), image sha256:cf8f0ab2ebe6, container removed (no label-matching container remains).
* API producer exit 0: 509 tests OK, skipped=1 (SQLite-only cross-process withdrawal); previously 217 skipped on SQLite.
* Core producer exit 0: 53 tests OK, no skips.
* Limits: not independent review; no live, AT, Azure, model run; private route off; no separate SQL login or database for the simulation store.
