# Research: 149 UX parent C1 fix

Disposition: executed. Planning Readiness: Ready.

Findings (review 149-ux-parent-independent-review-1426):

* F-1: programme_paging_browser_check.py presses Enter after the retry reaches page 2, but syncPager moves focus to programme-prev, so Enter navigates back. Fix: assert Next disabled, Previous enabled, focus on programme-prev, no request; remove the stale Enter. Later Tab to Reset still works because disabled Next is skipped.
* F-2: tautological check(..., True) at the end of the added block; the expect calls already prove it. Remove.
* F-3: HELD_CHECK_UNREADABLE lacks Owner:. Add "Owner: you, the signed-in reviewer." (matches 400 convention, same actor choosing a file) and extend test_content_standard.
* Manifest hashes cover workbench-manifest.json, workbench_browser_check.py, dataset.py, test_workbench.py only; none are touched, so no digest change expected (verified by tests).
* Chromium and the heavy lock are out of scope; verification by unit tests, ruff, mypy, AST.
