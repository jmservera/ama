---
title: Issue 440 live checkpoint research
description: Opening research record for the two unticked criteria of issue 440
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Live Azure authorised (rg `ama`, cap USD 700, no drills, no Key Vault rotation, no production change); this task needs no Azure mutation. Research disposition: executed (reuse of prior checkpoint records plus live issue/epic state).

Unticked criteria: (1) triage confirmed findings into deduplicated issue drafts and decide epic gating plus per-epic verdicts; (2) coordinator agent change as Major HVE Builder behaviour change, static review and behaviour testing, or justified non-applicability.

Findings are appended below as probes complete.

* Confirmed candidate findings: live `/api/time/status` 500 (ProgrammingError, reproduced); `check-legacy-references.py` 11 violations at head (reproduced); `ChatIsolation.turn` unreferenced (static); AI golden path fragility (static). Existing owners cover the rest (#350, #1837, #1258, #1259, #1840, #1844, #1274, #1397, #146).
* Epic state read from sub-issue lists: 14 continue (#113 conditional), 2 fix (#81, #195), 0 pivot proposed.
* Primary evidence note: `docs/reference/research/stabilization-checkpoint-triage-440-live-2026-11-18.md`; raw probes in `.copilot-tracking/evidence/2026-11-18/issue-440-live/`.
* Criterion 2: coordinator changed materially by #1903 (2026-11-18), #1843, #1821; HVE Builder review mode with behaviour testing delegated and recorded under `.copilot-tracking/hve-builder/2026-11-18/issue-440-live-*`.

Planning Readiness: Ready. Tier FOCUSED; no src change.
