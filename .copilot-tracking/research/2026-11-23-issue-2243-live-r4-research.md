---
title: Issue 2243 research r4 (missing expiry setting mislabelled as ended)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready. Full evidence: docs/reference/research/issue-2243-live-r4-2026-11-23.md.

New angle (not covered by r1 to r3): `expires_at()` in `resident_demo/assistant.py` falls back to the closed default `EXPIRES` (2026-11-01) when `ZF_DEMO_EXPIRES_AT` is unset or invalid. That default is now in the past, so a missing or malformed setting produces the label "the AI exercise has ended", the very symptom reported in #2243, while the real cause is configuration. Operators cannot tell the two apart from the resident-facing label or the log reason.

Fix scope: add `expiry_configured()`; the two question and topic entry checks in `aoai.py` raise a distinct `expiry_not_set` reason (still fail closed) when the setting is absent or invalid; add a named label and a regression test. No Azure change, no deployment.
