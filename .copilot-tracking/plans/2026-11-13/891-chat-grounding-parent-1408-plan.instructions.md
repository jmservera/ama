# 891 parent integration plan

1. Merge 1599446, 4643283, e7daa01 with --no-ff; verify child blobs equal.
2. RED then GREEN: add api end-to-end tests in src/api/tests/test_chat_panel.py (PanelTests): (a) three owner questions on ZF-4 return cited answers with answer_source and source_kind, never withheld; (b) post-dispatch provider failure with synthetic tariff settles meter_root eligible=False.
3. Validate in /tmp/venv-chatparent-1408: listed unit tests, ruff check/format, mypy on core/agents/api.
4. code-review, review file, commit with trailer, record phases. No push.
Details: tests only use synthetic fixtures; no live LLM; no banned jargon in strings.

Critique (rubber-duck, once): Revise, applied directly. Failure test must use the real evidence/meter path with a failing transport, not the fake; ZF-4 tests need a ZF-4-aware fake model; validation commands listed explicitly: core test_chat_case_answers test_chat_panel test_ai_consumption test_chat_memory test_chat_privacy; agents test_chat_model test_chat_eval; api test_chat_panel test_chat_widget_focus test_content_standard test_chat_isolation.
