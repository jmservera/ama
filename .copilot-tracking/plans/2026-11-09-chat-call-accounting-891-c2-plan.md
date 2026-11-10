---
title: Issue 891 chat call accounting C2 plan
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c2
---

## Objective and scope

* Fix the test-isolation defect and the "upper bound" terminology. No production source change. No receipt provenance, global counter, provider restriction, chat_panel, activation or gate change. Focused tier. Criterion 2 of #891 stays unmet; Refs #891 only.
* Files: `src/core/tests/test_ai_dispatch_marker.py`, `src/agents/README.md`, and honest wording notes in the C2 records. C1 records are not edited (a C2 note records the correction).

## Phases

1. Red: add regressions first. (a) After this TestCase runs (via `unittest.TextTestRunner` on the loaded suite), `data_protection.dispatch_hold` is the original object. (b) Same interpreter: marker module then `test_ai_input_bounds` style guard/dispatch module (a subprocess running `unittest` on marker then `test_data_protection`/`test_ai_consumption`) passes. Red against the current code: the restored-original assertion fails.
2. Fix: guard-denial case uses a scoped `with mock.patch(...)` around only that attempt; the setUp loop is replaced by a per-case fresh `Ai`/ledger factory, not repeated `setUp`.
3. Small pins: opener `.open` raising (fence withdrawal) counts 1; `TimeoutError` and `HTTPError` count 1. Stubs only.
4. Wording: README and docstring say unverified legacy assumption, not an upper bound, exact count or billing estimate.
5. Checks: core marker, guard (`test_data_protection`), `test_ai_consumption*`, `test_ai_input_bounds`; agents chat and full; ruff, format, mypy.
