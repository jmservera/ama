# Changes: issue #227 browser evidence slice

* `src/api/checks/safety_screens_browser_check.py`: new browser check for both safety screens (new file).
* `src/api/README.md`: one paragraph describing the check.

Validation: check passes for both roles with pinned axe 4.10.3 (zero violations, nothing incomplete). No production code changed. Divergences: none.
