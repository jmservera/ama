---
title: Issue 530 C5 actual chat SQL and employee browser execution details
ms.date: 2026-11-08
---

## Runtime

* Root `/home/azureuser/.local/share/ama/gates/g530-c5` (new, root filesystem, short path for Chromium sockets): `snap/` (git archive of HEAD), `venv/`, `tmp/`, `home/`, `cache/`, `safety/`, `logs/`, `out/`. Env: `HOME`, `TMPDIR`, `PYTHONDONTWRITEBYTECODE`, `PYTHONPYCACHEPREFIX`, `PIP_CACHE_DIR` inside the root; `ZF_DATA` points at `unused-data` inside the root (never the default store). Browser binaries: `PLAYWRIGHT_BROWSERS_PATH` set to the root only if the existing cache lacks the needed revision (install then, log separately).
* Lock: one `flock -n` holder process (`flock -n /tmp/ama-rpi-heavy.lock bash <script>`) covers setup, both integrations and cleanup; the script is an execution wrapper kept in the external root, not a repository file.

## Selectors (from `src/api`, PYTHONPATH `<snap>/src/api/tests:<snap>/src/core/tests:<snap>/src/agents/tests`)

* `python -m unittest -v test_mssqlstore.MssqlChatPrivacy test_mssqlstore.MssqlChatRoleProjection test_mssqlstore.MssqlChatDemoMeter`
* Acceptance: 21 verbose `... ok` lines with unique ids (13, 4, 4), `Ran 21 tests`, `OK`, zero `skipped`, exit 0. Compare ids with `SQL_CHAT_REQUIRED_TESTS` from the trusted runner source.

## SQL container

* Image `mcr.microsoft.com/mssql/server:2022-latest` (local, id cf8f0ab2ebe6), `docker run -d --label ama.rpi.owner=<token> --memory=3g --cpus=2 --publish=127.0.0.1::1433`, `MSSQL_MEMORY_LIMIT_MB=2048`, password in env only and never logged. Verify id, label, running state and a loopback-only port mapping from `docker inspect`, then `SELECT 1` and `CREATE DATABASE rpi_disposable` through the installed driver. Remove only the exact container id before the browser step.

## Browser

* Fetch axe 4.10.3 from the maintained URL (cdnjs, hash-verified `880970c0...8bb`, no other egress), run the maintained entry with `PYTHONPATH=<safety>:<tests paths>`, `--out <out>/employee-chat`. Evidence: console, `PASS employee chat:` line, `axe-results.json` with three states, zero violations, positive passes; screenshots/reports retained if the checker writes them.

## Origin proof

* `zava_forward.core/agents/api` and `checker`/test modules resolve under `<snap>` or the venv site-packages, with the installed wheels' contents compared to snapshot blobs; versions via `pip list`.

## Review route

* Authored Review, evidence commit with repository-local noreply identity, Copilot trailer, `Refs #530`. No push or PR. After the last commit the worktree must be ignored-clean.

## Critique amendments (F1-F7 applied before execution)

* F1: every suite and checker command prepends `<root>/safety` (runner-identical `sitecustomize` audit hook refusing non-loopback `socket.connect`) to PYTHONPATH; env mirrors the runner: `PYTHONNOUSERSITE=1`, `ZF_STORE=json`, `ZF_DATA=<root>/unused-data/zavaforward.json` (a file path, never created or read), SQL variables as in Research, `HOME`, `TMPDIR`, `XDG_CACHE_HOME`, `AZURE_CONFIG_DIR` inside the root. Prove the hook loads by a refused non-loopback connect before testing.
* F2: tests, checker and application packages must resolve as follows: `test_mssqlstore`, `employee_chat_browser_check` and other test modules under `<snap>/src/*/tests|checks`; `zava_forward.*` from the non-editable venv site-packages, with file content hashes compared to the snapshot blobs. Any other origin stops the run.
* F3: native Chromium egress cannot be enforced beyond the maintained boundary (the Python audit hook and the checker's abort of every non-base request; `unshare -rn` is unavailable to this user). This is the same boundary the maintained runner uses and is recorded as a limitation, not claimed as stronger. Chromium comes from the existing Playwright cache only if its revision matches the installed Playwright 1.64.0 (checked with the installed Playwright before use); a missing revision stops the run (no download of browsers), and axe is the single permitted external fetch, hash-verified.
* F4: the lock is taken with `flock -n -o` (close-on-exec for children), the wrapper traps EXIT/INT/TERM to remove only the exact owned container and terminate only owned child process groups, and release is verified with a non-blocking re-acquire after exit.
* F5: `owned_sql` conditions are replicated exactly (id equality, label, running, exactly one binding on 127.0.0.1 with a numeric port), re-inspected after readiness and immediately before the tests, with the runner's `ACCEPT_EULA=Y`, `MSSQL_PID=Developer`, readiness retry of up to 60 attempts, and the password only in the environment and scrubbed from logs.
* F6: result checks follow the runner: per-test region `ok` for each of the 21 ids, `Ran 21 tests`, `OK`, no skip lines. Browser: ordered exact state list, integer positive passes, empty violations, no "skipped" in log or JSON.
* F7: the execution HEAD and tree are those of the commit that adds these planning records (recorded in the changes record); drift from it, or of Main from 0f05e9aa, stops the run. Source identity is the git tree of that commit, and the snapshot contains the same tree.
