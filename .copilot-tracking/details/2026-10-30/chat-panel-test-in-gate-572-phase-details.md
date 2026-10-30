---
title: Chat panel gate phase details
ms.date: 2026-10-30
---

Task: #572, `chat-panel-test-in-gate-572`.

<!-- phase: P01 -->
## P01: Integrate exact execution and accounting

<!-- task: P01-T01 -->
### P01-T01: Scoped discovery exception

Current `check_skips` allows reasons globally, with stricter integration
rules. Keep that allowlist unchanged. Add one exact ID/reason pair scoped
to `project-api` non-integration accounting. Pass group context at both
`Runner.command` and `verify_commands`; retain enumerated skips and counts.
Wrong ID/reason/group or integration execution must fail.

<!-- task: P01-T02 -->
### P01-T02: Browser execution

Use the existing selector and shared fixture paths in `required_checks` and
`Runner.browser`, after Chromium install. Environment adds only the opt-in flag.
The existing command infrastructure injects external safety startup policy,
captures verbose unittest evidence and rejects skipped integration tests.
No new browser implementation or product change.

<!-- task: P01-T03 -->
### P01-T03: Regression and inventory

Within four methods, assert exact manifest/env/suite identity and actual runner
dispatch with isolated mocks, narrow discovery accounting and strict skip
rejection, and receipt tampering (missing command/flag/selector/skip).
Update existing full-receipt fixture suite count from eight to nine.
Document required ownership and reproduction in `src/README.md` and API README.
No changes to `.github/workflows/` or web assets.

<!-- phase: P02 -->
## P02: Validate, review, commit and exact-head gate

<!-- task: P02-T01 -->
### P02-T01: Local validation

Use installed `/tmp/mv/bin/python` if suitable, keeping caches/bytecode outside
checkout. First gate unit tests and focused actual Chromium selector with
`ZF_BROWSER_TESTS=1`. Then from `src/api` caller's exact unit command and
Ruff check/format/mypy. Heavy commands hold `flock -w 600
/tmp/ama-rpi-heavy.lock`; do not interfere with foreign owners.
Actual 600-second admission timed out with exit 1 before tests started.
Tooling regressions and API lightweight lint/types passed separately;
Chromium/API units remain blocked, not failed tests or successful execution.

<!-- task: P02-T02 -->
### P02-T02: Independent Review

One fresh reviewer assesses source diff, acceptance evidence and scope.
Preserve original findings; route open work instead of repeating Review.
No human or hosted approval is inferred.
Assess the implemented source with the known heavy-validation blocker;
do not characterize the overall result as conformant while AC1/AC4 evidence
is missing.

<!-- task: P02-T03 -->
### P02-T03: Committed exact-head evidence

Resolve GitHub account to privacy-safe local git identity, commit original RPI
evidence and implementation with required trailer and `Refs #572`. Fetch main.
Use fresh external output and full `--all` gate; runner itself takes the shared
lock with `--lock-timeout 600` (avoid nested flock deadlock). Verify receipt
against fetched current origin/main. Any later commit or input/base change
invalidates receipt. Final receipt remains external; no push.
