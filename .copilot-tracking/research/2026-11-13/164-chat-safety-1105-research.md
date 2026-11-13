---
title: Issue 164 chat safety verification research
task_slug: 164-chat-safety-1105
date: 2026-11-13
---

# Research: chat safety, grounding, memory and isolation unit verification

Base SHA 3b05143179f83235c5b4e80e70aad99bdc44d83f. Disposition: executed (read-only discovery). Planning Readiness: Ready.

Mandatory docs read at start (sizes only for the large ones; addendum and README searched, not read end to end): case_study_48_original.md, case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md (memory is context, not evidence).

## Candidate modules found

* src/core/tests: test_chat_memory, test_chat_privacy, test_chatthreads, test_chat_panel, test_chat_case_answers, test_chat_case_funding_sources, test_chat_dpia_record, test_regulatory_chat, test_ai_consumption
* src/agents/tests: test_chat_eval, test_chat_heldout, test_chat_provenance, test_chat_fixture, test_chat_fixture_roles, test_chat_model, test_regulatory_answers
* src/api/tests: test_chat_isolation, test_chat_panel, test_resident_chat_api, test_regulatory_chat_api, test_ai_boundary, test_chat_widget_focus

Memory-never-evidence: src/core/tests/test_chat_memory.py::test_prompt_memory_is_non_authoritative_and_never_evidence.
