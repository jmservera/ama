# Changes: issue #228 browser evidence slice

* `src/api/checks/procurement_screens_browser_check.py`: new check for the Package queue (Programme Manager) and Job pack (Contractor) screens.
* `src/api/README.md`: one paragraph describing the check.

Validation: the check passes for both roles with pinned axe 4.10.3 (zero violations, nothing incomplete); ruff check and format clean. No production code changed. Divergences: none.
