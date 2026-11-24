---
title: Issue 2303 r67 changes
---

No source edits. Added docs/reference/research/issue-2303-live-2026-11-24-r67.md, live-r0000067.json and live-r0000067.png. Tier: focused (no src change). Refs #2303.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| Local regression test fails when image lacks chat golden or variable | Proven | mutation: FAILED (failures=1); restored: 10 OK |
| Dockerfile copies chat_golden.json and sets ZF_CHAT_GOLDEN | Proven | src/api/Dockerfile lines 30, 34 |
| After deployment GET /api/ai/report 200 and Asset and board view loaded | Proven on 0000067 (94 to 105 s latency caveat) | 200 with consumption; no failure text |
| Full tier gate and external receipt | Unproven | no src change; coordinator owns gate |
