# Plan: issue #227 cross-home queue browser evidence

* [x] Phase 1: add `check_queue` and shared `scan_axe` to `src/api/checks/safety_screens_browser_check.py`.
* [x] Phase 2: README paragraph in `src/api/README.md`.
* [x] Phase 3: focused validation and RPI evidence.

Critique: executed once as self-critique. Applied: reuse the existing check file (no new tooling), keep axe optional and report SKIPPED as not a pass, assert read-only and no simulator text, do not claim WCAG acceptance. Stacked next slices (not started): #150 Fluent component proof; #155 human and AT validation.
