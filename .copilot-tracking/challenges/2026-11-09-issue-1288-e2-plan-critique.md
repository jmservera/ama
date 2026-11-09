---
title: Issue 1288 E2 plan critique
ms.date: 2026-11-09
---

One independent read-only critique (rubber-duck agent) of the E2 research, plan and details, 2026-11-09T10:25Z, before any source edit. Verdict: Revise. Applied as amendment A1 in the plan. No repeat critique.

1. High, worker bypass: `src/agents/src/zava_forward/agents/dispatch.py:231` builds and sends captured snapshots in a separate thread without the marker. Fix the worker boundary and test `handle` and redelivery against a real `Ai`. Disposition: accepted (A1.1).
2. High, untagged chat and direct calls: `src/core/src/zava_forward/core/chat_panel.py:607` sends free text and history. Define the boundary for unclassifiable text without inferring provenance. Disposition: partly accepted; no sensor path into chat was found, free text is disclosed as residual (A1.2).
3. Medium, mutable cursor ordering: `assistants.py:1337` rewrites `dispatched` on retry. Use immutable ordering or restart/back off. Disposition: accepted, immutable `id` walk (A1.3).
4. Medium, forecast still writes release state: `_due` reaches `release_reference` (`assistants.py:706`) and `assistant_release.py:69` can revoke and append events. Add a non-mutating assessment and compare release rows and events. Disposition: accepted (A1.4).
5. Medium, suspension test can pass vacuously: the details placed the suspension hook after the new refusal point. Separate old-race reproduction from the early-refusal test and add hook-reached and positive-control assertions. Disposition: accepted (A1.5).
