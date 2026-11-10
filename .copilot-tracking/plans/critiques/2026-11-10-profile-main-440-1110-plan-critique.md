# Profile-main checkpoint plan critique (issue 440, 2026-11-10)

Executed once on the final candidate plan and details by an independent read-only reviewer (`rubber-duck` subagent, model per runtime default). Verdict: Approve-with-changes. No user decision required; no finding conflicts with a confirmed decision. Never repeated for this task.

| # | Severity | Finding | Direct disposition |
| --- | --- | --- | --- |
| 1 | High | Test provenance unproven: system-python attempt could import another worktree's packages | Applied: module file paths recorded for every attempt; a result outside this worktree is classified blocked, not current-main proof |
| 2 | High | Attempt B unconditional and repeats both selectors | Applied: B only after an eligible dependency or wrong-path failure, only for affected selectors; earlier outcomes retained |
| 3 | Medium | Restore did not select the private interpreter | Applied: `/tmp/ama-440-profile-venv-1110/bin/python -m pip`, venv interpreter for later checks |
| 4 | Medium | Browser admission threshold and timeout undefined | Applied: no lock holder, `MemAvailable` at least 1.5 GiB (engineering threshold, not a repository rule), cached browser loads under pinned Playwright, `timeout 900`; else blocked |
| 5 | Medium | Current-main identity omits `origin/main` observation | Applied: local tracking ref value and observation time recorded; remote currency claimed only as of that fetch |

Plan, details and research updated before `plan-done`.
