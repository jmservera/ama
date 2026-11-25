---
title: Issue 2303 changes, revision 0000069 (2026-11-25)
---

No `src` change; evidence only. Tier: focused (documentation and evidence).

Added: `docs/reference/research/issue-2303-live-2026-11-25-r69.md`, `docs/reference/research/issue-2303-live-2026-11-25/` (probe, JSON, screenshot), and the RPI artifacts for 2026-11-25. Dockerfile mutation was run and restored; no Dockerfile diff remains.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Local regression test fails when the image lacks the chat golden file or variable | Proven | mutation run failed 1 of 10, restored run passed 10 |
| Dockerfile copies `chat_golden.json` and sets `ZF_CHAT_GOLDEN` | Proven | `src/api/Dockerfile` lines 30 and 34 |
| After deployment, `GET /api/ai/report` returns 200 and the Asset and board view shows a loaded AI report | Proven on revision 0000069 (latency caveat: 105 s API, 126 s UI) | `live-r0000069.json`, `live-r0000069.png` |
| Full tier: complete local gate and external receipt | Unproven | no `src` change; the brief forbids `rpi-checks.py --all`; the coordinator owns the gate |
