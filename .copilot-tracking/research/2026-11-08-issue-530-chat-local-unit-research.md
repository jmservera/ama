---
title: Issue 530 chat local-unit validation research
ms.date: 2026-11-08
---

* Task: `issue-530-chat-local-unit`. Research disposition: executed. Planning Readiness: Ready.
* Source identity: branch `test/chat-local-validation-530`, HEAD and fetched `origin/main` both `f548b65f4aa31eb92a2cc9cb801130e422daed7f`, clean tree.
* Scope: refresh LOCAL UNIT evidence only for merged employee chat (#530). The remaining criterion is "Local unit, browser and SQL checks pass; live verification recorded separately". Browser, SQL and live checks are out of scope and stay unmet; #531 is live-only and excluded. Historical #759/#680 observations are not current execution evidence.

## Findings

* `src/api/README.md` and `src/README.md` give the trusted import convention: from `src/api`, `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests`, plain `python -m unittest`. No command was taken from receipts.
* Runtime origin: the global user site holds editable installs of `zava-forward-*` pointing at another checkout (`/home/azureuser/source/ama`). A new external venv (`/tmp/rpi-530-venv-1108`, no site packages, nothing installed) with the PYTHONPATH above resolves `zava_forward.core`, `.agents` and `.api` and the namespace `zava_forward` only to this worktree's `src/*/src`. Origin is therefore proven without installing anything.
* Data safety: `ZF_DATA` is `/tmp/rpi-530-synthetic-1108.json` (does not exist; synthetic). The default private path is `~/.zava-forward/data/zavaforward.json` (`core/data_paths.py`). Selected tests build `Store` from `dataset.DATA` in `tempfile.TemporaryDirectory`, with provider stubs (`Mock`, local functions). The chosen modules contain no network or Azure call sites.
* Excluded as SQL-backed (SQLite `SqlStore`/ledger, outside this tier): `api/tests/test_chat_panel.py`, `api/tests/test_chat_isolation.py` (via `test_role_matrix` `SqlStore`), `core` `test_chat_panel.StoredQuestionTests` and `SqlRosterTests`, `test_chat_privacy.SqlChatPrivacy`, `test_ai_consumption_safety` (sqlite ledger). Browser: the opt-in Chromium case in `test_chat_panel` needs `ZF_BROWSER_TESTS=1` and is not selected.
* Selected (no SQL, no browser):
  * `test_chat_model`, `test_chat_provenance` (agents): provider failure to workflow-only, admission denial makes no provider call, consumption on callback exceptions, provenance.
  * `test_chat_case_answers` (core): grounded case answers.
  * `test_chat_privacy.MemoryStoreChatPrivacy` (core): redaction, retention and audit without unnecessary personal data on the JSON store.
  * `test_chat_panel` classes `PureTests`, `OutOfScopeTests`, `ActionClaimTests`, `LabelTests`, `UnstoredAskTests`, `GroundedUnstoredTests`, `StoredRulesFallbackTests` (core): AI-suggestion label, out-of-scope refusal, no action claims, grounded and fallback answers.
  * `test_chat_widget_focus` (api): executes the shared widget and employee adapter focus lifecycle in Node `vm` with stub DOM, no browser. Node 24.21.0 is present.
* Known coverage limits: deterministic ledger/cost boundaries exist only in SQLite-ledger tests, which are excluded; this evidence covers the chat-model admission and consumption boundary only. Role/scope proof via the API matrix is SQL-backed and excluded.
* `test_chat_provenance` creates its temporary directory under `src/agents`; the plan verifies the tree stays clean afterwards.

## Evidence boundary

Synthetic stubbed unit evidence. Not real-model efficacy, human exercise, employee-site acceptance, accessibility conformance, or SQL/browser/live acceptance.
