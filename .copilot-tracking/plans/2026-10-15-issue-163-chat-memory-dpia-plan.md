# Issue 163 plan

1. `mvp/zavaforward_mvp/chat_privacy.py`: data map, reference-gated decision, retention unset, rights locate/export/erase, redaction, diagnostic filter, portable SQL.
2. `mvp/tests/test_chat_privacy.py`.
3. `docs/reference/research/chat-memory-dpia.md`, index row, log entry.
4. Validate with the full mvp unittest suite; PR with `Refs #163`.

Critique (single pass): memory refuses special-category text rather than masking; no retention before approval; erasure returns counts only for the ledger. No conflicts with confirmed decisions.
