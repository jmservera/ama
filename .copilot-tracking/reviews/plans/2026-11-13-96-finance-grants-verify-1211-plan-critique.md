# Plan critique: 96-finance-grants-verify-1211

Executed once by rubber-duck. Verdict: Revise. Dispositions (applied directly):

1. Imports: use `PYTHONPATH=tests` for Core (bare module names) and `PYTHONPATH=tests:../core/tests:../agents/tests` for API; verify module resolution. Applied.
2. Offline: pip with `--no-index`; unset ZF_FINANCE_MSSQL, ZF_GRANT_MSSQL, ZF_GRANT_BROWSER, ZF_DATA, ZF_TEST_MSSQL. Setuptools/wheel upgrade only from local availability; otherwise record as not performed. Applied.
3. Source writes: set PYTHONDONTWRITEBYTECODE=1; remove any egg-info created under src/ after the run and confirm git status is tracking-only. Applied.
4. Coverage: add Core test_gates.py, test_taskqueues.py and API test_programme_screen.py as targeted extras only if they run cleanly; claims limited to executed modules. Applied.
5. Capture `$?` immediately per module; require Ran and OK lines. Applied.
6. AC boundaries stay as unchecked in research; passing tests grant no approval. Applied.
