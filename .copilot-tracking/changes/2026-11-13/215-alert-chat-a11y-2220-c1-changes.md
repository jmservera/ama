# 215 C1 changes

* Rebased branch onto origin/main 839774883 (no conflicts).
* src/api/checks/regulatory_ux_check.py: docstring shortened to fix E501.
* Ruff check and format pass on regulatory_ux_check.py and test_regulatory_a11y_cues.py. test_accessibility_baseline.py has pre-existing strict-rule findings from main (untouched).
* Focused unittest run: 39 tests OK (full src/api discover was not completed; stopped as too slow). Scenario manifest hashes verified.
* Not pushed; the coordinator reviews and pushes.
