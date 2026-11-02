# Changes: issue #229 browser evidence slice

* `src/api/checks/data_operator_browser_check.py`: new browser check for the data steward and operator view (new file).
* `src/api/README.md`: one paragraph describing the check.

Validation: check passes with pinned axe 4.10.3 (zero violations, nothing incomplete), Tab reach of four table regions, 320px reflow, no POST requests. No production code changed. Divergences: none.
