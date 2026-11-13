# Independent critique (rubber-duck) - verdict: changes required; dispositions below

Executed once. Findings and dispositions:
* API PYTHONPATH omitted `tests` - accepted: PYTHONPATH=tests:../core/tests:../agents/tests.
* Add test_resident_api.py and test_workflows.py - accepted.
* Env isolation - accepted: unset all ZF_* variables (incl. ZF_BROWSER_TESTS, ZF_RESIDENT_MSSQL, ZF_RESIDENT_AZURE_TEST), PYTHONDONTWRITEBYTECODE=1.
* pip upgrade network - brief mandates the upgrade; tolerated, failure recorded, not blocking.
* Loopback HTTP - accepted as local, not external network.
* Editable install artifacts - verify git status clean (ignored egg-info removed) before commit.
* test_sqlqueues not wholly MSSQL-gated - accepted; skips reported as observed.
* Node availability - recorded if relevant.
