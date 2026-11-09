---
title: Issue 530 actual SQL and employee browser validation preparation details
ms.date: 2026-11-08
---

## Future FULL admission (NOT ADMITTED; do not run now)

Preconditions at admission time: owner/coordinator grants the heavy window; the canonical lock is free, checked only by the runner itself with `--lock-timeout 0` (the runner default waits 600 seconds, so it must be set explicitly), and contention stops the run without polling or queueing; `git fetch origin main` and re-pin the base, then recompute every blob id below; HEAD is ignored-clean; the worktree path, namespace and import origin are proven to be this worktree (not another); disk and memory are admitted; Docker is available.

```text
python3 tools/rpi-checks.py --all --jobs 1 --lock-timeout 0 --base <fresh-origin-main-sha> \
  --out <new-external-dir> < /dev/null
python3 tools/rpi-checks.py --verify-receipt <out>/receipt.json --base <current-origin-main-sha> < /dev/null
```

One attached bounded invocation, no resume or manual background. The complete gate covers all 17 groups: `preflight`, five `project-*`, `namespace`, `static`, `infra`, `migration`, `browser`, `mssql`, four `image-*`, `logo-0600`. Expected coverage from existing tests: actual MSSQL chat thread storage (`test_mssqlstore.MssqlChatThreads`), the existing SQL release and ledger classes, three employee acceptance Chromium regressions, the chat-panel Chromium test, design-system browser check (no axe argument), and pinned axe on the case-journey and regulatory checks. Also actual-MSSQL chat-memory migration coverage via `MssqlLedgerMigration.test_populated_chat_memory_failure_rolls_back_and_retries` (storage migration only; it does not close the isolation, privacy or cost gaps).

## Not covered by the maintained gate (remaining gaps, named, not fabricated)

* Dedicated employee chat dialog/keyboard/axe journey: `python -m checks.employee_chat_browser_check --axe <pinned axe> --out <new dir>` from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests` (command from the trusted README, source blob `8d4a0d179c81`). Not in the browser group and not expressible through `--extra-test`.
* Actual MSSQL chat role projection, chat isolation, chat privacy and finite cost-ledger behaviour: only the SQLite proxies exist. Smallest prospective separate scope: new reviewed MSSQL-gated test classes plus `SQL_SELECTORS`, runner and runner-test updates, with critique and review; not done now.

## Source identities at 0f05e9aa (re-derive at admission)

`tools/rpi-checks.py` `4ead23d7543f`; `src/api/tests/test_mssqlstore.py` `4de768732547`; `src/core/tests/test_chatthreads.py` `642156469fbf`; `src/api/checks/employee_chat_browser_check.py` `8d4a0d179c81`; `src/api/checks/employee_acceptance_check.py` `1620a6dc4c11`; `src/api/tests/test_chat_isolation.py` `c3ee1168b246`; `src/core/tests/test_chat_privacy.py` `14b542c0e36a`.

## Review route

Independent exact-head assessment, hosted CI and human approvals remain required. A new PR targets Main with `Refs #530` only, never a closing keyword, after all of the above. Live, human and approval exclusions stay unmet.

## Critique

[.copilot-tracking/challenges/2026-11-08-issue-530-sql-browser-prep-critique.md](../challenges/2026-11-08-issue-530-sql-browser-prep-critique.md)
