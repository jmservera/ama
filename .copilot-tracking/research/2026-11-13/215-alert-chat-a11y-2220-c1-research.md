# 215 C1 research: rebase and E501 correction

* Disposition: executed (focused).
* Rebased the two original commits onto origin/main 839774883 (includes #1575, #1578). No conflicts; panels.js, test_accessibility_baseline.py, the WCAG baseline and log.md carry both slices. The log keeps #232 then #215 entries in order.
* Hosted failure: E501 at src/api/checks/regulatory_ux_check.py:253 (docstring 102 columns).
* regulatory_ux_check.py is not an entry in scenario-manifest.json; all four hashed entries (workbench manifest, workbench_browser_check.py, dataset.py, test_workbench.py) match working-tree bytes, so no hash change is needed.
* test_accessibility_baseline.py is unchanged by this branch and has pre-existing E501/UP031/format findings under the strict isolated rule set; out of scope, recorded as follow-up.
* Planning Readiness: Ready.
