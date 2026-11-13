# Details
Per module: `env -u ZF_DATA -u ZF_TEST_MSSQL /tmp/venv-79-1143/bin/python -m unittest -v <module>`; cwd src/core (PYTHONPATH=tests) or src/api (PYTHONPATH=../core/tests:../agents/tests). Parse "Ran N tests", "skipped=K", OK/FAILED. Skips reported as skips. Failures reported as-is, not fixed.

Amended after critique: API modules also test_resident_api, test_workflows; PYTHONPATH=tests:../core/tests:../agents/tests; unset every ZF_* variable; PYTHONDONTWRITEBYTECODE=1.
