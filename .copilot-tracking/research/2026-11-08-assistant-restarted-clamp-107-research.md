# Research: issue 107 restarted-process allowance clamp coverage (M1)

Date: 2026-11-08. Session 29d9e541-c760-43f7-805e-f6ccfbb6f37e. Mode: LIGHT. Research disposition: executed. Planning Readiness: Ready.

## Start state

* Worktree `/home/azureuser/source/ama-wt/issue-107-restarted-clamp`, branch `test/assistant-restarted-clamp-107`, HEAD `2e0c676ada9264b4322224a24bc98aa3367d4f4a`, tree `08f9a4f995a0a50f58b2a319618666c8c704ada9`, ignored-inclusive clean. Equals fetched `origin/main`.
* The earlier `test/assistant-process-races-107` branch and worktree (PR 1268, merged as `4194c49ea`) are untouched.
* Issue 107 is open. Mandatory entry documents (docs index, memory, API README) were consulted for context only; memory is not evidence.

## The gap (source-qualified finding, unaltered)

Finding 1 (Medium, nonblocking) in the preserved independent functional review: the merged restart step of `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance` restarts with the stored allowance exhausted (`used_calls` 2 of 2). `Assistants.disabled()` (`src/core/src/zava_forward/core/assistants.py:611-615`) rejects `used_calls >= min(stored_calls, configured_calls)` before the claim reaches the clamp update, so the restarted processes never run the clamp. The same-process test `test_allowance_no_restart_daily_reset_or_expiry_extension` (`src/api/tests/test_assistants.py:909-920`) covers the clamp on separate connections only. A successful, partially used claim from a restarted OS process is unexercised. This is a coverage gap, not a demonstrated production defect.

## Real semantics

* Pool row `assistant_allowance(calls,tokens,expires,used_calls,reserved_tokens)` is created by the first claim from that process's configuration and never replenished by later configuration.
* `disabled()` compares against `min(stored, configured)` for calls and tokens and `pool.expires <= now` for expiry; so a larger restart configuration cannot raise the limits.
* The first call allowance of 2 with default tokens `2000000` and expiry `2099-01-01` is stored by one successful worker call (`used_calls` 1). A restarted worker with `call_allowance=1000`, `token_allowance=9000000`, `expires=2100-01-01` runs `execute` on a pending proposal: one more success (`used_calls` 2) and then an allowance denial that disables the next proposal with "allowance exhausted" (as in the merged exhausted-restart assertions).
* Each success writes one `assistant_attempts` row, so two calls mean two attempts.

## Existing helper contract (`ProcessRaces`, `assistant_process_worker.py`)

`spawn(label, tasks, wave, gate, **cfg)`, `release`, `finish`, `provider_calls`, `pool` and `snapshot` already give deterministic bounded file barriers, a minimal child environment (SQL `ZF_SQL_*` only for the MSSQL class), an append-only provider call log and synthetic `ZF_DATA`. A worker runs its task list in order and returns one boolean per task. Sequential single-task workers need no scheduling assumption, so no helper change is needed.

## Wiring

The method goes in the `ProcessRaces` mixin, a base of `SqliteUnleasedRevocation` and `MssqlUnleasedRevocation`. `SQL_SELECTORS` in `tools/rpi-checks.py` selects `test_assistant_release.MssqlUnleasedRevocation`, so the actual-MSSQL group will discover it with no runner change; `--extra-test` is not used because it runs without `ZF_TEST_MSSQL=1` and would skip.

## Limits

Provider, authority and approvals are constructed fixtures. No real model, live approval, Azure or cost evidence. Whole 107/104 stay open. SQLite results are a proxy, not SQL acceptance.
