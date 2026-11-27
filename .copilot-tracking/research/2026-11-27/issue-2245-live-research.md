# Research: issue 2245 employee chat 500 and no generative answer

Date: 2026-11-27 (run 20261127T024556Z). Research disposition: executed (fresh live probes; notes of 2026-11-22 to 2026-11-27T01 reused for history).

Scope: re-prove each Expected criterion of the issue on the live demo API with recorded evidence. Findings are appended below once probes finish.

Planning Readiness: Ready.

Findings (live, revision ca-cutover-test-demo-api--0000130, created 2026-11-27T02:38Z): 6 of 8 direct thread creates at 200, 1 at 503 `sql-write-lock-busy` (the deliberate retryable status), plus 2 of 5 ask-probe creates at 503. One ask returned HTTP 500: log line `http-error POST /api/chat/threads/<id>/ask status=500 exc=ProgrammingError ... cause=sql-write-lock-busy` at 02:51:29Z, 26 s after `AI_USAGE ... calls=1 tokens=1165 outcome=returned` at 02:51:03Z. So a model call was made and paid, the answer was then lost because the write that saves it timed out on the SQL write lock (15 s) and the ask route deliberately keeps the 500 path (a failed POST may follow a committed step). This reproduces the issue symptom (spent call, no answer, 500) and is a real defect in `chat_panel.ChatPanel._ask.finish`: the assistant-message write is a single transaction that takes the lock first, so a lock timeout leaves nothing written and a bounded retry is safe.
Evidence: docs/reference/research/issue-2245-live-20261127T024556Z.md.
