# Details: 96-finance-grants-verify-1211

Core run: cd src/core/tests-dir parent `src/core`, `python -m unittest -v tests.<module>` per module using PYTHONPATH unset; API run from `src/api` with `PYTHONPATH=../core/tests:../agents/tests` (documented repo convention, not mvp).
Modules: see research artifact. Per-module capture: Ran N, OK, skipped=K, producer exit code via `$?` (no pipe masking; output redirected to log file, then sha256).
Skips: MSSQL and browser skips recorded literally from log, never converted to passes.
Risk: an import failure; record verbatim as blocker, do not edit src/.
