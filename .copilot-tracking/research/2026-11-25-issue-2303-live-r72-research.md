---
title: Issue 2303 research, revision 0000072 (2026-11-25)
---

Disposition: executed. Planning Readiness: Ready.

Findings: `src/api/Dockerfile` copies `chat_golden.json` (line 30) and sets `ZF_CHAT_GOLDEN` (line 34); `test_cutover_audit` covers it. Revision 0000072 (healthy, 100% traffic) returned 200 on `/api/ai/report` in 78 s; the Asset and board view rendered without the failure text. Full note: `docs/reference/research/issue-2303-live-2026-11-25-r72.md`.

Decision: evidence only; no `src` change, so focused tier.
