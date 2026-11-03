# Research: issue #227 cross-home queue browser evidence

Disposition: reused existing evidence; one focused check of merged work.

* Merged: #653 per-home screens, #776 per-home browser and axe check, #806 cross-home referral table (unit tested only; its review said "not browser-run").
* Unmet criteria after #806: browser proof of the cross-home table (criterion 1), no-simulator proof (criterion 6), WCAG/AT acceptance (#151, #155), Fluent component proof (#150).
* Smallest slice: extend `src/api/checks/safety_screens_browser_check.py` to open the cross-home table. No production code change.

Planning Readiness: Ready.
