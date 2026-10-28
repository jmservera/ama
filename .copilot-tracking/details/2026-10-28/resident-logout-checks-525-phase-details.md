---
title: Resident logout check correction details
ms.date: 2026-10-28
---

Task: PR-525-PRRT_kwDOUU8JX86xVDWZ.

## P01: Correct and validate checks

### P01-T01

Capture token and `/demo/session` session_id before either normal logout or
intercepted failure. Validate HTTP 200, signed_in exactly true and a nonempty
string session_id, then view HTTP 200 with that fence. A shared helper checks
the retained cookie value, requires exactly HTTP 401 for
`/demo/view` with `X-Resident-Session`, and checks a 200 `/demo/session` response
for present fields with exactly false signed_in and null session_id. Strengthen existing isolated replay
with the captured fence. Keep independent Bob-session unaffected assertion.

### P01-T02

Add up to four unit tests in the existing browser-fixture test module. Mock a
browser context's cookies and API responses to verify success and rejection of
an authenticated view, wrong retained cookie and invalid session status.
Assert exact request fence arguments. Within four methods use subtests for
view statuses 200/409/503, non-200 session status, true/missing signed_in and
nonnull/missing session_id. Keep
Playwright imports type-only. Update API browser-check documentation.

### P01-T03

Create a separate external venv because the inspected prior venv has stale
editable imports. Install existing pinned project extras, not new dependencies.
Run relevant resident demo/check/chat/assistant units in one unittest command.
Run Ruff with line limit 100 and explicit E501 selection, plus mypy for changed
Python files. Run actual assistant (SQLite agenda) and account browser checks.
Run demo browser with a new memory/CPU-bounded loopback SQL Server and random
in-memory fake password; never inspect a foreign SQL container or stored secrets.
These drivers have no `--mssql`; the demo driver itself is always SQL-backed.
Hold `/tmp/ama-rpi-heavy.lock` with flock -n for heavy execution. Retry admission
briefly only within a 40-minute monotonic deadline; never wait indefinitely.

## P02: Review and publication

### P02-T01

Fresh independent reviewer reads this correction's diff, research, plan, critique
and actual validation evidence. One Review; material open findings route later,
not into an unrecorded repeat Review.

### P02-T02

Resolve GitHub id/login for local privacy-safe author/committer identity. Commit
with Conventional Commit and required Co-authored-by trailer. Repository policy
requires an external exact-head full receipt before publication; that runner
executes az offline Bicep commands. Caller forbids all az, not merely deployment.
Do not invoke az or fabricate a passing receipt. Record that blocker if unresolved.

### P02-T03

If publication is eligible, fetch main, verify receipt at current origin/main,
obtain independent exact-head assessment, normal push only, and reply/resolve
PRRT_kwDOUU8JX86xVDWZ. PR body must retain Refs #520 and no closing keyword.
If blocked, do not claim remote correction or thread resolution.
