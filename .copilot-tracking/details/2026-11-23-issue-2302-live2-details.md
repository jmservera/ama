---
title: Details for #2302 (second live run)
date: 2026-11-23
---

Phase 2: replace the numeric-only `value === 0` check in `cost()` with a test that also matches strings of the form `0`, `0.0`, `0.000000`, `-0` after trim. Phase 3 commands: `python3 -m unittest test_overview_ai_economics_100` in `src/api`, plus `test_accessibility_baseline` and `test_content_standard`.
