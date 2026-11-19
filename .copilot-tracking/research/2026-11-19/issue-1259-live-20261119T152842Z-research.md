---
title: Issue 1259 research (live worker)
---

Task: first unticked criterion of #1259 buildable for the demo is "Add regular-file and dangling-link regressions ... demonstrate failure before fix".
Disposition: executed (source and test read; pre-fix mutation run).

Findings: the fix and regressions already exist on main (commit cd687abad, `UnusableArchivePathTests` in `src/core/tests/test_ranking_publication_runner.py`; guard `_names` in `ranking_publication.py`). Only the "failure before fix" demonstration was unrecorded.
Planning Readiness: Ready. No source change needed; criterion 5 (hosted checks, independent assessment, FULL receipt) needs humans/hosted CI.
