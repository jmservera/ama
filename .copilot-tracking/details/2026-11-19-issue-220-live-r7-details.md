# Details: issue 220 r7

* Phase 1: add `docs/reference/research/issue-220-live-r7-stop-2026-11-19.md`; append a log entry in `docs/reference/log.md`.
* Phase 2: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 test_challenge_no_retaliation_220 test_issue_220_challenge_route test_challenges` (30 OK).
