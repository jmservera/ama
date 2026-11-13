# Details: 218 RAI controls unit verification (revised after critique)

* Critique verdict Revise; all four findings applied directly (discovery, offline, source safety, per-module counts).
* One command per module: cd src/P and run env -u ZF_DATA -u ZF_TEST_MSSQL PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../core/tests:../agents/tests /tmp/venv-218-1222/bin/python -m unittest discover -s tests -p test_MODULE.py -v.
* Pip steps are mandated by the brief and run as specified; any index failure is recorded, not worked around. Check git status for non-ignored src/ changes after editable installs and report.
* Each of the 11 modules needs Ran N with N greater than 0; skips parsed per module.
* Logs under /tmp/218-1222-logs; exit code saved directly after each producer; sha256 per log.
* No src/ or docs/ edits; only .copilot-tracking files committed.
* AC boundary: synthetic or scripted proof only; OQ-017, OQ-018, OD-35 human exercises are not covered.
