---
title: Details 164 chat safety verification
task_slug: 164-chat-safety-1105
---

# Details

Modules (unittest, run from each package with sibling tests dirs on PYTHONPATH only as the repo guide states: core/tests and agents/tests for api):

* core: test_chat_memory test_chat_privacy test_chatthreads test_chat_panel test_chat_case_answers test_chat_case_funding_sources test_chat_dpia_record test_regulatory_chat test_ai_consumption
* agents: test_chat_eval test_chat_heldout test_chat_provenance test_chat_fixture test_chat_model test_regulatory_answers
* api: test_chat_fixture_roles test_chat_isolation test_chat_panel test_resident_chat_api test_regulatory_chat_api test_ai_boundary

Guards: any module needing MSSQL/browser is recorded as skipped, never faked. Exit code captured directly via $? into a file. Network/Docker/browser: none started.
Acceptance: all modules exit 0; skips enumerated; live LLM and human-labelled held-out gates recorded as unperformed.
