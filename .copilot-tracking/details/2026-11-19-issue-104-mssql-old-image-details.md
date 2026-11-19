# Details

Phase 1: in src/api/tests/test_assistant_restart_non_replenishment.py import `MssqlFixture`, `os`, add the subclass with `unittest.skipUnless(os.environ.get("ZF_TEST_MSSQL") == "1", ...)`.
Phase 2: `docker run` mssql 2022 bound to 127.0.0.1:1433; ZF_SQL_AUTH=password, ZF_SQL_TRUST_CERT=1; run `python3 -m unittest test_assistant_restart_non_replenishment` from src/api.
