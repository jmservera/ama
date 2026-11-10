---
title: Issue 891 chat call accounting changes
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109
---

## Chronology (actual UTC, 2026-11-09)

* 22:32:24 Research active. 22:35:40 research artifact written (probe at about 22:35 on unmodified source).
* 22:36 to 22:37 plan, details; one critique by an independent read-only subagent; dispositions applied to plan and details.
* 22:37:35 planning evidence committed (`e5296ed81`) before any `src/` edit.
* 22:37:57 regression tests written and run RED against unmodified `chat.py` (4 failures). The state file was moved to Implement seconds after the test file was written (recorded in the state, not backdated).
* 22:38 correction in `chat.py`, README note; green. 22:38 to 22:42 targeted validation. Source commit `da1c49a1c`.
* Correction cycles spent: 0 of 5. One formatter fix (`ruff format` of the new test helper) was applied inside the first implementation before any review and is not counted as a post-review cycle.

## Changes

* `src/agents/src/zava_forward/agents/chat.py`: new `provider_calls(envelope)`; `ChatModel` uses it. Zero calls for `disabled`, `input-refused` and `financial-held` without `meter_id`; one otherwise.
* `src/agents/tests/test_chat_model.py`: synthetic `Ledger`, `metered_model` (real core `Ai`, counted transport stub, guard stubbed to allow) and six tests: hold before reservation (meter missing, reserve held) is 0 and equals transport; hold after transport (response then hold, failure then hold) is 1; reserved hold before transport is conservatively 1; provider failure is 1; input refusal is 0; the real `ChatPanel` receipt and `chat.turn` audit detail equal the transport count for all three financial cases.
* `src/agents/README.md`: counting rule and limitations (consumption provenance section).
* Not changed: `core/ai.py`, server, store, schema, navigation, Quality, any dependency manifest, workflow or Dockerfile. No provider, model, network, Azure or spend.

## Red and green evidence (raw logs in `/home/azureuser/source/ama-demo-wt/logs-891-fresh-accounting-1109/`, not committed)

* `repro-before.log` (copy of `/tmp/891-fresh/repro-before.log`): transport 0, `ChatModel.calls` 1 for meter missing and reserve held.
* `red-test_chat_model.log`: 13 tests, 4 failures (`(1, None) != (0, None)` twice, `1 != 0` twice), exit 1.
* `green-test_chat_model.log`: 13 tests OK.

## Targeted validation (owner DEMO tier; focused, not the full gate)

| Check | Exit | Result |
| --- | --- | --- |
| agents `test_chat_model` | 0 | 13 OK (also after format: `post-format-test_chat_model.log`) |
| agents `test_chat_model test_dispatch test_worker` | 0 | 34 OK |
| agents `discover -p 'test_chat_*.py'` | 0 | 83 OK |
| agents full suite | 0 | 309 OK |
| core `test_chat_panel`, `test_ai_consumption*`, `test_chatthreads`, `test_*demo*` | 0 | OK; pattern `test_ai_registry*` matched no file (exit 5, no tests; recorded, not a pass) |
| api `test_continuity` (22), `test_ai_call_site_inventory` (6), `test_chat_panel` (55, 1 skipped: opt-in local Chromium), `test_chat_isolation` (32), `test_ai_consumption_api` (17) | 0 | OK. The first attempt failed with `ModuleNotFoundError: zava_forward.api` (log `api-continuity-before-install.log`), so `pip install -e src/api` was run (`pip-install-api.log`); no manifest change |
| `ruff check .` (agents) | 0 | All checks passed |
| `ruff format --check .` (agents) | 1 then 0 | First run flagged the new test helper (raw `ruff-format.log`); formatted; re-check 0 (`ruff-format-after.log`) |
| `mypy` (agents) | 0 | no issues in 47 files |

Not run: browser tests (skipped opt-in, no browser service), SQL, complete local gate, hosted CI. Classification: focused tier (agents adapter, tests and docs only; no workflow, dependency, deployment, permission, secret, security-control or gate change). The `test_ai_consumption_api` loopback stub is an owned localhost server inside the test, not a provider.

## AC mapping

* #891 criterion 2 (unticked): this change contributes one bounded part, per-call accounting of the chat adapter; the token, cost, privacy, retention and refusal conjunction is NOT proven here. Criteria 1, 3, 4, 5 and 6 are already delivered and unchanged; default deny, switch, disclaimer and fallback tests re-ran green. Refs #891 only.

## Remaining limitations

* Over-count remains for a `dispatch_check` hold after reservation and for a prompt-output guard denial (the envelope cannot distinguish them). An exact fix needs a transport marker in `core/ai.py`, a shared path requiring coordinator serialization; not done.
* The zero-call rule depends on the core `Ai.evidence` envelope contract (`meter_id` set right after `reserve`, before the transport).
* No live observation, real provider, deployment or cost evidence is produced.
