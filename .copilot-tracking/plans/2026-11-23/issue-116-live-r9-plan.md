# Plan 2026-11-23, issue 116 live r9

1. Count the UTF-8 bytes of a string `user` plus `system` in `approved_payload` (src/core/src/zava_forward/core/ai.py), so the shared allowlist refuses oversize before the verifier and the protection hold.
2. Add two tests in src/core/tests/test_ai_input_bounds.py.
3. Run core bounds, spy and dispatch-marker suites, api boundary inventories, then mypy and ruff in src/core.
4. Evidence note docs/reference/research/issue-116-live-r9-evidence-2026-11-23.md, index row, log entry, changes record with per-criterion table.
5. One local commit, no push.
