# 521 cutoff verify details

P2: python3 -m venv /tmp/venv-521-1045; /tmp/venv-521-1045/bin/pip install --no-deps -e src/core -e src/api; import zava_forward.core.resident_showcase and print __file__.
P3: from repo root, with venv python: `python -m unittest src/core/tests/test_resident_showcase.py`, and infra/tests modules test_resident_demo_secrets, test_resident_demo_deploy, test_resident_assistant, each capturing exit status directly into a status file (no pipeline tail). Missing third-party deps are recorded as blockers, not installed beyond --no-deps unless needed by pip policy.
Critique amendments: also run src/core/tests/test_resident_showcase_sql.py with ZF_TEST_MSSQL unset (renderer checks; DB checks reported unverified); require Python >=3.12; verify __file__ for both zava_forward.core and zava_forward.api; set PYTHONDONTWRITEBYTECODE=1 and clean untracked egg-info/tmp outputs so git status stays clean; az bicep build tests that cannot run offline are recorded as skipped/blocked, not passed; zero tests or setup failure means blocked.
P4: table rows: source, consumer, test, doc, with file:line from research; verdict 100 percent consistent or exact discrepancy.
