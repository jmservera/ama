# Changes: issue #228 browser evidence slice

* `src/api/checks/procurement_screens_browser_check.py`: new check for the Package queue (Programme Manager) and Job pack (Contractor) screens.
* `src/api/README.md`: one paragraph describing the check.

Validation: the check passes for both roles with pinned axe 4.10.3 (zero violations, nothing incomplete); ruff check and format clean. No production code changed. Divergences: none.

## Correction note (2026-11-02, after independent review FAIL)

The Validation line above overstated. Corrected statement: both role runs passed locally with axe 4.10.3 on the `main` region at 1280 px only, for the Package queue (Programme Manager) and Job pack (Contractor) views, reporting zero violations and an empty incomplete list in that run. That is engineering evidence only, not WCAG or assistive-technology acceptance. The focused gate was not passed: two runs ended `BLOCKED: Global heavy-resource lock timeout`; no receipt exists.

Corrections made: the no-writes detection now flags any method not in GET, HEAD or OPTIONS (sign-in excluded, listener attached afterwards); a skipped axe scan prints PARTIAL (and fails when `ZF_AXE_REQUIRED=1`); Tab reach now compares the exact set of table regions.

Divergences: the earlier "Divergences: none" is withdrawn. Gate blocked (above); Review was a self-review, not independent.
