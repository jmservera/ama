---
title: Issue 619 live changes (2026-11-23)
ms.date: 2026-11-23
---

## Changes

* Added `docs/reference/research/issue-619-live-at-consent-evidence-2026-11-23.md`.
* Added drivers, redacted JSON and screenshots under `.copilot-tracking/evidence/2026-11-23/issue-619-live/`.
* Updated the `docs/reference/README.md` index and appended `docs/reference/log.md`.
* No `src/` change; no Azure resource created or changed; nothing to delete. Tier FOCUSED. `rpi-checks.py --all` not run.
* Validation: 127 targeted tests pass; live drivers on revisions 0000054 and 0000026 (axe 0 violations on case view, blocker case, employee chat, resident panel).

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Screen reader testing recorded by a person | Unproven; owner-gated (production, #1907) |
| 2 | Keyboard testing recorded by a person | Scripted proof passes; person record unproven |
| 3 | Zoom testing recorded by a person | Reflow proven by proxy; 200 percent text assessed as not a code gap; person record unproven |
| 4 | Consent step proven with a real resident journey | Proven on the synthetic demo only; real resident, DPO and Legal owner-gated |
| 5 | #550 consent step before any data is used | Proven for the demo (no request before consent, unit test); consented AI answer not observed because the AI usage guard holds |
| 6 | #552 Fluent 2 and WCAG baselines preserved | Partly proven (axe, baseline tests); no Fluent 2 re-audit, no conformance claim |
