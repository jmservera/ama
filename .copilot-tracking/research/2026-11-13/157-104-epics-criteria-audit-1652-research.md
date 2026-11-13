<!-- markdownlint-disable-file -->
# Research: #157 and #104 software-provable criteria audit

Research disposition: executed. Planning Readiness: Ready.

## Scope

* #157: "No memory is used as evidence for a controlled decision"; "Chat consumption is bounded and reported before activation ... (BRD AC-103)".
* #104: "AI never approves, executes, ranks or mutates controlled records"; "#432 is complete, or its gap is recorded ..."; "No registered AI capability is enabled beyond the exercise without finite, owner-approved call, token and budget limits and an owned alert (BRD NFR-012)".
* Base: worktree HEAD `3ffb8c0e7`; `origin/main` is `dad57ef4f`, which differs only in #131 tenure files, none relevant here.

## Starting evidence (files to read and test)

* Memory: `src/core/src/zava_forward/core/chatthreads.py` (`_clean_evidence` rejects `CM-` ids), `chat_panel.py` (`memory_used=False` in receipts), `tests/test_chat_memory.py`, `test_chatthreads.py`.
* Chat bounds: `chat_panel.py` (`MAX_INPUT_CHARS`, `MAX_HISTORY_CHARS`, `LIMIT_REACHED`, workflow-only fallback), `chat_demo_meter.py`, `ai_consumption.py`, `regulatory_usage.py`, tests `test_chat_panel.py`, `test_ai_consumption*.py`.
* AI authority: `core/ai.py`, `ai_tasks.py` (review, proposals), `agents` tests for ranking and Proposed state.
* Cost: `ai_consumption.py`, `agents/candidate_comparison.py`, `paired_trial.py`, `docs/reference/resources/ai-tokenomics.md`.

Detailed findings are recorded in the changes artifact.
