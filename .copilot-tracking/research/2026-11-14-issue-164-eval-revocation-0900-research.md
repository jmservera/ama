---
title: Issue 164 revocation and effort research
description: Issue 164 revocation and effort research
ms.date: 2026-11-14
---

## Findings

* The named `src/core/.../chat_eval.py` does not exist. The harness is `src/agents/src/zava_forward/agents/chat_eval.py` (retired-core boundary: core must not import agents). Work and tests were placed in `src/agents`; `ai_eval.py` and `src/api/` untouched.
* Golden file already has mid-thread revocation scenarios (permission-*, stale history, memory persists across permission change) and a not-manufactured approval/consent scenario.
* Gap: no explicit report section for chat-only failures and complete review effort apart from single-turn results; required scenarios were not named, so deletion would go unnoticed.
* Planning readiness: Ready. Research disposition: executed.
