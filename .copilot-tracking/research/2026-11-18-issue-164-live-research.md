---
title: Issue 164 live research
description: Opening research record for the unticked criteria of issue 164
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Live Azure authorised (rg `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Research disposition: executed.

Unticked criteria: (1) thresholds approved and chat task registered with accountable reviewer and enable/disable state; (2) results bound to serving-model and control versions with approved thresholds, reviewers and pass/fail/insufficient outcomes; (3) competent human exercises on seeded critical suggestions; (4) actual calls need approved payload handling and finite authorisation, plus human consent/accessibility/privacy approval; (5) adding criteria does not authorise chat implementation, memory capture, calls, deployment or live use.

Findings are appended below as probes complete.

* Live probe (`evidence/2026-11-18/issue-164-live/`): chat task registered, `enabled` false, thresholds `proposed` (approved_by null), accountable individual unknown, demo-only activation by `jmservera` (2026-11-03).
* Three live asks (cited answer, approve refusal, injection) returned correct outcomes from rules; 0 model calls (`provider-unavailable`/`not-called`); consumption unchanged at 16 calls, 1 failure, 1 unknown liability that routes to workflow-only.
* Offline chat eval tests: 54 OK.
* Primary evidence note: `docs/reference/research/issue-164-live-chat-grounding-evidence-2026-11-18.md`.
* Result: no criterion newly tickable; criteria 3 and 4 need people/approvals, criteria 1 and 2 need threshold approval, a named individual and an actual-model run.

Planning Readiness: Ready. Tier FOCUSED; no src change.
