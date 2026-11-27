# Plan: issue 2245 live proof and post-model write retry (2026-11-27)

Tier: FULL (src change in src/core). Local commit only; no push.

1. Retry the assistant-message save in `ChatPanel._ask.finish` on `is_write_lock_busy` (bounded, 2 extra attempts), outside the in-process lock, so a generated answer is not lost to a transient lock timeout. The write is one transaction that takes the lock first, so a timeout leaves nothing to repeat. Audit writes keep their behaviour.
2. Add one focused test in `src/core/tests/test_chat_panel.py` (HybridAttributionTests): first save raises a lock-busy driver error, the reply still returns with the model answer; a persistent lock-busy still raises.
3. Run src/core chat tests, mypy, ruff in src/core.
4. Write the research note, changes record with per-criterion table, review, log and index entries.
Per-criterion proof: live probes (already run) and a deploy-less statement: the fix is not deployed (live Azure changes out of scope), so the live 500 after the fix is unproven.
