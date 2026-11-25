---
title: Issue 2303 changes, revision 0000072 (2026-11-25)
---

No `src` change; evidence only. Tier: focused (documentation and evidence). The question was whether 0000072 still returns 500; it does not.

Added: `docs/reference/research/issue-2303-live-2026-11-25-r72.md`, `docs/reference/research/issue-2303-live-2026-11-25-r72/` (probe, JSON, screenshot), and the RPI artifacts for 2026-11-25 r72. The Dockerfile mutation was run and restored; no Dockerfile diff remains.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Local regression test fails when the image lacks the chat golden file or variable | Proven | mutation run failed 1 of 10, restored run passed 10 |
| Dockerfile copies `chat_golden.json` and sets `ZF_CHAT_GOLDEN` | Proven | `src/api/Dockerfile` lines 30 and 34 |
| After deployment, `GET /api/ai/report` returns 200 and the Asset and board view shows a loaded AI report | Proven on revision 0000072 (latency caveat: 78 s API, 95 s UI) | `live-r0000072.json`, `live-r0000072.png` |
| Full tier: complete local gate and external receipt | Unproven | no `src` change; the brief forbids `rpi-checks.py --all`; the coordinator owns the gate |
