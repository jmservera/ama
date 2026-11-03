# Changes: demo authority 521 r1

* Shared cap moved to 2028-01-01T00:00:00Z.
* Tests updated in core, infra and api (80 core tests, 33 infra, 47 api passed; 27 SQL Server tests skipped, no server).
* Docs: infra README extension section and updated steps, API README, KB index, log entry.
* Divergence: none. Not run: SQL Server tests, gate, full suites, benchmarks. Ruff on infra tests shows pre-existing findings (unchanged); ruff on the other changed files has none from this change; mypy clean on resident_showcase.py.
* Unmet: criterion 1 pending independent exact-head review; criterion 4 (live apply) unmet.
