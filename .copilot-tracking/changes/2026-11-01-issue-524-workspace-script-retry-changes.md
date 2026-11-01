# Changes: #524

* Added research, plan, changes and review artifacts under `.copilot-tracking/`.
* Added a dated entry to `docs/reference/log.md` recording the cause evidence and the pending live check.
* No source or test changes; the retry already exists from #527; release-URL reuse and the four-test suite come from later changes (#594, #538).
* Validation: `python3 -m unittest tests.test_workspace_scripts` in `src/api` passed (4 tests).
* Divergence: the request assumed implementation work; evidence showed it was already delivered.
