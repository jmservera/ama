# Research: PR 1635 Cycle 1 mypy no-untyped-call

* Hosted src-api job 132353513764 runs mypy in src/api with no file args (files = src, tests, checks); reproduced locally: 1 error, 254 files.
* Cause: typed setUpClass calls untyped App.__init__ (tests/test_epic149_landmarks_skip_link_focus_order.py:84).
* Planning Readiness: Ready. Disposition: executed.
