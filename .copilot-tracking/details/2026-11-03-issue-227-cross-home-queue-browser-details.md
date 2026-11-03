# Details: issue #227 cross-home queue browser evidence

* Phase 1: before opening a home, locate the "Hazard referrals across this page of homes" panel; assert the columns (aware at, source, destination, sent, received, accepted, state, follow-up, pause status), ZF-1 H-1..H-6 listed (SA-007), pending and unsent text, "not a portfolio total", no button/form/input/select/textarea, no simulator wording in main, labelled focusable region reached by Tab, optional pinned axe scan.
* Phase 2: one README paragraph.
* Validation: ruff check, mypy (--cache-dir=/tmp/mypy-227), the browser check itself, tests.test_safety_screens.
